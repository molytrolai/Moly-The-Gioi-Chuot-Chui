#!/usr/bin/env python3
"""High-Quality Cartoon & Pixel-Perfect Asset Generator for Server Selection, Login Dialogs, and Super Lamu VIP.

Creates authentic glossy cartoon assets with:
- Dark stroke outlines (thao tác viền chuẩn game)
- Inner 3D candy highlights & glossy reflections
- Rich Vietnamese typography with full diacritics
"""

import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT_DIR = Path(__file__).resolve().parents[1]
ASSETS_DIR = ROOT_DIR / "scratch" / "localized_assets"
ASSETS_DIR.mkdir(parents=True, exist_ok=True)

FONT_TAHOMA_BD = r"C:\Windows\Fonts\tahomabd.ttf"
FONT_ARIAL_BD = r"C:\Windows\Fonts\arialbd.ttf"
FONT_COMIC_BD = r"C:\Windows\Fonts\comicbd.ttf"

def draw_pill_button(w, h, text, font_size, primary_color, border_color, text_color=(255, 255, 255), stroke_color=(100, 30, 0), stroke_w=2):
    """Draw a glossy cartoon pill button with top highlight."""
    # Render at 2x resolution for super crisp anti-aliasing
    scale = 2
    sw, sh = w * scale, h * scale
    im = Image.new("RGBA", (sw, sh), (0, 0, 0, 0))
    draw = ImageDraw.Draw(im)
    r = sh // 2
    
    # Outer border
    draw.rounded_rectangle([2, 2, sw - 3, sh - 3], radius=r, fill=primary_color, outline=border_color, width=3 * scale)
    
    # Top highlight ellipse
    hl_h = int(sh * 0.45)
    hl_color = (255, 255, 255, 140)
    draw.rounded_rectangle([4 * scale, 3 * scale, sw - 4 * scale, hl_h], radius=r - 2, fill=hl_color)
    
    # Text
    try:
        font = ImageFont.truetype(FONT_TAHOMA_BD, font_size * scale)
    except:
        font = ImageFont.truetype(FONT_ARIAL_BD, font_size * scale)
        
    bbox = font.getbbox(text)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    tx = (sw - tw) // 2 - bbox[0]
    ty = (sh - th) // 2 - bbox[1] - 1 * scale
    
    # Text stroke
    for ox in range(-stroke_w * scale, stroke_w * scale + 1):
        for oy in range(-stroke_w * scale, stroke_w * scale + 1):
            if ox*ox + oy*oy <= (stroke_w * scale)**2:
                draw.text((tx + ox, ty + oy), text, font=font, fill=stroke_color)
    # Text fill
    draw.text((tx, ty), text, font=font, fill=text_color)
    
    # Downsample with Lanczos
    res = im.resize((w, h), Image.Resampling.LANCZOS)
    return res

def draw_glossy_rect_button(w, h, text, font_size, bg_top, bg_bot, border_color, text_color=(255, 255, 255), stroke_color=(100, 20, 0)):
    """Draw a candy rectangular button with rounded corners and gloss."""
    scale = 2
    sw, sh = w * scale, h * scale
    im = Image.new("RGBA", (sw, sh), (0, 0, 0, 0))
    draw = ImageDraw.Draw(im)
    r = 6 * scale
    
    # Vertical gradient
    for y in range(sh):
        t = y / sh
        r_c = int(bg_top[0] * (1 - t) + bg_bot[0] * t)
        g_c = int(bg_top[1] * (1 - t) + bg_bot[1] * t)
        b_c = int(bg_top[2] * (1 - t) + bg_bot[2] * t)
        draw.line([(r, y), (sw - r, y)], fill=(r_c, g_c, b_c, 255))
        
    # Outer stroke outline
    draw.rounded_rectangle([1, 1, sw - 2, sh - 2], radius=r, outline=border_color, width=3 * scale)
    
    # Top reflection
    draw.rounded_rectangle([3 * scale, 3 * scale, sw - 3 * scale, int(sh * 0.42)], radius=r - 1, fill=(255, 255, 255, 120))
    
    # Text
    try:
        font = ImageFont.truetype(FONT_TAHOMA_BD, font_size * scale)
    except:
        font = ImageFont.truetype(FONT_ARIAL_BD, font_size * scale)
        
    bbox = font.getbbox(text)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    tx = (sw - tw) // 2 - bbox[0]
    ty = (sh - th) // 2 - bbox[1] - 1 * scale
    
    st_w = 2 * scale
    for ox in range(-st_w, st_w + 1):
        for oy in range(-st_w, st_w + 1):
            if ox*ox + oy*oy <= st_w**2:
                draw.text((tx + ox, ty + oy), text, font=font, fill=stroke_color)
    draw.text((tx, ty), text, font=font, fill=text_color)
    
    return im.resize((w, h), Image.Resampling.LANCZOS)

