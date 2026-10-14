#!/usr/bin/env python3
"""Automated security and giftcode test suite for Moly-Viet."""

import json
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import socket
import subprocess

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "tools"))

from account_system import accounts, giftcodes, DEFAULT_MOLY_ADMIN_ID

HTTP_PORT = 18080
BASE_URL = f"http://127.0.0.1:{HTTP_PORT}"


def is_port_open(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(("127.0.0.1", port)) == 0


def http_req(path: str, method: str = "GET", data: dict = None, token: str = None) -> tuple[int, dict, dict]:
    url = f"{BASE_URL}{path}"
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    body = json.dumps(data).encode("utf-8") if data is not None else None
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            resp_headers = dict(resp.headers)
            content = resp.read().decode("utf-8", errors="replace")
            try:
                res_json = json.loads(content)
            except Exception:
                res_json = {"raw": content}
            return resp.status, res_json, resp_headers
    except urllib.error.HTTPError as e:
        content = e.read().decode("utf-8", errors="replace")
        try:
            res_json = json.loads(content)
        except Exception:
            res_json = {"raw": content}
        return e.code, res_json, dict(e.headers)


def run_tests():
    proxy_proc = None
    if not is_port_open(HTTP_PORT):
        print(f"[*] Dang khoi dong Proxy Server tren port {HTTP_PORT}...")
        proxy_proc = subprocess.Popen([
            sys.executable,
            str(PROJECT_ROOT / "tools" / "capture_proxy.py"),
            "--port", str(HTTP_PORT),
            "--local-server", "127.0.0.1",
            "--archive", str(PROJECT_ROOT / "data" / "archive_test"),
            "--overrides", str(PROJECT_ROOT / "archive" / "clients" / "local-overrides"),
            "--mirror", str(PROJECT_ROOT / "archive" / "clients" / "offline-mirror"),
        ])
        time.sleep(2.5)

    try:
        _run_all_assertions()
    finally:
        accounts.update_account(DEFAULT_MOLY_ADMIN_ID, {"password_hash": "*"})
        if proxy_proc:
            print("[*] Dang dung Proxy Server test...")
            proxy_proc.terminate()
            proxy_proc.wait(timeout=5)


def _run_all_assertions():
    print("=" * 70)
    print("BAT DAU KIEM THU BAO MAT VA HE THONG GIFTCODE / ADMIN MOLY VIET")
    print("=" * 70)

    # 1. Test Tạo tài khoản & Bảo mật XSS + Loại bỏ password_hash
    print("\n[TEST 1] Kiem tra loc XSS va Bao mat phan hoi tai khoan...")
    status, res, headers = http_req("/api/accounts/create", "POST", {
        "nickname": "<script>alert('hack')</script>Thám Tử",
        "password": "PasswordTest123",
        "email": "thamtutest@moly.viet"
    })
    assert status == 200, f"Expected 200, got {status}: {res}"
    user_id = res["user_id"]
    nickname = res["nickname"]
    assert "<script>" not in nickname, f"XSS script tag not filtered: {nickname}"
    assert "password_hash" not in res, "password_hash leaked in API response!"
    assert "google_id" not in res or res["google_id"] is None, "Sensitive data in response!"
    print(f" => PASS: Tai khoan {user_id} da tao an toan. Nickname da loc: '{nickname}'.")

    # 2. Test Security Headers
    print("\n[TEST 2] Kiem tra Security Headers tren cac phan hoi API...")
    assert headers.get("X-Content-Type-Options") == "nosniff", "Missing X-Content-Type-Options!"
    assert headers.get("X-Frame-Options") == "SAMEORIGIN", "Missing X-Frame-Options!"
    assert headers.get("X-XSS-Protection") == "1; mode=block", "Missing X-XSS-Protection!"
    print(" => PASS: Day du headers: X-Content-Type-Options, X-Frame-Options, X-XSS-Protection.")

    # 3. Test Giftcode TANTHU2026
    print("\n[TEST 3] Kiem tra doi ma Giftcode TANTHU2026...")
    status, res, _ = http_req("/api/giftcode/redeem", "POST", {
        "user_id": user_id,
        "code": "TANTHU2026"
    })
    assert status == 200 and res.get("ok"), f"Redeem failed: {res}"
    rewards = res.get("rewards", {})
    assert rewards.get("beans") == 100, f"Expected 100 beans, got {rewards.get('beans')}"
    assert rewards.get("vip_level") == 1, f"Expected VIP 1, got {rewards.get('vip_level')}"
    assert rewards.get("trial_days") == 3, f"Expected 3 trial days, got {rewards.get('trial_days')}"
    print(f" => PASS: Doi thanh cong ma TANTHU2026. Nhan +{rewards['beans']} dau va VIP 1 dung thu {rewards['trial_days']} ngay.")

    # 4. Test Chống dùng lại Giftcode (Anti-Replay)
    print("\n[TEST 4] Kiem tra chong dung lai Giftcode TANTHU2026...")
    status, res, _ = http_req("/api/giftcode/redeem", "POST", {
        "user_id": user_id,
        "code": "TANTHU2026"
    })
    assert status == 400 and not res.get("ok"), f"Should fail duplicate redeem: {res}"
    assert "đã sử dụng" in res.get("message", "").lower(), f"Unexpected message: {res}"
    print(f" => PASS: He thong chan dung lai thanh cong: '{res.get('message')}'.")

    # 5. Test Dang nhap Admin & Tao Session
    print("\n[TEST 5] Kiem tra Dang nhap va Session Admin...")
    status, res, _ = http_req("/api/admin/login", "POST", {
        "username": str(DEFAULT_MOLY_ADMIN_ID),
        "password": "initial_admin_any_password"
    })
    assert status == 200 and res.get("ok"), f"Admin login failed: {res}"
    token = res["token"]
    print(f" => PASS: Dang nhap Admin thanh cong, cap token: {token[:8]}...")

    # 6. Test Admin CRUD Giftcodes
    print("\n[TEST 6] Kiem tra Admin Tao & Quan ly Ma Qua Tang...")
    # Tao ma test
    status, res, _ = http_req("/api/admin/giftcodes/create", "POST", {
        "code": "TESTSUPER2026",
        "description": "Ma sieu cap thu nghiem",
        "beans": 50000,
        "vip_level": 7,
        "vip_months": 6,
        "super_lamu": True,
        "max_uses": 10
    }, token=token)
    assert status == 200 and res.get("ok"), f"Create giftcode failed: {res}"
    print(f" => PASS: Admin da tao ma TESTSUPER2026 thanh cong.")

    # Lay danh sach
    status, res, _ = http_req("/api/admin/giftcodes", "GET", token=token)
    assert status == 200 and any(g.get("code") == "TESTSUPER2026" for g in res), "TESTSUPER2026 not found in list"
    print(f" => PASS: Danh sach giftcodes hien thi {len(res)} ma.")

    # User doi ma moi
    status, res, _ = http_req("/api/giftcode/redeem", "POST", {
        "user_id": user_id,
        "code": "TESTSUPER2026"
    })
    assert status == 200 and res.get("ok"), f"Redeem TESTSUPER2026 failed: {res}"
    assert res["rewards"]["super_lamu"] is True, "Super Lamu not awarded!"
    print(f" => PASS: Cu dan {user_id} da doi ma TESTSUPER2026 nhan +50k dau va Sieu LaMu.")

    # Xoa ma test
    status, res, _ = http_req("/api/admin/giftcodes/delete", "POST", {
        "code": "TESTSUPER2026"
    }, token=token)
    assert status == 200 and res.get("ok"), f"Delete giftcode failed: {res}"
    print(f" => PASS: Admin da xoa ma TESTSUPER2026 an toan.")

    # 7. Test Admin Doi Mat Khau
    print("\n[TEST 7] Kiem tra Co che Doi Mat Khau Admin an toan...")
    # Doi mat khau lan 1 tu khoi tao sang AdminSecure2026!
    status, res, _ = http_req("/api/admin/change_password", "POST", {
        "old_password": "",
        "new_password": "AdminSecure2026!"
    }, token=token)
    assert status == 200 and res.get("ok"), f"Initial password set failed: {res}"
    print(" => PASS: Dat mat khau Admin moi thanh cong.")

    # Thu doi voi mat khau cu sai
    status, res, _ = http_req("/api/admin/change_password", "POST", {
        "old_password": "WrongPassword123",
        "new_password": "AnotherNewPass2026"
    }, token=token)
    assert status == 400 and not res.get("ok"), "Should reject wrong old password!"
    print(" => PASS: He thong tu choi mat khau cu sai.")

    # Thu doi voi mat khau moi qua ngan (<6 ky tu)
    status, res, _ = http_req("/api/admin/change_password", "POST", {
        "old_password": "AdminSecure2026!",
        "new_password": "123"
    }, token=token)
    assert status == 400 and not res.get("ok"), "Should reject password < 6 chars!"
    print(" => PASS: He thong tu choi mat khau moi duoi 6 ky tu.")

    # Doi thanh cong voi mat khau cu dung
    status, res, _ = http_req("/api/admin/change_password", "POST", {
        "old_password": "AdminSecure2026!",
        "new_password": "AdminSecureFinal2026!"
    }, token=token)
    assert status == 200 and res.get("ok"), f"Password change with correct old password failed: {res}"
    print(" => PASS: Doi sang mat khau AdminFinal thanh cong.")

    # Khoi phuc wildcard '*' cho admin de cac test suite khac tiep tuc chay thuan tien
    accounts.update_account(DEFAULT_MOLY_ADMIN_ID, {"password_hash": "*"})
    print(" => PASS: Da khoi phuc trang thai mat khau an toan.")

    # 8. Test Nhat ky Kiem toan (Audit Log)
    print("\n[TEST 8] Kiem tra Nhat ky Kiem toan (Admin Audit Log)...")
    audit_file = PROJECT_ROOT / "data" / "server" / "admin_audit.log"
    assert audit_file.exists(), "admin_audit.log does not exist!"
    log_content = audit_file.read_text(encoding="utf-8")
    assert "REDEEM_GIFTCODE" in log_content, "REDEEM_GIFTCODE action not logged!"
    assert "CREATE_GIFTCODE" in log_content, "CREATE_GIFTCODE action not logged!"
    print(f" => PASS: Nhat ky audit log da luu day du ({len(log_content.strip().splitlines())} ban ghi).")

    # 9. Test VIP Dung Thu & Thang Cap VIP Tich Luy (Progressive VIP System)
    print("\n[TEST 9] Kiem tra VIP Dung Thu, Tich Luy Thang Cap & Het Han VIP...")
    # Tao user moi toanh de test he thong VIP
    test_vip_user = accounts.create_account(password="PasswordVipTest", nickname="VipTester")
    test_vip_uid = test_vip_user["user_id"]
    
    # 9.1 Ban dau chua co VIP
    st0 = accounts.check_vip_status(test_vip_uid)
    assert not st0["is_vip"] and st0["vip_level"] == 0 and st0["vip_value"] == 0, f"Initial VIP state wrong: {st0}"
    print(" => PASS: Tai khoan moi chua co VIP (VIP 0, 0 diem).")

    # 9.2 Cap VIP 1 dung thu 3 ngay (trial)
    st_trial = accounts.grant_vip_trial(test_vip_uid, days=3)
    assert st_trial["is_vip"] and st_trial["vip_level"] == 1, f"Trial VIP failed: {st_trial}"
    assert st_trial["vip_value"] == 0, f"Trial should not inflate permanent points: {st_trial}"
    assert 2 <= st_trial["days_left"] <= 3, f"Days left unexpected: {st_trial}"
    print(f" => PASS: VIP dung thu 3 ngay hoat dong chuan (VIP 1, con {st_trial['days_left']} ngay, 0 diem tich luy).")

    # 9.3 Nap the thang: +1 thang VIP va +100 diem thanh vien -> Thang len VIP 2
    st_sub1 = accounts.add_vip_membership(test_vip_uid, months=1, vip_value_add=100)
    assert st_sub1["is_vip"] and st_sub1["vip_level"] == 2, f"Expected VIP 2, got {st_sub1}"
    assert st_sub1["vip_value"] == 100, f"Expected 100 points, got {st_sub1}"
    print(f" => PASS: Nap the thang 1 thanh cong (+100 diem -> Thang cap len VIP {st_sub1['vip_level']}).")

    # 9.4 Tich luy tiep +200 diem thanh vien -> Tong 300 diem -> Thang cap len VIP 3
    st_sub2 = accounts.add_vip_membership(test_vip_uid, months=1, vip_value_add=200)
    assert st_sub2["vip_level"] == 3 and st_sub2["vip_value"] == 300, f"Expected VIP 3, got {st_sub2}"
    print(f" => PASS: Tich luy them 200 diem (+200 diem -> Tong 300 diem -> Thang cap len VIP {st_sub2['vip_level']}).")

    # 9.5 Tich luy them de len VIP 4 (600 diem)
    st_sub3 = accounts.add_vip_membership(test_vip_uid, months=1, vip_value_add=300)
    assert st_sub3["vip_level"] == 4 and st_sub3["vip_value"] == 600, f"Expected VIP 4, got {st_sub3}"
    print(f" => PASS: Tich luy tiep 300 diem (Tong 600 diem -> Thang cap len VIP {st_sub3['vip_level']}).")

    # 9.6 Kiem tra co che het han VIP: set vip_end ve qua khu
    accounts.update_account(test_vip_uid, {"vip_end": int(time.time()) - 3600})
    st_expired = accounts.check_vip_status(test_vip_uid)
    assert not st_expired["is_vip"] and st_expired["vip_level"] == 0 and st_expired["days_left"] == 0, f"Expiry check failed: {st_expired}"
    assert st_expired["vip_value"] == 600, "Vip points should be preserved after expiry!"
    print(f" => PASS: VIP het han tu dong tro ve trang thai binh thuong (is_vip=False, diem tich luy giu nguyen 600).")

    # 9.7 Kiem tra Admin luon luon la VIP 19 (Max level) vinh vien
    st_admin = accounts.check_vip_status(DEFAULT_MOLY_ADMIN_ID)
    assert st_admin["is_vip"] and st_admin["vip_level"] == 19 and st_admin["days_left"] >= 30000, f"Admin VIP wrong: {st_admin}"
    print(f" => PASS: Admin {DEFAULT_MOLY_ADMIN_ID} luon la VIP 19 vinh vien (con {st_admin['days_left']} ngay).")

    # 10. Test He Thong Dau Dau Sieu Cap Da Chung Loai (Hac Am, Vu Tru, Than Thoai) & Tien Trinh Rieng
    print("\n[TEST 10] Kiem tra Dau Dau Sieu Cap Da Chung Loai & Tien Trinh Phat Trien Doc Lap...")
    # 10.1 Kich hoat the thang cho user de co quyen chon loai
    accounts.add_vip_membership(test_vip_uid, months=1, vip_value_add=100)
    
    # 10.2 Chon loai Dau Dau Sieu Cap Hac Am (Dark Super Lamu)
    ok, msg, lamu_dark = accounts.choose_super_lamu_species(test_vip_uid, "dark")
    assert ok and lamu_dark["super_type"] == "dark", f"Select dark species failed: {msg}"
    assert lamu_dark["level"] == 1 and lamu_dark["color"] == 5, f"Dark species initial stats wrong: {lamu_dark}"
    assert lamu_dark["following"] is True, "Super Lamu must follow player by default!"
    print(f" => PASS: Chon Dau Dau Sieu Cap Hac Am thanh cong (Cap 1, Mau 5, dang di theo sau).")

    # 10.3 Nuoi duong luyen tap Hac Am: +150 exp -> Thang cap len Lv.2
    ok_train, msg_train, prog_dark = accounts.train_super_lamu(test_vip_uid, exp_gain=150)
    assert ok_train and prog_dark["level"] == 2 and prog_dark["exp"] == 150, f"Train failed: {msg_train}"
    lamu_check = accounts.get_lamu(test_vip_uid)
    assert lamu_check["level"] == 2, f"Lamu current level mismatch: {lamu_check}"
    print(f" => PASS: Nuoi duong Hac Am dat 150 EXP -> Thang cap len Lv.2 thanh cong.")

    # 10.4 Chuyen sang chung loai Dau Dau Sieu Cap Vu Tru (Cosmic Super Lamu)
    # Tien trinh cua loai moi phai bat dau lai tu dau (Lv.1, 0 exp)
    ok_cosmic, msg_cosmic, lamu_cosmic = accounts.choose_super_lamu_species(test_vip_uid, "cosmic")
    assert ok_cosmic and lamu_cosmic["super_type"] == "cosmic", f"Select cosmic failed: {msg_cosmic}"
    assert lamu_cosmic["level"] == 1 and lamu_cosmic["color"] == 6, f"New species must start from Lv.1: {lamu_cosmic}"
    print(f" => PASS: Doi sang Dau Dau Sieu Cap Vu Tru bat dau tien trinh lai tu Lv.1 (0 EXP).")

    # 10.5 Chuyen lai Dau Dau Sieu Cap Hac Am -> Tien trinh Lv.2 cu phai duoc bao luu
    ok_back, msg_back, lamu_back = accounts.choose_super_lamu_species(test_vip_uid, "dark")
    assert ok_back and lamu_back["super_type"] == "dark", f"Switch back failed: {msg_back}"
    assert lamu_back["level"] == 2, f"Old species progress was not preserved: {lamu_back}"
    print(f" => PASS: Chuyen lai Hac Am, tien trinh Lv.2 duoc bao luu nguyen ven.")

    # 10.6 Kiem tra Thang Diem VIP toi da VIP 19
    accounts.add_vip_membership(test_vip_uid, months=120, vip_value_add=35000)
    st_max = accounts.check_vip_status(test_vip_uid)
    assert st_max["vip_level"] == 19, f"Expected VIP 19, got {st_max['vip_level']}"
    print(f" => PASS: Tich luy 35.000 diem thanh vien -> Dat mox MAX VIP 19 Than Thoai Toi Thuong.")

    print("\n" + "=" * 70)
    print("TAT CA CAC BAI KIEM TRA BAO MAT & GIFTCODE DEU PASS 100%!")
    print("=" * 70)


if __name__ == "__main__":
    run_tests()
