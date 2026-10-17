#!/usr/bin/env python3
"""Pack all user-edited map backgrounds cleanly into SWFs with ZERO plaque overlays."""

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

# 1. Core 4 Maps already edited by user (Clean versions without plaque)
CORE_4_MAPS = [
    ("Map 1 (Lâu Đài Moly)", "Map_10001.swf", ["Map_10001.swf", "1.swf"], "5", ROOT / "work/exported/Map1/5.jpg"),
    ("Map 2 (Quảng Trường Ái Tâm)", "Map_10002.swf", ["Map_10002.swf", "2.swf"], "57", ROOT / "work/exported/Map2/57.jpg"),
    ("Map 3 (Phố Mua Sắm Taotao)", "Map_10003.swf", ["Map_10003.swf", "3.swf"], "4", ROOT / "work/exported/Map3/4.jpg"),
    ("Map 4 (Chân Núi Molylaya)", "Map_10004.swf", ["Map_10004.swf", "4.swf"], "15", ROOT / "work/exported/Map4/15.jpg"),
]

# 2. Additional maps in scratch/cac_map_can_sua
ADDITIONAL_MAPS = [
    ("Map 6 (Khu Vui Chơi Miền Tây)", "Map_10006.swf", ["Map_10006.swf", "6.swf"], "3", "map_06_khu_vui_choi_mien_tay_tag_3.png"),
    ("Map 7 (Khu Vui Chơi Miền Đông)", "Map_10007.swf", ["Map_10007.swf", "7.swf"], "5", "map_07_khu_vui_choi_mien_dong_tag_5.png"),
    ("Map 8 (Hồ Thần Bí)", "Map_10008.swf", ["Map_10008.swf", "8.swf"], "14", "map_08_ho_than_bi_tag_14.jpg"),
    ("Map 9 (Trang Trại Ánh Dương)", "Map_10009.swf", ["Map_10009.swf", "9.swf"], "7", "map_09_trang_trai_anh_duong_tag_7.jpg"),
    ("Map 10 (Nông Trại Vui Vẻ)", "Map_10010.swf", ["Map_10010.swf", "10.swf"], "15", "map_10_nong_trai_vui_ve_tag_15.jpg"),
    ("Map 28 (Học Viện Lamu)", "Map_10028.swf", ["Map_10028.swf", "28.swf"], "7", "map_28_hoc_vien_lamu_tag_7.jpg"),
    ("Map 37 (Đỉnh Núi Molylaya)", "37.swf", ["37.swf"], "139", "map_37_dinh_nui_molylaya_tag_139.png"),
    ("Map 38 (Sân Bóng Đá Moly)", "Map_10038.swf", ["Map_10038.swf", "38.swf"], "26", "map_38_san_bong_da_moly_tag_26.png"),
    ("Map 47 (Quảng Trường Hạt Nhỏ)", "Map_10047.swf", ["Map_10047.swf", "47.swf"], "3", "map_47_quang_truong_hat_nho_tag_3.png"),
    ("Map 77 (Đại Học Moly)", "Map_10077.swf", ["Map_10077.swf", "77.swf"], "5", "map_77_dai_hoc_moly_tag_5.jpg"),
    ("Map 83 (Sở Giao Thông)", "Map_10083.swf", ["Map_10083.swf", "83.swf"], "7", "map_83_so_giao_thong_tag_7.jpg"),
    ("Map 109 (Vườn Lâu Đài)", "Map_10109.swf", ["Map_10109.swf", "109.swf"], "5", "map_109_vuon_lau_dai_tag_5.jpg"),
]

def pack_single(name, src_swf_name, dst_names, tag_id, img_path):
    src_swf = MIRROR_MAP / src_swf_name
    if not src_swf.exists():
        src_swf = OVERRIDES_MAP / src_swf_name
    if not src_swf.exists():
        print(f"  [BỎ QUA] Không tìm thấy SWF gốc: {src_swf_name}")
        return False
    if not img_path.exists():
        return False

    temp_out = TEMP_DIR / f"temp_{src_swf_name}"
    cmd = [JAVA, "-jar", FFDEC, "-replace", str(src_swf), str(temp_out), str(tag_id), str(img_path)]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"  [LỖI] FFDec thất bại khi nạp {img_path.name}: {res.stderr}")
        return False

    for dst_name in dst_names:
        dst = OVERRIDES_MAP / dst_name
        shutil.copy2(temp_out, dst)
        print(f"  -> Đã cập nhật thành công: {dst.name} ({dst.stat().st_size:,} bytes)")
    return True

def pack_all():
    print("======================================================================")
    print("      NẠP ẢNH NỀN MAP CỦA USER VÀO SWF (100% NGUYÊN BẢN, KHÔNG Ô NỔI)  ")
    print("======================================================================")

    print("\n1. Nạp 4 Map cốt lõi đã được bạn sửa (Lâu Đài, Ái Tâm, Taotao, Tuyết):")
    for name, src_swf, dsts, tag, img in CORE_4_MAPS:
        print(f"[Xử lý] {name}: {img.name}")
        pack_single(name, src_swf, dsts, tag, img)

    print("\n2. Kiểm tra các map khác từ scratch/cac_map_can_sua/:")
    for name, src_swf, dsts, tag, fname in ADDITIONAL_MAPS:
        img_path = USER_MAPS_DIR / fname
        if img_path.exists():
            # Check if file has been modified compared to mirror or if user wants to pack it
            print(f"[Xử lý] {name} từ {fname}:")
            pack_single(name, src_swf, dsts, tag, img_path)

    print("\n======================================================================")
    print("   HOÀN TẤT NẠP TẤT CẢ MAP CỦA USER!                                 ")
    print("======================================================================")

if __name__ == "__main__":
    pack_all()
