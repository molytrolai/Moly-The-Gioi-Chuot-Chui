import os
from PIL import Image, ImageDraw, ImageFont

def get_font(size):
    for p in ["C:/Windows/Fonts/arialbd.ttf", "C:/Windows/Fonts/tahomabd.ttf", "C:/Windows/Fonts/segoeuib.ttf"]:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()

def draw_bubble_text(draw, x, y, text, font, fill, stroke_fill, stroke_width):
    for dx in range(-stroke_width, stroke_width + 1):
        for dy in range(-stroke_width, stroke_width + 1):
            if dx*dx + dy*dy <= stroke_width*stroke_width:
                draw.text((x + dx, y + dy), text, font=font, fill=stroke_fill)
    draw.text((x, y), text, font=font, fill=fill)

def patch_toolbar_icon(src_path, out_path, vi_text, font_size=10, badge_h=19):
    im = Image.open(src_path).convert("RGBA")
    w, h = im.size
    draw = ImageDraw.Draw(im)
    
    # Bottom badge area to clear
    by0 = h - badge_h - 1
    # Clear the bottom region by setting alpha=0
    pix = im.load()
    for y in range(by0, h):
        for x in range(w):
            pix[x, y] = (0, 0, 0, 0)
            
    # Draw golden-orange badge with deep red border
    bx0, bx1 = 1, w - 2
    by1 = h - 2
    r = 7
    # Outer golden glow
    draw.rounded_rectangle([bx0-1, by0-1, bx1+1, by1+1], radius=r+1, fill=(255, 204, 0, 255))
    # Deep red border
    draw.rounded_rectangle([bx0, by0, bx1, by1], radius=r, fill=(160, 20, 0, 255))
    # Inner golden orange body
    draw.rounded_rectangle([bx0+1, by0+1, bx1-1, by1-1], radius=r-1, fill=(245, 150, 10, 255))
    # Top gloss
    draw.rounded_rectangle([bx0+2, by0+1, bx1-2, by0 + (badge_h//2)], radius=r-2, fill=(255, 215, 60, 200))
    
    font = get_font(font_size)
    bbox = draw.textbbox((0, 0), vi_text, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    tx = (w - tw) // 2
    ty = by0 + (badge_h - th) // 2 - 2
    
    # Bold white text with deep brown-red stroke
    draw_bubble_text(draw, tx, ty, vi_text, font, (255, 255, 255, 255), (120, 20, 0, 255), 2)
    im.save(out_path)
    print("Saved:", out_path)

if __name__ == "__main__":
    os.makedirs("work/test_icons", exist_ok=True)
    patch_toolbar_icon("work/audit_images/ui/6844.png", "work/test_icons/6844_tuido.png", "TÚI ĐỒ", font_size=11, badge_h=18)
    patch_toolbar_icon("work/audit_images/ui/6849.png", "work/test_icons/6849_banbe.png", "BẠN BÈ", font_size=11, badge_h=18)
    patch_toolbar_icon("work/audit_images/ui/3279.png", "work/test_icons/3279_bando.png", "BẢN ĐỒ", font_size=10, badge_h=16)