def draw_server_title_banner(w=338, h=41):
    """Draw 'CHỌN MÁY CHỦ' 3D title with metallic bar backing."""
    scale = 2
    sw, sh = w * scale, h * scale
    im = Image.new("RGBA", (sw, sh), (0, 0, 0, 0))
    draw = ImageDraw.Draw(im)
    
    # Metallic translucent bar in the middle
    bar_y1 = int(sh * 0.3)
    bar_y2 = int(sh * 0.95)
    for y in range(bar_y1, bar_y2):
        t = (y - bar_y1) / (bar_y2 - bar_y1)
        val = int(80 + 100 * (1 - abs(t - 0.5) * 2))
        alpha = int(140 + 60 * (1 - abs(t - 0.5) * 2))
        draw.line([(0, y), (sw, y)], fill=(val, val, val + 20, alpha))
        
    text = "CHỌN MÁY CHỦ"
    try:
        font = ImageFont.truetype(FONT_COMIC_BD, 21 * scale)
    except:
        font = ImageFont.truetype(FONT_ARIAL_BD, 21 * scale)
        
    bbox = font.getbbox(text)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    tx = (sw - tw) // 2 - bbox[0]
    ty = (sh - th) // 2 - bbox[1] - 2 * scale
    
    # 3D Drop shadow
    for d in range(4 * scale, 0, -1):
        draw.text((tx, ty + d), text, font=font, fill=(180, 50, 0, 255))
        
    # White thick stroke
    st_w = 4 * scale
    for ox in range(-st_w, st_w + 1):
        for oy in range(-st_w, st_w + 1):
            if ox*ox + oy*oy <= st_w**2:
                draw.text((tx + ox, ty + oy), text, font=font, fill=(255, 255, 255, 255))
                
    # Orange candy fill
    draw.text((tx, ty), text, font=font, fill=(255, 140, 0, 255))
    
    return im.resize((w, h), Image.Resampling.LANCZOS)

def draw_flame_full(w=28, h=30):
    """Draw a burning flame icon with 'ĐẦY' text."""
    scale = 3
    sw, sh = w * scale, h * scale
    im = Image.new("RGBA", (sw, sh), (0, 0, 0, 0))
    draw = ImageDraw.Draw(im)
    
    # Outer flame points
    outer_poly = [
        (sw * 0.5, 0), (sw * 0.75, sh * 0.35), (sw * 0.95, sh * 0.25),
        (sw * 0.98, sh * 0.65), (sw * 0.85, sh * 0.95), (sw * 0.5, sh),
        (sw * 0.15, sh * 0.95), (sw * 0.02, sh * 0.65), (sw * 0.05, sh * 0.25),
        (sw * 0.25, sh * 0.35)
    ]
    draw.polygon(outer_poly, fill=(240, 40, 0, 255), outline=(255, 255, 255, 255))
    
    # Inner flame
    inner_poly = [
        (sw * 0.5, sh * 0.2), (sw * 0.7, sh * 0.45), (sw * 0.8, sh * 0.7),
        (sw * 0.5, sh * 0.9), (sw * 0.2, sh * 0.7), (sw * 0.3, sh * 0.45)
    ]
    draw.polygon(inner_poly, fill=(255, 220, 0, 255))
    
    # Text "ĐẦY"
    try:
        font = ImageFont.truetype(FONT_TAHOMA_BD, 10 * scale)
    except:
        font = ImageFont.truetype(FONT_ARIAL_BD, 10 * scale)
    text = "ĐẦY"
    bbox = font.getbbox(text)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    tx = (sw - tw) // 2 - bbox[0]
    ty = (sh - th) // 2 - bbox[1] + 2 * scale
    
    # Stroke
    for ox in [-2, -1, 0, 1, 2]:
        for oy in [-2, -1, 0, 1, 2]:
            draw.text((tx + ox, ty + oy), text, font=font, fill=(120, 0, 0, 255))
    draw.text((tx, ty), text, font=font, fill=(255, 255, 255, 255))
    
    return im.resize((w, h), Image.Resampling.LANCZOS)

