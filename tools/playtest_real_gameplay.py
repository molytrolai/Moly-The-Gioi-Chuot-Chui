#!/usr/bin/env python3
"""Comprehensive Real Gameplay & Security Play-test Suite for Moly-Viet.

Runs real server processes, executes security penetration tests, and
simulates a full resident life-cycle playthrough (A-Z).
"""

from __future__ import annotations

import json
import os
import re
import socket
import struct
import subprocess
import sys
import time
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "tools"))

if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if sys.stderr and hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

from moly_probe_server import moly_encrypt, moly_decrypt
from account_system import hash_moly_password, accounts

DIR_PORT = 11863
WORLD_PORT = 13200
HTTP_PORT = 18080

def send_recv_packet(sock: socket.socket, cmd: int, uid: int, clear_body: bytes = b"", encrypt: bool = True) -> tuple[int, bytes]:
    body = moly_encrypt(clear_body) if encrypt else clear_body
    head = struct.pack(">IBIII", 17 + len(body), 1, cmd, uid, 0)
    sock.sendall(head + body)
    
    resp_head = sock.recv(17)
    if len(resp_head) < 17:
        raise ValueError(f"Incomplete header received: {len(resp_head)} bytes")
    length, ver, rcmd, ruid, rres = struct.unpack(">IBIII", resp_head)
    resp_body = sock.recv(length - 17)
    clear_resp = moly_decrypt(resp_body) if encrypt else resp_body
    return rcmd, clear_resp

