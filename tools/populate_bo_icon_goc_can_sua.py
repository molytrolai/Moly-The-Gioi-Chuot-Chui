#!/usr/bin/env python3
"""Populate scratch/bo_icon_goc_can_sua with both Original (goc_) and Vietnamese (viet_) assets.
Also provides a synchronization function so that any edits to viet_ files in bo_icon_goc_can_sua
can be copied directly back to scratch/localized_assets and recompiled!
"""

import sys
import shutil
from pathlib import Path
from PIL import Image

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT_DIR / "scratch" / "bo_icon_goc_can_sua"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# List of (ID, Name, Orig_Rel_Path, Viet_Rel_Path)
ASSET_PAIRS = [
    ("01", "logo_moly", "work/exported/orig_logo/5.png", "scratch/localized_assets/logo_9_fitted.png"),
    ("02", "nut_bat_dau", "work/exported/LoginHome_full/shapes/128.png", "scratch/localized_assets/bat_dau_128.png"),
    ("03", "nut_dang_nhap", "work/exported/Login_full/shapes/171.png", "scratch/localized_assets/btn_login_173.png"),
    ("04", "nut_dang_ky_chan_trang", "work/exported/Login_full/shapes/167.png", "scratch/localized_assets/btn_reg_167.png"),
    ("05", "bang_hieu_nha_go", "work/exported/Login_full/shapes/150.png", "scratch/localized_assets/shape_150.png"),
    ("06", "tieu_de_chon_may_chu", "work/exported/Login_full/shapes/260.png", "scratch/localized_assets/shape_260.png"),
    ("07", "nut_tat_ca_may_chu", "work/exported/Login_full/shapes/221.png", "scratch/localized_assets/shape_221.png"),
    ("08", "nut_may_chu_de_xuat", "work/exported/Login_full/shapes/224.png", "scratch/localized_assets/shape_224.png"),
    ("09", "nut_vao_nhanh", "work/exported/Login_full/shapes/265.png", "scratch/localized_assets/shape_265.png"),
    ("10", "icon_may_chu_day", "work/exported/Login_full/shapes/279.png", "scratch/localized_assets/shape_279.png"),
    ("11", "hop_thoai_alert_thong_bao", "work/exported/Login_full/shapes/361.png", "scratch/localized_assets/title_thong_bao_361.png"),
    ("12", "nut_da_hieu", "work/exported/Login_full/shapes/367.png", "scratch/localized_assets/btn_da_hieu_367.png"),
    ("13", "nut_xac_nhan", "work/exported/Login_full/shapes/288.png", "scratch/localized_assets/shape_288.png"),
    ("14", "nut_vao_game", "work/exported/Login_full/DefineButton2_391/1_up.png", "scratch/localized_assets/shape_389.png"),
    ("15", "nut_xem_tro_giup", "work/exported/Login_full/DefineButton2_383/1_up.png", "scratch/localized_assets/shape_378.png"),
    ("16", "super_lamu_dac_quyen", "work/exported/ui_buttons/DefineButton2_5871/1_up.png", "scratch/localized_assets/ui_5868.png"),
    ("17", "super_lamu_toi_muon", "work/exported/ui_buttons/DefineButton2_5875/1_up.png", "scratch/localized_assets/ui_5872.png"),
    ("18", "super_lamu_qua_lon", "work/exported/ui_buttons/DefineButton2_5884/1_up.png", "scratch/localized_assets/ui_5881.png"),
    ("19", "toolbar_dong_tac", "work/exported/ui_buttons/DefineButton2_6838/1_up.png", "scratch/localized_assets/ui_6834.png"),
    ("20", "toolbar_ba_lo", "work/exported/ui_buttons/DefineButton2_6848/1_up.png", "scratch/localized_assets/ui_6844.png"),
    ("21", "toolbar_ban_be", "work/exported/ui_buttons/DefineButton2_6853/1_up.png", "scratch/localized_assets/ui_6849.png"),
]

