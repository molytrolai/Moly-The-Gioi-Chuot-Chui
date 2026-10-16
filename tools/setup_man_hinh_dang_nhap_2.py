#!/usr/bin/env python3
"""Setup dedicated editing folder for Saved Accounts / Quick Login Screen (Image 2)."""

import sys
import shutil
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = Path(__file__).resolve().parents[1]
SRC_SHAPES = ROOT_DIR / "work" / "exported" / "Login_full" / "shapes"
OUT_DIR = ROOT_DIR / "scratch" / "man_hinh_dang_nhap_2"
OUT_DIR.mkdir(parents=True, exist_ok=True)

FONT_TAHOMA_BD = r"C:\Windows\Fonts\tahomabd.ttf"
FONT_ARIAL_BD = r"C:\Windows\Fonts\arialbd.ttf"

def draw_text_stroke(draw, pos, text, font, fill_color, stroke_color, stroke_width=2):
    x, y = pos
    for dx in range(-stroke_width, stroke_width + 1):
        for dy in range(-stroke_width, stroke_width + 1):
            if dx * dx + dy * dy <= stroke_width * stroke_width:
                draw.text((x + dx, y + dy), text, font=font, fill=stroke_color)
    draw.text((x, y), text, font=font, fill=fill_color)

def setup_folder():
    print(f"Setting up Image 2 components in: {OUT_DIR}")
    
    # 1. Shape 73: 2 Notice Boxes (946 x 96)
    shutil.copy2(SRC_SHAPES / "73.png", OUT_DIR / "goc_01_thong_bao_2_hop_trai_phai_shape_73.png")
    
    # Create draft for Shape 73
    im73 = Image.new("RGBA", (946, 96), (0, 0, 0, 0))
    d73 = ImageDraw.Draw(im73)
    font_box = ImageFont.truetype(FONT_ARIAL_BD, 11)
    
    # Left box text (centered in range 1..271, center = 136)
    left_lines = [
        "Chào mừng đến Moly VN!",
        "Cổng nạp Đậu Vàng & Kim Đậu tại web.",
        "Tham gia sự kiện nhận quà hot!"
    ]
    y_left = 14
    for l in left_lines:
        bbox = font_box.getbbox(l)
        w = bbox[2] - bbox[0]
        x = 136 - w // 2
        draw_text_stroke(d73, (x, y_left), l, font_box, (255, 235, 180, 255), (60, 40, 20, 255), 2)
        y_left += 24
        
    # Right box text (centered in range 674..944, center = 809)
    right_lines = [
        "Lưu ý: Không chia sẻ mật khẩu",
        "cho bất kỳ ai để tránh lừa đảo.",
        "Hỗ trợ cư dân 24/7 tại diễn đàn!"
    ]
    y_right = 14
    for l in right_lines:
        bbox = font_box.getbbox(l)
        w = bbox[2] - bbox[0]
        x = 809 - w // 2
        draw_text_stroke(d73, (x, y_right), l, font_box, (255, 235, 180, 255), (60, 40, 20, 255), 2)
        y_right += 24
        
    im73.save(OUT_DIR / "01_thong_bao_2_hop_trai_phai_shape_73.png")
    print("  Created 01_thong_bao_2_hop_trai_phai_shape_73.png (946x96)")

    # 2. Shape 79: Nút Dùng Moly Khác (98 x 17)
    shutil.copy2(SRC_SHAPES / "79.png", OUT_DIR / "goc_02_nut_dung_moly_khac_shape_79.png")
    im79 = Image.new("RGBA", (98, 17), (0, 0, 0, 0))
    d79 = ImageDraw.Draw(im79)
    f79 = ImageFont.truetype(FONT_TAHOMA_BD, 9)
    b79 = f79.getbbox("DÙNG MOLY KHÁC")
    w79 = b79[2] - b79[0]
    draw_text_stroke(d79, ((98 - w79) // 2, 1), "DÙNG MOLY KHÁC", f79, (255, 240, 100, 255), (140, 40, 0, 255), 2)
    im79.save(OUT_DIR / "02_nut_dung_moly_khac_shape_79.png")
    print("  Created 02_nut_dung_moly_khac_shape_79.png (98x17)")

    # 3. Shape 107: Nút Xóa Lưu (84 x 17)
    shutil.copy2(SRC_SHAPES / "107.png", OUT_DIR / "goc_03_nut_xoa_luu_shape_107.png")
    im107 = Image.new("RGBA", (84, 17), (0, 0, 0, 0))
    d107 = ImageDraw.Draw(im107)
    f107 = ImageFont.truetype(FONT_TAHOMA_BD, 11)
    bbox107 = f107.getbbox("XÓA LƯU")
    w107 = bbox107[2] - bbox107[0]
    draw_text_stroke(d107, ((84 - w107) // 2, 1), "XÓA LƯU", f107, (255, 240, 100, 255), (140, 40, 0, 255), 2)
    im107.save(OUT_DIR / "03_nut_xoa_luu_shape_107.png")
    print("  Created 03_nut_xoa_luu_shape_107.png (84x17)")

    # 4. Shape 104: Nút Đăng Nhập Cam Lớn Trên Bục Gỗ (94 x 43)
    shutil.copy2(SRC_SHAPES / "104.png", OUT_DIR / "goc_04_nut_dang_nhap_cam_shape_104.png")
    im104 = Image.new("RGBA", (94, 43), (0, 0, 0, 0))
    d104 = ImageDraw.Draw(im104)
    f104 = ImageFont.truetype(FONT_TAHOMA_BD, 16)
    # 2 lines: "ĐĂNG" & "NHẬP" stacked or 1 line?
    # In original 104.png, "登录" is horizontal (2 characters).
    # Let's test 1 line "ĐĂNG NHẬP" with font 14
    f104_1 = ImageFont.truetype(FONT_TAHOMA_BD, 13)
    b104 = f104_1.getbbox("ĐĂNG NHẬP")
    w104 = b104[2] - b104[0]
    # Draw with 3D drop shadow
    x104 = (94 - w104) // 2
    y104 = 10
    draw_text_stroke(d104, (x104, y104 + 2), "ĐĂNG NHẬP", f104_1, (120, 20, 0, 255), (80, 10, 0, 255), 3)
    draw_text_stroke(d104, (x104, y104), "ĐĂNG NHẬP", f104_1, (255, 255, 230, 255), (180, 20, 0, 255), 3)
    im104.save(OUT_DIR / "04_nut_dang_nhap_cam_shape_104.png")
    print("  Created 04_nut_dang_nhap_cam_shape_104.png (94x43)")

    # 5. Shape 114: Nhãn Mật Khẩu (57 x 30)
    shutil.copy2(SRC_SHAPES / "114.png", OUT_DIR / "goc_05_nhan_mat_khau_shape_114.png")
    im114 = Image.new("RGBA", (57, 30), (0, 0, 0, 0))
    d114 = ImageDraw.Draw(im114)
    f114 = ImageFont.truetype(FONT_TAHOMA_BD, 13)
    b114 = f114.getbbox("MK:")
    w114 = b114[2] - b114[0]
    draw_text_stroke(d114, ((57 - w114) // 2, 5), "MK:", f114, (255, 235, 100, 255), (140, 40, 0, 255), 2)
    im114.save(OUT_DIR / "05_nhan_mat_khau_shape_114.png")
    print("  Created 05_nhan_mat_khau_shape_114.png (57x30)")

    # 6. Shape 84: Nút Quên MK (61 x 17)
    shutil.copy2(SRC_SHAPES / "84.png", OUT_DIR / "goc_06_nut_quen_mk_shape_84.png")
    im84 = Image.new("RGBA", (61, 17), (0, 0, 0, 0))
    d84 = ImageDraw.Draw(im84)
    f84 = ImageFont.truetype(FONT_TAHOMA_BD, 10)
    b84 = f84.getbbox("QUÊN MK")
    w84 = b84[2] - b84[0]
    draw_text_stroke(d84, ((61 - w84) // 2, 1), "QUÊN MK", f84, (255, 240, 100, 255), (140, 40, 0, 255), 2)
    im84.save(OUT_DIR / "06_nut_quen_mk_shape_84.png")
    print("  Created 06_nut_quen_mk_shape_84.png (61x17)")

    # 7. Shape 87: Nút Đổi MK (61 x 17)
    shutil.copy2(SRC_SHAPES / "87.png", OUT_DIR / "goc_07_nut_doi_mk_shape_87.png")
    im87 = Image.new("RGBA", (61, 17), (0, 0, 0, 0))
    d87 = ImageDraw.Draw(im87)
    f87 = ImageFont.truetype(FONT_TAHOMA_BD, 10)
    b87 = f87.getbbox("ĐỔI MK")
    w87 = b87[2] - b87[0]
    draw_text_stroke(d87, ((61 - w87) // 2, 1), "ĐỔI MK", f87, (255, 240, 100, 255), (140, 40, 0, 255), 2)
    im87.save(OUT_DIR / "07_nut_doi_mk_shape_87.png")
    print("  Created 07_nut_doi_mk_shape_87.png (61x17)")

    # 8. Shape 90: Nút Bảo Mật (60 x 17)
    shutil.copy2(SRC_SHAPES / "90.png", OUT_DIR / "goc_08_nut_bao_mat_shape_90.png")
    im90 = Image.new("RGBA", (60, 17), (0, 0, 0, 0))
    d90 = ImageDraw.Draw(im90)
    f90 = ImageFont.truetype(FONT_TAHOMA_BD, 10)
    b90 = f90.getbbox("BẢO MẬT")
    w90 = b90[2] - b90[0]
    draw_text_stroke(d90, ((60 - w90) // 2, 1), "BẢO MẬT", f90, (255, 240, 100, 255), (140, 40, 0, 255), 2)
    im90.save(OUT_DIR / "08_nut_bao_mat_shape_90.png")
    print("  Created 08_nut_bao_mat_shape_90.png (60x17)")

    # Also generate button preview composites so user can see in context
    bg_pill_114 = Image.open(SRC_SHAPES / "75.png").convert("RGBA")
    bg_pill_78 = Image.open(SRC_SHAPES / "82.png").convert("RGBA")
    bg_login = Image.open(SRC_SHAPES / "93.png").convert("RGBA")
    
    # Preview 2: Dùng Moly khác
    prev2 = bg_pill_114.copy()
    prev2.alpha_composite(im79, ((prev2.width - im79.width) // 2, (prev2.height - im79.height) // 2))
    prev2.save(OUT_DIR / "xem_truoc_02_nut_dung_moly_khac.png")

    # Preview 3: Xóa lưu
    prev3 = bg_pill_114.copy()
    prev3.alpha_composite(im107, ((prev3.width - im107.width) // 2, (prev3.height - im107.height) // 2))
    prev3.save(OUT_DIR / "xem_truoc_03_nut_xoa_luu.png")

    # Preview 4: Đăng nhập
    prev4 = bg_login.copy()
    prev4.alpha_composite(im104, ((prev4.width - im104.width) // 2, (prev4.height - im104.height) // 2 - 4))
    prev4.save(OUT_DIR / "xem_truoc_04_nut_dang_nhap_cam.png")

    # Preview 6: Quên MK
    prev6 = bg_pill_78.copy()
    prev6.alpha_composite(im84, ((prev6.width - im84.width) // 2, (prev6.height - im84.height) // 2))
    prev6.save(OUT_DIR / "xem_truoc_06_nut_quen_mk.png")

    # Preview 7: Đổi MK
    prev7 = bg_pill_78.copy()
    prev7.alpha_composite(im87, ((prev7.width - im87.width) // 2, (prev7.height - im87.height) // 2))
    prev7.save(OUT_DIR / "xem_truoc_07_nut_doi_mk.png")

    # Preview 8: Bảo mật
    prev8 = bg_pill_78.copy()
    prev8.alpha_composite(im90, ((prev8.width - im90.width) // 2, (prev8.height - im90.height) // 2))
    prev8.save(OUT_DIR / "xem_truoc_08_nut_bao_mat.png")

    # Create README
    readme_text = """BỘ THÀNH PHẦN GIAO DIỆN MÀN HÌNH ĐĂNG NHẬP 2 (CHỌN TÀI KHOẢN ĐÃ LƯU)
Dự án: Moly - Thế Giới Chuột Chũi VN
Thư mục: E:\\Codex\\Projects\\Moly-The-Gioi-Chuot-Chui\\scratch\\man_hinh_dang_nhap_2\\

DANH SÁCH FILE CẦN THAY THẾ / SỬA:
----------------------------------------------------------------------------------------------------------------
1. 01_thong_bao_2_hop_trai_phai_shape_73.png (946 x 96 px)
   - Thay thế Shape 73 trong Login.swf
   - Chứa chữ của 2 hộp màu tối bên trái và bên phải chân màn hình.
   - Nửa trái (x: 1..272): Thông báo nạp tiền / sự kiện.
   - Nửa phải (x: 675..945): Lưu ý an toàn tài khoản.
   - File gốc tiếng Trung đối chiếu: goc_01_thong_bao_2_hop_trai_phai_shape_73.png

2. 02_nut_dung_moly_khac_shape_79.png (98 x 17 px)
   - Thay thế Shape 79 trong Login.swf (chữ của nút vàng góc dưới bên trái)
   - Tiếng Trung gốc: "用其他摩尔登录" -> Bản mẫu: "DÙNG MOLY KHÁC"
   - File xem trước khi lắp vào nút: xem_truoc_02_nut_dung_moly_khac.png

3. 03_nut_xoa_luu_shape_107.png (84 x 17 px)
   - Thay thế Shape 107 trong Login.swf (chữ của nút xóa tài khoản lưu)
   - Tiếng Trung gốc: "清除记录" -> Bản mẫu: "XÓA LƯU"
   - File xem trước: xem_truoc_03_nut_xoa_luu.png

4. 04_nut_dang_nhap_cam_shape_104.png (94 x 43 px)
   - Thay thế Shape 104 trong Login.swf (chữ nút ĐĂNG NHẬP cam trên bục gỗ ở giữa)
   - Tiếng Trung gốc: "登录" -> Bản mẫu: "ĐĂNG NHẬP"
   - File xem trước: xem_truoc_04_nut_dang_nhap_cam.png

5. 05_nhan_mat_khau_shape_114.png (57 x 30 px)
   - Thay thế Shape 114 trong Login.swf (nhãn chữ trước ô nhập mật khẩu)
   - Tiếng Trung gốc: "密码：" -> Bản mẫu: "MK:"

6. 06_nut_quen_mk_shape_84.png (61 x 17 px)
   - Thay thế Shape 84 trong Login.swf (nút vàng thứ 1 ở góc phải)
   - Tiếng Trung gốc: "找回密码" -> Bản mẫu: "QUÊN MK"
   - File xem trước: xem_truoc_06_nut_quen_mk.png

7. 07_nut_doi_mk_shape_87.png (61 x 17 px)
   - Thay thế Shape 87 trong Login.swf (nút vàng thứ 2 ở góc phải)
   - Tiếng Trung gốc: "修改密码" -> Bản mẫu: "ĐỔI MK"
   - File xem trước: xem_truoc_07_nut_doi_mk.png

8. 08_nut_bao_mat_shape_90.png (60 x 17 px)
   - Thay thế Shape 90 trong Login.swf (nút vàng thứ 3 ở góc phải)
   - Tiếng Trung gốc: "密码保护" -> Bản mẫu: "BẢO MẬT"
   - File xem trước: xem_truoc_08_nut_bao_mat.png

HƯỚNG DẪN:
- Bạn có thể mở bất kỳ file nào có tiền tố `01_` đến `08_` để chỉnh sửa theo ý thích bằng Photoshop hoặc app vẽ.
- Lưu đúng định dạng PNG trong suốt (RGBA), đúng kích thước ghi trong ngoặc.
- Sau khi bạn sửa xong, chỉ cần báo lại cho trợ lý để đóng gói tự động vào game.
"""
    (OUT_DIR / "README_HUONG_DAN.txt").write_text(readme_text, encoding="utf-8")
    print(f"\nAll files created successfully in: {OUT_DIR}")

if __name__ == "__main__":
    setup_folder()
