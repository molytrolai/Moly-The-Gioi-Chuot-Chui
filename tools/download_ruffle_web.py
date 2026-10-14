#!/usr/bin/env python3
"""Download and cache Ruffle WebAssembly bundle locally."""

import sys
import urllib.request
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

PROJECT_ROOT = Path("E:/Codex/Projects/Moly-Viet")
RUFFLE_DIR = PROJECT_ROOT / "web" / "static" / "ruffle"
RUFFLE_DIR.mkdir(parents=True, exist_ok=True)

BASE_URL = "https://unpkg.com/@ruffle-rs/ruffle@0.7.1"

FILES_TO_DOWNLOAD = [
    "ruffle.js",
    "core.ruffle.16d61072ac7fdc4d5013.js",
    "core.ruffle.994eeef0a471a88cd0e3.js",
    "172de42e6619eac8f371.wasm",
    "878d548199cddef07035.wasm",
]

print(f"Downloading Ruffle Web (0.7.1) to: {RUFFLE_DIR}...")

for fname in FILES_TO_DOWNLOAD:
    target_path = RUFFLE_DIR / fname
    if target_path.exists() and target_path.stat().st_size > 0:
        print(f"  [EXISTS] {fname} ({target_path.stat().st_size:,} bytes)")
        continue

    url = f"{BASE_URL}/{fname}"
    print(f"  [FETCHING] {fname} from {url}...")
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = resp.read()
            target_path.write_bytes(data)
            print(f"  [SAVED] {fname} ({len(data):,} bytes)")
    except Exception as e:
        print(f"  [ERROR] Downloading {fname}: {e}")

print("Ruffle Web download completed.")
