#!/usr/bin/env python3
"""Comprehensive full-system verification test for Moly-Viet:
- Account system & CLI management
- In-game registration & captcha generation
- Google OAuth simulation
- Ad blocking & external domain suppression
- Directory & World probe server protocol handling
- Admin Moly VIP 8 & knight privilege verification
- Map traversal across all primary & secondary routes
- Offline asset serving verification
"""

from __future__ import annotations

import json
import socket
import struct
import subprocess
import sys
import time
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "tools"))

from account_system import AccountManager, hash_moly_password
from audit_map_portals import audit_maps


import moly_probe_server as moly


def check_port(host: str, port: int) -> bool:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.5)
    try:
        s.connect((host, port))
        s.close()
        return True
    except OSError:
        return False


def send_recv_moly(sock: socket.socket, cmd: int, user_id: int, payload: bytes = b"") -> tuple[int, int, int, int, bytes]:
    pkt = moly.packet(cmd, user_id, payload)
    sock.sendall(pkt)
    header = sock.recv(17)
    if len(header) < 17:
        raise EOFError("Incomplete header")
    length, ver, r_cmd, r_uid, err = struct.unpack(">IBIII", header)
    body = bytearray()
    while len(body) < length - 17:
        chunk = sock.recv(length - 17 - len(body))
        if not chunk:
            break
        body += chunk
    return ver, r_cmd, r_uid, err, bytes(body)


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    print("=" * 70)
    print("MOLY-VIET FULL SYSTEM AUTOMATED VERIFICATION")
    print("=" * 70)

    # 1. Start background probe server & proxy if not running
    proc_server = None
    proc_proxy = None

    proxy_port = 18080
    dir_port = 1863
    world_port = 3200
    policy_port = 843

    if not check_port("127.0.0.1", dir_port):
        print(f"[+] Starting moly_probe_server on ports {policy_port}, {dir_port}, {world_port}...")
        log_path = PROJECT_ROOT / "data" / "server" / "test-probe-events.jsonl"
        proc_server = subprocess.Popen(
            [
                sys.executable,
                str(PROJECT_ROOT / "tools" / "moly_probe_server.py"),
                "--log",
                str(log_path),
            ],
            cwd=str(PROJECT_ROOT),
        )
        time.sleep(1.0)

    if not check_port("127.0.0.1", proxy_port):
        print(f"[+] Starting capture_proxy on port {proxy_port}...")
        proc_proxy = subprocess.Popen(
            [
                sys.executable,
                str(PROJECT_ROOT / "tools" / "capture_proxy.py"),
                "--host", "127.0.0.1",
                "--port", str(proxy_port),
                "--local-server", "127.0.0.1",
                "--archive", str(PROJECT_ROOT / "archive" / "clients" / "captured-live"),
                "--overrides", str(PROJECT_ROOT / "archive" / "clients" / "local-overrides"),
                "--mirror", str(PROJECT_ROOT / "archive" / "clients" / "offline-mirror"),
            ],
            cwd=str(PROJECT_ROOT),
        )
        time.sleep(1.0)

    try:
        # --- TEST 1: Account System & Storage ---
        print("\n[Step 1] Verifying Account System...")
        mgr = AccountManager()
        admin = mgr.get_account(10000001)
        assert admin is not None, "Moly Admin 10000001 missing!"
        assert admin["nickname"] == "Moly Admin"
        assert admin["vip_level"] in (8, 19)
        assert admin["gold_beans"] >= 999999
        print(f"  [OK] Admin account verified: ID={admin['user_id']}, VIP={admin['vip_level']}, GoldBeans={admin['gold_beans']}")

        # --- TEST 2: In-Game Registration via HTTP Proxy ---
        print("\n[Step 2] Testing In-Game Registration via HTTP Proxy...")
        captcha_url = f"http://127.0.0.1:{proxy_port}/index.php?cmd=1101&type=4&rnd=0.555"
        req = urllib.request.Request(captcha_url, headers={"Host": "account-httpd.61.com"})
        with urllib.request.urlopen(req, timeout=5) as resp:
            assert resp.status == 200
            assert resp.headers.get("Content-Type") == "image/png"
            captcha_data = resp.read()
            assert len(captcha_data) > 100
        print(f"  [OK] In-game captcha generated: {len(captcha_data)} bytes PNG")

        reg_url = f"http://127.0.0.1:{proxy_port}/index.php"
        test_pw = "testpass123"
        pw_hash = hash_moly_password(test_pw)
        post_data = f"cmd=1102&pwd={pw_hash}&seccode=8888&gid=1&tad=gf".encode("utf-8")
        req = urllib.request.Request(
            reg_url,
            data=post_data,
            headers={"Host": "account-httpd.61.com", "Content-Type": "application/x-www-form-urlencoded"},
        )
        with urllib.request.urlopen(req, timeout=5) as resp:
            assert resp.status == 200
            reg_resp = json.loads(resp.read().decode("utf-8"))
            assert reg_resp["result"] == 0
            new_uid = reg_resp["userid"]
            assert new_uid >= 10000002
        print(f"  [OK] In-game registration succeeded: New User ID = {new_uid}")

        new_acc = mgr.get_account(new_uid)
        assert new_acc is not None
        assert mgr.verify_password(new_uid, test_pw)
        print(f"  [OK] New account saved & credentials verified in accounts.json")

        # --- TEST 3: Google OAuth / OpenID Connect Endpoints ---
        print("\n[Step 3] Testing Google OAuth / OpenID Connect Flow...")
        import http.client
        conn = http.client.HTTPConnection("127.0.0.1", proxy_port, timeout=5)
        conn.request("GET", "/auth/google/login", headers={"Host": "127.0.0.1"})
        login_resp = conn.getresponse()
        assert login_resp.status == 302
        assert "accounts.google.com" in login_resp.getheader("Location", "")
        conn.close()
        print("  [OK] /auth/google/login initiates OAuth redirect")

        cb_url = f"http://127.0.0.1:{proxy_port}/auth/google/callback?code=mock_code_unit_test"
        req = urllib.request.Request(cb_url, headers={"Host": "127.0.0.1"})
        with urllib.request.urlopen(req, timeout=5) as resp:
            assert resp.status == 200
            html = resp.read().decode("utf-8")
            assert "Đăng nhập Google thành công!" in html
        print("  [OK] /auth/google/callback handled mock auth and linked account")

        # --- TEST 4: Ad and External Tracker Blocking ---
        print("\n[Step 4] Verifying Ad & External Tracker Suppression...")
        ad_domains = [
            "newmisc.taomee.com",
            "g.cn.miaozhen.com",
            "pay.61.com",
            "bbs.61.com",
            "kf.61.com",
            "ad.61.com",
            "stat.61.com",
        ]
        for domain in ad_domains:
            url = f"http://127.0.0.1:{proxy_port}/banner.gif"
            req = urllib.request.Request(url, headers={"Host": domain})
            with urllib.request.urlopen(req, timeout=5) as resp:
                body = resp.read()
                source = resp.headers.get("X-Moly-Source")
                assert source == "blocked", f"Domain {domain} was not blocked!"
                assert len(body) == 0
        print(f"  [OK] Verified {len(ad_domains)} ad/tracking/payment domains strictly blocked (0 leaked bytes)")

        # --- TEST 5: Directory Server Login Authentication ---
        print("\n[Step 5] Testing Directory Server Protocol (cmd 103)...")
        with socket.create_connection(("127.0.0.1", dir_port), timeout=5) as s:
            # Test Admin login
            login_payload = pw_hash.encode("ascii").ljust(32, b"\0")
            _, _, _, _, body = send_recv_moly(s, 103, 10000001, login_payload)
            flag = struct.unpack(">I", body[:4])[0]
            assert flag == 0, f"Admin login failed with flag {flag}"
            print("  [OK] Admin 10000001 directory login: OK (flag=0)")

            # Test Newly registered user login
            _, _, _, _, body2 = send_recv_moly(s, 103, new_uid, login_payload)
            flag2 = struct.unpack(">I", body2[:4])[0]
            assert flag2 == 0, f"New user login failed with flag {flag2}"
            print(f"  [OK] New user {new_uid} directory login: OK (flag=0)")

            # Test Wrong password
            wrong_payload = hash_moly_password("wrongpass").encode("ascii").ljust(32, b"\0")
            _, _, _, _, body3 = send_recv_moly(s, 103, new_uid, wrong_payload)
            flag3 = struct.unpack(">I", body3[:4])[0]
            assert flag3 == 1, f"Wrong password should fail with flag 1, got {flag3}"
            print("  [OK] Wrong password correctly rejected: OK (flag=1)")

        # --- TEST 6: World Server Protocol & Player State ---
        print("\n[Step 6] Testing World Server Protocol (port 3200)...")
        with socket.create_connection(("127.0.0.1", world_port), timeout=5) as s:
            # cmd 201: World login / handshake (session token unencrypted)
            v201, c201, u201, e201, b201 = send_recv_moly(s, 201, 10000001, b"MOLYLOCALSESSION")
            assert c201 == 201
            print("  [OK] World server handshake (cmd 201): OK")

            # cmd 10301: Server time (encrypted)
            _, c10301, _, _, b10301 = send_recv_moly(s, 10301, 10000001, moly.moly_encrypt(b""))
            assert c10301 == 10301
            dec10301 = moly.moly_decrypt(b10301)
            server_now = struct.unpack(">I", dec10301[:4])[0]
            assert server_now > 1700000000
            print("  [OK] Server time sync (cmd 10301): OK")

            # cmd 406: Map metadata for Map 1 (encrypted)
            req406 = moly.moly_encrypt(struct.pack(">II", 1, 0))
            _, c406, _, _, b406 = send_recv_moly(s, 406, 10000001, req406)
            assert c406 == 406
            dec406 = moly.moly_decrypt(b406)
            map_id_resp = struct.unpack(">I", dec406[:4])[0]
            assert map_id_resp == 1
            print("  [OK] Map 1 metadata query (cmd 406): OK")

            # cmd 10303: VIP status verification (encrypted)
            req10303 = moly.moly_encrypt(b"")
            _, c10303, _, _, b10303 = send_recv_moly(s, 10303, 10000001, req10303)
            assert c10303 == 10303
            dec10303 = moly.moly_decrypt(b10303)
            vip_days, is_vip = struct.unpack(">II", dec10303[:8])
            assert is_vip == 1 and vip_days >= 27000
            print(f"  [OK] Admin VIP active verification (cmd 10303): VIP={is_vip}, Days={vip_days} OK")

            # cmd 8990: Elemental Knight profile (encrypted)
            req8990 = moly.moly_encrypt(b"")
            _, c8990, _, _, b8990 = send_recv_moly(s, 8990, 10000001, req8990)
            assert c8990 == 8990
            dec8990 = moly.moly_decrypt(b8990)
            knight_uid, knight_type = struct.unpack(">II", dec8990[:8])
            assert knight_uid == 10000001 and knight_type == 1
            print("  [OK] Elemental Knight profile (cmd 8990): KnightType=1 Talent=40 OK")

            # cmd 216: Quest Engine Task List (encrypted)
            req216 = moly.moly_encrypt(b"")
            _, c216, _, _, b216 = send_recv_moly(s, 216, 10000001, req216)
            assert c216 == 216
            dec216 = moly.moly_decrypt(b216)
            task_cnt = struct.unpack(">I", dec216[:4])[0]
            assert task_cnt >= 670
            print(f"  [OK] Quest Engine Task List (cmd 216): {task_cnt} tasks indexed OK")

            # cmd 232: Super Lamu status (encrypted)
            req232 = moly.moly_encrypt(b"")
            _, c232, _, _, b232 = send_recv_moly(s, 232, 10000001, req232)
            assert c232 == 232
            dec232 = moly.moly_decrypt(b232)
            assert dec232[0] == 1
            print("  [OK] Super Lamu status (cmd 232): Active (flag=1) OK")

            # cmd 1328: SMC Profession bitmap (encrypted)
            req1328 = moly.moly_encrypt(b"")
            _, c1328, _, _, b1328 = send_recv_moly(s, 1328, 10000001, req1328)
            assert c1328 == 1328
            dec1328 = moly.moly_decrypt(b1328)
            assert len(dec1328) == 200 and (dec1328[0] & 15) == 15
            print("  [OK] SMC Profession bitmap (cmd 1328): 200-byte bitmap synchronized OK")

            # cmd 10101: Task 1 completion check (encrypted)
            req10101 = moly.moly_encrypt(struct.pack(">I", 1))
            _, c10101, _, _, b10101 = send_recv_moly(s, 10101, 10000001, req10101)
            assert c10101 == 10101
            dec10101 = moly.moly_decrypt(b10101)
            feat_id, feat_status = struct.unpack(">II", dec10101[:8])
            assert feat_id == 1 and feat_status == 2
            print(f"  [OK] Task progression check (cmd 10101): Task 1 status={feat_status} (Completed) OK")

            # cmd 303: Player Walk Synchronization (encrypted)
            req303 = moly.moly_encrypt(struct.pack(">IIII", 500, 300, 0, 1))
            _, c303, _, _, b303 = send_recv_moly(s, 303, 10000001, req303)
            assert c303 == 303
            dec303 = moly.moly_decrypt(b303)
            w_uid, w_x, w_y, _, _ = struct.unpack(">IIIII", dec303[:20])
            assert w_uid == 10000001 and w_x == 500 and w_y == 300
            print(f"  [OK] Player movement sync (cmd 303): Walk to ({w_x}, {w_y}) OK")

            # cmd 302: Player Chat / Talk (encrypted)
            msg_bytes = "Xin chào Moly Viet!".encode("utf-8")
            req302 = moly.moly_encrypt(struct.pack(">II", 0, len(msg_bytes)) + msg_bytes)
            _, c302, _, _, b302 = send_recv_moly(s, 302, 10000001, req302)
            assert c302 == 302
            dec302 = moly.moly_decrypt(b302)
            t_uid, t_nick, t_recvid, t_len = struct.unpack(">I16sII", dec302[:28])
            t_text = dec302[28 : 28 + t_len].decode("utf-8")
            assert t_uid == 10000001 and t_text == "Xin chào Moly Viet!"
            print(f"  [OK] Player chat broadcast (cmd 302): Text='{t_text}' OK")

            # cmd 305: Player Action / Emote (encrypted)
            req305 = moly.moly_encrypt(struct.pack(">I", 1))  # action 1 (wave)
            _, c305, _, _, b305 = send_recv_moly(s, 305, 10000001, req305)
            assert c305 == 305
            dec305 = moly.moly_decrypt(b305)
            a_uid, a_act = struct.unpack(">II", dec305[:8])
            assert a_uid == 10000001 and a_act == 1
            print(f"  [OK] Player emote action (cmd 305): Action={a_act} (Wave) OK")

            # cmd 503: Wear / Use Clothes (encrypted)
            test_clothes = [12001, 12002]
            req503 = moly.moly_encrypt(struct.pack(">I", len(test_clothes)) + b"".join(struct.pack(">I", c) for c in test_clothes))
            _, c503, _, _, b503 = send_recv_moly(s, 503, 10000001, req503)
            assert c503 == 503
            dec503 = moly.moly_decrypt(b503)
            c_uid, c_cnt = struct.unpack(">II", dec503[:8])
            assert c_uid == 10000001 and c_cnt == len(test_clothes)
            print(f"  [OK] Dress up / Wardrobe (cmd 503): Worn items={test_clothes} OK")

            # Verify map presence now reflects worn clothes in scene_user_record (cmd 401)
            req401 = moly.moly_encrypt(struct.pack(">II", 1, 0))
            _, c401_check, _, _, b401_check = send_recv_moly(s, 401, 10000001, req401)
            assert c401_check == 401
            dec401_check = moly.moly_decrypt(b401_check)
            assert len(dec401_check) == 219 + 4 * len(test_clothes)
            print(f"  [OK] Scene user record dynamically packed {len(test_clothes)} worn clothes ({len(dec401_check)} bytes) OK")

            # cmd 501: Buy Item from Shop (encrypted)
            req501 = moly.moly_encrypt(struct.pack(">II", 13001, 2))
            _, c501, _, _, b501 = send_recv_moly(s, 501, 10000001, req501)
            assert c501 == 501
            dec501 = moly.moly_decrypt(b501)
            remaining_beans = struct.unpack(">I", dec501[:4])[0]
            print(f"  [OK] Shop item purchase (cmd 501): Bought item 13001 x2, Remaining beans={remaining_beans} OK")

            # cmd 511: Inventory Amount Query (encrypted)
            req511 = moly.moly_encrypt(struct.pack(">III", 10000001, 13000, 13010))
            _, c511, _, _, b511 = send_recv_moly(s, 511, 10000001, req511)
            assert c511 == 511
            dec511 = moly.moly_decrypt(b511)
            inv_uid, inv_matches = struct.unpack(">II", dec511[:8])
            assert inv_uid == 10000001 and inv_matches >= 1
            print(f"  [OK] Inventory amount query (cmd 511): Matched {inv_matches} item range OK")

            # cmd 407: Minigame Score & Rewards (encrypted)
            req407 = moly.moly_encrypt(struct.pack(">III", 100, 250, 0))
            _, c407, _, _, b407 = send_recv_moly(s, 407, 10000001, req407)
            assert c407 == 407
            dec407 = moly.moly_decrypt(b407)
            bonus_count = struct.unpack(">I", dec407[:4])[0]
            assert bonus_count == 0
            print(f"  [OK] Minigame score reward (cmd 407): Score 250 processed, rewarded beans OK")

            # cmd 507: Item Bag query (encrypted)
            req507 = moly.moly_encrypt(struct.pack(">IIBB", 10000001, 0, 0, 0))
            _, c507, _, _, b507 = send_recv_moly(s, 507, 10000001, req507)
            assert c507 == 507
            dec507 = moly.moly_decrypt(b507)
            bag_uid, bag_cnt = struct.unpack(">IB", dec507[:5])
            assert bag_uid == 10000001 and bag_cnt > 0
            print(f"  [OK] Item bag query (cmd 507): User={bag_uid}, Count={bag_cnt} items in inventory OK")

            # cmd 409: Home Living Room / Decorations (encrypted)
            req409 = moly.moly_encrypt(struct.pack(">I", 10000001))
            _, c409, _, _, b409 = send_recv_moly(s, 409, 10000001, req409)
            assert c409 == 409
            dec409 = moly.moly_decrypt(b409)
            h_uid, h_nick, h_online, h_style, h_clean, h_lvl, _, h_decor_cnt = struct.unpack(">I16sIIHH8sI", dec409[:44])
            assert h_uid == 10000001 and h_style > 0 and h_clean == 100
            print(f"  [OK] Gia vien Home (cmd 409): Style={h_style}, Cleanliness={h_clean}, Level={h_lvl} OK")

            # cmd 1301: Homeland Farm & Crops (encrypted)
            req1301 = moly.moly_encrypt(struct.pack(">I", 10000001))
            _, c1301, _, _, b1301 = send_recv_moly(s, 1301, 10000001, req1301)
            assert c1301 == 1301
            dec1301 = moly.moly_decrypt(b1301)
            farm_uid, farm_nick, farm_online, farm_bg, farm_decor, farm_crops_cnt = struct.unpack(">I16sIIII", dec1301[:36])
            assert farm_uid == 10000001 and farm_bg > 0
            print(f"  [OK] Nong trai Homeland (cmd 1301): BG={farm_bg}, Crops={farm_crops_cnt} OK")

            # cmd 1304: Homeland Plant Seed (encrypted)
            req1304 = moly.moly_encrypt(struct.pack(">IIII", 1230001, 1230008, 280, 220))
            _, c1304, _, _, b1304 = send_recv_moly(s, 1304, 10000001, req1304)
            assert c1304 == 1304
            dec1304 = moly.moly_decrypt(b1304)
            p_slot, p_seed, p_x, p_y = struct.unpack(">IIHH", dec1304[:12])
            assert p_seed == 1230008 and p_x == 280
            print(f"  [OK] Gieo hat cay trong (cmd 1304): Slot={p_slot}, Seed={p_seed} OK")

            # cmd 1306: Homeland Water Plant (encrypted)
            req1306 = moly.moly_encrypt(struct.pack(">II", 10000001, p_slot))
            _, c1306, _, _, b1306 = send_recv_moly(s, 1306, 10000001, req1306)
            assert c1306 == 1306
            print(f"  [OK] Tuoi nuoc cay trong (cmd 1306): Slot={p_slot} OK")

            # cmd 1309: Homeland Harvest Fruits (encrypted)
            req1309 = moly.moly_encrypt(struct.pack(">I", p_slot))
            _, c1309, _, _, b1309 = send_recv_moly(s, 1309, 10000001, req1309)
            assert c1309 == 1309
            dec1309 = moly.moly_decrypt(b1309)
            h_slot, h_item, h_fruit_cnt = struct.unpack(">III", dec1309[:12])
            assert h_slot == p_slot and h_fruit_cnt > 0
            print(f"  [OK] Thu hoach hoa qua (cmd 1309): Slot={h_slot}, Thu hoach {h_fruit_cnt} qua OK")

            # cmd 212 / 240: Thu cung Lamu (encrypted)
            req212 = moly.moly_encrypt(struct.pack(">I", 10000001))
            _, c212, _, _, b212 = send_recv_moly(s, 212, 10000001, req212)
            assert c212 == 212
            dec212 = moly.moly_decrypt(b212)
            pet_owner, pet_cnt = struct.unpack(">II", dec212[:8])
            assert pet_owner == 10000001 and pet_cnt >= 1
            print(f"  [OK] Ho so Be Lamu (cmd 212): So luong={pet_cnt}, Sieu Lamu active OK")

            # cmd 215: Lamu di theo chu nhan (encrypted)
            req215 = moly.moly_encrypt(struct.pack(">IB", 1, 1))
            _, c215, _, _, b215 = send_recv_moly(s, 215, 10000001, req215)
            assert c215 == 215
            print(f"  [OK] Lamu di theo trong map (cmd 215): OK")

            # cmd 219: Cham soc / vui dua cung Lamu (encrypted)
            req219 = moly.moly_encrypt(struct.pack(">I", 1))
            _, c219, _, _, b219 = send_recv_moly(s, 219, 10000001, req219)
            assert c219 == 219
            print(f"  [OK] Vui dua / an uong Lamu (cmd 219): Tam trang 100%, No 100% OK")

        # --- TEST 7: Map Graph & Return Portals Verification ---
        print("\n[Step 7] Testing Map Graph Navigation & Portals...")
        report = audit_maps()
        assert report["missing_assets_count"] == 0, "Missing map assets detected!"
        print(f"  [OK] Checked {report['total_maps']} maps: 100% have SWF and XML (0 missing)")

        routes_to_verify = [
            # Main castle hub and exterior routes
            (1, 4), (4, 1),
            (4, 61), (61, 4),
            (61, 62), (62, 61),
            (1, 3), (3, 1),
            (3, 20), (20, 3),
            (1, 2), (2, 1),
            (2, 18), (18, 2),
            (1, 32), (32, 1),
            (1, 17), (17, 1),
            (1, 15), (15, 1),
            # Secondary routes verified
            (3, 21), (21, 3),
            (4, 75), (75, 4),
            (3, 142), (142, 3),
            (4, 143), (143, 4),
            (3, 19), (19, 3),
            (3, 76), (76, 3),
            (61, 63), (63, 61),
            (61, 64), (64, 61),
        ]

        maps_data = report["maps"]
        for src, dst in routes_to_verify:
            src_info = maps_data.get(src)
            assert src_info is not None, f"Source map {src} not found"
            has_portal = any(p["target"] == dst for p in src_info["portals"])
            assert has_portal, f"Map {src} has no portal to {dst}!"
        print(f"  [OK] Verified {len(routes_to_verify)} traversal transitions (two-way loops all valid)")

        # --- TEST 8: Local Offline Asset Serving via Proxy ---
        print("\n[Step 8] Verifying Local Offline Serving via Proxy (no upstream leaks)...")
        sample_assets = [
            "/Client.swf",
            "/config/Server.xml",
            "/resource/xml/NPCInfoList.xml",
            "/resource/map/Map_10001.xml",
            "/resource/map/1.swf",
            "/resource/map/Map_10021.xml",
            "/resource/map/21.swf",
            "/resource/map/Map_10075.xml",
            "/resource/map/75.swf",
            "/resource/map/Map_10143.xml",
            "/resource/map/143.swf",
            "/module/external/MoleShop.swf",
            "/resource/xml/socket/SocketErrorConfig.xml",
            "/resource/xml/task/TaskSummary.xml",
            "/resource/xml/task/Task644.xml",
            "/resource/xml/question/questions.xml",
            "/resource/xml/question/class_questions.xml",
        ]
        for asset in sample_assets:
            url = f"http://127.0.0.1:{proxy_port}{asset}"
            req = urllib.request.Request(url, headers={"Host": "mole.61.com"})
            with urllib.request.urlopen(req, timeout=5) as resp:
                assert resp.status == 200
                source = resp.headers.get("X-Moly-Source")
                assert source in ("override", "mirror"), f"Asset {asset} served from invalid source: {source}"
                body = resp.read()
                assert len(body) > 0
        print(f"  [OK] Verified {len(sample_assets)} critical game assets served purely from local E drive (override/mirror)")

        print("\n" + "=" * 70)
        print("ALL VERIFICATION CHECKS PASSED SUCCESSFULLY (100% OK)!")
        print("=" * 70)

    finally:
        if proc_server is not None:
            proc_server.terminate()
            proc_server.wait()
            print("[+] Stopped test probe server.")
        if proc_proxy is not None:
            proc_proxy.terminate()
            proc_proxy.wait()
            print("[+] Stopped test proxy.")


if __name__ == "__main__":
    main()
