import os
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

def get_font(size, bold=True):
    font_paths = [
        "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/segoeuib.ttf" if bold else "C:/Windows/Fonts/segoeui.ttf",
        "C:/Windows/Fonts/tahomabd.ttf" if bold else "C:/Windows/Fonts/tahoma.ttf",
    ]
    for p in font_paths:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                pass
    return ImageFont.load_default()

def render_organic_bubble_text(w, h, text_lines, font_size=10, y_offset=0, line_spacing=0):
    """
    Renders text onto a transparent canvas with the exact original 3-layer bubble contour:
    1. Outer golden yellow halo (rgb 245, 185, 0)
    2. Deep burgundy red stroke (rgb 145, 18, 18)
    3. Pure white face (rgb 255, 255, 255)
    """
    text_layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(text_layer)
    font = get_font(font_size, bold=True)
    
    # Calculate bounding boxes and positions
    line_infos = []
    total_h = 0
    for line in text_lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        lw = bbox[2] - bbox[0]
        lh = bbox[3] - bbox[1]
        line_infos.append((line, lw, lh))
        total_h += lh + line_spacing
    total_h -= line_spacing
    
    cur_y = y_offset
    
    # 1. Outer Golden-Yellow Halo (radius 3)
    halo_layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    halo_draw = ImageDraw.Draw(halo_layer)
    y_ptr = cur_y
    for line, lw, lh in line_infos:
        lx = (w - lw) // 2
        for dx in range(-3, 4):
            for dy in range(-3, 4):
                if dx*dx + dy*dy <= 10:
                    halo_draw.text((lx + dx, y_ptr + dy), line, font=font, fill=(245, 185, 0, 255))
        y_ptr += lh + line_spacing
        
    # 2. Deep Burgundy Red Stroke (radius 1.5 - 2)
    stroke_layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    stroke_draw = ImageDraw.Draw(stroke_layer)
    y_ptr = cur_y
    for line, lw, lh in line_infos:
        lx = (w - lw) // 2
        for dx in range(-2, 3):
            for dy in range(-2, 3):
                if dx*dx + dy*dy <= 4:
                    stroke_draw.text((lx + dx, y_ptr + dy), line, font=font, fill=(140, 20, 20, 255))
        y_ptr += lh + line_spacing
        
    # 3. Pure White Face
    face_layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    face_draw = ImageDraw.Draw(face_layer)
    y_ptr = cur_y
    for line, lw, lh in line_infos:
        lx = (w - lw) // 2
        face_draw.text((lx, y_ptr), line, font=font, fill=(255, 255, 255, 255))
        y_ptr += lh + line_spacing
        
    # Composite layers
    final_text = Image.alpha_composite(halo_layer, stroke_layer)
    final_text = Image.alpha_composite(final_text, face_layer)
    return final_text

def craft_icon_candidate(src_path, text_lines, font_size=10, y_clear_start=25, text_y_pos=26, line_spacing=0):
    im = Image.open(src_path).convert("RGBA")
    w, h = im.size
    
    # 1. Clear original text area smoothly
    pix = im.load()
    for y in range(max(0, y_clear_start), h):
        for x in range(w):
            # If in lower part, erase Chinese characters
            pix[x, y] = (0, 0, 0, 0)
            
    # 2. Render authentic bubble text
    text_canvas = render_organic_bubble_text(w, h, text_lines, font_size=font_size, y_offset=text_y_pos, line_spacing=line_spacing)
    
    # 3. Alpha composite
    result = Image.alpha_composite(im, text_canvas)
    return result

def craft_map_icon(src_path):
    im = Image.open(src_path).convert("RGBA")
    w, h = im.size
    
    # In 3279.png, the text "地图" sits on the earthen bank between y=38 and y=62, x=22 to x=54
    # Let's restore the earthen bank texture seamlessly
    pix = im.load()
    earth_col = (156, 74, 30, 255)
    earth_dark = (118, 52, 22, 255)
    
    # Clear old characters
    for y in range(40, 62):
        for x in range(20, 56):
            if pix[x, y][3] > 0:
                # Fill with natural earth gradient
                mix = (y - 40) / 22.0
                r = int(earth_col[0] * (1 - mix) + earth_dark[0] * mix)
                g = int(earth_col[1] * (1 - mix) + earth_dark[1] * mix)
                b = int(earth_col[2] * (1 - mix) + earth_dark[2] * mix)
                pix[x, y] = (r, g, b, 255)
                
    # Now draw "BẢN ĐỒ" with golden-brown bubble style
    text_layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(text_layer)
    font = get_font(12, bold=True)
    
    text = "BẢN ĐỒ"
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    tx = (w - tw) // 2 - 4
    ty = 42
    
    # Halo / glow
    for dx in range(-3, 4):
        for dy in range(-3, 4):
            if dx*dx + dy*dy <= 9:
                draw.text((tx + dx, ty + dy), text, font=font, fill=(255, 215, 0, 255))
    # Dark brown stroke
    for dx in range(-2, 3):
        for dy in range(-2, 3):
            if dx*dx + dy*dy <= 4:
                draw.text((tx + dx, ty + dy), text, font=font, fill=(90, 25, 10, 255))
    # White face
    draw.text((tx, ty), text, font=font, fill=(255, 255, 255, 255))
    
    return Image.alpha_composite(im, text_layer)

