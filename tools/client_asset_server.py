#!/usr/bin/env python3
"""Lightweight local asset server for the standalone Moly-Viet desktop client.

This script runs on the player's computer to serve the 257 offline map assets and
Vietnamese local overrides with 0-second loading delay, while connecting to the
online game server. It contains NO backend server code and NO user database.
"""

from __future__ import annotations

import argparse
import mimetypes
import os
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit

PROJECT_ROOT = Path(__file__).resolve().parents[1]
OVERRIDE_ROOT = PROJECT_ROOT / "archive" / "clients" / "local-overrides"
MIRROR_ROOT = PROJECT_ROOT / "archive" / "clients" / "offline-mirror"
CONFIG_FILE = PROJECT_ROOT / "server_address.txt"


def get_game_server() -> str:
    """Reads configured game server host from server_address.txt or defaults."""
    if CONFIG_FILE.is_file():
        try:
            val = CONFIG_FILE.read_text(encoding="utf-8").strip()
            if val:
                return val
        except Exception:
            pass
    return "127.0.0.1"


class ClientAssetHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        # Quiet logging
        pass

    def do_GET(self) -> None:
        parsed = urlsplit(self.path)
        host_header = self.headers.get("Host", "")
        host, _, _ = host_header.partition(":")
        host = (parsed.hostname or host or "mole.61.com").lower()

        # Match path against local overrides or offline mirror
        rel_path = parsed.path.lstrip("/")
        candidates = [
            Path(host) / rel_path,
            Path("mole.61.com") / rel_path,
        ]

        game_server = get_game_server()

        for cand in candidates:
            for source_root in (OVERRIDE_ROOT, MIRROR_ROOT):
                if not source_root or not source_root.exists():
                    continue
                file_path = (source_root / cand).resolve()
                if not file_path.is_file():
                    continue

                body = file_path.read_bytes()

                # Rewrite server.xml to point to online game server
                if parsed.path.lower() == "/config/server.xml":
                    text = body.decode("utf-8", errors="ignore")
                    text = text.replace('ip="123.206.131.236"', f'ip="{game_server}"')
                    text = text.replace('ip="123.206.131.63"', f'ip="{game_server}"')
                    body = text.encode("utf-8")

                mime = mimetypes.guess_type(file_path.name)[0] or "application/octet-stream"
                self.send_response(200, "OK")
                self.send_header("Content-Type", mime)
                self.send_header("Content-Length", str(len(body)))
                self.send_header("Connection", "close")
                self.end_headers()
                self.wfile.write(body)
                return

        self.send_error(404, "File Not Found")


def run_asset_server(port: int = 18080) -> None:
    server = ThreadingHTTPServer(("127.0.0.1", port), ClientAssetHandler)
    server.serve_forever()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Moly Desktop Client Asset Server")
    parser.add_argument("--port", type=int, default=18080)
    args = parser.parse_args()
    run_asset_server(args.port)
