#!/usr/bin/env python3
"""Pack user-edited map backgrounds into game SWFs in local-overrides."""

import sys
import shutil
import subprocess
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

JAVA = r"C:\Program Files\Microsoft\jdk-21.0.12.101-hotspot\bin\java.exe"
PROJECT_ROOT = Path(__file__).resolve().parents[1]
FFDEC = str(PROJECT_ROOT / "tools" / "ffdec-26.3.0" / "ffdec-cli.jar")

MIRROR_MAP = PROJECT_ROOT / "archive" / "clients" / "offline-mirror" / "mole.61.com" / "resource" / "map"
OVERRIDES_MAP = PROJECT_ROOT / "archive" / "clients" / "local-overrides" / "mole.61.com" / "resource" / "map"
OVERRIDES_MAP.mkdir(parents=True, exist_ok=True)

TEMP_DIR = PROJECT_ROOT / "work" / "temp_map_pack"
TEMP_DIR.mkdir(parents=True, exist_ok=True)

# Map configurations
# (Map_Name, Source_SWF, Target_SWF_List, Tag_ID, New_Image_Path)
MAP_REPLACES = [
    (
        "Map 1 (Lâu Đài Moly)",
        MIRROR_MAP / "Map_10001.swf",
        [OVERRIDES_MAP / "Map_10001.swf", OVERRIDES_MAP / "1.swf"],
        "5",
        PROJECT_ROOT / "work" / "exported" / "Map1" / "5.jpg"
    ),
    (
        "Map 2 (Quảng Trường Ái Tâm)",
        MIRROR_MAP / "Map_10002.swf",
        [OVERRIDES_MAP / "Map_10002.swf", OVERRIDES_MAP / "2.swf"],
        "57",
        PROJECT_ROOT / "work" / "exported" / "Map2" / "57.jpg"
    ),
    (
        "Map 3 (Phố Mua Sắm Taotao)",
        MIRROR_MAP / "Map_10003.swf",
        [OVERRIDES_MAP / "Map_10003.swf", OVERRIDES_MAP / "3.swf"],
        "4",
        PROJECT_ROOT / "work" / "map_buildings" / "map3_bg_vi.jpg"
    ),
    (
        "Map 4 (Chân Núi Molylaya / Bãi Trượt Tuyết)",
        MIRROR_MAP / "Map_10004.swf",
        [OVERRIDES_MAP / "Map_10004.swf", OVERRIDES_MAP / "4.swf"],
        "15",
        PROJECT_ROOT / "work" / "exported" / "Map4" / "15.jpg"
    ),
]

def pack_maps():
    print("======================================================================")
    print("      NẠP ẢNH NỀN BIỂN HIỆU MAP CỦA USER VÀO GAME CLIENT SWF         ")
    print("======================================================================")
    
    for name, src_swf, dst_list, tag_id, img_path in MAP_REPLACES:
        print(f"\n[Xử lý] {name}...")
        if not img_path.exists():
            print(f"  [BỎ QUA] Không tìm thấy ảnh: {img_path}")
            continue
        if not src_swf.exists():
            print(f"  [BỎ QUA] Không tìm thấy swf gốc: {src_swf}")
            continue
            
        temp_out = TEMP_DIR / f"temp_{src_swf.stem}.swf"
        cmd = [JAVA, "-jar", FFDEC, "-replace", str(src_swf), str(temp_out), str(tag_id), str(img_path)]
        print(f"  Thay thế Tag {tag_id} bằng {img_path.name}...")
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode != 0:
            print(f"  [LỖI] FFDec thất bại:\n{res.stderr}")
            continue
            
        for dst in dst_list:
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(temp_out, dst)
            print(f"  -> Cài đặt thành công: {dst.name} ({dst.stat().st_size:,} bytes)")

    print("\n======================================================================")
    print("   HOÀN TẤT NẠP TOÀN BỘ ẢNH NỀN BIỂN HIỆU MAP MỚI VÀO GAME!         ")
    print("======================================================================")

if __name__ == "__main__":
    pack_maps()