def craft_topui_82(src_path):
    im = Image.open(src_path).convert("RGBA")
    w, h = im.size
    # Clear text inside wooden plaque (x: 10 to 74, y: 7 to 25)
    pix = im.load()
    board_bg = (255, 252, 230, 255)
    for y in range(7, 26):
        for x in range(10, 75):
            pix[x, y] = board_bg
            
    draw = ImageDraw.Draw(im)
    font = get_font(10, bold=True)
    text = "QUÀ TẶNG"
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    tx = (w - tw) // 2
    ty = (h - th) // 2 - 1
    
    # Warm brown stroke
    for dx in range(-1, 2):
        for dy in range(-1, 2):
            draw.text((tx + dx, ty + dy), text, font=font, fill=(180, 80, 20, 255))
    draw.text((tx, ty), text, font=font, fill=(120, 40, 10, 255))
    return im

def craft_topui_366(src_path):
    im = Image.open(src_path).convert("RGBA")
    w, h = im.size
    # Clear text area y >= 38
    pix = im.load()
    for y in range(38, h):
        for x in range(w):
            pix[x, y] = (0, 0, 0, 0)
            
    text_canvas = render_organic_bubble_text(w, h, ["GIA VIÊN MỚI"], font_size=10, y_offset=42)
    return Image.alpha_composite(im, text_canvas)

