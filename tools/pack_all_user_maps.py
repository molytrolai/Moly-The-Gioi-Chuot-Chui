#!/usr/bin/env python3
"""Pack all user-edited map backgrounds cleanly into SWFs with ZERO plaque overlays.

Authoritatively includes:
1. Core 4 Maps from work/exported:
   - Map 1 (Lâu Đài Moly): Tag 5 (Background) & Tag 124 (Cổng vòm)
   - Map 2 (Quảng Trường Ái Tâm): Tag 57
   - Map 3 (Phố Mua Sắm Taotao): Tag 4
   - Map 4 (Chân Núi Molylaya / Bãi Trượt Tuyết): Tag 15
2. Newly User-Edited Maps from scratch/cac_map_can_sua:
   - Map 7 (Khu Vui Chơi Miền Đông): Tag 5
   - Map 28 (Học Viện Lamu): Tag 7
   - Map 37 (Đỉnh Núi Molylaya): Tag 139
   - Map 77 (Đại Học Moly): Tag 5
   - Map 109 (Vườn Lâu Đài): Tag 5
"""

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

MIRROR_MAP = ROOT / "archive" / "clients" / "offline-mirror" / "mole.61.com" / "resource" / "map"
OVERRIDES_MAP = ROOT / "archive" / "clients" / "local-overrides" / "mole.61.com" / "resource" / "map"
OVERRIDES_MAP.mkdir(parents=True, exist_ok=True)

TEMP_DIR = ROOT / "work" / "temp_map_pack"
TEMP_DIR.mkdir(parents=True, exist_ok=True)

USER_MAPS_DIR = ROOT / "scratch" / "cac_map_can_sua"

# Maps edited and confirmed by the user
CONFIRMED_USER_MAPS = [
    # Core 4 Maps
    ("Map 1 (Lâu Đài Moly - Background)", "Map_10001.swf", ["Map_10001.swf", "1.swf"], "5", ROOT / "work/exported/Map1/5.jpg"),
    ("Map 1 (Lâu Đài Moly - Cổng Vòm)", "Map_10001.swf", ["Map_10001.swf", "1.swf"], "124", ROOT / "work/exported/Map1/124.png"),
    ("Map 2 (Quảng Trường Ái Tâm)", "Map_10002.swf", ["Map_10002.swf", "2.swf"], "57", ROOT / "work/exported/Map2/57.jpg"),
    ("Map 3 (Phố Mua Sắm Taotao)", "Map_10003.swf", ["Map_10003.swf", "3.swf"], "4", ROOT / "work/exported/Map3/4.jpg"),
    ("Map 4 (Chân Núi Molylaya)", "Map_10004.swf", ["Map_10004.swf", "4.swf"], "15", ROOT / "work/exported/Map4/15.jpg"),
    
    # 5 Newly Edited Maps (10/17 Evening)
    ("Map 7 (Khu Vui Chơi Miền Đông)", "Map_10007.swf", ["Map_10007.swf", "7.swf"], "5", USER_MAPS_DIR / "map_07_khu_vui_choi_mien_dong_tag_5.jpg"),
    ("Map 28 (Học Viện Lamu)", "Map_10028.swf", ["Map_10028.swf", "28.swf"], "7", USER_MAPS_DIR / "map_28_hoc_vien_lamu_tag_7.jpg"),
    ("Map 37 (Đỉnh Núi Molylaya)", "37.swf", ["37.swf"], "139", USER_MAPS_DIR / "map_37_dinh_nui_molylaya_tag_139.png"),
    ("Map 77 (Đại Học Moly)", "Map_10077.swf", ["Map_10077.swf", "77.swf"], "5", USER_MAPS_DIR / "map_77_dai_hoc_moly_tag_5.jpg"),
    ("Map 109 (Vườn Lâu Đài)", "Map_10109.swf", ["Map_10109.swf", "109.swf"], "5", USER_MAPS_DIR / "map_109_vuon_lau_dai_tag_5.jpg"),
]

def pack_single(name, src_swf_name, dst_names, tag_id, img_path):
    if not img_path.exists():
        print(f"  [BỎ QUA] Không tìm thấy ảnh user: {img_path}")
        return False

    src_swf = MIRROR_MAP / src_swf_name
    if not src_swf.exists():
        src_swf = OVERRIDES_MAP / src_swf_name
    if not src_swf.exists():
        print(f"  [BỎ QUA] Không tìm thấy SWF gốc: {src_swf_name}")
        return False

    temp_out = TEMP_DIR / f"temp_{src_swf_name}"
    cmd = [JAVA, "-jar", FFDEC, "-replace", str(src_swf), str(temp_out), str(tag_id), str(img_path)]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"  [LỖI] FFDec thất bại khi nạp {img_path.name} vào {src_swf_name}: {res.stderr}")
        return False

    sync_dirs = [
        OVERRIDES_MAP,
        ROOT / "archive" / "clients" / "offline-mirror" / "mole.61.com" / "resource" / "map",
        ROOT / "archive" / "clients" / "captured-live" / "named" / "mole.61.com" / "resource" / "map",
    ]

    for dst_name in dst_names:
        for sdir in sync_dirs:
            if sdir.exists():
                dst = sdir / dst_name
                shutil.copy2(temp_out, dst)
        print(f"  -> Đã cập nhật thành công: {dst_names} từ {img_path.name} ({temp_out.stat().st_size:,} bytes)")
    return True

def pack_all():
    print("======================================================================")
    print("      NẠP TẤT CẢ MAP ĐÃ ĐƯỢC USER CHỈNH SỬA VÀO GAME (100% NGUYÊN BẢN) ")
    print("======================================================================")

    success_count = 0
    for name, src_swf, dsts, tag, img in CONFIRMED_USER_MAPS:
        print(f"\n[Xử lý] {name} (Tag {tag})")
        if pack_single(name, src_swf, dsts, tag, img):
            success_count += 1

    print("\n======================================================================")
    print(f"   HOÀN TẤT NẠP {success_count}/{len(CONFIRMED_USER_MAPS)} MAP CỦA USER!")
    print("======================================================================")

if __name__ == "__main__":
    pack_all()
