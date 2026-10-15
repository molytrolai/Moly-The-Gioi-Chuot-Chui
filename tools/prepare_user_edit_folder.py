import os
import shutil
from pathlib import Path
from PIL import Image

def prepare_user_edit_folder():
    edit_dir = Path("CHINH_SUA_ICON")
    edit_dir.mkdir(parents=True, exist_ok=True)
    
    # 1. BẢN ĐỒ (3279)
    src_3279 = Path("work/audit_images/ui/3279.png")
    dst_3279_goc = edit_dir / "1_BANDO_3279_GOC.png"
    shutil.copy2(src_3279, dst_3279_goc)
    
    # Clean background for 3279 (erasing the Chinese text "地图" inside the magnifying glass / grass mound)
    im_3279 = Image.open(src_3279).convert("RGBA")
    w, h = im_3279.size
    pix = im_3279.load()
    # Chinese text is at y=43..62, x=20..42 inside the golden magnifying glass
    cleaned_3279 = im_3279.copy()
    cpix = cleaned_3279.load()
    for y in range(43, 63):
        for x in range(16, 46):
            r, g, b, a = pix[x, y]
            # Replace dark red / white text pixels with magnifying glass mirror gradient
            if r > 180 and g > 180 and b > 180:
                cpix[x, y] = (255, 230, 200, 240)
            elif r > 100 and g < 60 and b < 60:
                cpix[x, y] = (245, 210, 180, 240)
    cleaned_3279.save(edit_dir / "1_BANDO_3279_NEN_SACH.png")
    
    # Upscaled 4x for high-res drawing
    im_3279.resize((w * 4, h * 4), Image.Resampling.NEAREST).save(edit_dir / "1_BANDO_3279_PHONG_TO_4X.png")
    
    # 2. QUÀ TẶNG (82)
    src_82 = Path("work/audit_images/topUI/82.png")
    dst_82_goc = edit_dir / "2_QUATANG_82_GOC.png"
    shutil.copy2(src_82, dst_82_goc)
    
    # Clean background for 82 (wood board)
    im_82 = Image.open(src_82).convert("RGBA")
    w2, h2 = im_82.size
    pix2 = im_82.load()
    cleaned_82 = im_82.copy()
    cpix2 = cleaned_82.load()
    for y in range(7, 24):
        for x in range(12, 73):
            r, g, b, a = pix2[x, y]
            if a > 0:
                # restore creamy wood board color
                cpix2[x, y] = (253, 240, 192, 255)
    cleaned_82.save(edit_dir / "2_QUATANG_82_NEN_SACH.png")
    
    # Upscaled 4x
    im_82.resize((w2 * 4, h2 * 4), Image.Resampling.NEAREST).save(edit_dir / "2_QUATANG_82_PHONG_TO_4X.png")
    
    # 3. Create HUONG_DAN.txt
    readme_text = """======================================================================
THƯ MỤC CHỈNH SỬA ICON THEO Ý BẠN (MOLY - THẾ GIỚI CHUỘT CHŨI VN)
======================================================================

Trong thư mục này gồm có:

1. ICON BẢN ĐỒ (UI_3279):
   - 1_BANDO_3279_GOC.png: File ảnh gốc chuẩn từ game (78 x 66 px).
   - 1_BANDO_3279_NEN_SACH.png: Bản đã bóc sạch chữ Trung Quốc (chỉ còn đảo cỏ và kính lúp để bạn gõ chữ lên nếu muốn).
   - 1_BANDO_3279_PHONG_TO_4X.png: Bản phóng to 4x (312 x 264 px) để bạn dễ nhìn từng điểm ảnh.

2. ICON QUÀ TẶNG (TOPUI_82):
   - 2_QUATANG_82_GOC.png: File ảnh gốc chuẩn từ game (84 x 31 px).
   - 2_QUATANG_82_NEN_SACH.png: Bản bảng gỗ đã bóc sạch chữ Trung Quốc.
   - 2_QUATANG_82_PHONG_TO_4X.png: Bản phóng to 4x (336 x 124 px).

HƯỚNG DẪN LƯU VÀ BÀN GIAO:
- Sau khi bạn chỉnh sửa xong bằng Photoshop, Paint hoặc trình chỉnh sửa ảnh, bạn có thể lưu đè trực tiếp vào một trong hai nơi:
  + Nơi 1: Lưu ngay tại thư mục này với tên:
      CHINH_SUA_ICON\\ui_3279.png
      CHINH_SUA_ICON\\topui_82.png
  + Nơi 2: Hoặc lưu thẳng vào thư mục đích:
      scratch\\localized_assets\\ui_3279.png
      scratch\\localized_assets\\topui_82.png

- Sau khi lưu xong, bạn chỉ cần nhắn: "Tôi đã sửa xong", tôi sẽ lập tức đóng gói toàn bộ vào file game SWF cho bạn!
"""
    (edit_dir / "HUONG_DAN.txt").write_text(readme_text, encoding="utf-8")
    print("Prepared CHINH_SUA_ICON directory successfully!")

if __name__ == "__main__":
    prepare_user_edit_folder()
