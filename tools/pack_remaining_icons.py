#!/usr/bin/env python3
"""Pack user-edited icons from scratch/bo_icon_can_sua_tiep/ into game SWFs."""

import os
import sys
import shutil
import subprocess
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

JAVA = r"C:\Program Files\Microsoft\jdk-21.0.12.101-hotspot\bin\java.exe"
ROOT = Path(__file__).resolve().parents[1]
FFDEC = str(ROOT / "tools" / "ffdec-26.3.0" / "ffdec-cli.jar")

OVERRIDES_ROOT = ROOT / "archive" / "clients" / "local-overrides" / "mole.61.com"
SRC_FOLDER = ROOT / "scratch" / "bo_icon_can_sua_tiep"
TEMP_DIR = ROOT / "work" / "temp_icon_pack"
TEMP_DIR.mkdir(parents=True, exist_ok=True)

# Map from prefix to relative SWF path
SWF_TARGETS = {
    "LoginHome": OVERRIDES_ROOT / "resource" / "login" / "LoginHome.swf",
    "Login": OVERRIDES_ROOT / "resource" / "login" / "Login.swf",
    "topUI": OVERRIDES_ROOT / "resource" / "ui" / "topUI.swf",
    "ui": OVERRIDES_ROOT / "resource" / "ui" / "ui.swf",
    "SuperLahmIntro": OVERRIDES_ROOT / "module" / "external" / "SuperLahmIntroPanel.swf",
    "SuperLamuGift": OVERRIDES_ROOT / "module" / "external" / "SuperLamuGiftMain.swf",
}

def pack_icons():
    print("======================================================================")
    print("        NẠP CÁC ICON ĐÃ SỬA TỪ bo_icon_can_sua_tiep VÀO GAME         ")
    print("======================================================================")

    if not SRC_FOLDER.exists():
        print(f"Không tìm thấy thư mục: {SRC_FOLDER}")
        return

    # Group files by SWF
    files_by_swf = {}
    for f in SRC_FOLDER.glob("*.png"):
        parts = f.stem.split("_")
        if len(parts) >= 2:
            swf_key = parts[0]
            tag_id = parts[1]
            if swf_key in SWF_TARGETS:
                files_by_swf.setdefault(swf_key, []).append((tag_id, f))

    for swf_key, tag_list in files_by_swf.items():
        swf_path = SWF_TARGETS[swf_key]
        if not swf_path.exists():
            print(f"  [BỎ QUA] Không tìm thấy SWF: {swf_path.name}")
            continue

        print(f"\n[Xử lý] {swf_path.name} ({len(tag_list)} icon)...")
        curr_swf = swf_path
        temp_a = TEMP_DIR / f"temp_{swf_key}_a.swf"
        temp_b = TEMP_DIR / f"temp_{swf_key}_b.swf"
        curr_input = swf_path
        next_output = temp_a

        for tag_id, img_file in tag_list:
            cmd = [JAVA, "-jar", FFDEC, "-replace", str(curr_input), str(next_output), str(tag_id), str(img_file)]
            res = subprocess.run(cmd, capture_output=True, text=True)
            if res.returncode == 0:
                print(f"  -> Thay thế Tag {tag_id} ({img_file.name}) thành công!")
                curr_input = next_output
                next_output = temp_b if curr_input == temp_a else temp_a
            else:
                print(f"  [LỖI] Tag {tag_id}: {res.stderr}")

        shutil.copy2(curr_input, swf_path)
        print(f"  => Cập nhật hoàn tất: {swf_path.name} ({swf_path.stat().st_size:,} bytes)")

    print("\n======================================================================")
    print("   HOÀN TẤT ĐÓNG GÓI TOÀN BỘ ICON MỚI VÀO GAME CLIENT!               ")
    print("======================================================================")

if __name__ == "__main__":
    pack_icons()
