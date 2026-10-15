#!/usr/bin/env python3
"""HTTP-only recording proxy for publicly downloaded Moly client assets.

It intentionally forwards only GET and HEAD. Request bodies, cookies and
authentication headers are neither accepted nor archived.
"""

from __future__ import annotations

import argparse
import hashlib
import http.client
import json
import mimetypes
import os
import re
import secrets
import socket
import sys
import threading
import time
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")


HOP_BY_HOP = {
    "connection",
    "keep-alive",
    "proxy-authenticate",
    "proxy-authorization",
    "te",
    "trailer",
    "transfer-encoding",
    "upgrade",
}

BLOCKED_EXTERNAL_HOSTS = {
    "newmisc.taomee.com", "g.cn.miaozhen.com", "view.admaster.com.cn",
    "dc.61.com", "v.61.com", "baike.baidu.com", "news.61.com",
    "v.taomee.com", "seer.61.com", "imole.61.com",
    "haohaoting.61.com", "114.61.com", "e.61.com",
    "ad.61.com", "stat.61.com", "track.61.com", "log.61.com",
}
REDIRECT_SERVICE_HOSTS = {
    "pay.61.com", "pay.51mole.com", "account.61.com", "account-httpd.61.com",
    "reg.51mole.com", "reg.61.com", "service.61.com", "bbs.61.com",
    "event.61.com", "game.61.com", "vip.61.com", "kf.61.com", "home.51mole.com",
}
ACCOUNT_SERVICE_HOSTS = {
    "account-httpd.61.com", "account.61.com", "reg.51mole.com",
}
LOCAL_CONTROL_HOSTS = {"127.0.0.1", "localhost"}
NPC_JOBLIST_PATTERN = re.compile(
    r"^/resource/xml/npc/npcjoblist\d+\.xml$", re.IGNORECASE
)

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data" / "server"
AD_CONFIG_PATH = DATA_DIR / "ad_config.json"
ADS_DIR = PROJECT_ROOT / "archive" / "clients" / "local-overrides" / "ads"
WEB_DIR = PROJECT_ROOT / "web"
DOWNLOAD_DIR = WEB_DIR / "download"
DESKTOP_ZIP_PATH = DOWNLOAD_DIR / "Moly Thế Giới Chuột chũi.zip"
ANDROID_APK_PATH = DOWNLOAD_DIR / "Moly Thế Giới Chuột chũi.apk"


def get_ad_config() -> dict:
    if AD_CONFIG_PATH.exists():
        try:
            return json.loads(AD_CONFIG_PATH.read_text(encoding="utf-8"))
        except Exception:
            pass
PROXY_START_TIME = time.time()
ADMIN_SESSIONS: dict[str, dict[str, Any]] = {}
ADMIN_SESSIONS_LOCK = threading.Lock()


def create_admin_session(user_id: int = 10000001) -> str:
    token = secrets.token_hex(24)
    with ADMIN_SESSIONS_LOCK:
        ADMIN_SESSIONS[token] = {
            "user_id": user_id,
            "expires": time.time() + 86400,
        }
    return token


def verify_admin_session(token: str) -> bool:
    if not token:
        return False
    with ADMIN_SESSIONS_LOCK:
        sess = ADMIN_SESSIONS.get(token)
        if not sess:
            return False
        if time.time() > sess["expires"]:
            del ADMIN_SESSIONS[token]
            return False
        return True


def get_admin_token(headers: Any, query_token: str = "") -> str:
    if query_token:
        return query_token.strip()
    x_token = headers.get("X-Admin-Token", "")
    if x_token:
        return x_token.strip()
    auth = headers.get("Authorization", "")
    if auth.startswith("Bearer "):
        return auth[7:].strip()
    cookie = headers.get("Cookie", "")
    for part in cookie.split(";"):
        k, _, v = part.strip().partition("=")
        if k in ("moly_admin_token", "moly_admin_session"):
            return v.strip()
    return ""


def get_admin_user_id(token: str) -> int:
    if not token:
        return 0
    with ADMIN_SESSIONS_LOCK:
        sess = ADMIN_SESSIONS.get(token)
        if sess and time.time() <= sess["expires"]:
            return int(sess.get("user_id", 10000001))
    return 0


class RateLimiter:
    """Thread-safe in-memory rate limiter and anti-brute-force lockout."""
    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._reg_times: dict[str, list[float]] = {}
        self._failed_logins: dict[str, list[float]] = {}
        self._giftcode_times: dict[str, list[float]] = {}

    def allow_registration(self, ip: str, max_requests: int = 5, window_sec: float = 60.0) -> bool:
        now = time.time()
        with self._lock:
            timestamps = self._reg_times.setdefault(ip, [])
            timestamps = [t for t in timestamps if now - t < window_sec]
            if len(timestamps) >= max_requests:
                self._reg_times[ip] = timestamps
                return False
            timestamps.append(now)
            self._reg_times[ip] = timestamps
            return True

    def allow_giftcode(self, ip: str, max_requests: int = 5, window_sec: float = 60.0) -> bool:
        now = time.time()
        with self._lock:
            timestamps = self._giftcode_times.setdefault(ip, [])
            timestamps = [t for t in timestamps if now - t < window_sec]
            if len(timestamps) >= max_requests:
                self._giftcode_times[ip] = timestamps
                return False
            timestamps.append(now)
            self._giftcode_times[ip] = timestamps
            return True

    def check_login_allowed(self, ip: str, max_failures: int = 5, lockout_sec: float = 900.0) -> bool:
        now = time.time()
        with self._lock:
            failures = self._failed_logins.get(ip, [])
            failures = [t for t in failures if now - t < lockout_sec]
            self._failed_logins[ip] = failures
            return len(failures) < max_failures

    def record_failed_login(self, ip: str) -> None:
        now = time.time()
        with self._lock:
            self._failed_logins.setdefault(ip, []).append(now)

    def record_successful_login(self, ip: str) -> None:
        with self._lock:
            self._failed_logins.pop(ip, None)


rate_limiter = RateLimiter()


try:
    from account_system import accounts, google_oidc, giftcodes, recharges, otp_mgr, recovery_mgr
    from websocket_bridge import make_handshake_response, bridge_sockets
except ImportError:
    import sys
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from account_system import accounts, google_oidc, giftcodes, recharges, otp_mgr, recovery_mgr
    from websocket_bridge import make_handshake_response, bridge_sockets


def make_captcha_image(code: str = "6868") -> bytes:
    try:
        from io import BytesIO
        from PIL import Image, ImageDraw
        img = Image.new("RGB", (120, 40), color=(245, 248, 252))
        draw = ImageDraw.Draw(img)
        draw.line((0, 20, 120, 20), fill=(200, 215, 230), width=1)
        draw.line((10, 5, 110, 35), fill=(210, 220, 235), width=1)
        draw.text((32, 10), code, fill=(30, 70, 150))
        buf = BytesIO()
        img.save(buf, format="PNG")
        return buf.getvalue()
    except Exception:
        import base64
        return base64.b64decode(
            "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="
        )


class AssetArchive:
    def __init__(self, root: Path) -> None:
        self.root = root
        self.objects = root / "objects"
        self.manifest = root / "requests.jsonl"
        self.objects.mkdir(parents=True, exist_ok=True)
        self._lock = threading.Lock()

    def record(
        self,
        *,
        url: str,
        status: int,
        response_headers: list[tuple[str, str]],
        body: bytes,
    ) -> None:
        digest = hashlib.sha256(body).hexdigest()
        object_path = self.objects / digest[:2] / digest
        object_path.parent.mkdir(parents=True, exist_ok=True)
        if not object_path.exists():
            temp_path = object_path.with_suffix(f".{os.getpid()}.tmp")
            temp_path.write_bytes(body)
            try:
                temp_path.replace(object_path)
            except FileExistsError:
                temp_path.unlink(missing_ok=True)

        entry = {
            "captured_at": datetime.now(timezone.utc).isoformat(),
            "method": "GET",
            "url": url,
            "status": status,
            "sha256": digest,
            "size": len(body),
            "content_type": next(
                (value for name, value in response_headers if name.lower() == "content-type"),
                None,
            ),
        }
        line = json.dumps(entry, ensure_ascii=False, separators=(",", ":")) + "\n"
        with self._lock:
            with self.manifest.open("a", encoding="utf-8", newline="") as stream:
                stream.write(line)


