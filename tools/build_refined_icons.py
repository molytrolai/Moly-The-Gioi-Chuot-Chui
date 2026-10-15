import os
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

def get_font_supersampled(size, bold=True):
    font_paths = [
        "C:/Windows/Fonts/ariblk.ttf",       # Arial Black (extra bold, round)
        "C:/Windows/Fonts/seguiemb.ttf",     # Segoe UI Semibold
        "C:/Windows/Fonts/arialbd.ttf",      # Arial Bold
    ]
    for p in font_paths:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                pass
    return ImageFont.load_default()

def render_supersampled_bubble_text(w, h, text_lines, base_font_size=10, y_offset=26, scale=4, line_spacing=0):
    """
    Renders text at 4x resolution with 3-layer organic bubble contours:
    1. Outer Golden-Yellow Halo (rgb 255, 200, 0)
    2. Deep Crimson/Burgundy Stroke (rgb 145, 18, 18)
    3. Crisp White Face with top highlight (rgb 255, 255, 255)
    Then scales down with Lanczos for smooth, anti-aliased perfection.
    """
    W = w * scale
    H = h * scale
    font_size = int(base_font_size * scale)
    y_ptr = int(y_offset * scale)
    spacing = int(line_spacing * scale)
    
    font = get_font_supersampled(font_size, bold=True)
    
    # Measure lines
    dummy_draw = ImageDraw.Draw(Image.new("RGBA", (1, 1)))
    line_infos = []
    for line in text_lines:
        bbox = dummy_draw.textbbox((0, 0), line, font=font)
        lw = bbox[2] - bbox[0]
        lh = bbox[3] - bbox[1]
        line_infos.append((line, lw, lh))
        
    # Layer 1: Golden Halo (radius 10-12 at 4x)
    halo_canvas = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    halo_draw = ImageDraw.Draw(halo_canvas)
    r_halo = int(3.2 * scale)
    cur_y = y_ptr
    for line, lw, lh in line_infos:
        lx = (W - lw) // 2
        for dx in range(-r_halo, r_halo + 1):
            for dy in range(-r_halo, r_halo + 1):
                if dx*dx + dy*dy <= r_halo * r_halo:
                    halo_draw.text((lx + dx, cur_y + dy), line, font=font, fill=(255, 195, 0, 255))
        cur_y += lh + spacing
        
    # Layer 2: Deep Crimson Stroke (radius 6-8 at 4x)
    stroke_canvas = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    stroke_draw = ImageDraw.Draw(stroke_canvas)
    r_stroke = int(1.8 * scale)
    cur_y = y_ptr
    for line, lw, lh in line_infos:
        lx = (W - lw) // 2
        for dx in range(-r_stroke, r_stroke + 1):
            for dy in range(-r_stroke, r_stroke + 1):
                if dx*dx + dy*dy <= r_stroke * r_stroke:
                    stroke_draw.text((lx + dx, cur_y + dy), line, font=font, fill=(140, 18, 18, 255))
        cur_y += lh + spacing
        
    # Layer 3: Pure White Face
    face_canvas = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    face_draw = ImageDraw.Draw(face_canvas)
    cur_y = y_ptr
    for line, lw, lh in line_infos:
        lx = (W - lw) // 2
        face_draw.text((lx, cur_y), line, font=font, fill=(255, 255, 255, 255))
        cur_y += lh + spacing
        
    # Composite layers at 4x
    full_hi = Image.alpha_composite(halo_canvas, stroke_canvas)
    full_hi = Image.alpha_composite(full_hi, face_canvas)
    
    # Downscale with Lanczos
    return full_hi.resize((w, h), Image.Resampling.LANCZOS)

