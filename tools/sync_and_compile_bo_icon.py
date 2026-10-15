#!/usr/bin/env python3
"""Sync user edits from scratch/bo_icon_goc_can_sua to scratch/localized_assets and compile all SWFs."""

import sys
import shutil
import subprocess
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT_DIR / "scratch" / "bo_icon_goc_can_sua"
ASSETS_DIR = ROOT_DIR / "scratch" / "localized_assets"

# Map viet_{id}_{name}.png to destination in scratch/localized_assets
SYNC_MAP = {
    "viet_01_logo_moly.png": ASSETS_DIR / "logo_9_fitted.png",
    "viet_02_nut_bat_dau.png": ASSETS_DIR / "bat_dau_128.png",
    "viet_03_nut_dang_nhap.png": ASSETS_DIR / "btn_login_173.png",
    "viet_04_nut_dang_ky_chan_trang.png": ASSETS_DIR / "btn_reg_167.png",
    "viet_05_bang_hieu_nha_go.png": ASSETS_DIR / "shape_150.png",
    "viet_06_tieu_de_chon_may_chu.png": ASSETS_DIR / "shape_260.png",
    "viet_07_nut_tat_ca_may_chu.png": ASSETS_DIR / "shape_221.png",
    "viet_08_nut_may_chu_de_xuat.png": ASSETS_DIR / "shape_224.png",
    "viet_09_nut_vao_nhanh.png": ASSETS_DIR / "shape_265.png",
    "viet_10_icon_may_chu_day.png": ASSETS_DIR / "shape_279.png",
    "viet_11_hop_thoai_alert_thong_bao.png": ASSETS_DIR / "title_thong_bao_361.png",
    "viet_12_nut_da_hieu.png": ASSETS_DIR / "btn_da_hieu_367.png",
    "viet_13_nut_xac_nhan.png": ASSETS_DIR / "shape_288.png",
    "viet_14_nut_vao_game.png": ASSETS_DIR / "shape_389.png",
    "viet_15_nut_xem_tro_giup.png": ASSETS_DIR / "shape_378.png",
    "viet_16_super_lamu_dac_quyen.png": ASSETS_DIR / "ui_5868.png",
    "viet_17_super_lamu_toi_muon.png": ASSETS_DIR / "ui_5872.png",
    "viet_18_super_lamu_qua_lon.png": ASSETS_DIR / "ui_5881.png",
    "viet_19_toolbar_dong_tac.png": ASSETS_DIR / "ui_6834.png",
    "viet_20_toolbar_ba_lo.png": ASSETS_DIR / "ui_6844.png",
    "viet_21_toolbar_ban_be.png": ASSETS_DIR / "ui_6849.png",
}

def sync_and_compile():
    print("=== Syncing edited icons from bo_icon_goc_can_sua -> localized_assets ===")
    
    # Check if user saved item 18 to goc_18_super_lamu_qua_lon.png
    goc_18 = SRC_DIR / "goc_18_super_lamu_qua_lon.png"
    viet_18 = SRC_DIR / "viet_18_super_lamu_qua_lon.png"
    if goc_18.exists() and viet_18.exists():
        if goc_18.stat().st_mtime > viet_18.stat().st_mtime:
            print("  [Auto-detect] User updated goc_18_super_lamu_qua_lon.png -> Syncing to viet_18")
            shutil.copy2(goc_18, viet_18)

    synced = 0
    for src_name, dst_path in SYNC_MAP.items():
        src_path = SRC_DIR / src_name
        if src_path.exists():
            shutil.copy2(src_path, dst_path)
            synced += 1
            print(f"  Synced: {src_name} -> {dst_path.name}")

    # Duplicate states for hover / active button frames
    DUPLICATE_MAP = {
        ASSETS_DIR / "shape_288.png": [ASSETS_DIR / "shape_289.png"],
        ASSETS_DIR / "shape_378.png": [ASSETS_DIR / "shape_381.png"],
        ASSETS_DIR / "btn_da_hieu_367.png": [ASSETS_DIR / "btn_da_hieu_368.png", ASSETS_DIR / "btn_da_hieu_369.png"],
        ASSETS_DIR / "ui_5868.png": [ASSETS_DIR / "ui_5869.png", ASSETS_DIR / "ui_5870.png"],
        ASSETS_DIR / "ui_5872.png": [ASSETS_DIR / "ui_5873.png", ASSETS_DIR / "ui_5874.png"],
        ASSETS_DIR / "ui_5881.png": [ASSETS_DIR / "ui_5882.png", ASSETS_DIR / "ui_5883.png"],
        ASSETS_DIR / "ui_6834.png": [ASSETS_DIR / "ui_6836.png"],
        ASSETS_DIR / "ui_6844.png": [ASSETS_DIR / "ui_6846.png"],
        ASSETS_DIR / "ui_6849.png": [ASSETS_DIR / "ui_6851.png"],
    }
    for src_f, dst_list in DUPLICATE_MAP.items():
        if src_f.exists():
            for d in dst_list:
                shutil.copy2(src_f, d)

    print(f"Synced {synced} assets.")
    print("\n=== Recompiling master SWFs ===")
    subprocess.run([sys.executable, str(ROOT_DIR / "scratch" / "build_home.py")], check=True)
    subprocess.run([sys.executable, str(ROOT_DIR / "scratch" / "build_login.py")], check=True)
    subprocess.run([sys.executable, str(ROOT_DIR / "tools" / "compile_master_game_swfs.py")], check=True)
    print("\nAll SWFs recompiled successfully with your updated icons!")

if __name__ == "__main__":
    sync_and_compile()
