#!/usr/bin/env python3
"""End-to-End integration test for Moly-Viet Web Portal and WebSocket Bridge."""

import http.client
import json
import os
import socket
import subprocess
import sys
import time
from pathlib import Path
from urllib.parse import urlsplit

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "tools"))

from websocket_bridge import make_handshake_response, read_ws_frame, send_ws_frame


def run_test():
    print("=== STARTING INTEGRATION TEST FOR WEB PORTAL & WEBSOCKET BRIDGE ===")

    # 1. Start moly_probe_server.py
    server_cmd = [
        sys.executable,
        str(PROJECT_ROOT / "tools" / "moly_probe_server.py"),
        "--log",
        str(PROJECT_ROOT / "data" / "server" / "test-probe-events.jsonl"),
    ]
    server_proc = subprocess.Popen(server_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"[*] Started moly_probe_server (PID: {server_proc.pid})")

    # 2. Start capture_proxy.py
    proxy_cmd = [
        sys.executable,
        str(PROJECT_ROOT / "tools" / "capture_proxy.py"),
        "--archive", str(PROJECT_ROOT / "archive" / "clients" / "captured-live"),
        "--host", "127.0.0.1",
        "--port", "18081",  # Use dedicated test port 18081
        "--local-server", "127.0.0.1",
        "--overrides", str(PROJECT_ROOT / "archive" / "clients" / "local-overrides"),
        "--mirror", str(PROJECT_ROOT / "archive" / "clients" / "offline-mirror"),
    ]
    proxy_proc = subprocess.Popen(proxy_cmd)
    print(f"[*] Started capture_proxy on port 18081 (PID: {proxy_proc.pid})")

    time.sleep(2.0)

    try:
        conn = http.client.HTTPConnection("127.0.0.1", 18081, timeout=5)

        # Test 1: GET / (Homepage)
        print("\n[Test 1] GET / (Homepage)")
        conn.request("GET", "/")
        res = conn.getresponse()
        body = res.read()
        assert res.status == 200, f"Expected 200, got {res.status}"
        assert b"MOLY - TH\xe1\xba\xbe GI\xe1\xbb\x9aI CHU\xe1\xbb\x98T CH\xc5\xa8I" in body or b"Moly" in body
        print("  -> PASSED! Homepage rendered successfully.")

        # Test 2: GET /play.html
        print("\n[Test 2] GET /play.html (Game Stage)")
        conn.request("GET", "/play.html")
        res = conn.getresponse()
        body = res.read()
        assert res.status == 200, f"Expected 200, got {res.status}"
        assert b"socketProxy" in body
        assert b"/static/ruffle/ruffle.js" in body
        print("  -> PASSED! Play stage rendered with Ruffle socketProxy.")

        # Test 3: GET /assets/logo-horizontal.png
        print("\n[Test 3] GET /assets/logo-horizontal.png")
        conn.request("GET", "/assets/logo-horizontal.png")
        res = conn.getresponse()
        body = res.read()
        assert res.status == 200 and len(body) > 100000, f"Expected 200 PNG, got {res.status}, {len(body)} bytes"
        print(f"  -> PASSED! Logo loaded ({len(body):,} bytes).")

        # Test 4: GET /download/Moly-The-Gioi-Chuot-Chui.zip
        print("\n[Test 4] GET /download/Moly-The-Gioi-Chuot-Chui.zip (Direct Download)")
        conn.request("GET", "/download/Moly-The-Gioi-Chuot-Chui.zip")
        res = conn.getresponse()
        disp = res.getheader("Content-Disposition", "")
        length = int(res.getheader("Content-Length", 0))
        res.read()
        assert res.status == 200 and length > 50000000, f"Expected >50MB zip, got {res.status}, {length}"
        assert "attachment" in disp, f"Expected attachment disposition, got: {disp}"
        print(f"  -> PASSED! Direct Desktop Zip served: {length / (1024*1024):.2f} MB, disposition: {disp}")

        # Test 4B: GET /download/Moly-The-Gioi-Chuot-Chui.apk
        print("\n[Test 4B] GET /download/Moly-The-Gioi-Chuot-Chui.apk (Android APK Download)")
        conn.request("GET", "/download/Moly-The-Gioi-Chuot-Chui.apk")
        res = conn.getresponse()
        disp = res.getheader("Content-Disposition", "")
        mime = res.getheader("Content-Type", "")
        length = int(res.getheader("Content-Length", 0))
        res.read()
        assert res.status == 200 and length > 10000000, f"Expected >10MB apk, got {res.status}, {length}"
        assert "android.package-archive" in mime, f"Expected APK mime type, got: {mime}"
        assert "attachment" in disp, f"Expected attachment disposition, got: {disp}"
        print(f"  -> PASSED! Android APK served: {length / (1024*1024):.2f} MB, mime: {mime}")

        # Test 5: GET /Client.swf via browser fallback
        print("\n[Test 5] GET /Client.swf (Browser fallback to mole.61.com)")
        conn.request("GET", "/Client.swf")
        res = conn.getresponse()
        body = res.read()
        assert res.status == 200 and len(body) == 20695, f"Expected 20695 bytes SWF, got {res.status}, {len(body)}"
        print(f"  -> PASSED! Client.swf loaded via browser request ({len(body)} bytes).")

        # Test 6: GET /config/server.xml with local replacement
        print("\n[Test 6] GET /config/server.xml")
        conn.request("GET", "/config/server.xml")
        res = conn.getresponse()
        body = res.read()
        assert res.status == 200, f"Expected 200, got {res.status}"
        assert b'ip="127.0.0.1"' in body, f"Expected local IP replacement, got: {body.decode('utf-8')}"
        print("  -> PASSED! server.xml resolved with local server IP replacement.")

        # Test 7: WebSocket Bridge to Login Server (port 1863)
        print("\n[Test 7] WebSocket Handshake & Login Packet to /ws/1863")
        ws_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ws_sock.connect(("127.0.0.1", 18081))
        
        req = (
            "GET /ws/1863 HTTP/1.1\r\n"
            "Host: 127.0.0.1:18081\r\n"
            "Upgrade: websocket\r\n"
            "Connection: Upgrade\r\n"
            "Sec-WebSocket-Key: dGhlIHNhbXBsZSBub25jZQ==\r\n"
            "Sec-WebSocket-Version: 13\r\n"
            "\r\n"
        )
        ws_sock.sendall(req.encode("ascii"))
        
        # Read HTTP 101 Switching Protocols response
        resp_header = b""
        while b"\r\n\r\n" not in resp_header:
            chunk = ws_sock.recv(1024)
            if not chunk:
                break
            resp_header += chunk
        
        assert b"101 Switching Protocols" in resp_header, f"Expected 101, got: {resp_header.decode('latin-1')}"
        assert b"Sec-WebSocket-Accept: s3pPLMBiTxaQ9kYGzzhZRbK+xOo=" in resp_header
        print("  -> WebSocket handshake upgraded to port 1863 successfully!")

        # Send policy probe or login packet frame
        send_ws_frame(ws_sock, b"<policy-file-request/>\0", opcode=0x02)
        op, payload = read_ws_frame(ws_sock)
        assert op == 2 and b"<cross-domain-policy>" in payload, f"Expected policy XML, got {op}, {payload}"
        print(f"  -> Bi-directional WebSocket packet exchange verified ({len(payload)} bytes received)!")
        ws_sock.close()

        print("\n========================================================")
        print("🎉 ALL 7 INTEGRATION TESTS PASSED WITH 100% SUCCESS! 🎉")
        print("========================================================")

    finally:
        try:
            conn.close()
        except Exception:
            pass
        server_proc.terminate()
        proxy_proc.terminate()
        server_proc.wait(timeout=3)
        proxy_proc.wait(timeout=3)


if __name__ == "__main__":
    run_test()
