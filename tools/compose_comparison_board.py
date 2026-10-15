#!/usr/bin/env python3
"""Compose the comprehensive Side-by-Side Comparison Board: Original vs. Modified Vietnamese Assets.

Generates:
- artifact/so_sanh_icon_va_thanh_phan_goc_va_sua.png
- scratch/so_sanh_icon_va_thanh_phan_goc_va_sua.png
"""

import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT_DIR = Path(__file__).resolve().parents[1]
ASSETS_DIR = ROOT_DIR / "scratch" / "localized_assets"
ARTIFACT_DIR = Path(r"C:\Users\Admin\.gemini\antigravity\brain\d4dabd4b-b6d4-48ee-a5a1-e1257d3f4391")
ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)

OUT_IMG_ARTIFACT = ARTIFACT_DIR / "so_sanh_icon_va_thanh_phan_goc_va_sua.png"
OUT_IMG_SCRATCH = ROOT_DIR / "scratch" / "so_sanh_icon_va_thanh_phan_goc_va_sua.png"

FONT_TAHOMA_BD = r"C:\Windows\Fonts\tahomabd.ttf"
FONT_ARIAL_BD = r"C:\Windows\Fonts\arialbd.ttf"

def get_font(size, bold=True):
    try:
        return ImageFont.truetype(FONT_TAHOMA_BD if bold else r"C:\Windows\Fonts\tahoma.ttf", size)
    except:
        return ImageFont.truetype(FONT_ARIAL_BD, size)

def load_img(path, max_w=None, max_h=None, crop_box=None):
    p = Path(path)
    if not p.exists():
        w = max_w or 100
        h = max_h or 40
        im = Image.new("RGBA", (w, h), (45, 45, 55, 255))
        d = ImageDraw.Draw(im)
        d.text((5, 5), p.name[:15], fill=(200, 200, 200))
        return im
        
    im = Image.open(p).convert("RGBA")
    if crop_box:
        im = im.crop(crop_box)
        
    if max_w and max_h:
        scale = min(max_w / im.width, max_h / im.height)
        if scale < 1.0 or (im.width < max_w * 0.4 and im.height < max_h * 0.4):
            nw = max(1, int(im.width * scale))
            nh = max(1, int(im.height * scale))
            im = im.resize((nw, nh), Image.Resampling.LANCZOS)
    return im