def main():
    out_dir = Path("work/icon_candidates")
    out_dir.mkdir(parents=True, exist_ok=True)
    
    print("=== CRAFTING AUTHENTIC ICON CANDIDATES ===")
    
    # 1. Map Icon 3279.png
    map_cand = craft_map_icon("work/audit_images/ui/3279.png")
    map_cand.save(out_dir / "3279_bando.png")
    print("  [OK] 3279_bando.png")
    
    # 2. Action Icons (6834 / 6836)
    # Option A: Stacked "ĐỘNG" / "TÁC" (large readable font 9)
    act_a = craft_icon_candidate("work/audit_images/ui/6834.png", ["ĐỘNG", "TÁC"], font_size=9, y_clear_start=24, text_y_pos=24, line_spacing=-2)
    act_a.save(out_dir / "6834_dongtac_stacked.png")
    # Option B: "CỬ CHỈ" (single line font 8.5)
    act_b = craft_icon_candidate("work/audit_images/ui/6834.png", ["CỬ CHỈ"], font_size=8.5, y_clear_start=25, text_y_pos=30)
    act_b.save(out_dir / "6834_cuchi.png")
    # Option C: "ĐỘNG TÁC" (compact font 7.5 bold)
    act_c = craft_icon_candidate("work/audit_images/ui/6834.png", ["ĐỘNG TÁC"], font_size=7.5, y_clear_start=25, text_y_pos=30)
    act_c.save(out_dir / "6834_dongtac_inline.png")
    
    # Larger state 6836
    act_36 = craft_icon_candidate("work/audit_images/ui/6836.png", ["ĐỘNG", "TÁC"], font_size=10, y_clear_start=26, text_y_pos=26, line_spacing=-2)
    act_36.save(out_dir / "6836_dongtac.png")
    print("  [OK] 6834 / 6836 Action variants")
    
    # 3. Throw / Bullseye (6839 / 6841) -> "NÉM"
    throw_39 = craft_icon_candidate("work/audit_images/ui/6839.png", ["NÉM"], font_size=11, y_clear_start=25, text_y_pos=28)
    throw_39.save(out_dir / "6839_nem.png")
    throw_41 = craft_icon_candidate("work/audit_images/ui/6841.png", ["NÉM"], font_size=12, y_clear_start=27, text_y_pos=30)
    throw_41.save(out_dir / "6841_nem.png")
    print("  [OK] 6839 / 6841 Ném")
    
    # 4. Backpack (6844 / 6846) -> "BA LÔ" and "TÚI ĐỒ"
    bag_a = craft_icon_candidate("work/audit_images/ui/6844.png", ["BA LÔ"], font_size=9.5, y_clear_start=25, text_y_pos=29)
    bag_a.save(out_dir / "6844_balo.png")
    bag_b = craft_icon_candidate("work/audit_images/ui/6844.png", ["TÚI ĐỒ"], font_size=8.5, y_clear_start=25, text_y_pos=29)
    bag_b.save(out_dir / "6844_tuido.png")
    bag_46 = craft_icon_candidate("work/audit_images/ui/6846.png", ["BA LÔ"], font_size=10.5, y_clear_start=27, text_y_pos=31)
    bag_46.save(out_dir / "6846_balo.png")
    print("  [OK] 6844 / 6846 Backpack variants")
    
    # 5. Friends (6849 / 6851) -> "BẠN BÈ"
    fr_49 = craft_icon_candidate("work/audit_images/ui/6849.png", ["BẠN BÈ"], font_size=8.5, y_clear_start=24, text_y_pos=28)
    fr_49.save(out_dir / "6849_banbe.png")
    fr_51 = craft_icon_candidate("work/audit_images/ui/6851.png", ["BẠN BÈ"], font_size=9.5, y_clear_start=26, text_y_pos=30)
    fr_51.save(out_dir / "6851_banbe.png")
    print("  [OK] 6849 / 6851 Bạn bè")
    
    # 6. Angel (6854 / 6856) -> "THIÊN SỨ"
    angel_54 = craft_icon_candidate("work/audit_images/ui/6854.png", ["THIÊN SỨ"], font_size=7.5, y_clear_start=25, text_y_pos=29)
    angel_54.save(out_dir / "6854_thiensu.png")
    angel_54_stack = craft_icon_candidate("work/audit_images/ui/6854.png", ["THIÊN", "SỨ"], font_size=9, y_clear_start=24, text_y_pos=24, line_spacing=-2)
    angel_54_stack.save(out_dir / "6854_thiensu_stack.png")
    angel_56 = craft_icon_candidate("work/audit_images/ui/6856.png", ["THIÊN SỨ"], font_size=8.5, y_clear_start=27, text_y_pos=31)
    angel_56.save(out_dir / "6856_thiensu.png")
    print("  [OK] 6854 / 6856 Thiên sứ")
    
    # 7. Homestead / Farm (6859 / 6861) -> "GIA VIÊN" and "VƯỜN"
    farm_59_a = craft_icon_candidate("work/audit_images/ui/6859.png", ["GIA VIÊN"], font_size=7.5, y_clear_start=23, text_y_pos=26)
    farm_59_a.save(out_dir / "6859_giavien.png")
    farm_59_b = craft_icon_candidate("work/audit_images/ui/6859.png", ["VƯỜN"], font_size=10.5, y_clear_start=23, text_y_pos=26)
    farm_59_b.save(out_dir / "6859_vuon.png")
    farm_61 = craft_icon_candidate("work/audit_images/ui/6861.png", ["GIA VIÊN"], font_size=8.5, y_clear_start=24, text_y_pos=28)
    farm_61.save(out_dir / "6861_giavien.png")
    print("  [OK] 6859 / 6861 Gia viên")
    
    # 8. Shop (6864 / 6866) -> "SHOP" and "TIỆM"
    shop_64_a = craft_icon_candidate("work/audit_images/ui/6864.png", ["SHOP"], font_size=10, y_clear_start=23, text_y_pos=26)
    shop_64_a.save(out_dir / "6864_shop.png")
    shop_64_b = craft_icon_candidate("work/audit_images/ui/6864.png", ["TIỆM"], font_size=10, y_clear_start=23, text_y_pos=26)
    shop_64_b.save(out_dir / "6864_tiem.png")
    shop_66 = craft_icon_candidate("work/audit_images/ui/6866.png", ["SHOP"], font_size=11, y_clear_start=25, text_y_pos=28)
    shop_66.save(out_dir / "6866_shop.png")
    print("  [OK] 6864 / 6866 Shop")
    
    # 9. House / Home (6929 / 6931) -> "NHÀ Ở"
    house_29 = craft_icon_candidate("work/audit_images/ui/6929.png", ["NHÀ Ở"], font_size=9, y_clear_start=25, text_y_pos=29)
    house_29.save(out_dir / "6929_nhao.png")
    house_31 = craft_icon_candidate("work/audit_images/ui/6931.png", ["NHÀ Ở"], font_size=10, y_clear_start=27, text_y_pos=31)
    house_31.save(out_dir / "6931_nhao.png")
    print("  [OK] 6929 / 6931 Nhà ở")
    
    # 10. TopUI 82 -> "QUÀ TẶNG"
    topui_82 = craft_topui_82("work/audit_images/topUI/82.png")
    topui_82.save(out_dir / "topui_82_quatang.png")
    print("  [OK] topui_82_quatang.png")
    
    # 11. TopUI 366 -> "GIA VIÊN MỚI"
    topui_366 = craft_topui_366("work/audit_images/topUI/366.png")
    topui_366.save(out_dir / "topui_366_giavienmoi.png")
    print("  [OK] topui_366_giavienmoi.png")
    
    print("\n=== ALL ICON CANDIDATES CRAFTED SUCCESSFULLY! ===")

if __name__ == "__main__":
    main()
