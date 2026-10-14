#!/usr/bin/env python3
"""Verification suite for Extended Protocols (204, 207, 606, 610, 802) and Quick Register."""

from __future__ import annotations

import json
import socket
import struct
import subprocess
import sys
import time
from pathlib import Path
from urllib.request import Request, urlopen

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "tools"))

if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if sys.stderr and hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

from moly_probe_server import moly_encrypt, moly_decrypt

SERVER_PORT = 13205
HTTP_PORT = 18090

def send_recv_packet(sock: socket.socket, cmd: int, uid: int, clear_body: bytes = b"") -> tuple[int, bytes]:
    enc_body = moly_encrypt(clear_body)
    head = struct.pack(">IBIII", 17 + len(enc_body), 1, cmd, uid, 0)
    sock.sendall(head + enc_body)
    
    resp_head = sock.recv(17)
    if len(resp_head) < 17:
        raise ValueError("Incomplete header")
    length, ver, rcmd, ruid, rres = struct.unpack(">IBIII", resp_head)
    resp_body = sock.recv(length - 17)
    clear_resp = moly_decrypt(resp_body)
    return rcmd, clear_resp

def main():
    print("=" * 70)
    print("VERIFYING EXTENDED COMMUNITY PROTOCOLS & QUICK REGISTRATION")
    print("=" * 70)

    # 1. Start Server
    srv_proc = subprocess.Popen([
        sys.executable,
        str(PROJECT_ROOT / "tools" / "moly_probe_server.py"),
        "--ports", str(SERVER_PORT),
        "--log", str(PROJECT_ROOT / "data" / "test_extended.log")
    ])

    # 2. Start Proxy
    proxy_proc = subprocess.Popen([
        sys.executable,
        str(PROJECT_ROOT / "tools" / "capture_proxy.py"),
        "--port", str(HTTP_PORT),
        "--local-server", "127.0.0.1",
        "--archive", str(PROJECT_ROOT / "data" / "archive_test")
    ])

    time.sleep(2)
    try:
        # [Test 1] Quick Web Registration API
        print("\n[Step 1] Testing 1-Click Web Quick Registration (/api/accounts/create)...")
        req_data = json.dumps({
            "nickname": "Chuột Chũi Hà Nội",
            "password": "mypassword123",
            "vip": 0,
            "beans": 1000
        }).encode("utf-8")
        req = Request(f"http://127.0.0.1:{HTTP_PORT}/api/accounts/create", data=req_data, headers={"Content-Type": "application/json"})
        with urlopen(req) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            new_uid = data["user_id"]
            print(f"  [OK] Created New Account UID: {new_uid}, Nick: {data['nickname']}")
            assert new_uid >= 10000000, "Invalid UID generated"

        # [Test 2] TCP World Connection & cmd 201 login
        print("\n[Step 2] Testing TCP Login for Admin (10000001)...")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(("127.0.0.1", SERVER_PORT))
        cmd, body = send_recv_packet(sock, 201, 10000001)
        print(f"  [OK] Logged in to World Server (cmd {cmd}, body size: {len(body)})")

        # [Test 3] cmd 204: User Profile Detail Card
        print("\n[Step 3] Testing cmd 204 (User Profile Detail Card)...")
        cmd, body = send_recv_packet(sock, 204, 10000001, struct.pack(">I", 10000001))
        assert cmd == 204, f"Expected cmd 204, got {cmd}"
        assert len(body) >= 215, f"cmd 204 body too short: {len(body)}"
        uid, nick = struct.unpack(">I16s", body[:20])
        print(f"  [OK] Profile Card returned successfully for UID {uid}: {nick.decode('utf-8', errors='ignore').strip()}")

        # [Test 4] cmd 207: User Basic Info
        print("\n[Step 4] Testing cmd 207 (User Basic Info)...")
        cmd, body = send_recv_packet(sock, 207, 10000001, struct.pack(">I", new_uid))
        assert cmd == 207, f"Expected cmd 207, got {cmd}"
        assert len(body) == 49, f"cmd 207 expected 49 bytes, got {len(body)}"
        print(f"  [OK] User Basic Info returned successfully (49 bytes exact match)!")

        # [Test 5] cmd 606 & 610: Friend List and Online Query
        print("\n[Step 5] Testing cmd 606 & cmd 610 (Friend List & Friends Online)...")
        cmd, body = send_recv_packet(sock, 606, 10000001)
        assert cmd == 606 and len(body) == 4, f"cmd 606 failed: {len(body)}"
        cnt = struct.unpack(">I", body)[0]
        assert cnt == 0, f"Expected 0 friends, got {cnt}"

        cmd, body = send_recv_packet(sock, 610, 10000001)
        assert cmd == 610 and len(body) == 2, f"cmd 610 failed: {len(body)}"
        print("  [OK] Friend List & Online Friends queries clean (no client hangs)!")

        # [Test 6] cmd 802: Pigeon Mailbox
        print("\n[Step 6] Testing cmd 802 (Pigeon Mailbox Postcards)...")
        cmd, body = send_recv_packet(sock, 802, 10000001)
        assert cmd == 802 and len(body) == 6, f"cmd 802 failed: {len(body)}"
        tot, unread, read = struct.unpack(">HHH", body)
        assert tot == 0 and unread == 0 and read == 0
        print("  [OK] Mailbox query returned 0 unread/read letters (no client hangs)!")

        sock.close()
        print("\n" + "=" * 70)
        print("🎉 ALL EXTENDED COMMUNITY PROTOCOL TESTS PASSED 100%!")
        print("=" * 70)

    finally:
        srv_proc.terminate()
        proxy_proc.terminate()
        srv_proc.wait()
        proxy_proc.wait()

if __name__ == "__main__":
    main()