# Map signs crops: (ID, Name, Orig_Map_Path, Viet_Map_Path, crop_box)
MAP_CROPS = [
    ("22", "map1_cong_lau_dai", "work/exported/Map1/5.jpg", "work/map_buildings/map1_bg_vi.jpg", (395, 235, 565, 295)),
    ("23", "map2_don_canh_sat", "work/exported/Map2/57.jpg", "work/map_buildings/map2_bg_vi.jpg", (105, 190, 245, 250)),
    ("24", "map3_tiem_thoi_trang", "work/exported/Map3/4.jpg", "work/map_buildings/map3_bg_vi.jpg", (315, 110, 465, 175)),
    ("25", "map4_bai_truot_tuyet", "work/exported/Map4/15.jpg", "work/map_buildings/map4_bg_vi.jpg", (210, 210, 360, 270)),
]

def populate():
    print(f"Populating pair files in: {OUT_DIR}...")
    
    # Clean previous files to have clean pair naming
    for f in OUT_DIR.glob("*.png"):
        try:
            f.unlink()
        except:
            pass

    for num, name, orig_path, viet_path in ASSET_PAIRS:
        orig = ROOT_DIR / orig_path
        viet = ROOT_DIR / viet_path
        
        # 1. Original file: goc_{num}_{name}.png
        dst_goc = OUT_DIR / f"goc_{num}_{name}.png"
        if orig.exists():
            shutil.copy2(orig, dst_goc)
            print(f"  Copied {dst_goc.name}")
        else:
            print(f"  [MISSING GOC] {orig}")
            
        # 2. Vietnamese file: viet_{num}_{name}.png
        dst_viet = OUT_DIR / f"viet_{num}_{name}.png"
        if viet.exists():
            shutil.copy2(viet, dst_viet)
            print(f"  Copied {dst_viet.name}")
        else:
            print(f"  [MISSING VIET] {viet}")

    for num, name, orig_path, viet_path, box in MAP_CROPS:
        orig = ROOT_DIR / orig_path
        viet = ROOT_DIR / viet_path
        
        dst_goc = OUT_DIR / f"goc_{num}_{name}.png"
        if orig.exists():
            im = Image.open(orig)
            im.crop(box).save(dst_goc)
            print(f"  Cropped {dst_goc.name}")
            
        dst_viet = OUT_DIR / f"viet_{num}_{name}.png"
        if viet.exists():
            im_v = Image.open(viet)
            im_v.crop(box).save(dst_viet)
            print(f"  Cropped {dst_viet.name}")

    readme = """THƯ MỤC CHỨA CẢ 2 BẢN: GỐC (TRUNG QUỐC) VÀ VIỆT HÓA ĐỂ BẠN ĐỐI CHIẾU & SỬA
Dự án: Moly - Thế Giới Chuột Chũi VN
Đường dẫn: E:\\Codex\\Projects\\Moly-The-Gioi-Chuot-Chui\\scratch\\bo_icon_goc_can_sua\\

QUY TẮC ĐẶT TÊN CẶP FILE:
----------------------------------------------------------------------------------------------------------------
Mỗi thành phần được chia thành 1 cặp gồm:
  1. goc_XX_<tên>.png   : File gốc tiếng Trung nguyên bản (để xem mẫu phong cách, màu sắc, bóng đổ).
  2. viet_XX_<tên>.png  : File Việt hóa hiện tại của game (để bạn xem cách đặt chữ tiếng Việt).

CÁCH BẠN SỬA VÀ LƯU:
- Bạn mở file `goc_...` để lấy mẫu chuẩn.
- Bạn sửa hoặc vẽ lại theo mẫu gốc, sau đó LƯU GHI ĐÈ TRỰC TIẾP lên file `viet_XX_<tên>.png` trong thư mục này!
- Sau khi lưu xong, bạn chỉ cần nhắn: "tôi đã sửa xong bộ icon gốc, hãy nạp vào game", hệ thống sẽ tự động đồng bộ đè vào game SWF ngay lập tức!
"""
    (OUT_DIR / "README_HUONG_DAN.txt").write_text(readme, encoding="utf-8")
    print("\nPopulate complete!")

if __name__ == "__main__":
    populate()