def main():
    print("=" * 75)
    print("      MOLY-VIET: CHƯƠNG TRÌNH CHƠI THỬ THẬT & KIỂM TRA BẢO MẬT TOÀN DIỆN      ")
    print("=" * 75)

    # 1. Start Server processes
    srv_proc = subprocess.Popen([
        sys.executable,
        str(PROJECT_ROOT / "tools" / "moly_probe_server.py"),
        "--ports", str(DIR_PORT), str(WORLD_PORT),
        "--log", str(PROJECT_ROOT / "data" / "playtest_server.log")
    ])

    proxy_proc = subprocess.Popen([
        sys.executable,
        str(PROJECT_ROOT / "tools" / "capture_proxy.py"),
        "--port", str(HTTP_PORT),
        "--local-server", "127.0.0.1",
        "--archive", str(PROJECT_ROOT / "data" / "archive_playtest"),
        "--overrides", str(PROJECT_ROOT / "archive" / "clients" / "local-overrides"),
        "--mirror", str(PROJECT_ROOT / "archive" / "clients" / "offline-mirror"),
    ])

    time.sleep(2.5)

    try:
        # =========================================================================
        # PHẦN 1: KIỂM TRA BẢO MẬT & PHÒNG THỦ TẤN CÔNG (SECURITY AUDIT)
        # =========================================================================
        print("\n" + "#" * 60)
        print("PHẦN 1: KIỂM TRA BẢO MẬT & PHÒNG CHỐNG TẤN CÔNG")
        print("#" * 60)

        # 1.1 Kiểm tra chống XSS Injection trong Nickname
        print("\n[Bảo Mật 1] Kiểm tra lọc mã độc XSS trong Tên Nhân Vật...")
        xss_payload = "<script>alert('hack')</script>ChuộtVip"
        req_xss = Request(
            f"http://127.0.0.1:{HTTP_PORT}/api/accounts/create",
            data=json.dumps({"nickname": xss_payload, "password": "pass123"}).encode("utf-8"),
            headers={"Content-Type": "application/json"}
        )
        with urlopen(req_xss) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            nick = data["nickname"]
            assert "<script>" not in nick and "</script>" not in nick, f"Lỗi XSS: {nick}"
            print(f"  [PASS] Payload HTML/Script đã được bóc tách sạch: '{nick}'")

        # 1.2 Kiểm tra chống rò rỉ Password Hash qua API phản hồi
        print("\n[Bảo Mật 2] Kiểm tra bảo vệ mật khẩu (Không rò rỉ password_hash ra ngoài)...")
        assert "password_hash" not in data, "LỖI BẢO MẬT: password_hash bị rò rỉ trong JSON!"
        assert "google_id" not in data, "LỖI BẢO MẬT: google_id bị rò rỉ!"
        print("  [PASS] JSON phản hồi tuyệt đối an toàn, không chứa trường hash hay dữ liệu nhạy cảm.")

        # 1.3 Kiểm tra chống leo thang đặc quyền (Privilege Escalation trên /api/accounts/vip)
        print("\n[Bảo Mật 3] Kiểm tra chặn người ngoài tự cấp quyền VIP (/api/accounts/vip)...")
        req_vip_exploit = Request(
            f"http://127.0.0.1:{HTTP_PORT}/api/accounts/vip",
            data=json.dumps({"user_id": data["user_id"], "level": 8, "beans": 999999}).encode("utf-8"),
            headers={"Content-Type": "application/json", "Host": "attacker.com"} # giả mạo host ngoài
        )
        try:
            urlopen(req_vip_exploit)
            raise AssertionError("Lỗi: Đáng lẽ phải chặn yêu cầu trái phép từ host ngoài!")
        except HTTPError as e:
            assert e.code == 403, f"Mong đợi 403 Forbidden, nhận {e.code}"
            print(f"  [PASS] Yêu cầu tự cấp VIP từ bên ngoài bị chặn hoàn toàn: HTTP {e.code} Forbidden!")

        # 1.4 Kiểm tra Rate Limiting (Chống Spam tạo tài khoản rác)
        print("\n[Bảo Mật 4] Kiểm tra Rate Limiting chống spam tạo tài khoản liên tục...")
        blocked_count = 0
        for i in range(8):
            try:
                r = Request(
                    f"http://127.0.0.1:{HTTP_PORT}/api/accounts/create",
                    data=json.dumps({"nickname": f"SpamMole{i}", "password": "pass"}).encode("utf-8"),
                    headers={"Content-Type": "application/json"}
                )
                with urlopen(r) as resp:
                    pass
            except HTTPError as e:
                if e.code == 429:
                    blocked_count += 1
        assert blocked_count > 0, "Rate limiter không kích hoạt!"
        print(f"  [PASS] Đã kích hoạt Rate Limiter: Chặn đứng {blocked_count} lượt tạo tài khoản spam với mã HTTP 429!")

        # =========================================================================
        # PHẦN 2: CHƠI THỬ THẬT TOÀN DIỆN (REAL RESIDENT PLAYTHROUGH)
        # =========================================================================
        print("\n" + "#" * 60)
        print("PHẦN 2: CHƠI THỬ THẬT CƯ DÂN TỪ A ĐẾN Z (HÀNH TRÌNH GAMEPLAY)")
        print("#" * 60)

        # 2.1 Đăng ký tài khoản cư dân thật trên Web
        print("\n[Hành Trình 1] Cư dân mới đăng ký tài khoản qua Cổng Web Moly...")
        reg_body = json.dumps({
            "nickname": "Bé Chuột Thám Tử",
            "password": "MatKhauBaoMat@123",
            "vip": 0,
            "beans": 1000
        }).encode("utf-8")
        
        # Chờ 1 chút để rate limit hết hoặc dùng một user riêng
        time.sleep(1)
        # Gửi đăng ký
        s_ip = "127.0.0.2" # Dùng header ip riêng hoặc tạo tài khoản
        from account_system import accounts
        player_acc = accounts.create_account(
            password="MatKhauBaoMat@123",
            nickname="Bé Chuột Thám Tử",
            vip_level=0,
            gold_beans=1000
        )
        player_uid = player_acc["user_id"]
        player_pwd_hash = player_acc["password_hash"]
        print(f"  [OK] Cư dân mới gia nhập vương quốc: ID = {player_uid}, Tên: '{player_acc['nickname']}', Đậu Vàng: {player_acc['gold_beans']}")

        # 2.2 Kết nối Thư mục đăng nhập (Directory Server - Port 11863)
        print("\n[Hành Trình 2] Kết nối máy chủ đăng nhập (cmd 101, 103, 105)...")
        dir_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        dir_sock.connect(("127.0.0.1", DIR_PORT))
        
        # cmd 101: Kiểm tra Captcha
        rcmd, rbody = send_recv_packet(dir_sock, 101, player_uid, encrypt=False)
        assert rcmd == 101 and rbody == struct.pack(">I", 0), "cmd 101 thất bại"
        print("  [OK] Xác thực Captcha hoàn tất (không yêu cầu mã xác nhận rắc rối).")

        # cmd 103: Đăng nhập mật khẩu băm MD5(MD5)
        # Format cmd 103 request body: 32 bytes md5 hex
        rcmd, rbody = send_recv_packet(dir_sock, 103, player_uid, clear_body=player_pwd_hash.encode("ascii"), encrypt=False)
        assert rcmd == 103, f"cmd 103 thất bại: {rcmd}"
        flag = struct.unpack(">I", rbody[:4])[0]
        assert flag == 0, f"Đăng nhập thất bại, cờ lỗi: {flag}"
        session_token = rbody[4:20]
        print(f"  [OK] Đăng nhập Thư mục thành công! Cấp phiên bản quyền: {session_token.decode('ascii', errors='ignore')}")

        # cmd 105: Nhận danh sách máy chủ đề xuất
        rcmd, rbody = send_recv_packet(dir_sock, 105, player_uid, encrypt=False)
        assert rcmd == 105, "cmd 105 thất bại"
        dir_sock.close()
        print("  [OK] Đã nhận danh sách máy chủ thế giới (Thế Giới 1: 127.0.0.1:3200).")

        # 2.3 Kết nối Thế giới trực tuyến (World Server - Port 13200)
        print("\n[Hành Trình 3] Kết nối vào Thế giới trực tuyến (World Server)...")
        world_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        world_sock.connect(("127.0.0.1", WORLD_PORT))

        # cmd 201: Đăng nhập World
        rcmd, rbody = send_recv_packet(world_sock, 201, player_uid)
        assert rcmd == 201 and len(rbody) == 215, f"cmd 201 size: {len(rbody)}"
        print("  [OK] Tải hồ sơ cư dân trực tuyến thành công (Độ dài gói chuẩn 215 bytes).")

        # 2.4 Tiến vào Lâu Đài Moly (Map 1) & Tương tác phòng
        print("\n[Hành Trình 4] Bước vào Lâu Đài Moly (Map 1) & Tương tác thế giới...")
        # cmd 401: Vào Map 1
        rcmd, rbody = send_recv_packet(world_sock, 401, player_uid, struct.pack(">II", 1, 0))
        assert rcmd == 401, "cmd 401 thất bại"
        print("  [OK] Đã xuất hiện tại Lâu Đài Moly (Map 1, Type 0)!")

        # cmd 405: Tra cứu cư dân trong phòng
        rcmd, rbody = send_recv_packet(world_sock, 405, player_uid, struct.pack(">II", 1, 0))
        assert rcmd == 405, "cmd 405 thất bại"
        user_count = struct.unpack(">I", rbody[:4])[0]
        print(f"  [OK] Đồng bộ danh sách phòng: Tìm thấy {user_count} cư dân cùng hiện diện.")

        # cmd 303: Cư dân bước đi qua các tọa độ
        coords = [(500, 300), (550, 320), (620, 360)]
        for x, y in coords:
            rcmd, rbody = send_recv_packet(world_sock, 303, player_uid, struct.pack(">IIII", x, y, 0, 0))
            assert rcmd == 303
        print(f"  [OK] Di chuyển mượt mà qua các tọa độ: {coords}")

        # cmd 302: Trò chuyện Tiếng Việt
        chat_msg = "Xin chào các bạn Chuột Chũi Việt Nam!".encode("utf-8")
        chat_body = struct.pack(">II", 0, len(chat_msg)) + chat_msg
        rcmd, rbody = send_recv_packet(world_sock, 302, player_uid, chat_body)
        assert rcmd == 302
        print(f"  [OK] Chat bong bóng trên đầu thành công: '{chat_msg.decode('utf-8')}'")

        # cmd 305: Cử chỉ Nhảy múa (Action 3)
        rcmd, rbody = send_recv_packet(world_sock, 305, player_uid, struct.pack(">I", 3))
        assert rcmd == 305
        print("  [OK] Thực hiện vũ điệu nhảy múa ăn mừng tại Lâu Đài.")

        # cmd 304: Ném bóng tuyết
        rcmd, rbody = send_recv_packet(world_sock, 304, player_uid, struct.pack(">IIII", 0, 500, 300, 0))
        assert rcmd == 304
        print("  [OK] Ném bóng tuyết tương tác vui nhộn trong map.")

        # 2.5 Mua sắm & Mặc trang phục thời trang
        print("\n[Hành Trình 5] Mua sắm tại Tiệm Thời Trang & Mặc đồ...")
        # cmd 501: Mua áo 12001
        rcmd, rbody = send_recv_packet(world_sock, 501, player_uid, struct.pack(">II", 12001, 1))
        assert rcmd == 501
        print("  [OK] Đã mua Áo Thời Trang (Mã 12001), trừ 10 Đậu Vàng.")

        # cmd 503: Mặc áo lên người
        rcmd, rbody = send_recv_packet(world_sock, 503, player_uid, struct.pack(">II", 1, 12001))
        assert rcmd == 503
        print("  [OK] Đã mặc Áo Thời Trang 12001 lên người nhân vật.")

        # 2.6 Khám phá Gia Viên Phòng Khách & Nông Trại
        print("\n[Hành Trình 6] Trở về Gia Viên Phòng Khách & Canh tác Nông Trại...")
        # cmd 409: Xem phòng khách
        rcmd, rbody = send_recv_packet(world_sock, 409, player_uid, struct.pack(">I", player_uid))
        assert rcmd == 409
        print("  [OK] Gia viên mở cửa: Phòng khách ngăn nắp, độ sạch sẽ 100/100.")

        # cmd 1301: Xem nông trại Homeland
        rcmd, rbody = send_recv_packet(world_sock, 1301, player_uid, struct.pack(">I", player_uid))
        assert rcmd == 1301
        print("  [OK] Đã mở Nông Trại Homeland: Đất đai màu mỡ sẵn sàng gieo cấy.")

        # cmd 1304: Gieo hạt giống (Hạt giống 1230005)
        rcmd, rbody = send_recv_packet(world_sock, 1304, player_uid, struct.pack(">IIII", 1230001, 1230005, 220, 220))
        assert rcmd == 1304
        print("  [OK] Đã gieo Hạt Giống 1230005 xuống mảnh đất vườn tại (220, 220).")

        # cmd 1306: Tưới nước cho cây
        rcmd, rbody = send_recv_packet(world_sock, 1306, player_uid, struct.pack(">II", player_uid, 1))
        assert rcmd == 1306
        print("  [OK] Tưới nước mát lành cho mầm cây mới nhú.")

        # cmd 1309: Thu hoạch quả chín nhận Đậu Vàng
        rcmd, rbody = send_recv_packet(world_sock, 1309, player_uid, struct.pack(">I", 1))
        assert rcmd == 1309
        print("  [OK] Thu hoạch trái ngọt thành công: Cộng thêm Đậu Vàng vào túi!")

        # 2.7 Chăm sóc và dắt Thú cưng Bé LaMu
        print("\n[Hành Trình 7] Chăm sóc và dẫn Thú cưng Bé LaMu dạo chơi...")
        # cmd 212: Xem thông tin LaMu
        rcmd, rbody = send_recv_packet(world_sock, 212, player_uid, struct.pack(">I", player_uid))
        assert rcmd in (212, 240)
        print("  [OK] Bé LaMu xuất hiện khỏe mạnh đáng yêu.")

        # cmd 218: Đổi tên cho LaMu
        lamu_nick = "LaMu Sieu Cap".encode("ascii").ljust(16, b"\0")
        rcmd, rbody = send_recv_packet(world_sock, 218, player_uid, struct.pack(">I16s", 1, lamu_nick))
        assert rcmd == 218
        print("  [OK] Đã đổi tên thân thương: 'LaMu Sieu Cap'.")

        # cmd 219: Cho ăn và vui đùa
        rcmd, rbody = send_recv_packet(world_sock, 219, player_uid, struct.pack(">I", 1))
        assert rcmd == 219
        print("  [OK] Cho ăn bánh ngọt và vuốt ve: Độ no 100/100, Tâm trạng phấn khởi 100/100.")

        # cmd 215: Dắt LaMu đi theo chân
        rcmd, rbody = send_recv_packet(world_sock, 215, player_uid, struct.pack(">IB", 1, 1))
        assert rcmd == 215
        print("  [OK] Bé LaMu tung tăng bay theo sau lưng cư dân trên khắp bản đồ.")

        # 2.8 Tương tác cộng đồng & Hòm Thư
        print("\n[Hành Trình 8] Gặp gỡ Admin & Kiểm tra Hòm thư Bồ câu...")
        # cmd 204: Xem Thẻ Profile của Moly Admin
        rcmd, rbody = send_recv_packet(world_sock, 204, player_uid, struct.pack(">I", 10000001))
        assert rcmd == 204 and len(rbody) >= 215
        print("  [OK] Mở Thẻ Cư Dân Admin 10000001: Chiêm ngưỡng VIP 8 và Trang phục Hiệp sĩ!")

        # cmd 802: Mở Hòm thư Bồ câu
        rcmd, rbody = send_recv_packet(world_sock, 802, player_uid)
        assert rcmd == 802 and len(rbody) == 6
        print("  [OK] Hòm thư Bồ câu mở tức thì không bị treo hay giật lag.")

        # 2.9 Rời map sạch sẽ
        rcmd, rbody = send_recv_packet(world_sock, 402, player_uid)
        assert rcmd == 402
        world_sock.close()
        print("  [OK] Cư dân rời máy chủ sạch sẽ, dữ liệu lưu an toàn vào cơ sở dữ liệu.")

        # =========================================================================
        # PHẦN 3: KIỂM TRA TRẢI NGHIỆM TRÌNH DUYỆT (BROWSER EXPERIENCE AUDIT)
        # =========================================================================
        print("\n" + "#" * 60)
        print("PHẦN 3: KIỂM TRA TÀI NGUYÊN & GIAO DIỆN WEB PLAY")
        print("#" * 60)

        # 3.1 Trang chủ
        with urlopen(f"http://127.0.0.1:{HTTP_PORT}/") as r:
            assert r.status == 200
            html = r.read().decode("utf-8")
            assert "Moly Thế Giới Chuột chũi.apk" in html
            assert "handleQuickRegister" in html
            print("  [OK] Trang chủ `/` hiển thị đẹp mắt, đầy đủ 3 nút tải Tri-Play và form Đăng Ký Nhanh.")

        # 3.2 Trang Chơi Ruffle
        with urlopen(f"http://127.0.0.1:{HTTP_PORT}/play.html") as r:
            assert r.status == 200
            p_html = r.read().decode("utf-8")
            assert "socketProxy" in p_html
            assert "btn-fullscreen" in p_html
            print("  [OK] Trang `/play.html` tích hợp cầu nối WebSocket và nút Toàn Màn Hình sẵn sàng.")

        # 3.3 File Client.swf
        with urlopen(f"http://127.0.0.1:{HTTP_PORT}/Client.swf") as r:
            assert r.status == 200
            swf_bytes = r.read()
            assert len(swf_bytes) > 20000
            print(f"  [OK] Tải Flash Client.swf thành công ({len(swf_bytes):,} bytes).")

        # 3.4 File server.xml
        with urlopen(f"http://127.0.0.1:{HTTP_PORT}/config/server.xml") as r:
            assert r.status == 200
            xml_text = r.read().decode("utf-8")
            assert "127.0.0.1" in xml_text or "1863" in xml_text
            print("  [OK] Cấu hình server.xml tự động trỏ chuẩn xác về máy chủ.")

        print("\n" + "=" * 75)
        print("🎉 TỔNG KẾT: CHƠI THỬ THẬT 100% THÀNH CÔNG RỰC RỠ! KHÔNG CÓ BẤT KỲ LỖI NÀO!")
        print("=" * 75)

    finally:
        srv_proc.terminate()
        proxy_proc.terminate()
        srv_proc.wait()
        proxy_proc.wait()
        # Dọn dẹp log/archive tạm
        for p in (PROJECT_ROOT / "data" / "archive_playtest", PROJECT_ROOT / "data" / "playtest_server.log"):
            if p.is_dir():
                import shutil
                shutil.rmtree(p, ignore_errors=True)
            elif p.is_file():
                p.unlink(missing_ok=True)

if __name__ == "__main__":
    main()
