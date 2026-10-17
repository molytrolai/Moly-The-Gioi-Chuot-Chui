#!/usr/bin/env python3
"""Pack and synchronize topUI.swf, ui.swf, and SuperLahmIntroPanel.swf with user assets and localized texts."""

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

ICON_ROOT = ROOT / "chinh_sua_icon_game"
OVERRIDES = ROOT / "archive" / "clients" / "local-overrides" / "mole.61.com"
MIRROR = ROOT / "archive" / "clients" / "offline-mirror" / "mole.61.com"
CAPTURED = ROOT / "archive" / "clients" / "captured-live" / "named" / "mole.61.com"
WORK_TEMP = ROOT / "work" / "temp_ui_pack"
WORK_TEMP.mkdir(parents=True, exist_ok=True)

def sync_file(src, relative_path):
    destinations = [
        OVERRIDES / relative_path,
        MIRROR / relative_path,
        CAPTURED / relative_path,
    ]
    for dst in destinations:
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        print(f"  ✓ Synced to: {dst} ({dst.stat().st_size:,} bytes)")

def pack_topui():
    print("\n--- 1. PACKING topUI.swf ---")
    src = MIRROR / "resource" / "ui" / "topUI.swf"
    if not src.exists():
        src = OVERRIDES / "resource" / "ui" / "topUI.swf"
    
    curr = src
    # Replace images from folder 16
    folder16 = ICON_ROOT / "16_thanh_dieu_huong_dinh_topui"
    if folder16.exists():
        for img in sorted(folder16.glob("*.*")):
            if img.suffix.lower() in [".png", ".jpg", ".jpeg"] and img.stem.isdigit():
                cid = img.stem
                out_swf = WORK_TEMP / f"topui_rep_{cid}.swf"
                cmd = [JAVA, "-jar", FFDEC, "-replace", str(curr), str(out_swf), cid, str(img)]
                res = subprocess.run(cmd, capture_output=True, text=True)
                if res.returncode == 0:
                    curr = out_swf
                    print(f"  [topUI] Replaced image {cid} from {img.name}")
    
    # Import translated text
    txt_dir = WORK_TEMP / "topui_texts"
    txt_dir.mkdir(parents=True, exist_ok=True)
    texts = {
        "81.txt": "Lâu Đài Moly",
        "442.txt": "Phúc Lợi & Sự Kiện",
        "447.txt": "Nông Sản",
        "452.txt": "Tiệm A Phúc",
    }
    for fname, val in texts.items():
        (txt_dir / fname).write_text(val, encoding="utf-8")
        
    out_txt_swf = WORK_TEMP / "topui_final.swf"
    cmd_txt = [JAVA, "-jar", FFDEC, "-importText", str(curr), str(out_txt_swf), str(txt_dir)]
    res_txt = subprocess.run(cmd_txt, capture_output=True, text=True)
    if res_txt.returncode == 0:
        curr = out_txt_swf
        print("  [topUI] Imported Vietnamese texts successfully")
        
    sync_file(curr, "resource/ui/topUI.swf")

def pack_ui():
    print("\n--- 2. PACKING ui.swf ---")
    src = OVERRIDES / "resource" / "ui" / "ui.swf"
    if not src.exists():
        src = MIRROR / "resource" / "ui" / "ui.swf"
        
    curr = src
    # Replace images from folder 17
    folder17 = ICON_ROOT / "17_bang_dong_tac_ui"
    if folder17.exists():
        for img in sorted(folder17.glob("*.*")):
            if img.suffix.lower() in [".png", ".jpg", ".jpeg"] and img.stem.isdigit():
                cid = img.stem
                out_swf = WORK_TEMP / f"ui_rep_{cid}.swf"
                cmd = [JAVA, "-jar", FFDEC, "-replace", str(curr), str(out_swf), cid, str(img)]
                res = subprocess.run(cmd, capture_output=True, text=True)
                if res.returncode == 0:
                    curr = out_swf
                    print(f"  [UI] Replaced image {cid} from {img.name}")

    # Import translated texts
    txt_dir = WORK_TEMP / "ui_texts"
    txt_dir.mkdir(parents=True, exist_ok=True)
    texts = {
        "1252.txt": "Bạn có chắc muốn xóa bạn bè không?",
        "1698.txt": "Bạn có muốn kết bạn không?",
        "2950.txt": "Bạn có chắc muốn thêm vào danh sách chặn không?",
        "4054.txt": "Độ đói:",
        "4055.txt": "Độ khát:",
        "4056.txt": "Sạch sẽ:",
        "4057.txt": "Tâm trạng:",
        "4061.txt": "Giờ",
        "4062.txt": "Tuổi:",
        "4143.txt": "Đậu Đậu Siêu Cấp",
        "4144.txt": "Tìm hiểu đặc quyền",
        "4385.txt": "Chúc mừng! Người này đã trở thành bạn của bạn.",
        "4478.txt": "Nhấn Enter để gửi",
        "4479.txt": "Ctrl+Enter để gửi",
    }
    for fname, val in texts.items():
        (txt_dir / fname).write_text(val, encoding="utf-8")
        
    out_txt_swf = WORK_TEMP / "ui_final.swf"
    cmd_txt = [JAVA, "-jar", FFDEC, "-importText", str(curr), str(out_txt_swf), str(txt_dir)]
    res_txt = subprocess.run(cmd_txt, capture_output=True, text=True)
    if res_txt.returncode == 0:
        curr = out_txt_swf
        print("  [UI] Imported Vietnamese texts successfully")
        
    sync_file(curr, "resource/ui/ui.swf")

def pack_super_lahm():
    print("\n--- 3. PACKING SuperLahmIntroPanel.swf ---")
    src = OVERRIDES / "module" / "external" / "SuperLahmIntroPanel.swf"
    if not src.exists():
        src = MIRROR / "module" / "external" / "SuperLahmIntroPanel.swf"
        
    curr = src
    folder18 = ICON_ROOT / "18_bang_gioi_thieu_dau_dau_sieu_cap"
    if folder18.exists():
        for img in sorted(folder18.glob("*.*")):
            if img.suffix.lower() in [".png", ".jpg", ".jpeg"] and img.stem.isdigit():
                cid = img.stem
                out_swf = WORK_TEMP / f"lahm_rep_{cid}.swf"
                cmd = [JAVA, "-jar", FFDEC, "-replace", str(curr), str(out_swf), cid, str(img)]
                res = subprocess.run(cmd, capture_output=True, text=True)
                if res.returncode == 0:
                    curr = out_swf
                    print(f"  [SuperLahm] Replaced image {cid} from {img.name}")
                    
    sync_file(curr, "module/external/SuperLahmIntroPanel.swf")

def main():
    print("======================================================================")
    print("   NẠP 3 BỘ GIAO DIỆN VÀ BẢN ĐỊA HÓA VÀO GAME FLASH                   ")
    print("======================================================================")
    pack_topui()
    pack_ui()
    pack_super_lahm()
    print("\n======================================================================")
    print("   HOÀN TẤT NẠP TẤT CẢ GIAO DIỆN VÀ BẢN ĐỊA HÓA VÀO GAME!             ")
    print("======================================================================")

if __name__ == "__main__":
    main()
