#!/usr/bin/env python3
"""Comprehensive unit test for capture proxy, probe server, and account integration."""

from __future__ import annotations

import json
import socket
import struct
import threading
import time
import unittest
import urllib.parse
import urllib.request
from pathlib import Path

import capture_proxy
import moly_probe_server as moly
from account_system import accounts, DEFAULT_MOLY_ADMIN_ID, hash_moly_password


PROXY_PORT = 19080
DIRECTORY_PORT = 11863
WORLD_PORT = 13200


def receive_packet(connection: socket.socket) -> tuple[int, int, int, int, bytes]:
    header = connection.recv(17)
    if len(header) != 17:
        raise AssertionError(f"short header: {len(header)}")
    length, version, command, user_id, result = struct.unpack(">IBIII", header)
    body = bytearray()
    while len(body) < length - 17:
        chunk = connection.recv(length - 17 - len(body))
        if not chunk:
            raise AssertionError("connection ended during packet body")
        body += chunk
    return version, command, user_id, result, bytes(body)


class TestProxyAndServer(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.archive_dir = Path(__file__).resolve().parents[1] / "data" / "test_archive"
        cls.archive_dir.mkdir(parents=True, exist_ok=True)

        # Start Proxy Server on test port
        archive = capture_proxy.AssetArchive(cls.archive_dir)
        capture_proxy.ProxyHandler.archive = archive
        capture_proxy.ProxyHandler.local_server = "127.0.0.1"
        cls.proxy_server = capture_proxy.ThreadingHTTPServer(
            ("127.0.0.1", PROXY_PORT), capture_proxy.ProxyHandler
        )
        cls.proxy_thread = threading.Thread(
            target=cls.proxy_server.serve_forever, daemon=True
        )
        cls.proxy_thread.start()

        # Start Moly Probe Server on test ports
        cls.probe_log = cls.archive_dir / "probe.log"
        recorder = moly.Recorder(cls.probe_log)
        cls.moly_servers = [
            moly.ThreadedServer(("127.0.0.1", DIRECTORY_PORT), recorder),
            moly.ThreadedServer(("127.0.0.1", WORLD_PORT), recorder),
        ]
        cls.moly_threads = [
            threading.Thread(target=s.serve_forever, daemon=True)
            for s in cls.moly_servers
        ]
        for t in cls.moly_threads:
            t.start()

        time.sleep(0.3)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.proxy_server.shutdown()
        cls.proxy_server.server_close()
        for s in cls.moly_servers:
            s.shutdown()
            s.server_close()

    def test_proxy_captcha_generation(self) -> None:
        url = f"http://127.0.0.1:{PROXY_PORT}/index.php?cmd=1101&type=4&rnd=0.123"
        req = urllib.request.Request(
            url, headers={"Host": "account-httpd.61.com"}
        )
        with urllib.request.urlopen(req, timeout=5) as resp:
            self.assertEqual(resp.status, 200)
            self.assertEqual(resp.headers.get("Content-Type"), "image/png")
            data = resp.read()
            self.assertTrue(data.startswith(b"\x89PNG\r\n\x1a\n"))

    def test_proxy_in_game_registration(self) -> None:
        url = f"http://127.0.0.1:{PROXY_PORT}/index.php"
        post_data = urllib.parse.urlencode({
            "cmd": "1102",
            "pwd": "test_player_pwd",
            "cfmpwd": "test_player_pwd",
            "seccode": "6868",
            "gid": "1",
            "tad": "gf",
        }).encode("utf-8")
        req = urllib.request.Request(
            url,
            data=post_data,
            headers={
                "Host": "account-httpd.61.com",
                "Content-Type": "application/x-www-form-urlencoded",
            },
        )
        with urllib.request.urlopen(req, timeout=5) as resp:
            self.assertEqual(resp.status, 200)
            res = json.loads(resp.read().decode("utf-8"))
            self.assertEqual(res.get("result"), 0)
            new_uid = res.get("userid")
            self.assertGreater(new_uid, DEFAULT_MOLY_ADMIN_ID)

            # Check that account is stored and can authenticate
            ok, acc = accounts.authenticate(new_uid, "test_player_pwd")
            self.assertTrue(ok)
            self.assertIsNotNone(acc)

    def test_proxy_google_oauth_routes(self) -> None:
        # Test auth redirect without following to Google
        import http.client
        conn = http.client.HTTPConnection("127.0.0.1", PROXY_PORT, timeout=5)
        conn.request("GET", "/auth/google/login", headers={"Host": "127.0.0.1"})
        resp = conn.getresponse()
        self.assertEqual(resp.status, 302)
        self.assertIn("accounts.google.com", resp.getheader("Location", ""))
        conn.close()

        # Test callback
        cb_url = f"http://127.0.0.1:{PROXY_PORT}/auth/google/callback?code=mock_code_12345"
        cb_req = urllib.request.Request(cb_url, headers={"Host": "127.0.0.1"})
        with urllib.request.urlopen(cb_req, timeout=5) as resp:
            self.assertEqual(resp.status, 200)
            html = resp.read().decode("utf-8")
            self.assertIn("Đăng nhập Google thành công!", html)

    def test_proxy_blocked_external_ad_hosts(self) -> None:
        url = f"http://127.0.0.1:{PROXY_PORT}/track"
        req = urllib.request.Request(
            url, headers={"Host": "g.cn.miaozhen.com"}
        )
        with urllib.request.urlopen(req, timeout=5) as resp:
            self.assertEqual(resp.status, 200)
            self.assertEqual(resp.headers.get("X-Moly-Blocked"), "external-content")
            self.assertEqual(len(resp.read()), 0)

    def test_directory_server_auth(self) -> None:
        # Create user
        acc = accounts.create_account(password="securepass99", nickname="Test Mole")
        uid = acc["user_id"]

        with socket.create_connection(("127.0.0.1", DIRECTORY_PORT), timeout=3) as conn:
            # Correct password hash
            pwd_hash = hash_moly_password("securepass99").encode("ascii")
            req_body = pwd_hash.ljust(32, b"\0")
            conn.sendall(moly.packet(103, uid, req_body))
            ver, cmd, user_id, res, body = receive_packet(conn)
            self.assertEqual(cmd, 103)
            self.assertEqual(user_id, uid)
            flag = struct.unpack(">I", body[:4])[0]
            self.assertEqual(flag, 0)  # 0 = success

            # Wrong password hash
            wrong_hash = b"0123456789abcdef0123456789abcdef"
            conn.sendall(moly.packet(103, uid, wrong_hash))
            ver, cmd, user_id, res, body = receive_packet(conn)
            self.assertEqual(cmd, 103)
            flag = struct.unpack(">I", body[:4])[0]
            self.assertEqual(flag, 1)  # 1 = wrong password

            # Admin account always succeeds
            conn.sendall(moly.packet(103, DEFAULT_MOLY_ADMIN_ID, b"any_pass".ljust(32, b"\0")))
            ver, cmd, user_id, res, body = receive_packet(conn)
            self.assertEqual(cmd, 103)
            flag = struct.unpack(">I", body[:4])[0]
            self.assertEqual(flag, 0)


if __name__ == "__main__":
    unittest.main()