class ProxyHandler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"
    archive: AssetArchive
    local_server: str | None = None
    override_root: Path | None = None
    mirror_root: Path | None = None

    def log_message(self, format: str, *args: object) -> None:
        print(
            datetime.now(timezone.utc).isoformat(),
            self.client_address[0],
            flush=True,
        )

    def _send_json(self, data: Any, status: int = 200) -> None:
        encoded = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded)))
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("X-Frame-Options", "SAMEORIGIN")
        self.send_header("X-XSS-Protection", "1; mode=block")
        self.send_header("Connection", "close")
        self.end_headers()
        self.wfile.write(encoded)

    def do_CONNECT(self) -> None:
        self.send_error(405, "HTTPS tunneling is intentionally disabled")

    def do_POST(self) -> None:
        parsed = urlsplit(self.path)
        host_header = self.headers.get("Host", "")
        host, _, _ = host_header.partition(":")
        host = (parsed.hostname or host).lower()

        if host in ACCOUNT_SERVICE_HOSTS or parsed.path == "/index.php":
            from urllib.parse import parse_qs
            content_length = int(self.headers.get("Content-Length", 0))
            raw_body = self.rfile.read(content_length)
            form = parse_qs(raw_body.decode("utf-8", errors="ignore"))
            cmd = form.get("cmd", [""])[0]
            if cmd == "1102":
                pwd = form.get("pwd", ["123456"])[0]
                new_acc = accounts.create_account(
                    password=pwd, nickname="Moly Viet", vip_level=0, gold_beans=1000
                )
                res_json = json.dumps(
                    {"result": 0, "userid": int(new_acc["user_id"])}
                ).encode("utf-8")
                self.send_response(200, "OK")
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.send_header("Content-Length", str(len(res_json)))
                self.send_header("Connection", "close")
                self.end_headers()
                self.wfile.write(res_json)
                print(f"In-game registration created new account: {new_acc['user_id']}", flush=True)
                return

        if host in LOCAL_CONTROL_HOSTS or parsed.path.startswith("/api/accounts/") or parsed.path.startswith("/api/user/lamu/"):
            client_ip = self.client_address[0]
            if parsed.path == "/api/accounts/create":
                if not rate_limiter.allow_registration(client_ip):
                    self._send_json({"error": "Bạn đã tạo quá nhiều tài khoản trong thời gian ngắn! Vui lòng thử lại sau 1 phút."}, status=429)
                    return
                content_length = int(self.headers.get("Content-Length", 0))
                raw_body = self.rfile.read(content_length)
                payload = json.loads(raw_body.decode("utf-8", errors="ignore"))
                nick = str(payload.get("nickname", "Moly Viet"))
                nick = re.sub(r"<[^>]+>", "", nick).strip()
                if not nick:
                    nick = "Moly Viet"
                acc = accounts.create_account(
                    password=payload.get("password", "123456"),
                    nickname=nick[:16],
                    email=payload.get("email"),
                    vip_level=0,
                    gold_beans=1000,
                )
                safe_acc = {k: v for k, v in acc.items() if k not in ("password_hash", "google_id")}
                self._send_json(safe_acc, status=200)
                return
            elif parsed.path == "/api/accounts/vip":
                token = get_admin_token(self.headers)
                if host not in LOCAL_CONTROL_HOSTS and not verify_admin_session(token):
                    self._send_json({"error": "Không có quyền thay đổi VIP!"}, status=403)
                    return
                content_length = int(self.headers.get("Content-Length", 0))
                raw_body = self.rfile.read(content_length)
                payload = json.loads(raw_body.decode("utf-8", errors="ignore"))
                ok = accounts.set_vip(
                    user_id=int(payload["user_id"]),
                    vip_level=int(payload.get("level", 8)),
                    gold_beans=int(payload.get("beans", 999999)),
                    months=int(payload.get("months", 120)),
                )
                self._send_json({"ok": ok}, status=200)
                return

            elif parsed.path == "/api/user/lamu/species":
                content_length = int(self.headers.get("Content-Length", 0))
                payload = json.loads(self.rfile.read(content_length).decode("utf-8", errors="ignore"))
                uid = int(payload.get("user_id", 0))
                species = str(payload.get("species", "classic"))
                ok, msg, lamu = accounts.choose_super_lamu_species(uid, species)
                self._send_json({"ok": ok, "message": msg, "lamu": lamu}, status=200 if ok else 400)
                return

            elif parsed.path == "/api/user/lamu/train":
                content_length = int(self.headers.get("Content-Length", 0))
                payload = json.loads(self.rfile.read(content_length).decode("utf-8", errors="ignore"))
                uid = int(payload.get("user_id", 0))
                exp_gain = int(payload.get("exp_gain", 50))
                ok, msg, prog = accounts.train_super_lamu(uid, exp_gain)
                self._send_json({"ok": ok, "message": msg, "progress": prog}, status=200 if ok else 400)
                return

            elif parsed.path == "/api/user/lamu/status":
                content_length = int(self.headers.get("Content-Length", 0))
                payload = json.loads(self.rfile.read(content_length).decode("utf-8", errors="ignore"))
                uid = int(payload.get("user_id", 0))
                st = accounts.get_super_lamu_status(uid)
                self._send_json({"ok": True, "status": st}, status=200)
                return

        if host in LOCAL_CONTROL_HOSTS or parsed.path.startswith("/api/"):
            if parsed.path == "/api/giftcode/redeem":
                client_ip = self.client_address[0]
                if not rate_limiter.allow_giftcode(client_ip):
                    self._send_json({"ok": False, "message": "Bạn thao tác đổi mã quá nhanh! Vui lòng chờ 1 phút."}, status=429)
                    return
                content_length = int(self.headers.get("Content-Length", 0))
                raw_body = self.rfile.read(content_length)
                try:
                    payload = json.loads(raw_body.decode("utf-8", errors="ignore"))
                except Exception:
                    self._send_json({"ok": False, "message": "Dữ liệu gửi lên không hợp lệ!"}, status=400)
                    return
                try:
                    uid = int(payload.get("user_id", 0))
                except (ValueError, TypeError):
                    uid = 0
                code = str(payload.get("code", "")).strip()
                if uid <= 0 or not code:
                    self._send_json({"ok": False, "message": "Vui lòng nhập đầy đủ ID Moly và Mã quà tặng!"}, status=400)
                    return
                ok, msg, rewards = giftcodes.redeem_giftcode(code, uid)
                if ok:
                    accounts.log_audit("REDEEM_GIFTCODE", uid, {"code": code, "rewards": rewards, "ip": client_ip})
                self._send_json({"ok": ok, "message": msg, "rewards": rewards}, status=200 if ok else 400)
                return

            elif parsed.path == "/api/user/register":
                client_ip = self.client_address[0]
                if not rate_limiter.allow_registration(client_ip):
                    self._send_json({"ok": False, "message": "Bạn đăng ký quá nhiều lần! Vui lòng chờ 1 phút."}, status=429)
                    return
                content_length = int(self.headers.get("Content-Length", 0))
                payload = json.loads(self.rfile.read(content_length).decode("utf-8", errors="ignore"))
                uname = str(payload.get("username", "")).strip()
                pwd = str(payload.get("password", "")).strip()
                fname = str(payload.get("fullname", "")).strip()
                nick = str(payload.get("nickname", "")).strip() or fname or uname or "Cư Dân Moly"
                em = str(payload.get("email", "")).strip()
                bday = str(payload.get("birthday", "")).strip() or "2010-01-01"

                if not uname:
                    self._send_json({"ok": False, "message": "Tên đăng nhập không được để trống!"}, status=400)
                    return
                if not re.fullmatch(r"[a-zA-Z0-9_]{4,30}", uname):
                    self._send_json({"ok": False, "message": "Tên đăng nhập phải từ 4-30 ký tự, không dấu, không khoảng trắng, chỉ gồm chữ cái, số và dấu gạch dưới!"}, status=400)
                    return
                if len(pwd) < 6:
                    self._send_json({"ok": False, "message": "Mật khẩu phải có tối thiểu 6 ký tự!"}, status=400)
                    return
                if not em or "@" not in em:
                    self._send_json({"ok": False, "message": "Địa chỉ Email/Gmail không hợp lệ!"}, status=400)
                    return

                try:
                    acc = accounts.create_account(
                        password=pwd,
                        username=uname,
                        fullname=fname,
                        nickname=nick,
                        email=em,
                        birthday=bday,
                        gold_beans=1000
                    )
                except ValueError as err:
                    self._send_json({"ok": False, "message": str(err)}, status=400)
                    return

                uid = acc["user_id"]
                accounts.grant_vip_trial(uid, days=3)
                accounts.log_audit("WEB_REGISTER", uid, {"username": uname, "nickname": nick, "email": em, "ip": client_ip})
                display_id = str(uid)
                sso_session = f"{(int(uid) & 0xFFFFFFFF):08x}4d4f4c594c4f43414c53455353494f4e"
                self._send_json({
                    "ok": True,
                    "user_id": uid,
                    "display_id": display_id,
                    "username": acc["username"],
                    "fullname": acc["fullname"],
                    "nickname": acc["nickname"],
                    "email": acc["email"],
                    "birthday": acc["birthday"],
                    "vip_level": 1,
                    "gold_beans": acc.get("gold_beans", 1000),
                    "sso_session": sso_session,
                    "message": f"Tạo tài khoản thành công! Mã số Moly (ID ngẫu nhiên) của bạn là: {display_id}"
                })
                return

            elif parsed.path == "/api/user/login":
                client_ip = self.client_address[0]
                if not rate_limiter.check_login_allowed(client_ip):
                    self._send_json({"ok": False, "message": "Đã nhập sai quá 5 lần! Vui lòng thử lại sau 15 phút."}, status=429)
                    return
                content_length = int(self.headers.get("Content-Length", 0))
                payload = json.loads(self.rfile.read(content_length).decode("utf-8", errors="ignore"))
                identifier = payload.get("identifier") or payload.get("username") or payload.get("user_id")
                pwd = str(payload.get("password", "")).strip()

                if not identifier:
                    self._send_json({"ok": False, "message": "Vui lòng nhập Tên đăng nhập, ID Moly hoặc Email!"}, status=400)
                    return

                ok, acc = accounts.authenticate(identifier, pwd)
                if not ok or not acc:
                    rate_limiter.record_failed_login(client_ip)
                    self._send_json({"ok": False, "message": "Tên đăng nhập, ID hoặc mật khẩu không chính xác!"}, status=401)
                    return

                rate_limiter.record_successful_login(client_ip)
                uid = int(acc["user_id"])
                display_id = "00000000" if uid == 0 else str(uid)
                lamu_st = accounts.get_super_lamu_status(uid)
                sso_session = f"{(uid & 0xFFFFFFFF):08x}4d4f4c594c4f43414c53455353494f4e"
                self._send_json({
                    "ok": True,
                    "sso_session": sso_session,
                    "account": {
                        "user_id": uid,
                        "display_id": display_id,
                        "username": acc.get("username", display_id),
                        "fullname": acc.get("fullname", acc.get("nickname", "Cư Dân")),
                        "nickname": acc.get("nickname", "Cư Dân Moly"),
                        "email": acc.get("email", ""),
                        "birthday": acc.get("birthday", "2010-01-01"),
                        "vip_level": acc.get("vip_level", 0),
                        "is_vip": lamu_st.get("is_vip", False),
                        "vip_value": acc.get("vip_value", 0),
                        "gold_beans": acc.get("gold_beans", 0),
                        "is_admin": acc.get("is_admin", False),
                        "lamu": lamu_st,
                        "sso_session": sso_session
                    }
                })
                return

            elif parsed.path == "/api/user/get_info":
                content_length = int(self.headers.get("Content-Length", 0))
                payload = json.loads(self.rfile.read(content_length).decode("utf-8", errors="ignore")) if content_length > 0 else {}
                identifier = payload.get("identifier") or payload.get("user_id") or payload.get("username")
                acc = accounts.get_account_by_identifier(identifier)
                if not acc:
                    self._send_json({"ok": False, "message": "Không tìm thấy tài khoản!"}, status=404)
                    return
                uid = int(acc["user_id"])
                display_id = "00000000" if uid == 0 else str(uid)
                lamu_st = accounts.get_super_lamu_status(uid)
                sso_session = f"{(uid & 0xFFFFFFFF):08x}4d4f4c594c4f43414c53455353494f4e"
                self._send_json({
                    "ok": True,
                    "account": {
                        "user_id": uid,
                        "display_id": display_id,
                        "username": acc.get("username", display_id),
                        "fullname": acc.get("fullname", acc.get("nickname", "Cư Dân")),
                        "nickname": acc.get("nickname", "Cư Dân Moly"),
                        "email": acc.get("email", ""),
                        "birthday": acc.get("birthday", "2010-01-01"),
                        "vip_level": acc.get("vip_level", 0),
                        "is_vip": lamu_st.get("is_vip", False),
                        "vip_value": acc.get("vip_value", 0),
                        "gold_beans": acc.get("gold_beans", 0),
                        "is_admin": acc.get("is_admin", False),
                        "lamu": lamu_st,
                        "sso_session": sso_session
                    }
                })
                return

            elif parsed.path == "/api/user/update_profile":
                content_length = int(self.headers.get("Content-Length", 0))
                payload = json.loads(self.rfile.read(content_length).decode("utf-8", errors="ignore"))
                uid = payload.get("user_id")
                if uid is None:
                    self._send_json({"ok": False, "message": "Thiếu mã tài khoản!"}, status=400)
                    return
                fname = payload.get("fullname")
                nick = payload.get("nickname")
                em = payload.get("email")
                bday = payload.get("birthday")
                ok, msg, updated = accounts.update_profile(uid, fullname=fname, nickname=nick, email=em, birthday=bday)
                if ok and updated:
                    actual_uid = int(updated["user_id"])
                    display_id = "00000000" if actual_uid == 0 else str(actual_uid)
                    lamu_st = accounts.get_super_lamu_status(actual_uid)
                    sso_session = f"{(actual_uid & 0xFFFFFFFF):08x}4d4f4c594c4f43414c53455353494f4e"
                    self._send_json({
                        "ok": True,
                        "message": msg,
                        "account": {
                            "user_id": actual_uid,
                            "display_id": display_id,
                            "username": updated.get("username", display_id),
                            "fullname": updated.get("fullname", ""),
                            "nickname": updated.get("nickname", ""),
                            "email": updated.get("email", ""),
                            "birthday": updated.get("birthday", ""),
                            "vip_level": updated.get("vip_level", 0),
                            "is_vip": lamu_st.get("is_vip", False),
                            "vip_value": updated.get("vip_value", 0),
                            "gold_beans": updated.get("gold_beans", 0),
                            "is_admin": updated.get("is_admin", False),
                            "lamu": lamu_st,
                            "sso_session": sso_session
                        }
                    })
                else:
                    self._send_json({"ok": False, "message": msg}, status=400)
                return

            elif parsed.path == "/api/user/reset_password":
                content_length = int(self.headers.get("Content-Length", 0))
                payload = json.loads(self.rfile.read(content_length).decode("utf-8", errors="ignore"))
                identifier = payload.get("identifier") or payload.get("username") or payload.get("user_id")
                em = str(payload.get("email", "")).strip()
                bday = str(payload.get("birthday", "")).strip()
                new_pwd = str(payload.get("new_password", "")).strip()
                if not identifier or not em or not bday or not new_pwd:
                    self._send_json({"ok": False, "message": "Vui lòng nhập đầy đủ Tên đăng nhập/ID, Email, Ngày sinh và Mật khẩu mới!"}, status=400)
                    return
                ok, msg = accounts.reset_password_with_info(identifier, em, bday, new_pwd)
                self._send_json({"ok": ok, "message": msg}, status=200 if ok else 400)
                return

            elif parsed.path == "/api/user/change_password":
                client_ip = self.client_address[0]
                content_length = int(self.headers.get("Content-Length", 0))
                payload = json.loads(self.rfile.read(content_length).decode("utf-8", errors="ignore"))
                uid = payload.get("user_id", 0)
                old_pwd = str(payload.get("old_password", "")).strip()
                new_pwd = str(payload.get("new_password", "")).strip()
                if len(new_pwd) < 6:
                    self._send_json({"ok": False, "message": "Mật khẩu mới phải có tối thiểu 6 ký tự!"}, status=400)
                    return
                ok, msg = accounts.change_password(uid, old_pwd, new_pwd)
                if ok:
                    accounts.log_audit("CHANGE_USER_PASSWORD", uid, {"ip": client_ip})
                self._send_json({"ok": ok, "message": msg}, status=200 if ok else 400)
                return

            elif parsed.path == "/api/user/verify_target":
                content_length = int(self.headers.get("Content-Length", 0))
                payload = json.loads(self.rfile.read(content_length).decode("utf-8", errors="ignore"))
                identifier = payload.get("identifier") or payload.get("user_id")
                char = accounts.verify_character(identifier)
                if char:
                    self._send_json({"ok": True, "character": char})
                else:
                    self._send_json({"ok": False, "message": "Không tìm thấy nhân vật tương ứng với ID này trong hệ thống!"}, status=404)
                return

            elif parsed.path == "/api/recharge/create":
                client_ip = self.client_address[0]
                content_length = int(self.headers.get("Content-Length", 0))
                payload = json.loads(self.rfile.read(content_length).decode("utf-8", errors="ignore"))
                identifier = payload.get("user_id")
                target = accounts.get_account_by_identifier(identifier)
                if not target or target.get("is_admin", False) or target.get("user_id") in (0, 10000000, 10000001):
                    self._send_json({"ok": False, "message": "Nhân vật không tồn tại trong hệ thống! Vui lòng kiểm tra lại ID."}, status=404)
                    return
                uid = int(target["user_id"])
                method = str(payload.get("method", "card")).strip().lower()
                try:
                    amount = int(payload.get("amount", 10000))
                except (ValueError, TypeError):
                    amount = 10000

                if method == "card":
                    ok, msg, order = recharges.create_card_order(
                        user_id=uid,
                        card_telco=payload.get("card_telco", ""),
                        amount=amount,
                        card_serial=payload.get("card_serial", ""),
                        card_code=payload.get("card_code", ""),
                        client_ip=client_ip,
                    )
                else:  # qr transfer
                    ok, msg, order = recharges.create_qr_order(
                        user_id=uid,
                        amount=amount,
                        transfer_code=payload.get("transfer_code", None),
                        client_ip=client_ip,
                    )
                self._send_json({"ok": ok, "message": msg, "order": order}, status=200 if ok else 400)
                return

            elif parsed.path == "/api/user/recharge_vip":
                client_ip = self.client_address[0]
                content_length = int(self.headers.get("Content-Length", 0))
                payload = json.loads(self.rfile.read(content_length).decode("utf-8", errors="ignore"))
                identifier = payload.get("user_id")
                target = accounts.get_account_by_identifier(identifier)
                if not target or target.get("is_admin", False) or target.get("user_id") in (0, 10000000, 10000001):
                    self._send_json({"ok": False, "message": "Nhân vật không tồn tại trong hệ thống! Vui lòng kiểm tra lại ID."}, status=404)
                    return
                uid = int(target["user_id"])
                try:
                    amount = int(payload.get("amount", 10000))
                except (ValueError, TypeError):
                    amount = 10000
                if amount < 10000:
                    self._send_json({"ok": False, "message": "Số Đậu quy đổi tối thiểu là 10.000đ (tương ứng 100 Đậu Vàng & 100 Điểm VIP)!"}, status=400)
                    return
                points = amount // 100
                st = accounts.add_vip_membership(uid, months=1, vip_value_add=points)
                accounts.add_gold_beans(uid, points)
                accounts.log_audit("USER_BUY_BEANS", uid, {"amount": amount, "points": points, "ip": client_ip})
                self._send_json({
                    "ok": True,
                    "message": f"Mua Đậu & Hội Viên thành công! Đã chuyển {points} Đậu Vàng và cộng {points} Điểm Hội Viên cho cư dân {target.get('fullname') or target.get('nickname')} (Cấp hiện tại: VIP {st['vip_level']})!",
                    "status": st,
                    "character": accounts.verify_character(uid)
                })
                return

            elif parsed.path == "/api/otp/send":
                client_ip = self.client_address[0]
                content_length = int(self.headers.get("Content-Length", 0))
                payload = json.loads(self.rfile.read(content_length).decode("utf-8", errors="ignore"))
                identifier = payload.get("identifier") or payload.get("username") or payload.get("email") or payload.get("user_id")
                if not identifier:
                    self._send_json({"ok": False, "message": "Vui lòng nhập Tên đăng nhập, ID hoặc Email đã đăng ký!"}, status=400)
                    return
                ok, msg, data = otp_mgr.request_otp(identifier, client_ip)
                resp = {"ok": ok, "message": msg}
                resp.update(data)
                self._send_json(resp, status=200 if ok else 400)
                return

            elif parsed.path == "/api/otp/verify_and_reset":
                client_ip = self.client_address[0]
                content_length = int(self.headers.get("Content-Length", 0))
                payload = json.loads(self.rfile.read(content_length).decode("utf-8", errors="ignore"))
                user_id = payload.get("user_id")
                otp_code = payload.get("otp_code") or payload.get("otp")
                new_pwd = str(payload.get("new_password", "")).strip()
                if not user_id or not otp_code or not new_pwd:
                    self._send_json({"ok": False, "message": "Vui lòng nhập đầy đủ mã OTP và mật khẩu mới!"}, status=400)
                    return
                ok, msg = otp_mgr.verify_otp_and_reset_password(user_id, otp_code, new_pwd)
                self._send_json({"ok": ok, "message": msg}, status=200 if ok else 400)
                return

            elif parsed.path == "/api/user/email/send_verification":
                content_length = int(self.headers.get("Content-Length", 0))
                payload = json.loads(self.rfile.read(content_length).decode("utf-8", errors="ignore"))
                uid = payload.get("user_id")
                email = str(payload.get("email", "")).strip()
                client_ip = self.client_address[0]
                ok, msg, res = otp_mgr.request_verify_email_otp(uid, email, ip=client_ip)
                resp = {"ok": ok, "message": msg}
                resp.update(res)
                self._send_json(resp, status=200 if ok else 400)
                return

            elif parsed.path == "/api/user/email/verify":
                content_length = int(self.headers.get("Content-Length", 0))
                payload = json.loads(self.rfile.read(content_length).decode("utf-8", errors="ignore"))
                uid = payload.get("user_id")
                email = str(payload.get("email", "")).strip()
                otp_code = str(payload.get("otp_code") or payload.get("otp") or "").strip()
                ok, msg = otp_mgr.verify_email_and_bind(uid, email, otp_code)
                self._send_json({"ok": ok, "message": msg}, status=200 if ok else 400)
                return

            elif parsed.path == "/api/support/recovery_request":
                client_ip = self.client_address[0]
                content_length = int(self.headers.get("Content-Length", 0))
                payload = json.loads(self.rfile.read(content_length).decode("utf-8", errors="ignore"))
                ident = str(payload.get("identifier", "")).strip()
                contact_email = str(payload.get("contact_email", "")).strip()
                remembered_pwd = str(payload.get("remembered_password", "")).strip()
                bday = str(payload.get("birthday", "")).strip()
                notes = str(payload.get("notes", "")).strip()
                ok, msg, extra = recovery_mgr.submit_request(
                    identifier=ident,
                    contact_email=contact_email,
                    remembered_password=remembered_pwd,
                    birthday=bday,
                    notes=notes,
                    ip=client_ip
                )
                resp = {"ok": ok, "message": msg}
                resp.update(extra)
                self._send_json(resp, status=200 if ok else 400)
                return

        if host in LOCAL_CONTROL_HOSTS or parsed.path.startswith("/api/admin/"):
            client_ip = self.client_address[0]
            if parsed.path == "/api/admin/login":
                if not rate_limiter.check_login_allowed(client_ip):
                    self._send_json({"ok": False, "error": "Đã nhập sai quá 5 lần! IP tạm thời bị khóa 15 phút."}, status=429)
                    return
                content_length = int(self.headers.get("Content-Length", 0))
                payload = json.loads(self.rfile.read(content_length).decode("utf-8", errors="ignore"))
                username = str(payload.get("username", "")).strip()
                password = str(payload.get("password", "")).strip()
                pin = str(payload.get("pin") or payload.get("security_pin") or "").strip()

                acc = accounts.get_account_by_identifier(username)
                if not acc or not acc.get("is_admin", False):
                    rate_limiter.record_failed_login(client_ip)
                    self._send_json({"ok": False, "error": "Tài khoản không có quyền quản trị viên!"}, status=403)
                    return
                uid = int(acc["user_id"])
                if not accounts.verify_password(uid, password):
                    rate_limiter.record_failed_login(client_ip)
                    self._send_json({"ok": False, "error": "Mật khẩu quản trị không chính xác!"}, status=401)
                    return
                if not accounts.verify_admin_pin(pin):
                    rate_limiter.record_failed_login(client_ip)
                    self._send_json({"ok": False, "error": "Mã PIN bảo mật quản trị (6 số) không chính xác!"}, status=401)
                    return
                rate_limiter.record_successful_login(client_ip)
                token = create_admin_session(uid)
                self._send_json({"ok": True, "token": token, "user_id": uid, "display_id": "00000000" if uid == 0 else str(uid)})
                return

            elif parsed.path == "/api/admin/change_password":
                token = get_admin_token(self.headers)
                if not verify_admin_session(token):
                    self._send_json({"error": "Chưa xác thực quản trị"}, status=401)
                    return
                admin_uid = get_admin_user_id(token)
                content_length = int(self.headers.get("Content-Length", 0))
                payload = json.loads(self.rfile.read(content_length).decode("utf-8", errors="ignore"))
                old_pwd = str(payload.get("old_password", "")).strip()
                new_pwd = str(payload.get("new_password", "")).strip()
                pin = str(payload.get("pin", "")).strip()
                ok, msg = accounts.change_admin_password_with_pin(admin_uid, old_pwd, new_pwd, pin)
                if ok:
                    accounts.log_audit("CHANGE_ADMIN_PASSWORD", admin_uid, {"ip": client_ip})
                self._send_json({"ok": ok, "message": msg}, status=200 if ok else 400)
                return

            elif parsed.path == "/api/admin/change_pin":
                token = get_admin_token(self.headers)
                if not verify_admin_session(token):
                    self._send_json({"error": "Chưa xác thực quản trị"}, status=401)
                    return
                admin_uid = get_admin_user_id(token)
                content_length = int(self.headers.get("Content-Length", 0))
                payload = json.loads(self.rfile.read(content_length).decode("utf-8", errors="ignore"))
                old_pin = str(payload.get("old_pin", "")).strip()
                new_pin = str(payload.get("new_pin", "")).strip()
                ok, msg = accounts.change_admin_pin(admin_uid, old_pin, new_pin)
                if ok:
                    accounts.log_audit("CHANGE_ADMIN_PIN", admin_uid, {"ip": client_ip})
                self._send_json({"ok": ok, "message": msg}, status=200 if ok else 400)
                return

            elif parsed.path == "/api/admin/reset_credentials":
                if not rate_limiter.check_login_allowed(client_ip):
                    self._send_json({"ok": False, "error": "Đã nhập sai quá nhiều lần! IP tạm thời bị khóa 15 phút."}, status=429)
                    return
                content_length = int(self.headers.get("Content-Length", 0))
                payload = json.loads(self.rfile.read(content_length).decode("utf-8", errors="ignore"))
                email = str(payload.get("email", "")).strip()
                bday = str(payload.get("birthday", "")).strip()
                new_pwd = str(payload.get("new_password", "")).strip()
                new_pin = str(payload.get("new_pin", "")).strip()
                ok, msg = accounts.reset_admin_credentials(email, bday, new_pwd, new_pin)
                if ok:
                    accounts.log_audit("RESET_ADMIN_CREDENTIALS", 0, {"ip": client_ip, "email": email})
                self._send_json({"ok": ok, "message": msg}, status=200 if ok else 400)
                return

            elif parsed.path == "/api/admin/otp/send":
                if not rate_limiter.check_login_allowed(client_ip):
                    self._send_json({"ok": False, "message": "Quá nhiều yêu cầu thử! Vui lòng chờ 15 phút."}, status=429)
                    return
                admin_cfg = otp_mgr.get_config()
                admin_email = admin_cfg.get("admin_notify_email") or "traivuho@gmail.com"
                ok, msg, data = otp_mgr.request_admin_otp(admin_email, client_ip)
                resp_payload = {"ok": ok, "message": msg}
                resp_payload.update(data)
                self._send_json(resp_payload, status=200 if ok else 400)
                return

            elif parsed.path == "/api/admin/otp/verify_and_reset":
                if not rate_limiter.check_login_allowed(client_ip):
                    self._send_json({"ok": False, "message": "Quá nhiều yêu cầu thử! Vui lòng chờ 15 phút."}, status=429)
                    return
                content_length = int(self.headers.get("Content-Length", 0))
                payload = json.loads(self.rfile.read(content_length).decode("utf-8", errors="ignore"))
                otp_code = str(payload.get("otp_code", "")).strip()
                new_pwd = str(payload.get("new_password", "")).strip()
                new_pin = str(payload.get("new_pin", "")).strip()
                ok, msg = otp_mgr.verify_admin_otp_and_reset(otp_code, new_pwd, new_pin)
                if ok:
                    accounts.log_audit("RESET_ADMIN_CREDENTIALS_OTP", 0, {"ip": client_ip})
                self._send_json({"ok": ok, "message": msg}, status=200 if ok else 400)
                return

            elif parsed.path == "/api/admin/giftcodes/create":
                token = get_admin_token(self.headers)
                if not verify_admin_session(token):
                    self._send_json({"error": "Chưa xác thực quản trị"}, status=401)
                    return
                admin_uid = get_admin_user_id(token)
                content_length = int(self.headers.get("Content-Length", 0))
                payload = json.loads(self.rfile.read(content_length).decode("utf-8", errors="ignore"))
                code = str(payload.get("code", "")).strip().upper()
                if not code:
                    self._send_json({"ok": False, "error": "Mã quà tặng không được để trống!"}, status=400)
                    return
                gc = giftcodes.create_giftcode(
                    code=code,
                    description=str(payload.get("description", "")),
                    beans=int(payload.get("beans", 0)),
                    vip_level=int(payload.get("vip_level", 0)),
                    vip_months=int(payload.get("vip_months", 0)),
                    trial_days=int(payload.get("trial_days", 0)),
                    vip_value_add=int(payload.get("vip_value_add", 0)),
                    super_lamu=bool(payload.get("super_lamu", False)),
                    super_lamu_species=payload.get("super_lamu_species"),
                    items=payload.get("items", []),
                    max_uses=int(payload.get("max_uses", 100)),
                )
                accounts.log_audit("CREATE_GIFTCODE", admin_uid, {"code": code, "details": gc})
                self._send_json({"ok": True, "giftcode": gc})
                return

            elif parsed.path == "/api/admin/giftcodes/delete":
                token = get_admin_token(self.headers)
                if not verify_admin_session(token):
                    self._send_json({"error": "Chưa xác thực quản trị"}, status=401)
                    return
                admin_uid = get_admin_user_id(token)
                content_length = int(self.headers.get("Content-Length", 0))
                payload = json.loads(self.rfile.read(content_length).decode("utf-8", errors="ignore"))
                code = str(payload.get("code", "")).strip().upper()
                ok = giftcodes.delete_giftcode(code)
                if ok:
                    accounts.log_audit("DELETE_GIFTCODE", admin_uid, {"code": code})
                self._send_json({"ok": ok})
                return

            elif parsed.path == "/api/admin/logout":
                token = get_admin_token(self.headers)
                with ADMIN_SESSIONS_LOCK:
                    ADMIN_SESSIONS.pop(token, None)
                self._send_json({"ok": True})
                return

            elif parsed.path == "/api/admin/user/beans":
                token = get_admin_token(self.headers)
                if not verify_admin_session(token):
                    self._send_json({"error": "Chưa xác thực quản trị"}, status=401)
                    return
                content_length = int(self.headers.get("Content-Length", 0))
                payload = json.loads(self.rfile.read(content_length).decode("utf-8", errors="ignore"))
                uid = int(payload.get("user_id", 0))
                amt = int(payload.get("amount", 100000))
                accounts.add_gold_beans(uid, amt)
                self._send_json({"ok": True})
                return

            elif parsed.path == "/api/admin/user/vip":
                token = get_admin_token(self.headers)
                if not verify_admin_session(token):
                    self._send_json({"error": "Chưa xác thực quản trị"}, status=401)
                    return
                content_length = int(self.headers.get("Content-Length", 0))
                payload = json.loads(self.rfile.read(content_length).decode("utf-8", errors="ignore"))
                uid = int(payload.get("user_id", 0))
                lvl = int(payload.get("vip_level", 8))
                beans = payload.get("beans")
                months = int(payload.get("months", 120))
                accounts.set_vip(
                    uid,
                    vip_level=lvl,
                    gold_beans=int(beans) if beans is not None else None,
                    months=months,
                )
                self._send_json({"ok": True})
                return

            elif parsed.path == "/api/admin/user/vip_trial":
                token = get_admin_token(self.headers)
                if not verify_admin_session(token):
                    self._send_json({"error": "Chưa xác thực quản trị"}, status=401)
                    return
                content_length = int(self.headers.get("Content-Length", 0))
                payload = json.loads(self.rfile.read(content_length).decode("utf-8", errors="ignore"))
                uid = int(payload.get("user_id", 0))
                days = int(payload.get("days", 3))
                status = accounts.grant_vip_trial(uid, days=days)
                self._send_json({"ok": True, "status": status})
                return

            elif parsed.path == "/api/admin/user/vip_membership":
                token = get_admin_token(self.headers)
                if not verify_admin_session(token):
                    self._send_json({"error": "Chưa xác thực quản trị"}, status=401)
                    return
                content_length = int(self.headers.get("Content-Length", 0))
                payload = json.loads(self.rfile.read(content_length).decode("utf-8", errors="ignore"))
                uid = int(payload.get("user_id", 0))
                months = int(payload.get("months", 1))
                val_add = int(payload.get("vip_value_add", 100))
                status = accounts.add_vip_membership(uid, months=months, vip_value_add=val_add)
                self._send_json({"ok": True, "status": status})
                return

            elif parsed.path == "/api/admin/user/smc":
                token = get_admin_token(self.headers)
                if not verify_admin_session(token):
                    self._send_json({"error": "Chưa xác thực quản trị"}, status=401)
                    return
                content_length = int(self.headers.get("Content-Length", 0))
                payload = json.loads(self.rfile.read(content_length).decode("utf-8", errors="ignore"))
                uid = int(payload.get("user_id", 0))
                accounts.update_profession(uid, "police", 3, 1000)
                accounts.update_profession(uid, "guide", 3, 1000)
                accounts.update_profession(uid, "journalist", 3, 1000)
                accounts.update_profession(uid, "knight", 3, 1000)
                accounts.update_account(uid, {"element_knight_type": 1, "element_knight_talent": 40})
                self._send_json({"ok": True})
                return

            elif parsed.path == "/api/admin/user/super_lamu":
                token = get_admin_token(self.headers)
                if not verify_admin_session(token):
                    self._send_json({"error": "Chưa xác thực quản trị"}, status=401)
                    return
                content_length = int(self.headers.get("Content-Length", 0))
                payload = json.loads(self.rfile.read(content_length).decode("utf-8", errors="ignore"))
                uid = int(payload.get("user_id", 0))
                species = payload.get("species", "classic")
                res = accounts.choose_super_lamu_species(uid, species)
                accounts.update_lamu(uid, {
                    "hunger": 100,
                    "cleanliness": 100,
                    "mood": 100,
                    "skills": [1, 2, 3, 4],
                })
                self._send_json({"ok": True, "lamu": res})
                return

            elif parsed.path == "/api/admin/broadcast":
                token = get_admin_token(self.headers)
                if not verify_admin_session(token):
                    self._send_json({"error": "Chưa xác thực quản trị"}, status=401)
                    return
                content_length = int(self.headers.get("Content-Length", 0))
                payload = json.loads(self.rfile.read(content_length).decode("utf-8", errors="ignore"))
                msg = str(payload.get("message", ""))
                print(f"[ADMIN BROADCAST] {msg}", flush=True)
                self._send_json({"ok": True})
                return

            elif parsed.path == "/api/admin/recharge/approve":
                token = get_admin_token(self.headers)
                if not verify_admin_session(token):
                    self._send_json({"error": "Chưa xác thực quản trị"}, status=401)
                    return
                admin_uid = get_admin_user_id(token)
                content_length = int(self.headers.get("Content-Length", 0))
                payload = json.loads(self.rfile.read(content_length).decode("utf-8", errors="ignore"))
                order_id = str(payload.get("order_id", "")).strip()
                ok, msg, res = recharges.approve_order(order_id, admin_id=admin_uid)
                self._send_json({"ok": ok, "message": msg, "data": res}, status=200 if ok else 400)
                return

            elif parsed.path == "/api/admin/recharge/reject":
                token = get_admin_token(self.headers)
                if not verify_admin_session(token):
                    self._send_json({"error": "Chưa xác thực quản trị"}, status=401)
                    return
                admin_uid = get_admin_user_id(token)
                content_length = int(self.headers.get("Content-Length", 0))
                payload = json.loads(self.rfile.read(content_length).decode("utf-8", errors="ignore"))
                order_id = str(payload.get("order_id", "")).strip()
                reason = str(payload.get("reason", "")).strip()
                ok, msg, order = recharges.reject_order(order_id, admin_id=admin_uid, reason=reason)
                self._send_json({"ok": ok, "message": msg, "order": order}, status=200 if ok else 400)
                return

            elif parsed.path == "/api/admin/payment/config":
                token = get_admin_token(self.headers)
                if not verify_admin_session(token):
                    self._send_json({"error": "Chưa xác thực quản trị"}, status=401)
                    return
                content_length = int(self.headers.get("Content-Length", 0))
                payload = json.loads(self.rfile.read(content_length).decode("utf-8", errors="ignore"))
                cfg = recharges.update_payment_config(
                    bank_name=payload.get("bank_name", ""),
                    account_number=payload.get("account_number", ""),
                    account_name=payload.get("account_name", ""),
                    qr_image_url=payload.get("qr_image_url", ""),
                    note=payload.get("note", ""),
                )
                self._send_json({"ok": True, "message": "Cập nhật cấu hình thanh toán & QR thành công!", "config": cfg})
                return

            elif parsed.path == "/api/admin/user/ban":
                token = get_admin_token(self.headers)
                if not verify_admin_session(token):
                    self._send_json({"error": "Chưa xác thực quản trị"}, status=401)
                    return
                content_length = int(self.headers.get("Content-Length", 0))
                payload = json.loads(self.rfile.read(content_length).decode("utf-8", errors="ignore"))
                uid = payload.get("user_id")
                reason = payload.get("reason", "Vi phạm điều lệ cư dân Moly")
                ok, msg = accounts.ban_account(uid, reason)
                self._send_json({"ok": ok, "message": msg}, status=200 if ok else 400)
                return

            elif parsed.path == "/api/admin/user/unban":
                token = get_admin_token(self.headers)
                if not verify_admin_session(token):
                    self._send_json({"error": "Chưa xác thực quản trị"}, status=401)
                    return
                content_length = int(self.headers.get("Content-Length", 0))
                payload = json.loads(self.rfile.read(content_length).decode("utf-8", errors="ignore"))
                uid = payload.get("user_id")
                ok, msg = accounts.unban_account(uid)
                self._send_json({"ok": ok, "message": msg}, status=200 if ok else 400)
                return

            elif parsed.path == "/api/admin/user/give_item":
                token = get_admin_token(self.headers)
                if not verify_admin_session(token):
                    self._send_json({"error": "Chưa xác thực quản trị"}, status=401)
                    return
                content_length = int(self.headers.get("Content-Length", 0))
                payload = json.loads(self.rfile.read(content_length).decode("utf-8", errors="ignore"))
                uid = payload.get("user_id")
                item_id = int(payload.get("item_id", 0))
                count = int(payload.get("count", 1))
                is_cloth = bool(payload.get("is_cloth", True))
                ok, msg = accounts.give_item(uid, item_id, count, is_cloth)
                self._send_json({"ok": ok, "message": msg}, status=200 if ok else 400)
                return

            elif parsed.path == "/api/admin/email/config":
                token = get_admin_token(self.headers)
                if not verify_admin_session(token):
                    self._send_json({"error": "Chưa xác thực quản trị"}, status=401)
                    return
                content_length = int(self.headers.get("Content-Length", 0))
                payload = json.loads(self.rfile.read(content_length).decode("utf-8", errors="ignore"))
                gmail_user = str(payload.get("gmail_user", "")).strip()
                app_password = str(payload.get("app_password", "")).strip()
                sender = str(payload.get("sender_name", "Moly - Thế Giới Chuột Chũi VN")).strip()
                admin_notify = str(payload.get("admin_notify_email", "")).strip()
                ok = otp_mgr.update_config(gmail_user, app_password, sender, admin_notify_email=admin_notify)
                self._send_json({"ok": ok, "message": "Cập nhật cấu hình Gmail OTP thành công!", "config": otp_mgr.get_config()})
                return

            elif parsed.path == "/api/admin/recovery_requests/resolve":
                token = get_admin_token(self.headers)
                if not verify_admin_session(token):
                    self._send_json({"error": "Chưa xác thực quản trị"}, status=401)
                    return
                content_length = int(self.headers.get("Content-Length", 0))
                payload = json.loads(self.rfile.read(content_length).decode("utf-8", errors="ignore"))
                req_id = str(payload.get("request_id", "")).strip()
                new_pwd = str(payload.get("new_password", "")).strip()
                admin_note = str(payload.get("admin_note", "")).strip()
                ok, msg = recovery_mgr.resolve_request(req_id, new_password=new_pwd, admin_note=admin_note)
                self._send_json({"ok": ok, "message": msg}, status=200 if ok else 400)
                return

        self.send_error(405, "Request bodies are not supported for external hosts")

    def do_PUT(self) -> None:
        self.send_error(405, "Request bodies are intentionally disabled")

    def do_HEAD(self) -> None:
        self._forward(include_body=False)

    def do_GET(self) -> None:
        parsed = urlsplit(self.path)
        host_header = self.headers.get("Host", "")
        host, _, _ = host_header.partition(":")
        host = (parsed.hostname or host).lower()

        # 1. Handle WebSocket Upgrade (Ruffle socketProxy bridge)
        if parsed.path.startswith("/ws/") or self.headers.get("Upgrade", "").lower() == "websocket":
            port_match = re.search(r"/ws/(\d+)", parsed.path)
            target_port = int(port_match.group(1)) if port_match else 1863
            target_host = self.local_server or "127.0.0.1"

            key = self.headers.get("Sec-WebSocket-Key", "")
            subproto = self.headers.get("Sec-WebSocket-Protocol", None)
            if key:
                handshake_resp = make_handshake_response(key, subproto)
                self.request.sendall(handshake_resp)

                try:
                    target_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    target_sock.connect((target_host, target_port))
                    bridge_sockets(self.request, target_sock, f"TCP-{target_port}")
                except Exception as e:
                    print(f"[WS ERROR] Failed connecting to {target_host}:{target_port}: {e}", flush=True)
                finally:
                    self.close_connection = True
                return
            else:
                self.send_error(400, "Missing Sec-WebSocket-Key header")
                return

        # 2. Handle Web Portal & Direct Download endpoints
        if parsed.path in {"/", "/index.html"}:
            index_path = WEB_DIR / "index.html"
            if index_path.is_file():
                content = index_path.read_bytes()
                self.send_response(200, "OK")
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(content)))
                self.send_header("Connection", "close")
                self.end_headers()
                self.wfile.write(content)
                return

        if parsed.path in {"/play", "/play.html"}:
            play_path = WEB_DIR / "play.html"
            if play_path.is_file():
                content = play_path.read_bytes()
                self.send_response(200, "OK")
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(content)))
                self.send_header("Connection", "close")
                self.end_headers()
                self.wfile.write(content)
                return

        if parsed.path in {"/admin", "/admin.html"}:
            admin_path = WEB_DIR / "admin.html"
            if admin_path.is_file():
                content = admin_path.read_bytes()
                self.send_response(200, "OK")
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(content)))
                self.send_header("Connection", "close")
                self.end_headers()
                self.wfile.write(content)
                return

        if parsed.path == "/api/admin/stats":
            token = get_admin_token(self.headers)
            if not verify_admin_session(token):
                self._send_json({"error": "Chưa xác thực quản trị"}, status=401)
                return
            try:
                import moly_probe_server as moly_mod
                online_ccu = moly_mod.world_hub.get_online_count()
            except Exception:
                online_ccu = 0
            stats = {
                "total_accounts": len(accounts.list_accounts()),
                "online_ccu": online_ccu,
                "uptime_seconds": int(time.time() - PROXY_START_TIME),
                "server_status": "Hoạt động ổn định (Tri-Play Ready)",
            }
            self._send_json(stats)
            return

        if parsed.path == "/api/admin/users":
            token = get_admin_token(self.headers)
            if not verify_admin_session(token):
                self._send_json({"error": "Chưa xác thực quản trị"}, status=401)
                return
            all_users = accounts.list_accounts()
            clean_users = []
            for u in all_users:
                cu = dict(u)
                cu.pop("password_hash", None)
                clean_users.append(cu)
            self._send_json(clean_users)
            return

        if parsed.path == "/api/admin/giftcodes":
            token = get_admin_token(self.headers)
            if not verify_admin_session(token):
                self._send_json({"error": "Chưa xác thực quản trị"}, status=401)
                return
            self._send_json(giftcodes.list_giftcodes())
            return

        if parsed.path == "/api/user/lamu/status":
            from urllib.parse import parse_qs
            query = parse_qs(parsed.query)
            try:
                uid = int(query.get("user_id", [0])[0])
            except (ValueError, TypeError):
                uid = 0
            st = accounts.get_super_lamu_status(uid)
            self._send_json({"ok": True, "status": st})
            return

        if parsed.path == "/api/leaderboard":
            from urllib.parse import parse_qs
            query = parse_qs(parsed.query)
            try:
                limit = int(query.get("limit", [10])[0])
            except (ValueError, TypeError):
                limit = 10
            board = accounts.get_leaderboard(limit=limit)
            self._send_json({"ok": True, "leaderboard": board})
            return

        if parsed.path == "/api/newspaper/latest":
            news_data = {
                "ok": True,
                "issue_no": 128,
                "title": "Thời Báo Moly - Số Đặc Biệt: Đậu Đậu Siêu Cấp Trở Lại!",
                "date": "2026-10-15",
                "cover_img": "/assets/news_cover.png",
                "headlines": [
                    {
                        "id": 1,
                        "title": "Vương Quốc Chuột Chũi Chào Đón Cư Dân Mới",
                        "summary": "Tất cả các cư dân đăng ký tài khoản mới đều nhận được gói quà khởi nghiệp 50,000 Đậu Vàng và Thẻ Đậu Đậu Siêu Cấp 7 Ngày!",
                        "author": "Thị Trưởng Bồ Đào",
                        "date": "2026-10-15"
                    },
                    {
                        "id": 2,
                        "title": "Học Viện Kỹ Xảo SMC Khai Giảng Khóa Mới",
                        "summary": "Các nghề Cảnh Sát, Đầu Bếp, Nông Dân, Hướng Dẫn Viên đã chính thức mở ghi danh tại Lâu Đài Moly và Nông Trại Vui Vẻ.",
                        "author": "Đội Trưởng Kỵ Sĩ",
                        "date": "2026-10-14"
                    },
                    {
                        "id": 3,
                        "title": "Bí Ẩn Về Sự Xuất Hiện Của Đậu Đậu Siêu Cấp Đặc Biệt",
                        "summary": "Các nhà khoa học tại Phòng Thí Nghiệm Viện Nghiên Cứu Moly đang nghiên cứu 4 hệ tiến hóa đặc biệt của Đậu Đậu Siêu Cấp.",
                        "author": "Bác Sĩ Wow",
                        "date": "2026-10-13"
                    }
                ]
            }
            self._send_json(news_data)
            return

        if parsed.path == "/api/admin/email_config":
            token = get_admin_token(self.headers)
            if not verify_admin_session(token):
                self._send_json({"error": "Chưa xác thực quản trị"}, status=401)
                return
            self._send_json({"ok": True, "config": otp_mgr.get_config()})
            return

        if parsed.path == "/api/admin/recovery_requests":
            token = get_admin_token(self.headers)
            if not verify_admin_session(token):
                self._send_json({"error": "Chưa xác thực quản trị"}, status=401)
                return
            from urllib.parse import parse_qs
            query = parse_qs(parsed.query)
            status_f = query.get("status", [None])[0]
            requests = recovery_mgr.list_requests(status=status_f)
            self._send_json({"ok": True, "requests": requests})
            return

        if parsed.path == "/api/admin/backup":
            from urllib.parse import parse_qs
            query = parse_qs(parsed.query)
            q_token = query.get("token", [""])[0]
            token = get_admin_token(self.headers, q_token)
            if not verify_admin_session(token):
                self._send_json({"error": "Chưa xác thực quản trị"}, status=401)
                return
            import zipfile
            from io import BytesIO
            buf = BytesIO()
            with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
                if DATA_DIR.exists():
                    for json_f in DATA_DIR.glob("*.json"):
                        zf.write(json_f, arcname=f"database_backup/{json_f.name}")
            backup_bytes = buf.getvalue()
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"moly_backup_{ts}.zip"
            self.send_response(200, "OK")
            self.send_header("Content-Type", "application/zip")
            self.send_header("Content-Disposition", f'attachment; filename="{filename}"')
            self.send_header("Content-Length", str(len(backup_bytes)))
            self.send_header("Connection", "close")
            self.end_headers()
            self.wfile.write(backup_bytes)
            return

        if parsed.path == "/api/payment/config":
            cfg = recharges.get_payment_config()
            resp_dict = {"ok": True, "config": cfg}
            resp_dict.update(cfg)
            self._send_json(resp_dict)
            return

        if parsed.path == "/api/payment/generate_code":
            self._send_json({"ok": True, "code": recharges.generate_transfer_code()})
            return

        if parsed.path == "/api/recharge/orders":
            from urllib.parse import parse_qs
            query = parse_qs(parsed.query)
            user_id_raw = query.get("user_id", [None])[0]
            user_id = int(user_id_raw) if user_id_raw and user_id_raw.isdigit() else None
            status_f = query.get("status", [None])[0]
            orders = recharges.list_orders(user_id=user_id, status_filter=status_f)
            self._send_json({"ok": True, "orders": orders})
            return

        if parsed.path == "/api/admin/recharge/orders":
            token = get_admin_token(self.headers)
            if not verify_admin_session(token):
                self._send_json({"error": "Chưa xác thực quản trị"}, status=401)
                return
            from urllib.parse import parse_qs
            query = parse_qs(parsed.query)
            status_f = query.get("status", [None])[0]
            orders = recharges.list_orders(status_filter=status_f)
            now = datetime.now(timezone.utc)
            enhanced = []
            for o in orders:
                eo = dict(o)
                try:
                    c_dt = datetime.fromisoformat(o["created_at"].replace("Z", "+00:00"))
                    elapsed = int((now - c_dt).total_seconds())
                    remaining = max(0, 900 - elapsed)
                    eo["elapsed_seconds"] = elapsed
                    eo["review_remaining_seconds"] = remaining
                except Exception:
                    eo["elapsed_seconds"] = 0
                    eo["review_remaining_seconds"] = 0
                enhanced.append(eo)
            self._send_json({"ok": True, "orders": enhanced, "config": recharges.get_payment_config()})
            return

        if parsed.path.startswith("/assets/"):
            rel_path = parsed.path[8:].split("?")[0]
            target_file = (WEB_DIR / "assets" / rel_path).resolve()
            if (WEB_DIR / "assets").resolve() in target_file.parents and target_file.is_file():
                content = target_file.read_bytes()
                mime = mimetypes.guess_type(target_file.name)[0] or "application/octet-stream"
                self.send_response(200, "OK")
                self.send_header("Content-Type", mime)
                self.send_header("Content-Length", str(len(content)))
                self.send_header("Cache-Control", "public, max-age=604800")
                self.send_header("Connection", "close")
                self.end_headers()
                self.wfile.write(content)
                return

        if parsed.path.startswith("/static/"):
            rel_path = parsed.path[8:].split("?")[0]
            target_file = (WEB_DIR / "static" / rel_path).resolve()
            if (WEB_DIR / "static").resolve() in target_file.parents and target_file.is_file():
                content = target_file.read_bytes()
                mime = mimetypes.guess_type(target_file.name)[0] or "application/octet-stream"
                if target_file.suffix == ".wasm":
                    mime = "application/wasm"
                elif target_file.suffix == ".js":
                    mime = "application/javascript"
                self.send_response(200, "OK")
                self.send_header("Content-Type", mime)
                self.send_header("Content-Length", str(len(content)))
                self.send_header("Cache-Control", "public, max-age=604800, immutable")
                self.send_header("Connection", "close")
                self.end_headers()
                self.wfile.write(content)
                return

        if parsed.path.endswith(".apk") or "apk" in parsed.path.lower():
            if ANDROID_APK_PATH.is_file():
                content = ANDROID_APK_PATH.read_bytes()
                self.send_response(200, "OK")
                self.send_header("Content-Type", "application/vnd.android.package-archive")
                self.send_header("Content-Length", str(len(content)))
                self.send_header(
                    "Content-Disposition",
                    'attachment; filename="Moly The Gioi Chuot chui.apk"; filename*=UTF-8\'\'Moly%20Th%E1%BA%BF%20Gi%E1%BB%9Bi%20Chu%E1%BB%99t%20ch%C5%A9i.apk'
                )
                self.send_header("Connection", "close")
                self.end_headers()
                self.wfile.write(content)
                return
            else:
                self.send_error(404, "APK package not found")
                return

        if parsed.path in {"/download", "/download/Moly-The-Gioi-Chuot-Chui.zip"} or parsed.path.startswith("/download/"):
            if DESKTOP_ZIP_PATH.is_file():
                content = DESKTOP_ZIP_PATH.read_bytes()
                self.send_response(200, "OK")
                self.send_header("Content-Type", "application/zip")
                self.send_header("Content-Length", str(len(content)))
                self.send_header(
                    "Content-Disposition",
                    'attachment; filename="Moly The Gioi Chuot chui.zip"; filename*=UTF-8\'\'Moly%20Th%E1%BA%BF%20Gi%E1%BB%9Bi%20Chu%E1%BB%99t%20ch%C5%A9i.zip'
                )
                self.send_header("Connection", "close")
                self.end_headers()
                self.wfile.write(content)
                return
            else:
                self.send_error(404, "Desktop package not found")
                return

        if host in ACCOUNT_SERVICE_HOSTS or parsed.path == "/index.php":
            if "cmd=1101" in (parsed.query or ""):
                captcha_bytes = make_captcha_image("6868")
                self.send_response(200, "OK")
                self.send_header("Content-Type", "image/png")
                self.send_header("Content-Length", str(len(captcha_bytes)))
                self.send_header("Connection", "close")
                self.end_headers()
                self.wfile.write(captcha_bytes)
                return

        if host in LOCAL_CONTROL_HOSTS or parsed.path.startswith("/auth/google"):
            if parsed.path in {"/auth/google", "/auth/google/login", "/auth/google/"}:
                auth_url = google_oidc.build_authorization_url()
                self.send_response(302, "Found")
                self.send_header("Location", auth_url)
                self.send_header("Connection", "close")
                self.end_headers()
                return
            elif parsed.path == "/auth/google/callback":
                from urllib.parse import parse_qs
                query_params = parse_qs(parsed.query)
                code = query_params.get("code", [""])[0]
                google_sub = f"google_{code[:16]}" if code else "google_demo_player"
                acc = google_oidc.process_google_identity(
                    accounts,
                    google_sub=google_sub,
                    email=f"{google_sub}@moly.viet",
                    name="Moly Google",
                )
                html = f"""<!DOCTYPE html>
<html>
<head><meta charset="utf-8"><title>Moly - Thế Giới Chuột Chũi VN - Đăng nhập Google</title></head>
<body style="font-family: Arial, sans-serif; text-align: center; padding: 50px; background: #edf2f7;">
  <div style="background: white; border-radius: 12px; padding: 30px; display: inline-block; box-shadow: 0 4px 15px rgba(0,0,0,0.1); max-width: 480px;">
    <h2 style="color: #2b6cb0; margin-top: 0;">Đăng nhập Google thành công!</h2>
    <p>ID tài khoản Moly của bạn là:</p>
    <div style="font-size: 42px; font-weight: bold; color: #e53e3e; margin: 15px 0;">{acc['user_id']}</div>
    <p><strong>Biệt danh:</strong> {acc.get('nickname')}</p>
    <p style="color: #4a5568;"><strong>Email liên kết:</strong> {acc.get('email')}</p>
    <div style="margin-top: 25px; padding: 15px; background: #ebf8ff; border-radius: 8px; color: #2c5282; font-size: 14px;">
      Hãy mở game Moly - Thế Giới Chuột Chũi VN và đăng nhập bằng ID trên để tiếp tục!
    </div>
  </div>
</body>
</html>""".encode("utf-8")
                self.send_response(200, "OK")
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(html)))
                self.send_header("Connection", "close")
                self.end_headers()
                self.wfile.write(html)
                return
            elif parsed.path == "/api/accounts":
                token = get_admin_token(self.headers)
                if not verify_admin_session(token):
                    self._send_json({"error": "Chưa xác thực quản trị"}, status=401)
                    return
                data = json.dumps(
                    accounts.list_accounts(), ensure_ascii=False, indent=2
                ).encode("utf-8")
                self.send_response(200, "OK")
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.send_header("Content-Length", str(len(data)))
                self.send_header("Connection", "close")
                self.end_headers()
                self.wfile.write(data)
                return
            elif parsed.path == "/api/ads":
                cfg = get_ad_config()
                data = json.dumps(cfg, ensure_ascii=False, indent=2).encode("utf-8")
                self.send_response(200, "OK")
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.send_header("Content-Length", str(len(data)))
                self.send_header("Connection", "close")
                self.end_headers()
                self.wfile.write(data)
                return
            elif parsed.path.startswith("/ads/click"):
                from urllib.parse import parse_qs
                ad_id = ""
                if "/" in parsed.path[10:]:
                    ad_id = parsed.path[10:].strip("/")
                else:
                    qs = parse_qs(parsed.query)
                    ad_id = qs.get("id", [""])[0]
                cfg = get_ad_config()
                target_url = cfg.get("default_redirect", "https://molyviet.vn")
                for ad in cfg.get("ads", []):
                    if ad.get("id") == ad_id and ad.get("target_url"):
                        target_url = ad["target_url"]
                        break
                self.send_response(302, "Found")
                self.send_header("Location", target_url)
                self.send_header("Connection", "close")
                self.end_headers()
                return
            elif parsed.path.startswith("/ads/"):
                filename = parsed.path[5:].split("?")[0]
                target_file = (ADS_DIR / filename).resolve()
                if ADS_DIR.resolve() in target_file.parents and target_file.is_file():
                    data = target_file.read_bytes()
                    mime = mimetypes.guess_type(target_file.name)[0] or "image/png"
                    self.send_response(200, "OK")
                    self.send_header("Content-Type", mime)
                    self.send_header("Content-Length", str(len(data)))
                    self.send_header("Connection", "close")
                    self.end_headers()
                    self.wfile.write(data)
                    return
                self.send_error(404, "Ad banner not found")
                return
            elif parsed.path in {"/recharge", "/nap-the", "/nap-tien"}:
                self.send_response(302, "Found")
                self.send_header("Location", "/#recharge")
                self.send_header("Connection", "close")
                self.end_headers()
                return
            elif parsed.path == "/vip":
                html = """<!DOCTYPE html>
<html>
<head><meta charset="utf-8"><title>Moly - Thế Giới Chuột Chũi VN - Đặc Quyền VIP & Đậu Vàng</title></head>
<body style="font-family: Arial, sans-serif; text-align: center; padding: 50px; background: #fffaf0;">
  <div style="background: white; border-radius: 12px; padding: 30px; display: inline-block; box-shadow: 0 4px 15px rgba(0,0,0,0.1); max-width: 520px;">
    <h2 style="color: #d69e2e; margin-top: 0;">Đặc Quyền Cư Dân Moly - Thế Giới Chuột Chũi VN</h2>
    <p>Máy chủ nội bộ hỗ trợ mở khóa toàn bộ tính năng VIP và Đậu Vàng để trải nghiệm trọn vẹn thế giới game!</p>
    <div style="text-align: left; background: #feebc8; padding: 15px; border-radius: 8px; color: #744210; font-size: 14px; margin: 20px 0;">
      <div>• <strong>VIP 1 - VIP 19:</strong> Mở toàn bộ thú cưỡi, đồ thời trang hiệp sĩ, khu vực Rồng và nhà bay.</div>
      <div>• <strong>Đậu Vàng:</strong> Cấp Đậu Vàng để tự do mua sắm tại Cửa Hàng Moly.</div>
      <div>• <strong>Tài khoản Admin:</strong> ID <code>00000000</code> đã kích hoạt sẵn quyền quản trị tối cao.</div>
    </div>
    <p style="font-size: 13px; color: #718096;">Chúc bạn có những giây phút thư giãn tuyệt vời tại Moly - Thế Giới Chuột Chũi VN!</p>
  </div>
</body>
</html>""".encode("utf-8")
                self.send_response(200, "OK")
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(html)))
                self.send_header("Connection", "close")
                self.end_headers()
                self.wfile.write(html)
                return

        self._forward(include_body=True)

    def _forward(self, *, include_body: bool) -> None:
        parsed = urlsplit(self.path)
        if parsed.scheme:
            if parsed.scheme.lower() != "http":
                self.send_error(400, "Only plain HTTP asset URLs are supported")
                return
            host = parsed.hostname
            port = parsed.port or 80
            target = parsed.path or "/"
            if parsed.query:
                target += "?" + parsed.query
            absolute_url = self.path
        else:
            host_header = self.headers.get("Host", "")
            host, separator, port_text = host_header.partition(":")
            if not host:
                self.send_error(400, "Missing Host header")
                return
            port = int(port_text) if separator else 80
            target = self.path
            absolute_url = f"http://{host_header}{target}"

        if host.lower() in REDIRECT_SERVICE_HOSTS:
            path_lower = parsed.path.lower()
            if "pay" in host.lower() or "vip" in host.lower() or "recharge" in path_lower:
                dest = "http://127.0.0.1:18080/#recharge"
            elif "register" in path_lower or "reg" in host.lower():
                dest = "http://127.0.0.1:18080/#register"
            elif "change" in path_lower or "pwd" in path_lower:
                dest = "http://127.0.0.1:18080/play.html#profile"
            elif "forget" in path_lower or "find" in path_lower:
                dest = "http://127.0.0.1:18080/#forgot"
            elif "protect" in path_lower or "security" in path_lower:
                dest = "http://127.0.0.1:18080/#security"
            else:
                dest = "http://127.0.0.1:18080/"
            self.send_response(302, "Found")
            self.send_header("Location", dest)
            self.send_header("Connection", "close")
            self.end_headers()
            self.close_connection = True
            return

        if host.lower() in BLOCKED_EXTERNAL_HOSTS:
            response_headers = [
                ("Content-Type", "text/plain; charset=utf-8"),
                ("X-Moly-Blocked", "external-content"),
                ("X-Moly-Source", "blocked"),
            ]
            self.archive.record(
                url=absolute_url,
                status=200,
                response_headers=response_headers,
                body=b"",
            )
            self.send_response(200, "Blocked external content")
            for name, value in response_headers:
                self.send_header(name, value)
            self.send_header("Content-Length", "0")
            self.send_header("Connection", "close")
            self.end_headers()
            self.close_connection = True
            return

        outbound_headers: dict[str, str] = {}
        for name, value in self.headers.items():
            lower = name.lower()
            if lower in HOP_BY_HOP or lower in {"cookie", "authorization"}:
                continue
            outbound_headers[name] = value
        outbound_headers["Host"] = host if port == 80 else f"{host}:{port}"
        outbound_headers["Connection"] = "close"

        candidate_relatives = [Path(host.lower()) / parsed.path.lstrip("/")]
        if host.lower() != "mole.61.com":
            candidate_relatives.append(Path("mole.61.com") / parsed.path.lstrip("/"))

        for relative in candidate_relatives:
            for source_name, source_root in (
                ("override", self.override_root),
                ("mirror", self.mirror_root),
            ):
                if not source_root:
                    continue
                root = source_root.resolve()
                local_file = (root / relative).resolve()
                if root != local_file and root not in local_file.parents:
                    continue
                if not local_file.is_file():
                    continue

                original_body = local_file.read_bytes()
                client_body = original_body
                if self.local_server and parsed.path.lower() == "/config/server.xml":
                    text = original_body.decode("utf-8")
                    text = text.replace('ip="123.206.131.236"', f'ip="{self.local_server}"')
                    text = text.replace('ip="123.206.131.63"', f'ip="{self.local_server}"')
                    client_body = text.encode("utf-8")

                content_type = mimetypes.guess_type(local_file.name)[0] or "application/octet-stream"
                response_headers = [
                    ("Content-Type", content_type),
                    ("X-Moly-Source", source_name),
                ]
                if source_name == "override":
                    response_headers.append(("Cache-Control", "no-cache, no-store, must-revalidate"))
                    response_headers.append(("Pragma", "no-cache"))
                    response_headers.append(("Expires", "0"))
                elif local_file.suffix.lower() in {".swf", ".png", ".jpg", ".jpeg", ".mp3", ".wasm"}:
                    response_headers.append(("Cache-Control", "public, max-age=604800, immutable"))
                elif local_file.suffix.lower() in {".xml", ".json"}:
                    response_headers.append(("Cache-Control", "public, max-age=3600"))

                self.archive.record(
                    url=absolute_url,
                    status=200,
                    response_headers=response_headers,
                    body=original_body,
                )
                self.send_response(200, f"Local {source_name}")
                for name, value in response_headers:
                    self.send_header(name, value)
                self.send_header("Content-Length", str(len(client_body)))
                self.send_header("Connection", "close")
                self.end_headers()
                if include_body:
                    self.wfile.write(client_body)
                self.close_connection = True
                print(f"Served local {source_name} {local_file}", flush=True)
                return

        connection = http.client.HTTPConnection(host, port, timeout=30)
        try:
            connection.request(self.command, target, headers=outbound_headers)
            response = connection.getresponse()
            body = response.read() if include_body else b""
            response_headers = [
                (name, value)
                for name, value in response.getheaders()
                if name.lower() not in HOP_BY_HOP
                and name.lower() not in {"content-length", "set-cookie"}
            ]

            self.archive.record(
                url=absolute_url,
                status=response.status,
                response_headers=response_headers,
                body=body,
            )

            client_body = body
            client_status = response.status
            client_reason = response.reason
            client_headers = response_headers
            if response.status == 404 and NPC_JOBLIST_PATTERN.match(parsed.path):
                client_body = b'<?xml version="1.0" encoding="utf-8"?><NPCJobList />'
                client_status = 200
                client_reason = "Empty local NPC job list"
                client_headers = [
                    ("Content-Type", "application/xml; charset=utf-8"),
                    ("X-Moly-Fallback", "empty-npc-job-list"),
                ]
                print(f"Served empty fallback for missing {parsed.path}", flush=True)
            if (
                include_body
                and self.local_server
                and parsed.path.lower() == "/config/server.xml"
            ):
                text = body.decode("utf-8")
                text = text.replace('ip="123.206.131.236"', f'ip="{self.local_server}"')
                text = text.replace('ip="123.206.131.63"', f'ip="{self.local_server}"')
                client_body = text.encode("utf-8")
                print(
                    f"Rewrote Server.xml TCP endpoints to {self.local_server}",
                    flush=True,
                )

            self.send_response(client_status, client_reason)
            for name, value in client_headers:
                self.send_header(name, value)
            self.send_header("Content-Length", str(len(client_body)))
            self.send_header("Connection", "close")
            self.end_headers()
            if include_body:
                self.wfile.write(client_body)
        except Exception as error:
            self.send_error(502, f"Upstream request failed: {type(error).__name__}")
            print(f"Proxy error for {absolute_url}: {error}", flush=True)
        finally:
            connection.close()
            self.close_connection = True


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=18080)
    parser.add_argument("--archive", type=Path, required=True)
    parser.add_argument(
        "--local-server",
        help="Rewrite Server.xml game/login IP addresses for an isolated local test",
    )
    parser.add_argument(
        "--overrides",
        type=Path,
        help="Serve matching host/path files locally before contacting upstream",
    )
    parser.add_argument(
        "--mirror",
        type=Path,
        help="Serve a pinned host/path asset mirror after overrides and before upstream",
    )
    args = parser.parse_args()

    archive = AssetArchive(args.archive.resolve())
    ProxyHandler.archive = archive
    ProxyHandler.local_server = args.local_server
    ProxyHandler.override_root = args.overrides.resolve() if args.overrides else None
    ProxyHandler.mirror_root = args.mirror.resolve() if args.mirror else None
    server = ThreadingHTTPServer((args.host, args.port), ProxyHandler)
    print(
        f"Recording HTTP GET assets on http://{args.host}:{args.port} -> {archive.root}",
        flush=True,
    )
    server.serve_forever()


if __name__ == "__main__":
    main()
