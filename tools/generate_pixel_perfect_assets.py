#!/usr/bin/env python3
"""Generate pixel-perfect localized cartoon graphics for Moly VN."""

import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

OUTPUT_DIR = Path("scratch/localized_assets")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

FONT_BOLD = "C:/Windows/Fonts/segoeuib.ttf"
FONT_TAHOMA_BOLD = "C:/Windows/Fonts/tahomabd.ttf"
FONT_ARIAL_BOLD = "C:/Windows/Fonts/arialbd.ttf"

def draw_text_with_outline(draw, pos, text, font, fill_color, outline_color, outline_width=2):
    x, y = pos
    # Draw outline
    for dx in range(-outline_width, outline_width + 1):
        for dy in range(-outline_width, outline_width + 1):
            if dx * dx + dy * dy <= outline_width * outline_width:
                draw.text((x + dx, y + dy), text, font=font, fill=outline_color)
    # Draw main text
    draw.text((x, y), text, font=font, fill=fill_color)

def generate_bat_dau():
    """Generate 3D BẮT ĐẦU text for Button 168 (Shape 128).
    Original 128.svg bounds: 108 x 62 px.
    We create high-res 216 x 124 px image.
    """
    w, h = 216, 124
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    font = ImageFont.truetype(FONT_TAHOMA_BOLD, 36)
    
    # 2 lines: "BẮT" and "ĐẦU" stacked vertically for maximum size & punchiness
    lines = ["BẮT", "ĐẦU"]
    
    # Calculate bounding boxes
    bbox1 = font.getbbox(lines[0])
    w1, h1 = bbox1[2] - bbox1[0], bbox1[3] - bbox1[1]
    
    bbox2 = font.getbbox(lines[1])
    w2, h2 = bbox2[2] - bbox2[0], bbox2[3] - bbox2[1]
    
    y1 = 12
    y2 = y1 + h1 + 10
    x1 = (w - w1) // 2
    x2 = (w - w2) // 2
    
    # Layer 1: Dark red 3D drop shadow (simulate extrusion)
    for shift_y in range(6, 1, -1):
        for line, (x, y) in zip(lines, [(x1, y1 + shift_y), (x2, y2 + shift_y)]):
            draw_text_with_outline(draw, (x, y), line, font, fill_color=(139, 0, 0, 255), outline_color=(100, 0, 0, 255), outline_width=4)
            
    # Layer 2: Main golden text with rich outline
    for line, (x, y) in zip(lines, [(x1, y1), (x2, y2)]):
        draw_text_with_outline(draw, (x, y), line, font, fill_color=(255, 235, 59, 255), outline_color=(180, 20, 0, 255), outline_width=4)
        # Inner brighter highlight
        draw_text_with_outline(draw, (x, y - 1), line, font, fill_color=(255, 255, 200, 255), outline_color=(255, 200, 0, 255), outline_width=1)
        
    out_path = OUTPUT_DIR / "bat_dau_128.png"
    img.save(out_path, "PNG")
    print(f"Generated {out_path} ({img.size})")

