import os
from PIL import Image, ImageDraw, ImageFont

def get_font(size):
    for p in ["C:/Windows/Fonts/tahomabd.ttf", "C:/Windows/Fonts/segoeuib.ttf"]:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()

def build_topui_361():
    # 361.png is 100x100
    src = Image.open("work/audit_images/topUI/361.png").convert("RGBA")
    w, h = src.size
    
    # Text region is y=56 to 76.
    # The ribbon has red background.
    # We can clean the text region and redraw a neat banner with "HOẠT HÌNH" or "XEM PHIM"
    scale = 4
    W, H = w * scale, h * scale
    
    # Clean Chinese text in original
    cleaned = src.copy()
    pix = cleaned.load()
    for y in range(55, 78):
        for x in range(w):
            r, g, b, a = pix[x, y]
            # Chinese text is white/light pixels
            if a > 0 and (r > 200 and g > 200 and b > 200):
                # Replace with the surrounding red banner color (e.g. 210, 30, 40)
                pix[x, y] = (218, 32, 45, 255)
                
    # Now render bold Vietnamese text "HOẠT HÌNH"
    font = get_font(int(10.5 * scale))
    text_canvas = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    tdraw = ImageDraw.Draw(text_canvas)
    
    text = "HOẠT HÌNH"
    bbox = tdraw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    
    tx = (W - tw) // 2
    ty = int(58 * scale)
    
    # White text with subtle dark red stroke for contrast
    stroke_r = int(1.2 * scale)
    for dx in range(-stroke_r, stroke_r + 1):
        for dy in range(-stroke_r, stroke_r + 1):
            if dx*dx + dy*dy <= stroke_r * stroke_r:
                tdraw.text((tx + dx, ty + dy), text, font=font, fill=(120, 10, 20, 255))
    tdraw.text((tx, ty), text, font=font, fill=(255, 255, 255, 255))
    
    text_small = text_canvas.resize((w, h), Image.Resampling.LANCZOS)
    res = Image.alpha_composite(cleaned, text_small)
    res.save("work/icon_candidates/topui_361_hoathinh.png")
    print("Saved work/icon_candidates/topui_361_hoathinh.png")

def build_topui_82():
    # 82.png is (84, 31)
    src = Image.open("work/audit_images/topUI/82.png").convert("RGBA")
    w, h = src.size
    
    # Clean the inner yellow board (around x=12..72, y=6..25)
    cleaned = src.copy()
    pix = cleaned.load()
    board_color = (254, 241, 196, 255) # cream yellow of board
    for y in range(7, 24):
        for x in range(12, 73):
            r, g, b, a = pix[x, y]
            if a > 0:
                # Text is dark brown/orange
                pix[x, y] = (253, 240, 192, 255)
                
    scale = 4
    W, H = w * scale, h * scale
    
    # Version A: "QUÀ TẶNG" (large and clear)
    font_a = get_font(int(10.5 * scale))
    canvas_a = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw_a = ImageDraw.Draw(canvas_a)
    text_a = "QUÀ TẶNG"
    bbox_a = draw_a.textbbox((0, 0), text_a, font=font_a)
    ta_w = bbox_a[2] - bbox_a[0]
    tx_a = (W - ta_w) // 2
    ty_a = int(8.5 * scale)
    draw_a.text((tx_a, ty_a), text_a, font=font_a, fill=(160, 80, 20, 255))
    res_a = Image.alpha_composite(cleaned, canvas_a.resize((w, h), Image.Resampling.LANCZOS))
    res_a.save("work/icon_candidates/topui_82_quatang_clean.png")
    
    # Version B: "QUÀ TUẦN"
    font_b = get_font(int(9.5 * scale))
    canvas_b = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw_b = ImageDraw.Draw(canvas_b)
    text_b = "QUÀ TUẦN"
    bbox_b = draw_b.textbbox((0, 0), text_b, font=font_b)
    tb_w = bbox_b[2] - bbox_b[0]
    tx_b = (W - tb_w) // 2
    ty_b = int(9.0 * scale)
    draw_b.text((tx_b, ty_b), text_b, font=font_b, fill=(160, 80, 20, 255))
    res_b = Image.alpha_composite(cleaned, canvas_b.resize((w, h), Image.Resampling.LANCZOS))
    res_b.save("work/icon_candidates/topui_82_quatuan.png")
    print("Saved topui_82 versions")

build_topui_361()
build_topui_82()
