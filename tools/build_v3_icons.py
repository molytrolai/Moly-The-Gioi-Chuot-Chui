import os
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

def get_font_supersampled(size, bold=True):
    font_paths = [
        "C:/Windows/Fonts/tahomabd.ttf",     # Tahoma Bold (100% full Vietnamese support)
        "C:/Windows/Fonts/segoeuib.ttf",     # Segoe UI Bold
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
    W = w * scale
    H = h * scale
    font_size = int(base_font_size * scale)
    y_ptr = int(y_offset * scale)
    spacing = int(line_spacing * scale)
    
    font = get_font_supersampled(font_size, bold=True)
    
    dummy_draw = ImageDraw.Draw(Image.new("RGBA", (1, 1)))
    line_infos = []
    for line in text_lines:
        bbox = dummy_draw.textbbox((0, 0), line, font=font)
        lw = bbox[2] - bbox[0]
        lh = bbox[3] - bbox[1]
        line_infos.append((line, lw, lh))
        
    # Layer 1: Golden Halo Glow (r=3.2)
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
        
    # Layer 2: Deep Crimson / Burgundy Stroke (r=1.8)
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
        
    full_hi = Image.alpha_composite(halo_canvas, stroke_canvas)
    full_hi = Image.alpha_composite(full_hi, face_canvas)
    return full_hi.resize((w, h), Image.Resampling.LANCZOS)

def clean_original_text_smart(src_im, clear_threshold_y):
    im = src_im.copy().convert("RGBA")
    w, h = im.size
    pix = im.load()
    for y in range(clear_threshold_y, h):
        for x in range(w):
            r, g, b, a = pix[x, y]
            if a > 0:
                is_text = False
                # Original Chinese character strokes: white face, crimson stroke, yellow/golden glow
                if r > 210 and g > 210 and b > 210:
                    is_text = True
                elif r > 110 and g < 45 and b < 45:
                    is_text = True
                elif r > 210 and g > 150 and b < 50:
                    is_text = True
                elif y > clear_threshold_y + 3:
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

def cutout_ai_image(img_path, target_size):
    if not os.path.exists(img_path):
        return None
    im = Image.open(img_path).convert("RGBA")
    w, h = im.size
    pix = im.load()
    for y in range(h):
        for x in range(w):
            r, g, b, a = pix[x, y]
            if r > 235 and g > 235 and b > 235:
                dx = x - w // 2
                dy = y - h // 2
                if (dx*dx + dy*dy) ** 0.5 > w * 0.38:
                    pix[x, y] = (0, 0, 0, 0)
    bbox = im.getbbox()
    if bbox:
        im = im.crop(bbox)
    return im.resize(target_size, Image.Resampling.LANCZOS)

def main():
    out_dir = Path("work/icon_candidates")
    out_dir.mkdir(parents=True, exist_ok=True)
    
    print("=== REBUILDING ALL CANDIDATES WITH EXACT PIXEL-PERFECT BOUNDS ===")
    
    # 1. 3279 Map
    # Option 1: AI Master Island
    # Option 2: Authentic Golden Glow
    build_icon("work/audit_images/ui/3279.png", ["BẢN ĐỒ"], base_font_size=10, clear_y=42, text_y=42).save(out_dir / "3279_bando.png")
    
    # 2. 6834 / 6836 Action
    act_ai = cutout_ai_image(r"C:\Users\Admin\.gemini\antigravity-ide\brain\ae93fb41-d50f-40d1-b4ba-8a7e00a730ac\moly_action_icon_1791969934263.jpg", (36, 51))
    if act_ai:
        act_ai.save(out_dir / "6834_dongtac_ai.png")
    build_icon("work/audit_images/ui/6834.png", ["ĐỘNG", "TÁC"], base_font_size=8.5, clear_y=33, text_y=28, line_spacing=-3).save(out_dir / "6834_dongtac_v3.png")
    build_icon("work/audit_images/ui/6834.png", ["ĐỘNG TÁC"], base_font_size=7.2, clear_y=33, text_y=34).save(out_dir / "6834_dongtac_inline_v3.png")
    build_icon("work/audit_images/ui/6836.png", ["ĐỘNG", "TÁC"], base_font_size=9.5, clear_y=36, text_y=31, line_spacing=-3).save(out_dir / "6836_dongtac_v3.png")
    
    # 3. 6839 / 6841 Throw -> "NÉM"
    build_icon("work/audit_images/ui/6839.png", ["NÉM"], base_font_size=10.5, clear_y=33, text_y=33).save(out_dir / "6839_nem_v3.png")
    build_icon("work/audit_images/ui/6841.png", ["NÉM"], base_font_size=11.5, clear_y=36, text_y=36).save(out_dir / "6841_nem_v3.png")
    
    # 4. 6844 / 6846 Backpack -> "TÚI ĐỒ" & "BA LÔ"
    bag_ai = cutout_ai_image(r"C:\Users\Admin\.gemini\antigravity-ide\brain\ae93fb41-d50f-40d1-b4ba-8a7e00a730ac\moly_backpack_icon_1791969963126.jpg", (39, 50))
    if bag_ai:
        bag_ai.save(out_dir / "6844_tuido_ai.png")
    build_icon("work/audit_images/ui/6844.png", ["TÚI ĐỒ"], base_font_size=8.5, clear_y=33, text_y=33).save(out_dir / "6844_tuido_v3.png")
    build_icon("work/audit_images/ui/6844.png", ["BA LÔ"], base_font_size=9.5, clear_y=33, text_y=33).save(out_dir / "6844_balo_v3.png")
    build_icon("work/audit_images/ui/6846.png", ["TÚI ĐỒ"], base_font_size=9.5, clear_y=36, text_y=36).save(out_dir / "6846_tuido_v3.png")
    
    # 5. 6849 / 6851 Friends -> "BẠN BÈ" (100% full mole smile)
    build_icon("work/audit_images/ui/6849.png", ["BẠN BÈ"], base_font_size=8.0, clear_y=32, text_y=32).save(out_dir / "6849_banbe_v3.png")
    build_icon("work/audit_images/ui/6851.png", ["BẠN BÈ"], base_font_size=9.0, clear_y=35, text_y=35).save(out_dir / "6851_banbe_v3.png")
    
    # 6. 6854 / 6856 Angel -> "THIÊN SỨ"
    build_icon("work/audit_images/ui/6854.png", ["THIÊN SỨ"], base_font_size=7.2, clear_y=33, text_y=34).save(out_dir / "6854_thiensu_v3.png")
    build_icon("work/audit_images/ui/6854.png", ["THIÊN", "SỨ"], base_font_size=8.5, clear_y=33, text_y=29, line_spacing=-3).save(out_dir / "6854_thiensu_stack_v3.png")
    build_icon("work/audit_images/ui/6856.png", ["THIÊN SỨ"], base_font_size=8.2, clear_y=36, text_y=37).save(out_dir / "6856_thiensu_v3.png")
    
    # 7. 6859 / 6861 Homestead -> "GIA VIÊN" & "VƯỜN"
    build_icon("work/audit_images/ui/6859.png", ["GIA VIÊN"], base_font_size=7.8, clear_y=30, text_y=30).save(out_dir / "6859_giavien_v3.png")
    build_icon("work/audit_images/ui/6859.png", ["VƯỜN"], base_font_size=10.0, clear_y=30, text_y=30).save(out_dir / "6859_vuon_v3.png")
    build_icon("work/audit_images/ui/6861.png", ["GIA VIÊN"], base_font_size=8.8, clear_y=32, text_y=32).save(out_dir / "6861_giavien_v3.png")
    
    # 8. 6864 / 6866 Shop -> "SHOP" & "CỬA HÀNG"
    build_icon("work/audit_images/ui/6864.png", ["SHOP"], base_font_size=10.0, clear_y=31, text_y=30).save(out_dir / "6864_shop_v3.png")
    build_icon("work/audit_images/ui/6864.png", ["CỬA HÀNG"], base_font_size=6.2, clear_y=31, text_y=32).save(out_dir / "6864_cuahang_v3.png")
    build_icon("work/audit_images/ui/6866.png", ["SHOP"], base_font_size=11.0, clear_y=34, text_y=33).save(out_dir / "6866_shop_v3.png")
    
    # 9. 6929 / 6931 House -> "NHÀ Ở"
    build_icon("work/audit_images/ui/6929.png", ["NHÀ Ở"], base_font_size=9.0, clear_y=33, text_y=33).save(out_dir / "6929_nhao_v3.png")
    build_icon("work/audit_images/ui/6931.png", ["NHÀ Ở"], base_font_size=10.0, clear_y=36, text_y=36).save(out_dir / "6931_nhao_v3.png")
    
    print("=== PIXEL-PERFECT CANDIDATES REGENERATED! ===")

if __name__ == "__main__":
    main()
