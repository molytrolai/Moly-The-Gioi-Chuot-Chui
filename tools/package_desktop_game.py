#!/usr/bin/env python3
"""Packages the clean, standalone Desktop Client edition of Moly - The Gioi Chuot Chui.

Produces: web/download/Moly Thế Giới Chuột chũi.zip
Contains ONLY client assets and launcher. Strictly NO server code or admin credentials.
"""

from __future__ import annotations

import os
import sys
import zipfile
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = PROJECT_ROOT / "web" / "download"
ZIP_NAME = "Moly Thế Giới Chuột chũi.zip"
OUTPUT_ZIP = OUTPUT_DIR / ZIP_NAME

# Client-only files to include
INCLUDE_SPECS = [
    ("tools/ruffle-0.7.1", "tools/ruffle-0.7.1"),
    ("tools/client_asset_server.py", "tools/client_asset_server.py"),
    ("archive/clients/2026-10-09/china/Client.swf", "archive/clients/2026-10-09/china/Client.swf"),
    ("archive/clients/local-overrides", "archive/clients/local-overrides"),
    ("archive/clients/offline-mirror", "archive/clients/offline-mirror"),
]

PLAYER_BATCH_CONTENT = """@echo off
title Moly - The Gioi Chuot Chui
cd /d "%~dp0"
echo ======================================================================
echo             KHOI DONG THE GIOI CHUOT CHUI (MOLY VIET)
echo ======================================================================
echo [*] Dang nap 257 ban do offline va khoi dong Flash Ruffle...
echo [*] Hay dang nhap tai khoan cua ban hoac tao tai khoan moi de trai nghiem!
echo ======================================================================

start "" /b python tools/client_asset_server.py --port 18080
timeout /t 1 >nul
start "" tools/ruffle-0.7.1/ruffle.exe archive/clients/2026-10-09/china/Client.swf --spoof-url http://mole.61.com/Client.swf --base http://mole.61.com/ --proxy http://127.0.0.1:18080 --tcp-connections allow --graphics dx12 --width 1024 --height 768
"""

PLAYER_README_CONTENT = """======================================================================
               MOLY - THẾ GIỚI CHUỘT CHŨI (BẢN MÁY TÍNH)
======================================================================

1. CÁCH KHỞI ĐỘNG GAME:
   - Nhấp đúp chuột vào tệp biểu tượng "Moly Thế Giới Chuột Chũi.exe" để mở game.
   - Cửa sổ trò chơi sẽ mở lên tức thì, sẵn sàng trải nghiệm không cần cài đặt.
   - (Hoặc bạn cũng có thể mở tệp "Choi-Game.bat" làm phương án dự phòng).

2. TÀI KHOẢN TRẢI NGHIỆM:
   - Bạn có thể đăng ký tài khoản mới trực tiếp trên Web hoặc trong game.
   - Đăng nhập linh hoạt bằng: Tên tài khoản (Username), Gmail đã liên kết hoặc Mã ID Moly.
   - Cư dân khi tham gia sẽ được khám phá trọn vẹn thế giới thần tiên và hệ thống hiệp sĩ SMC!

3. TÍNH NĂNG VƯỢT TRỘI BẢN MÁY TÍNH:
   - Tải sẵn toàn bộ 257 bản đồ offline, chuyển map tức thì 0 giây.
   - 60 FPS mượt mà tuyệt đối, chuyển động chân thực.
   - Toàn bộ nội dung và 252 câu hỏi Minigame thuần Việt văn minh, sạch bóng quảng cáo.

Chúc các bạn có những giây phút thư giãn tuyệt vời tại Thế Giới Chuột Chũi!
======================================================================
"""


def create_package() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Creating clean standalone client zip at: {OUTPUT_ZIP}")

    # Temporary files for client distribution
    temp_bat = PROJECT_ROOT / "Choi-Game-Client.bat"
    temp_bat.write_text(PLAYER_BATCH_CONTENT, encoding="utf-8")

    temp_readme = PROJECT_ROOT / "Huong-Dan-Cai-Dat.txt"
    temp_readme.write_text(PLAYER_README_CONTENT, encoding="utf-8")

    temp_server = PROJECT_ROOT / "server_address.txt"
    if not temp_server.exists():
        temp_server.write_text("127.0.0.1", encoding="utf-8")

    specs = [
        ("Moly Thế Giới Chuột Chũi.exe", "Moly Thế Giới Chuột Chũi.exe"),
        ("Choi-Game-Client.bat", "Choi-Game.bat"),
        ("Huong-Dan-Cai-Dat.txt", "Huong-Dan-Choi.txt"),
        ("server_address.txt", "server_address.txt"),
    ] + list(INCLUDE_SPECS)

    total_files = 0
    with zipfile.ZipFile(OUTPUT_ZIP, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as zf:
        root_folder = "Moly Thế Giới Chuột chũi"

        for src_rel, dst_rel in specs:
            src_full = PROJECT_ROOT / src_rel
            if not src_full.exists():
                print(f"[WARN] Not found: {src_full}")
                continue

            if src_full.is_file():
                arcname = f"{root_folder}/{dst_rel}"
                zf.write(src_full, arcname)
                total_files += 1
            elif src_full.is_dir():
                for root, dirs, files in os.walk(src_full):
                    for f in files:
                        file_path = Path(root) / f
                        rel = file_path.relative_to(src_full)
                        arcname = f"{root_folder}/{dst_rel}/{rel.as_posix()}"
                        zf.write(file_path, arcname)
                        total_files += 1

    # Cleanup temporary staging files
    for tmp in (temp_bat, temp_readme):
        try:
            tmp.unlink()
        except Exception:
            pass

    # Also mirror to standard ASCII filename for web compatibility
    ascii_zip = OUTPUT_DIR / "Moly-The-Gioi-Chuot-Chui.zip"
    try:
        import shutil
        shutil.copy2(OUTPUT_ZIP, ascii_zip)
    except Exception as e:
        print(f"[WARN] Failed to copy ASCII zip: {e}")

    size_mb = OUTPUT_ZIP.stat().st_size / (1024 * 1024)
    print(f"[OK] Successfully packaged {total_files} files into '{OUTPUT_ZIP.name}' and '{ascii_zip.name}' ({size_mb:.2f} MB)")


if __name__ == "__main__":
    create_package()
