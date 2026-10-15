import os
import shutil
from pathlib import Path
from PIL import Image

def prepare_login_edit_folder():
    edit_dir = Path("CHINH_SUA_DANG_NHAP")
    edit_dir.mkdir(parents=True, exist_ok=True)
    
    targets = [
        ("1_BAT_DAU_btn_start_168", "data/decompiled/LoginHome/buttons/DefineButton2_168/1_up.png", "btn_start_168.png", (222, 258)),
        ("2_DANG_NHAP_btn_login_173", "data/decompiled/Login/buttons/DefineButton2_173/1_up.png", "btn_login_173.png", (243, 220)),
        ("3_DANG_KY_btn_reg_169", "data/decompiled/Login/buttons/DefineButton2_169/1_up.png", "btn_reg_169.png", (88, 17)),
        ("4_QUEN_MK_btn_forgot_160", "data/decompiled/Login/buttons/DefineButton2_160/1_up.png", "btn_forgot_160.png", (63, 18)),
        ("5_DOI_MK_btn_change_163", "data/decompiled/Login/buttons/DefineButton2_163/1_up.png", "btn_change_163.png", (64, 18)),
        ("6_BAO_MAT_btn_protect_166", "data/decompiled/Login/buttons/DefineButton2_166/1_up.png", "btn_protect_166.png", (63, 18)),
        ("7_XOA_LUU_btn_clear_109", "data/decompiled/Login/buttons/DefineButton2_109/1_up.png", "btn_clear_109.png", (133, 49)),
        ("8_TAI_KHOAN_LUU_btn_system_176", "data/decompiled/Login/buttons/DefineButton2_176/1_up.png", "btn_system_176.png", (154, 45)),
        ("9_THONG_BAO_randomMC_banner_3", "work/target_login_originals/randomMC/3.png", "randomMC_banner_3.png", (328, 238)),
        ("10_LOGO_image_148", "data/decompiled/Login/images/148.png", "image_148.png", (900, 200)),
    ]
    
    summary_lines = []
    
    for prefix, src_path, target_filename, (expected_w, expected_h) in targets:
        src = Path(src_path)
        if not src.exists():
            print(f"Warning: {src} not found!")
            continue
            
        im = Image.open(src)
        w, h = im.size
        
        # 1. Bản gốc chuẩn
        dst_goc = edit_dir / f"{prefix}_GOC_{w}x{h}.png"
        shutil.copy2(src, dst_goc)
        
        # 2. Bản phóng to 4x để nhìn rõ từng nét vẽ / điểm ảnh
        dst_4x = edit_dir / f"{prefix}_PHONG_TO_4X_{w*4}x{h*4}.png"
        im_4x = im.resize((w * 4, h * 4), Image.Resampling.NEAREST)
        im_4x.save(dst_4x)
        
        summary_lines.append(f"- {prefix}:\n  + Kích thước gốc: {w}x{h} px\n  + Tên file khi bạn xuất ra: {target_filename}")

    readme = f"""======================================================================
THƯ MỤC CÁC TỆP GỐC MÀN HÌNH ĐĂNG NHẬP (CHỜ BẠN TẠO / SỬA LẠI)
DỰ ÁN: MOLY - THẾ GIỚI CHUỘT CHŨI VN
======================================================================

Toàn bộ ảnh gốc chuẩn 100% từ game gốc Trung Quốc đã được trích xuất sẵn vào đây.
Mỗi nút gồm 2 file:
1. File *_GOC_*.png: Đúng kích thước pixel gốc của game.
2. File *_PHONG_TO_4X_*.png: Được phóng to 4 lần (giữ nguyên từng pixel) để bạn dễ quan sát chi tiết màu sắc, bóng đổ, viền và chi tiết hoạt hình gốc.

DANH SÁCH CÁC TỆP CẦN LÀM LẠI:
{chr(10).join(summary_lines)}

HƯỚNG DẪN BÀN GIAO:
- Sau khi bạn dùng AI hoặc Photoshop/trình vẽ tạo xong ảnh theo ý bạn:
  + Bạn có thể lưu ảnh thành phẩm (đúng kích thước gốc hoặc ảnh to) ngay tại thư mục này với tên chuẩn:
      CHINH_SUA_DANG_NHAP\\btn_start_168.png
      CHINH_SUA_DANG_NHAP\\btn_login_173.png
      CHINH_SUA_DANG_NHAP\\btn_reg_169.png
      CHINH_SUA_DANG_NHAP\\btn_forgot_160.png
      CHINH_SUA_DANG_NHAP\\btn_change_163.png
      CHINH_SUA_DANG_NHAP\\btn_protect_166.png
      CHINH_SUA_DANG_NHAP\\btn_clear_109.png
      CHINH_SUA_DANG_NHAP\\btn_system_176.png
      CHINH_SUA_DANG_NHAP\\randomMC_banner_3.png
      CHINH_SUA_DANG_NHAP\\image_148.png

  + Hoặc gửi ảnh trực tiếp vào đoạn chat / lưu vào scratch\\localized_assets\\

- Khi nào bạn làm xong, bạn chỉ cần nhắn: "tôi đã làm xong", tôi sẽ rà soát kỹ lưỡng, chỉnh kích thước pixel chuẩn xác và nạp vào game cho bạn!
"""
    (edit_dir / "HUONG_DAN.txt").write_text(readme, encoding="utf-8")
    print("CHINH_SUA_DANG_NHAP folder prepared successfully!")

if __name__ == "__main__":
    prepare_login_edit_folder()
