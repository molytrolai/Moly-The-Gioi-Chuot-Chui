#!/usr/bin/env python3
"""Render Web Service Keep-Alive Daemon.

Pings the server's /health endpoint every 5 minutes (300 seconds)
to prevent the free-tier service from spinning down due to inactivity.
Consumes minimal bandwidth (< 200 bytes per request, ~1.7 MB/month)
and 0 Neon database compute hours.
"""

import time
import urllib.request
import urllib.error
from datetime import datetime

TARGET_URL = "https://moly-the-gioi-chuot-chui.onrender.com/health"
INTERVAL_SECONDS = 300  # 5 minutes

def ping_server():
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    req = urllib.request.Request(
        TARGET_URL,
        headers={"User-Agent": "MolyVN-KeepAlive/1.0"}
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            status = resp.status
            body = resp.read().decode("utf-8", errors="ignore").strip()
            print(f"[{now_str}] Keep-alive Ping OK ({status}): {body}", flush=True)
            return True
    except urllib.error.HTTPError as e:
        print(f"[{now_str}] Keep-alive HTTP Error ({e.code}): {e.reason}", flush=True)
    except Exception as e:
        print(f"[{now_str}] Keep-alive Ping Error: {e}", flush=True)
    return False

def main():
    print(f"============================================================")
    print(f"   MOLY VN - RENDER KEEP-ALIVE DAEMON (Chu kỳ: 5 phút/lần)   ")
    print(f"   Mục tiêu: {TARGET_URL}")
    print(f"============================================================\n", flush=True)
    
    while True:
        ping_server()
        time.sleep(INTERVAL_SECONDS)

if __name__ == "__main__":
    main()