def clean_original_text_smart(src_im, clear_threshold_y):
    """
    Cleans out the Chinese text area while preserving upper character features (like chin, hands, smile).
    """
    im = src_im.copy().convert("RGBA")
    w, h = im.size
    pix = im.load()
    
    for y in range(clear_threshold_y, h):
        for x in range(w):
            r, g, b, a = pix[x, y]
            if a > 0:
                # Text pixels are white, red stroke, or golden halo
                is_text = False
                # White or near white
                if r > 210 and g > 210 and b > 210:
                    is_text = True
                # Deep red
                elif r > 100 and g < 50 and b < 50:
                    is_text = True
                # Golden yellow halo
                elif r > 200 and g > 150 and b < 60:
                    is_text = True
                # Near text bottom
                elif y > clear_threshold_y + 4:
                    is_text = True
                    
                if is_text:
                    pix[x, y] = (0, 0, 0, 0)
    return im

def build_icon(src_path, text_lines, base_font_size, clear_y, text_y, line_spacing=0):
    src = Image.open(src_path).convert("RGBA")
    w, h = src.size
    cleaned = clean_original_text_smart(src, clear_y)
    text_img = render_supersampled_bubble_text(w, h, text_lines, base_font_size=base_font_size, y_offset=text_y, line_spacing=line_spacing)
    return Image.alpha_composite(cleaned, text_img)

def process_map_candidate():
    # Process the high-res generated map image
    gen_path = Path(r"C:\Users\Admin\.gemini\antigravity-ide\brain\ae93fb41-d50f-40d1-b4ba-8a7e00a730ac\moly_map_candidate_1791969908213.jpg")
    if not gen_path.exists():
        return None
    im = Image.open(gen_path).convert("RGBA")
    
    # Cut out white checkered background
    pix = im.load()
    w, h = im.size
    # Flood-fill or transparency for background corners
    # Corner pixels are checkered background
    for y in range(h):
        for x in range(w):
            r, g, b, a = pix[x, y]
            # If checkered white/gray corner
            if r > 220 and g > 220 and b > 220:
                # Check distance from center
                dx = x - w // 2
                dy = y - h // 2
                dist = (dx*dx + dy*dy) ** 0.5
                if dist > w * 0.44:
                    pix[x, y] = (0, 0, 0, 0)
    # Crop to non-transparent bounding box
    bbox = im.getbbox()
    if bbox:
        im = im.crop(bbox)
        
    # Resize to exact SWF size (78, 66)
    im_swf = im.resize((78, 66), Image.Resampling.LANCZOS)
    return im_swf, im