def compose():
    print("Composing comprehensive side-by-side comparison board...")
    width = 1850
    height = 2750
    
    bg_color = (18, 22, 36, 255) # Deep cartoon navy background
    canvas = Image.new("RGBA", (width, height), bg_color)
    draw = ImageDraw.Draw(canvas)
    
    # 1. Header Banner
    draw.rectangle([0, 0, width, 140], fill=(26, 33, 56, 255))
    draw.line([(0, 140), (width, 140)], fill=(255, 180, 0, 255), width=4)
    
    title_font = get_font(32, bold=True)
    sub_font = get_font(18, bold=False)
    
    title_text = "BẢNG SO SÁNH THÀNH PHẦN & ICON: BẢN GỐC (TRUNG QUỐC) VS. BẢN VIỆT HÓA MOLY VN"
    sub_text = "Dự án: Moly - Thế Giới Chuột Chũi VN | Chuẩn mỹ thuật hoạt hình Candy 3D Glossy, Stroke đậm & Tỷ lệ chuẩn bản gốc"
    
    draw.text((40, 28), title_text, font=title_font, fill=(255, 215, 0, 255))
    draw.text((40, 85), sub_text, font=sub_font, fill=(200, 225, 255, 255))
    
    # Column Header Bar
    y = 155
    col_h = 44
    draw.rounded_rectangle([30, y, width - 30, y + col_h], radius=8, fill=(38, 48, 85, 255), outline=(90, 120, 190, 255), width=2)
    header_font = get_font(16, bold=True)
    draw.text((50, y + 11), "HẠNG MỤC / THÀNH PHẦN", font=header_font, fill=(255, 255, 255))
    draw.text((440, y + 11), "BẢN GỐC TAOMEE (TRUNG QUỐC)", font=header_font, fill=(255, 140, 140))
    draw.text((920, y + 11), "BẢN SỬA ĐỔI HOÀN THIỆN (VIỆT HÓA 3D)", font=header_font, fill=(110, 255, 160))
    draw.text((1380, y + 11), "ĐÁNH GIÁ PHONG CÁCH / ĐỒ HỌA", font=header_font, fill=(255, 220, 120))
    
    y += 58
    
    # Comparison Rows:
    # (Section, Name, Orig_path, Mod_path, Style_text, box_h, orig_sz, mod_sz, orig_crop, mod_crop)
    items = [
        # Nhóm 1: Login & Branding
        ("1. ĐĂNG NHẬP & THƯƠNG HIỆU", "Logo Game Moly VN", 
         "work/exported/orig_logo/5.png", "scratch/localized_assets/logo_9_fitted.png", 
         "Vector chuẩn, xóa sạch Taomee, giữ mascot nón vàng", 95, (330, 85), (330, 85), None, None),
         
        ("1. ĐĂNG NHẬP & THƯƠNG HIỆU", "Nút Bắt Đầu (LoginHome)", 
         "work/exported/LoginHome_full/shapes/128.png", "scratch/localized_assets/bat_dau_128.png", 
         "Ngọc hồng lựu 3D Ruby, viền vàng kim, lấp lánh", 90, (135, 75), (135, 75), None, None),
         
        ("1. ĐĂNG NHẬP & THƯƠNG HIỆU", "Nút Đăng Nhập (Login)", 
         "work/exported/Login_full/shapes/171.png", "scratch/localized_assets/btn_login_173.png", 
         "Cam Candy 3D, loại bỏ viền gỗ lồng đôi, viền đậm", 85, (155, 68), (155, 68), None, None),
         
        ("1. ĐĂNG NHẬP & THƯƠNG HIỆU", "Nút Đăng Ký Chân Trang", 
         "work/exported/Login_full/shapes/167.png", "scratch/localized_assets/btn_reg_167.png", 
         "Tỷ lệ khớp 100%, nét chữ sắc gọn, viền nâu đậm", 55, (110, 32), (110, 32), None, None),
         
        ("1. ĐĂNG NHẬP & THƯƠNG HIỆU", "Bảng Hiệu Nhà Gỗ Đăng Nhập", 
         "work/exported/Login_full/shapes/150.png", "scratch/localized_assets/shape_150.png", 
         "Gỗ sồi nâu đỏ vân tự nhiên, biển Moly VN ấm cúng", 110, (280, 95), (280, 95), None, None),

        # Nhóm 2: Server Selection
        ("2. BỘ CHỌN MÁY CHỦ (SERVER SELECTOR)", "Tiêu Đề Chọn Máy Chủ", 
         "work/exported/Login_full/shapes/260.png", "scratch/localized_assets/shape_260.png", 
         "Thanh kim loại mờ + Chữ 3D Cam 'CHỌN MÁY CHỦ'", 60, (338, 41), (338, 41), None, None),
         
        ("2. BỘ CHỌN MÁY CHỦ (SERVER SELECTOR)", "Nút Tất Cả Máy Chủ", 
         "work/exported/Login_full/shapes/221.png", "scratch/localized_assets/shape_221.png", 
         "Thỏi Jelly cam bóng viền vàng, ánh sáng vòm chuẩn", 55, (159, 32), (159, 32), None, None),
         
        ("2. BỘ CHỌN MÁY CHỦ (SERVER SELECTOR)", "Nút Máy Chủ Đề Xuất", 
         "work/exported/Login_full/shapes/224.png", "scratch/localized_assets/shape_224.png", 
         "Thỏi Jelly hồng tím bóng bẩy, viền sáng ngọt ngào", 55, (159, 32), (159, 32), None, None),
         
        ("2. BỘ CHỌN MÁY CHỦ (SERVER SELECTOR)", "Nút Vào Nhanh", 
         "work/exported/Login_full/shapes/265.png", "scratch/localized_assets/shape_265.png", 
         "Magenta Candy pill, chữ trắng viền hồng đậm nét", 50, (82, 22), (82, 22), None, None),
         
        ("2. BỘ CHỌN MÁY CHỦ (SERVER SELECTOR)", "Trạng Thái Máy Chủ Đầy", 
         "work/exported/Login_full/shapes/279.png", "scratch/localized_assets/shape_279.png", 
         "Ngọn lửa 3D rực cháy + chữ 'ĐẦY' sắc nét", 50, (28, 30), (28, 30), None, None),

        # Nhóm 3: Dialogs & Notices
        ("3. HỘP THOẠI & THÔNG BÁO", "Tiêu Đề Hộp Thoại Alert", 
         "work/exported/Login_full/shapes/361.png", "scratch/localized_assets/title_thong_bao_361.png", 
         "Biển mây xanh hoạt hình 'THÔNG BÁO' rực rỡ", 80, (90, 70), (90, 70), None, None),
         
        ("3. HỘP THOẠI & THÔNG BÁO", "Nút 'ĐÃ HIỂU' Xác Nhận", 
         "work/exported/Login_full/shapes/367.png", "scratch/localized_assets/btn_da_hieu_367.png", 
         "Nút kẹo thạch xanh viền trắng bóng 3D", 70, (139, 58), (139, 58), None, None),
         
        ("3. HỘP THOẠI & THÔNG BÁO", "Nút Xác Nhận / Hủy (Đỏ/Xanh)", 
         "work/exported/Login_full/shapes/288.png", "scratch/localized_assets/shape_288.png", 
         "Candy nút chữ nhật bo góc viền bóng phản chiếu", 55, (72, 33), (72, 33), None, None),
         
        ("3. HỘP THOẠI & THÔNG BÁO", "Nút Điều Hướng 'VÀO GAME'", 
         "work/exported/Login_full/DefineButton2_391/1_up.png", "scratch/localized_assets/shape_389.png", 
         "Cam glossy phản quang, viền trắng nổi khối 3D", 70, (148, 55), (148, 55), None, None),
         
        ("3. HỘP THOẠI & THÔNG BÁO", "Nút 'XEM TRỢ GIÚP'", 
         "work/exported/Login_full/DefineButton2_383/1_up.png", "scratch/localized_assets/shape_378.png", 
         "Xanh biển glossy sang trọng, viền trắng tinh tế", 70, (153, 55), (153, 55), None, None),

        # Nhóm 4: Super Lamu VIP
        ("4. MENU SUPER LA MỖ VIP", "Đặc Quyền Super La Mỗ", 
         "work/exported/ui_buttons/DefineButton2_5871/1_up.png", "scratch/localized_assets/ui_5868.png", 
         "Thỏi vàng hoàng gia bóng bẩy, viền vàng hổ phách", 50, (153, 26), (153, 26), None, None),
         
        ("4. MENU SUPER LA MỖ VIP", "Tôi Muốn Super La Mỗ", 
         "work/exported/ui_buttons/DefineButton2_5875/1_up.png", "scratch/localized_assets/ui_5872.png", 
         "Thỏi vàng hoàng gia bóng bẩy, viền vàng hổ phách", 50, (153, 26), (153, 26), None, None),
         
        ("4. MENU SUPER LA MỖ VIP", "Quà LỚn Super La Mỗ", 
         "work/exported/ui_buttons/DefineButton2_5884/1_up.png", "scratch/localized_assets/ui_5881.png", 
         "Thỏi vàng hoàng gia bóng bẩy, viền vàng hổ phách", 50, (153, 26), (153, 26), None, None),

        # Nhóm 5: Bottom Toolbar Icons
        ("5. THANH CÔNG CỤ DƯỚI (TOOLBAR)", "Icon 'ĐỘNG TÁC'", 
         "work/exported/ui_buttons/DefineButton2_6838/1_up.png", "scratch/localized_assets/ui_6834.png", 
         "Biển badge đỏ cam bo tròn, viền vàng sắc nét", 65, (40, 52), (40, 52), None, None),
         
        ("5. THANH CÔNG CỤ DƯỚI (TOOLBAR)", "Icon 'BA LÔ' (Hành Trang)", 
         "work/exported/ui_buttons/DefineButton2_6848/1_up.png", "scratch/localized_assets/ui_6844.png", 
         "Túi da học sinh cam bóng, chữ 'BA LÔ' viền vàng", 65, (42, 52), (42, 52), None, None),
         
        ("5. THANH CÔNG CỤ DƯỚI (TOOLBAR)", "Icon 'BẠN BÈ' (Hảo Hữu)", 
         "work/exported/ui_buttons/DefineButton2_6853/1_up.png", "scratch/localized_assets/ui_6849.png", 
         "Cặp đầu Moly đỏ đáng yêu, nhãn 'BẠN BÈ' nổi", 65, (45, 52), (45, 52), None, None),

        # Nhóm 6: Map Buildings
        ("6. BIỂN HIỆU CÔNG TRÌNH BẢN ĐỒ", "Cổng Vòm Lâu Đài (Map 1)", 
         "work/exported/Map1/5.jpg", "work/map_buildings/map1_bg_vi.jpg", 
         "Cổng vòm đá chạm vàng hoàng gia 'LÂU ĐÀI MOLY'", 95, (260, 80), (260, 80), (395, 235, 565, 295), (395, 235, 565, 295)),
         
        ("6. BIỂN HIỆU CÔNG TRÌNH BẢN ĐỒ", "Đồn Cảnh Sát Moly (Map 2)", 
         "work/exported/Map2/57.jpg", "work/map_buildings/map2_bg_vi.jpg", 
         "Biển hiệu cờ xanh cảnh sát 'CẢNH SÁT MOLY'", 85, (220, 70), (220, 70), (105, 190, 245, 250), (105, 190, 245, 250)),
         
        ("6. BIỂN HIỆU CÔNG TRÌNH BẢN ĐỒ", "Tiệm Thời Trang (Map 3)", 
         "work/exported/Map3/4.jpg", "work/map_buildings/map3_bg_vi.jpg", 
         "Biển vải lụa hồng uốn lượn 'TIỆM THỜI TRANG'", 85, (220, 70), (220, 70), (315, 110, 465, 175), (315, 110, 465, 175)),
         
        ("6. BIỂN HIỆU CÔNG TRÌNH BẢN ĐỒ", "Bãi Trượt Tuyết (Map 4)", 
         "work/exported/Map4/15.jpg", "work/map_buildings/map4_bg_vi.jpg", 
         "Biển gỗ núi tuyết phủ trắng 'BÃI TRƯỢT TUYẾT'", 85, (220, 70), (220, 70), (210, 210, 360, 270), (210, 210, 360, 270)),
    ]
    
    curr_section = None
    row_bg_toggle = False
    
    row_font_name = get_font(15, bold=True)
    row_font_desc = get_font(13, bold=False)
    section_font = get_font(16, bold=True)
    
    for sec, name, orig_path, mod_path, desc, row_h, orig_sz, mod_sz, orig_crop, mod_crop in items:
        if sec != curr_section:
            curr_section = sec
            draw.rectangle([30, y, width - 30, y + 36], fill=(32, 42, 75, 255))
            draw.text((45, y + 8), sec, font=section_font, fill=(255, 205, 80))
            y += 40
            row_bg_toggle = False
            
        r_color = (24, 29, 46, 255) if row_bg_toggle else (18, 22, 36, 255)
        draw.rectangle([30, y, width - 30, y + row_h], fill=r_color)
        draw.line([(30, y + row_h), (width - 30, y + row_h)], fill=(38, 46, 68, 255), width=1)
        row_bg_toggle = not row_bg_toggle
        
        # Col 1: Name
        draw.text((50, y + (row_h - 20) // 2), name, font=row_font_name, fill=(240, 240, 255))
        
        # Col 2: Orig Image
        orig_img = load_img(orig_path, orig_sz[0], orig_sz[1], orig_crop)
        ox = 430 + (420 - orig_img.width) // 2
        oy = y + (row_h - orig_img.height) // 2
        canvas.paste(orig_img, (ox, oy), orig_img if orig_img.mode == "RGBA" else None)
        
        # Col 3: Mod Image
        mod_img = load_img(mod_path, mod_sz[0], mod_sz[1], mod_crop)
        mx = 900 + (420 - mod_img.width) // 2
        my = y + (row_h - mod_img.height) // 2
        canvas.paste(mod_img, (mx, my), mod_img if mod_img.mode == "RGBA" else None)
        
        # Col 4: Description / Style
        draw.text((1370, y + (row_h - 18) // 2), desc, font=row_font_desc, fill=(185, 215, 245))
        
        y += row_h + 4
        
    final_canvas = canvas.crop((0, 0, width, y + 30))
    final_canvas.save(OUT_IMG_ARTIFACT)
    final_canvas.save(OUT_IMG_SCRATCH)
    print(f"\n[SUCCESS] Composed comparison board ({final_canvas.width}x{final_canvas.height} px)!")
    print(f"Saved to:\n  - {OUT_IMG_ARTIFACT}\n  - {OUT_IMG_SCRATCH}")

if __name__ == "__main__":
    compose()
