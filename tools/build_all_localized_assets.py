import os
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

def get_font(size, bold=True):
    font_paths = [
        "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/tahomabd.ttf" if bold else "C:/Windows/Fonts/tahoma.ttf",
        "C:/Windows/Fonts/segoeuib.ttf" if bold else "C:/Windows/Fonts/segoeui.ttf",
    ]
    for p in font_paths:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                pass
    return ImageFont.load_default()

def draw_bubble_text(draw, x, y, text, font, fill, stroke_fill, stroke_width):
    for dx in range(-stroke_width, stroke_width + 1):
        for dy in range(-stroke_width, stroke_width + 1):
            if dx * dx + dy * dy <= stroke_width * stroke_width:
                draw.text((x + dx, y + dy), text, font=font, fill=stroke_fill)
    draw.text((x, y), text, font=font, fill=fill)

def patch_toolbar_icon(src_path, out_path, vi_text, font_size=9, badge_h=18):
    if not os.path.exists(src_path):
        print(f"  [WARN] Source icon not found: {src_path}")
        return
    im = Image.open(src_path).convert("RGBA")
    w, h = im.size
    draw = ImageDraw.Draw(im)
    
    # Bottom badge area to clear
    by0 = h - badge_h - 1
    pix = im.load()
    for y in range(max(0, by0), h):
        for x in range(w):
            pix[x, y] = (0, 0, 0, 0)
            
    # Draw golden-orange badge with deep red border
    bx0, bx1 = 1, w - 2
    by1 = h - 2
    r = 6
    # Outer golden glow
    draw.rounded_rectangle([bx0 - 1, by0 - 1, bx1 + 1, by1 + 1], radius=r + 1, fill=(255, 204, 0, 255))
    # Deep red border
    draw.rounded_rectangle([bx0, by0, bx1, by1], radius=r, fill=(150, 20, 0, 255))
    # Inner golden orange body
    draw.rounded_rectangle([bx0 + 1, by0 + 1, bx1 - 1, by1 - 1], radius=r - 1, fill=(245, 145, 10, 255))
    # Top gloss
    draw.rounded_rectangle([bx0 + 2, by0 + 1, bx1 - 2, by0 + (badge_h // 2)], radius=r - 2, fill=(255, 215, 60, 200))
    
    font = get_font(font_size, bold=True)
    bbox = draw.textbbox((0, 0), vi_text, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    tx = (w - tw) // 2
    ty = by0 + (badge_h - th) // 2 - 2
    
    # Bold white text with deep brown-red stroke
    draw_bubble_text(draw, tx, ty, vi_text, font, (255, 255, 255, 255), (110, 15, 0, 255), 2)
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    im.save(out_path)
    print(f"  [OK] Patched toolbar icon: {os.path.basename(out_path)} ({vi_text})")

def create_batdau_shape_128(out_path):
    w, h = 108, 62
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(im)
    
    font = get_font(21, bold=True)
    
    # Two lines: BẮT and ĐẦU
    bbox1 = draw.textbbox((0, 0), "BẮT", font=font)
    tw1 = bbox1[2] - bbox1[0]
    x1 = (w - tw1) // 2
    y1 = 6
    
    bbox2 = draw.textbbox((0, 0), "ĐẦU", font=font)
    tw2 = bbox2[2] - bbox2[0]
    x2 = (w - tw2) // 2
    y2 = 30
    
    for t, x, y in [("BẮT", x1, y1), ("ĐẦU", x2, y2)]:
        # Golden outer glow
        for dx in range(-5, 6):
            for dy in range(-5, 6):
                if dx*dx + dy*dy <= 25:
                    draw.text((x + dx, y + dy), t, font=font, fill=(255, 235, 120, 255))
        # Deep red border
        for dx in range(-3, 4):
            for dy in range(-3, 4):
                if dx*dx + dy*dy <= 9:
                    draw.text((x + dx, y + dy), t, font=font, fill=(150, 25, 0, 255))
        # Inner warm yellow
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                draw.text((x + dx, y + dy), t, font=font, fill=(255, 210, 50, 255))
        # White face
        draw.text((x, y), t, font=font, fill=(255, 255, 240, 255))
        
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    im.save(out_path)
    print(f"  [OK] Created BẮT ĐẦU shape: {out_path}")

def create_moly_event_banner(out_path):
    w, h = 280, 200
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(im)
    
    # Festive red gradient banner card
    draw.rounded_rectangle([2, 2, w - 3, h - 3], radius=16, fill=(210, 28, 28, 255), outline=(255, 215, 0, 255), width=3)
    draw.rounded_rectangle([8, 8, w - 9, h - 9], radius=12, fill=(185, 20, 20, 255), outline=(255, 240, 150, 200), width=1)
    
    font_title = get_font(18, bold=True)
    font_sub = get_font(12, bold=True)
    font_btn = get_font(13, bold=True)
    
    # Gold decorative header
    draw_bubble_text(draw, 14, 20, "MOLY - THẾ GIỚI CHUỘT CHŨI", font_title, (255, 245, 160, 255), (90, 10, 10, 255), 3)
    draw_bubble_text(draw, 42, 50, "PHIÊN BẢN VIỆT NAM 2026", font_sub, (255, 255, 255, 255), (100, 15, 15, 255), 2)
    
    # Inner message box
    draw.rounded_rectangle([20, 78, w - 21, 140], radius=10, fill=(255, 248, 220, 255), outline=(255, 215, 0, 255), width=2)
    font_body = get_font(11, bold=False)
    draw.text((30, 88), "Trở về vương quốc tuổi thơ rực rỡ,", font=font_body, fill=(120, 40, 0, 255))
    draw.text((30, 106), "chăm sóc LaMu & kết nối bạn bè!", font=font_body, fill=(120, 40, 0, 255))
    draw.text((30, 122), "Máy chủ độc lập, trải nghiệm mượt mà.", font=font_body, fill=(200, 30, 30, 255))
    
    # Action button
    bx0, by0, bx1, by1 = 50, 152, w - 51, 186
    draw.rounded_rectangle([bx0, by0, bx1, by1], radius=14, fill=(16, 185, 129, 255), outline=(255, 255, 255, 255), width=2)
    draw_bubble_text(draw, bx0 + 24, by0 + 7, "KHÁM PHÁ NGAY", font_btn, (255, 255, 255, 255), (6, 95, 70, 255), 2)
    
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    im.save(out_path)
    print(f"  [OK] Created Moly VN event banner: {out_path}")

def main():
    print("=== BUILDING ALL LOCALIZED GRAPHICS AND ICONS ===")
    out_dir = Path("scratch/localized_assets")
    out_dir.mkdir(parents=True, exist_ok=True)
    
    # 1. Start Button Shape 128
    create_batdau_shape_128(str(out_dir / "shape_128.png"))
    
    # 2. Transparent spacers to erase Taomee logos in LoginHome.swf
    Image.new("RGBA", (114, 37), (0, 0, 0, 0)).save(out_dir / "transparent_171.png")
    Image.new("RGBA", (135, 41), (0, 0, 0, 0)).save(out_dir / "transparent_236.png")
    print("  [OK] Created transparent eraser images for Taomee logos")
    
    # 3. Moly VN Event Banner for randomMC.swf
    create_moly_event_banner(str(out_dir / "randomMC_banner_3.png"))
    
    # 4. Toolbar icons for ui.swf
    ui_icons = [
        ("3279.png", "BẢN ĐỒ", 10, 16),
        ("6834.png", "ĐỘNG TÁC", 6, 17),
        ("6836.png", "ĐỘNG TÁC", 6, 17),
        ("6839.png", "NÉM", 10, 18),
        ("6841.png", "NÉM", 10, 18),
        ("6844.png", "TÚI ĐỒ", 8, 18),
        ("6846.png", "TÚI ĐỒ", 8, 18),
        ("6849.png", "BẠN BÈ", 8, 18),
        ("6851.png", "BẠN BÈ", 8, 18),
        ("6854.png", "THIÊN SỨ", 7, 18),
        ("6856.png", "THIÊN SỨ", 7, 18),
        ("6859.png", "GIA VIÊN", 7, 18),
        ("6861.png", "GIA VIÊN", 7, 18),
        ("6864.png", "SHOP", 9, 18),
        ("6866.png", "SHOP", 9, 18),
        ("6929.png", "NHÀ Ở", 8, 18),
        ("6931.png", "NHÀ Ở", 8, 18),
    ]
    for fname, label, fsize, bh in ui_icons:
        src = Path("work/audit_images/ui") / fname
        dst = out_dir / f"ui_{fname}"
        patch_toolbar_icon(str(src), str(dst), label, font_size=fsize, badge_h=bh)
        
    # 5. TopUI icons
    topui_icons = [
        ("82.png", "QUÀ TẶNG", 8, 16),
        ("366.png", "GIA VIÊN", 8, 16),
    ]
    for fname, label, fsize, bh in topui_icons:
        src = Path("work/audit_images/topUI") / fname
        dst = out_dir / f"topui_{fname}"
        patch_toolbar_icon(str(src), str(dst), label, font_size=fsize, badge_h=bh)
        
    print("=== ALL LOCALIZED GRAPHICS BUILT SUCCESSFULLY! ===")

if __name__ == "__main__":
    main()