def generate_bottom_buttons():
    """Generate the 4 bottom pill buttons for Login.swf:
    - btn_forgot_158.png: QUÊN MK (120 x 33)
    - btn_change_161.png: ĐỔI MK (120 x 33)
    - btn_protect_164.png: BẢO MẬT (120 x 33)
    - btn_reg_167.png: ĐĂNG KÝ (168 x 33)
    """
    buttons = [
        ("btn_forgot_158.png", "QUÊN MK", 120, 33, 14),
        ("btn_change_161.png", "ĐỔI MK", 120, 33, 14),
        ("btn_protect_164.png", "BẢO MẬT", 120, 33, 14),
        ("btn_reg_167.png", "ĐĂNG KÝ", 168, 33, 15),
    ]
    
    for filename, text, w, h, font_size in buttons:
        img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        radius = h // 2
        
        # Outer border: Dark red/crimson
        draw.rounded_rectangle([0, 0, w - 1, h - 1], radius=radius, fill=(255, 120, 0, 255), outline=(150, 20, 0, 255), width=2)
        
        # Inner pill gradient / highlight
        draw.rounded_rectangle([2, 2, w - 3, h - 3], radius=radius - 2, fill=(255, 150, 0, 255), outline=(255, 220, 100, 255), width=1)
        
        # Upper specular gloss
        draw.rounded_rectangle([4, 3, w - 5, h // 2], radius=radius - 4, fill=(255, 200, 80, 180))
        
        font = ImageFont.truetype(FONT_TAHOMA_BOLD, font_size)
        bbox = font.getbbox(text)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
        
        tx = (w - tw) // 2
        ty = (h - th) // 2 - 2
        
        # Draw text with brown outline
        draw_text_with_outline(draw, (tx, ty), text, font, fill_color=(255, 255, 220, 255), outline_color=(120, 20, 0, 255), outline_width=2)
        
        out_path = OUTPUT_DIR / filename
        img.save(out_path, "PNG")
        print(f"Generated {out_path} ({img.size})")

def generate_alert_components():
    """Generate components for RES_Login_Alert in Login.swf:
    - Shape 361: THÔNG BÁO (180 x 60)
    - Shape 367, 368, 369: ĐÃ HIỂU (140 x 44)
    - Shape 372: HỦY (70 x 35)
    - Shape 376: ĐỒNG Ý (70 x 35)
    """
    # 1. Title THÔNG BÁO (Shape 361)
    img_title = Image.new("RGBA", (200, 60), (0, 0, 0, 0))
    draw_title = ImageDraw.Draw(img_title)
    font_title = ImageFont.truetype(FONT_TAHOMA_BOLD, 26)
    text_title = "THÔNG BÁO"
    bbox = font_title.getbbox(text_title)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    tx, ty = (200 - tw) // 2, (60 - th) // 2
    draw_text_with_outline(draw_title, (tx, ty), text_title, font_title, fill_color=(102, 34, 0, 255), outline_color=(255, 255, 255, 255), outline_width=2)
    img_title.save(OUTPUT_DIR / "title_thong_bao_361.png", "PNG")
    print(f"Generated title_thong_bao_361.png")
    
    # 2. Button ĐÃ HIỂU (Shape 367, 368, 369)
    # 367: Normal
    img_btn = Image.new("RGBA", (140, 44), (0, 0, 0, 0))
    draw_btn = ImageDraw.Draw(img_btn)
    font_btn = ImageFont.truetype(FONT_TAHOMA_BOLD, 18)
    text_btn = "ĐÃ HIỂU"
    bbox = font_btn.getbbox(text_btn)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    tx, ty = (140 - tw) // 2, (44 - th) // 2
    draw_text_with_outline(draw_btn, (tx, ty), text_btn, font_btn, fill_color=(255, 255, 255, 255), outline_color=(120, 40, 0, 255), outline_width=2)
    img_btn.save(OUTPUT_DIR / "btn_da_hieu_367.png", "PNG")
    img_btn.save(OUTPUT_DIR / "btn_da_hieu_368.png", "PNG")
    img_btn.save(OUTPUT_DIR / "btn_da_hieu_369.png", "PNG")
    print(f"Generated btn_da_hieu_367.png (and 368, 369)")
    
    # 3. Shape 372: HỦY & Shape 376: ĐỒNG Ý
    for name, t in [("btn_cancel_372.png", "HỦY"), ("btn_confirm_376.png", "ĐỒNG Ý")]:
        im = Image.new("RGBA", (80, 35), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        f = ImageFont.truetype(FONT_TAHOMA_BOLD, 14)
        bb = f.getbbox(t)
        bw, bh = bb[2] - bb[0], bb[3] - bb[1]
        bx, by = (80 - bw) // 2, (35 - bh) // 2
        draw_text_with_outline(d, (bx, by), t, f, fill_color=(255, 255, 255, 255), outline_color=(120, 40, 0, 255), outline_width=2)
        im.save(OUTPUT_DIR / name, "PNG")
        print(f"Generated {name}")

def generate_covenants_and_license():
    """Generate covenants (234), license (197), and CADPA tooltip (232) for LoginHome.swf."""
    # 1. Covenants (Shape 234): 714 x 102
    w, h = 714, 102
    img_cov = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw_cov = ImageDraw.Draw(img_cov)
    
    f_title = ImageFont.truetype(FONT_TAHOMA_BOLD, 22)
    f_body = ImageFont.truetype(FONT_TAHOMA_BOLD, 17)
    
    t_title = "QUY ƯỚC CƯ DÂN MOLY VN"
    t_l1 = "Tẩy chay game xấu  •  Chú ý tự bảo vệ  •  Đề phòng lừa đảo"
    t_l2 = "Chơi game điều độ  •  Phân bổ thời gian  •  Tận hưởng cuộc sống lành mạnh"
    
    draw_text_with_outline(draw_cov, (10, 8), t_title, f_title, fill_color=(180, 20, 20, 255), outline_color=(255, 255, 255, 255), outline_width=3)
    draw_text_with_outline(draw_cov, (10, 40), t_l1, f_body, fill_color=(90, 20, 70, 255), outline_color=(255, 255, 255, 255), outline_width=2)
    draw_text_with_outline(draw_cov, (10, 68), t_l2, f_body, fill_color=(90, 20, 70, 255), outline_color=(255, 255, 255, 255), outline_width=2)
    
    img_cov.save(OUTPUT_DIR / "covenants_234.png", "PNG")
    print(f"Generated covenants_234.png")
    
    # 2. License (Shape 197): 346 x 54
    w, h = 346, 54
    img_lic = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw_lic = ImageDraw.Draw(img_lic)
    f_lic1 = ImageFont.truetype(FONT_TAHOMA_BOLD, 17)
    f_lic2 = ImageFont.truetype(FONT_TAHOMA_BOLD, 15)
    
    draw_text_with_outline(draw_lic, (10, 6), "Moly - Thế Giới Chuột Chũi VN", f_lic1, fill_color=(150, 40, 0, 255), outline_color=(255, 255, 255, 255), outline_width=2)
    draw_text_with_outline(draw_lic, (10, 30), "Phiên Bản Tiếng Việt Độc Lập 2026", f_lic2, fill_color=(180, 60, 0, 255), outline_color=(255, 255, 255, 255), outline_width=2)
    img_lic.save(OUTPUT_DIR / "license_197.png", "PNG")
    print(f"Generated license_197.png")
    
    # 3. CADPA Tooltip (Shape 232): 564 x 218
    w, h = 564, 218
    img_cadpa = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw_cadpa = ImageDraw.Draw(img_cadpa)
    
    # Rounded speech bubble background
    draw_cadpa.rounded_rectangle([4, 4, w - 5, h - 5], radius=16, fill=(255, 255, 255, 245), outline=(34, 139, 34, 255), width=3)
    
    f_head = ImageFont.truetype(FONT_TAHOMA_BOLD, 20)
    f_text = ImageFont.truetype(FONT_BOLD, 15)
    
    draw_cadpa.text((20, 16), "HƯỚNG DẪN ĐỘ TUỔI (CADPA 8+)", font=f_head, fill=(20, 120, 40, 255))
    draw_cadpa.text((20, 52), "1. Trò chơi thích hợp cho cư dân từ 8 tuổi trở lên.", font=f_text, fill=(40, 40, 40, 255))
    draw_cadpa.text((20, 84), "2. Nội dung mang tính giáo dục, phát triển tư duy logic và gắn kết bạn bè.", font=f_text, fill=(40, 40, 40, 255))
    draw_cadpa.text((20, 116), "3. Khuyến nghị thời gian chơi điều độ, không quá 2 giờ mỗi ngày.", font=f_text, fill=(40, 40, 40, 255))
    draw_cadpa.text((20, 148), "4. Ba mẹ vui lòng đồng hành và hướng dẫn các bạn nhỏ trải nghiệm an toàn!", font=f_text, fill=(40, 40, 40, 255))
    
    img_cadpa.save(OUTPUT_DIR / "cadpa_tooltip_232.png", "PNG")
    print(f"Generated cadpa_tooltip_232.png")

if __name__ == "__main__":
    generate_bat_dau()
    generate_bottom_buttons()
    generate_alert_components()
    generate_covenants_and_license()
    print("\nAll pixel-perfect localized assets generated successfully!")