def generate_all():
    print("Generating pixel-perfect server selection and UI assets...")
    
    # 1. Server Selection Shapes
    # Shape 221: 查看全部服务器 -> TẤT CẢ MÁY CHỦ (159x32 orange pill)
    btn_221 = draw_pill_button(159, 32, "TẤT CẢ MÁY CHỦ", 13, (255, 120, 0), (255, 220, 50), text_color=(255, 255, 255), stroke_color=(160, 40, 0))
    btn_221.save(ASSETS_DIR / "shape_221.png")
    
    # Shape 224: 返回推荐服务器 -> MÁY CHỦ ĐỀ XUẤT (159x32 pink pill)
    btn_224 = draw_pill_button(159, 32, "MÁY CHỦ ĐỀ XUẤT", 13, (240, 60, 150), (255, 200, 230), text_color=(255, 255, 255), stroke_color=(140, 10, 80))
    btn_224.save(ASSETS_DIR / "shape_224.png")
    
    # Shape 260: 选择服务器 -> CHỌN MÁY CHỦ (338x41)
    title_260 = draw_server_title_banner(338, 41)
    title_260.save(ASSETS_DIR / "shape_260.png")
    
    # Shape 265: 快速开始 -> VÀO NHANH (82x22)
    btn_265 = draw_pill_button(82, 22, "VÀO NHANH", 11, (220, 50, 140), (255, 255, 255), text_color=(255, 255, 255), stroke_color=(120, 10, 70))
    btn_265.save(ASSETS_DIR / "shape_265.png")
    
    # Shape 279: 满 -> ĐẦY (28x30 flame)
    flame_279 = draw_flame_full(28, 30)
    flame_279.save(ASSETS_DIR / "shape_279.png")
    
    # 2. Login Dialog Buttons
    # Shape 288 & 289: 确定 -> XÁC NHẬN (Red glossy)
    draw_glossy_rect_button(72, 33, "XÁC NHẬN", 11, (255, 80, 0), (200, 20, 0), (255, 255, 255), stroke_color=(100, 10, 0)).save(ASSETS_DIR / "shape_288.png")
    draw_glossy_rect_button(79, 36, "XÁC NHẬN", 12, (255, 100, 20), (220, 30, 0), (255, 255, 255), stroke_color=(100, 10, 0)).save(ASSETS_DIR / "shape_289.png")
    
    # Shape 291 & 292: 取消 -> HỦY (Blue glossy)
    draw_glossy_rect_button(72, 33, "HỦY", 12, (0, 160, 240), (0, 100, 200), (255, 255, 255), stroke_color=(0, 40, 100)).save(ASSETS_DIR / "shape_291.png")
    draw_glossy_rect_button(80, 35, "HỦY", 13, (30, 180, 255), (0, 120, 220), (255, 255, 255), stroke_color=(0, 40, 100)).save(ASSETS_DIR / "shape_292.png")
    
    # Shape 304 & 305: 马上登陆 -> ĐĂNG NHẬP (Red glossy)
    draw_glossy_rect_button(72, 33, "ĐĂNG NHẬP", 9, (255, 80, 0), (200, 20, 0), (255, 255, 255), stroke_color=(100, 10, 0)).save(ASSETS_DIR / "shape_304.png")
    draw_glossy_rect_button(79, 36, "ĐĂNG NHẬP", 10, (255, 100, 20), (220, 30, 0), (255, 255, 255), stroke_color=(100, 10, 0)).save(ASSETS_DIR / "shape_305.png")
    
    # Shape 307 & 308: 保存密码 -> LƯU MK (Blue glossy)
    draw_glossy_rect_button(72, 33, "LƯU MK", 11, (0, 160, 240), (0, 100, 200), (255, 255, 255), stroke_color=(0, 40, 100)).save(ASSETS_DIR / "shape_307.png")
    draw_glossy_rect_button(80, 35, "LƯU MK", 12, (30, 180, 255), (0, 120, 220), (255, 255, 255), stroke_color=(0, 40, 100)).save(ASSETS_DIR / "shape_308.png")
    
    # Large End-Of-Login Buttons
    # Shape 378 & 381: 查看帮助 -> XEM TRỢ GIÚP (153x58)
    draw_glossy_rect_button(153, 58, "XEM TRỢ GIÚP", 16, (0, 180, 255), (0, 110, 220), (255, 255, 255), stroke_color=(0, 50, 120)).save(ASSETS_DIR / "shape_378.png")
    draw_glossy_rect_button(152, 58, "XEM TRỢ GIÚP", 16, (30, 200, 255), (0, 130, 240), (255, 255, 255), stroke_color=(0, 50, 120)).save(ASSETS_DIR / "shape_381.png")
    
    # Shape 385: 重新登陆 -> ĐĂNG NHẬP LẠI (148x57)
    draw_glossy_rect_button(148, 57, "ĐĂNG NHẬP LẠI", 15, (255, 100, 0), (210, 30, 0), (255, 255, 255), stroke_color=(120, 20, 0)).save(ASSETS_DIR / "shape_385.png")
    
    # Shape 389: 进入游戏 -> VÀO GAME (148x57)
    draw_glossy_rect_button(148, 57, "VÀO GAME", 18, (255, 110, 0), (210, 30, 0), (255, 255, 255), stroke_color=(120, 20, 0)).save(ASSETS_DIR / "shape_389.png")
    
    # Shape 393: 修改密码 -> ĐỔI MẬT KHẨU (148x57)
    draw_glossy_rect_button(148, 57, "ĐỔI MẬT KHẨU", 15, (0, 180, 255), (0, 110, 220), (255, 255, 255), stroke_color=(0, 50, 120)).save(ASSETS_DIR / "shape_393.png")
    
    # 3. Super Lamu VIP Buttons for ui.swf (153x26 golden glossy pills)
    # 5864: 超级拉姆GOGO购 -> MUA SẮM SUPER LA MỖ
    draw_pill_button(153, 26, "MUA SẮM SUPER LA MỖ", 10, (255, 140, 0), (255, 230, 80), stroke_color=(140, 40, 0)).save(ASSETS_DIR / "ui_5864.png")
    
    # 5868: 超级拉姆特权 -> ĐẶC QUYỀN SUPER LA MỖ
    draw_pill_button(153, 26, "ĐẶC QUYỀN SUPER LA MỖ", 10, (255, 140, 0), (255, 230, 80), stroke_color=(140, 40, 0)).save(ASSETS_DIR / "ui_5868.png")
    
    # 5872: 我要超级拉姆 -> TÔI MUỐN SUPER LA MỖ
    draw_pill_button(153, 26, "TÔI MUỐN SUPER LA MỖ", 10, (255, 140, 0), (255, 230, 80), stroke_color=(140, 40, 0)).save(ASSETS_DIR / "ui_5872.png")
    
    # 5876: 召唤超级拉姆 -> TRIỆU HỒI SUPER LA MỖ
    draw_pill_button(153, 26, "TRIỆU HỒI SUPER LA MỖ", 10, (255, 140, 0), (255, 230, 80), stroke_color=(140, 40, 0)).save(ASSETS_DIR / "ui_5876.png")
    
    # 5881: 超级拉姆大礼包 -> QUÀ LỚN SUPER LA MỖ
    draw_pill_button(153, 26, "QUÀ LỚN SUPER LA MỖ", 10, (255, 140, 0), (255, 230, 80), stroke_color=(140, 40, 0)).save(ASSETS_DIR / "ui_5881.png")
    
    print(f"Successfully generated all 18 pixel-perfect cartoon assets in {ASSETS_DIR}!")

if __name__ == "__main__":
    generate_all()