def main():
    out_dir = Path("work/icon_candidates")
    out_dir.mkdir(parents=True, exist_ok=True)
    
    print("=== BUILDING REFINED HD ICON CANDIDATES ===")
    
    # 1. Map Icon (both AI generated version & enhanced original version)
    map_swf, map_hd = process_map_candidate()
    if map_swf:
        map_swf.save(out_dir / "3279_bando_ai.png")
        map_hd.save(out_dir / "3279_bando_ai_hd.png")
        print("  [OK] 3279_bando_ai.png (from generated image)")
        
    # 2. Action (6834 & 6836)
    build_icon("work/audit_images/ui/6834.png", ["ĐỘNG", "TÁC"], base_font_size=9, clear_y=26, text_y=24, line_spacing=-3).save(out_dir / "6834_dongtac_v2.png")
    build_icon("work/audit_images/ui/6836.png", ["ĐỘNG", "TÁC"], base_font_size=10, clear_y=28, text_y=26, line_spacing=-3).save(out_dir / "6836_dongtac_v2.png")
    # Also single line variant:
    build_icon("work/audit_images/ui/6834.png", ["ĐỘNG TÁC"], base_font_size=7.5, clear_y=26, text_y=30).save(out_dir / "6834_dongtac_inline_v2.png")
    print("  [OK] 6834 / 6836 Action")
    
    # 3. Throw (6839 & 6841) -> "NÉM"
    build_icon("work/audit_images/ui/6839.png", ["NÉM"], base_font_size=11, clear_y=26, text_y=27).save(out_dir / "6839_nem_v2.png")
    build_icon("work/audit_images/ui/6841.png", ["NÉM"], base_font_size=12, clear_y=28, text_y=29).save(out_dir / "6841_nem_v2.png")
    print("  [OK] 6839 / 6841 Ném")
    
    # 4. Backpack (6844 & 6846) -> "TÚI ĐỒ" and "BA LÔ"
    build_icon("work/audit_images/ui/6844.png", ["TÚI ĐỒ"], base_font_size=9, clear_y=26, text_y=28).save(out_dir / "6844_tuido_v2.png")
    build_icon("work/audit_images/ui/6844.png", ["BA LÔ"], base_font_size=10, clear_y=26, text_y=28).save(out_dir / "6844_balo_v2.png")
    build_icon("work/audit_images/ui/6846.png", ["TÚI ĐỒ"], base_font_size=10, clear_y=28, text_y=30).save(out_dir / "6846_tuido_v2.png")
    print("  [OK] 6844 / 6846 Backpack")
    
    # 5. Friends (6849 & 6851) -> "BẠN BÈ" (Notice clear_y=27 so smile is kept!)
    build_icon("work/audit_images/ui/6849.png", ["BẠN BÈ"], base_font_size=9, clear_y=27, text_y=28).save(out_dir / "6849_banbe_v2.png")
    build_icon("work/audit_images/ui/6851.png", ["BẠN BÈ"], base_font_size=10, clear_y=29, text_y=30).save(out_dir / "6851_banbe_v2.png")
    print("  [OK] 6849 / 6851 Bạn bè")
    
    # 6. Angel (6854 & 6856) -> "THIÊN SỨ"
    build_icon("work/audit_images/ui/6854.png", ["THIÊN SỨ"], base_font_size=7.5, clear_y=26, text_y=29).save(out_dir / "6854_thiensu_v2.png")
    build_icon("work/audit_images/ui/6854.png", ["THIÊN", "SỨ"], base_font_size=9, clear_y=26, text_y=24, line_spacing=-3).save(out_dir / "6854_thiensu_stack_v2.png")
    build_icon("work/audit_images/ui/6856.png", ["THIÊN SỨ"], base_font_size=8.5, clear_y=28, text_y=31).save(out_dir / "6856_thiensu_v2.png")
    print("  [OK] 6854 / 6856 Thiên sứ")
    
    # 7. Homestead / Farm (6859 & 6861) -> "GIA VIÊN" and "NÔNG TRẠI"
    build_icon("work/audit_images/ui/6859.png", ["GIA VIÊN"], base_font_size=8, clear_y=24, text_y=26).save(out_dir / "6859_giavien_v2.png")
    build_icon("work/audit_images/ui/6859.png", ["VƯỜN"], base_font_size=10.5, clear_y=24, text_y=26).save(out_dir / "6859_vuon_v2.png")
    build_icon("work/audit_images/ui/6861.png", ["GIA VIÊN"], base_font_size=9, clear_y=25, text_y=28).save(out_dir / "6861_giavien_v2.png")
    print("  [OK] 6859 / 6861 Gia viên")
    
    # 8. Shop (6864 & 6866) -> "SHOP"
    build_icon("work/audit_images/ui/6864.png", ["SHOP"], base_font_size=10.5, clear_y=24, text_y=26).save(out_dir / "6864_shop_v2.png")
    build_icon("work/audit_images/ui/6866.png", ["SHOP"], base_font_size=11.5, clear_y=26, text_y=28).save(out_dir / "6866_shop_v2.png")
    print("  [OK] 6864 / 6866 Shop")
    
    # 9. House (6929 & 6931) -> "NHÀ Ở"
    build_icon("work/audit_images/ui/6929.png", ["NHÀ Ở"], base_font_size=9.5, clear_y=26, text_y=28).save(out_dir / "6929_nhao_v2.png")
    build_icon("work/audit_images/ui/6931.png", ["NHÀ Ở"], base_font_size=10.5, clear_y=28, text_y=30).save(out_dir / "6931_nhao_v2.png")
    print("  [OK] 6929 / 6931 Nhà ở")
    
    print("\n=== ALL V2 CANDIDATES GENERATED SUCCESSFULLY! ===")

if __name__ == "__main__":
    main()
