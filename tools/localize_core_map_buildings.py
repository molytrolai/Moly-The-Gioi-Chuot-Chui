#!/usr/bin/env python3
"""Localize Building Signboards and Architectural Textures for Core Map SWFs.

Draws authentic Vietnamese cartoon bubble signboards:
- Map 1 (Lâu Đài Moly): Map_10001.swf & 1.swf (chid: 5)
- Map 2 (Quảng Trường Ái Tâm): Map_10002.swf (chid: 57)
- Map 3 (Phố Mua Sắm Taotao): Map_10003.swf (chid: 4)
- Map 4 (Chân Núi Molylaya): Map_10004.swf (chid: 15)
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

JAVA_EXE = r"C:\Program Files\Microsoft\jdk-21.0.12.101-hotspot\bin\java.exe"
PROJECT_ROOT = Path(__file__).resolve().parents[1]
FFDEC_JAR = str(PROJECT_ROOT / "tools" / "ffdec-26.3.0" / "ffdec-cli.jar")

MIRROR_MAP = PROJECT_ROOT / "archive" / "clients" / "offline-mirror" / "mole.61.com" / "resource" / "map"
OVERRIDES_MAP = PROJECT_ROOT / "archive" / "clients" / "local-overrides" / "mole.61.com" / "resource" / "map"
OVERRIDES_MAP.mkdir(parents=True, exist_ok=True)

WORK_DIR = PROJECT_ROOT / "work" / "map_buildings"
WORK_DIR.mkdir(parents=True, exist_ok=True)

def get_font(size, bold=True):
    fonts = [
        "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/tahomabd.ttf" if bold else "C:/Windows/Fonts/tahoma.ttf",
        "C:/Windows/Fonts/segoeuib.ttf" if bold else "C:/Windows/Fonts/segoeui.ttf",
    ]
    for f in fonts:
        if os.path.exists(f):
            try:
                return ImageFont.truetype(f, size)
            except:
                pass
    return ImageFont.load_default()

def draw_bubble_text(draw, x, y, text, font, fill=(255, 255, 255, 255), stroke_fill=(70, 35, 10, 255), stroke_width=3):
    """Draws text with thick cartoon stroke outline."""
    for dx in range(-stroke_width, stroke_width + 1):
        for dy in range(-stroke_width, stroke_width + 1):
            if dx * dx + dy * dy <= stroke_width * stroke_width:
                draw.text((x + dx, y + dy), text, font=font, fill=stroke_fill)
    draw.text((x, y), text, font=font, fill=fill)

def draw_cute_plaque(im, box, text, font_size=15, fill_color=(245, 140, 20, 255), text_color=(255, 255, 255, 255), border_color=(70, 35, 10, 255), subtext=None):
    """Draws a cute rounded cartoon signboard with highlight and drop shadow."""
    draw = ImageDraw.Draw(im)
    x1, y1, x2, y2 = box
    w = x2 - x1
    h = y2 - y1
    r = min(h // 2, 14)
    
    # Shadow
    draw.rounded_rectangle([x1 + 3, y1 + 4, x2 + 3, y2 + 4], radius=r, fill=(0, 0, 0, 90))
    # Outer plaque
    draw.rounded_rectangle([x1, y1, x2, y2], radius=r, fill=fill_color, outline=border_color, width=3)
    # Glossy top highlight
    draw.rounded_rectangle([x1 + 3, y1 + 2, x2 - 3, y1 + h // 2], radius=r - 1, fill=(255, 255, 255, 90))
    
    # Text
    font = get_font(font_size, bold=True)
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    
    if subtext:
        tx = x1 + (w - tw) // 2
        ty = y1 + (h // 2 - th) // 2 + 1
        draw_bubble_text(draw, tx, ty, text, font, fill=text_color, stroke_fill=border_color, stroke_width=2)
        
        font_sub = get_font(font_size - 4, bold=True)
        sbbox = draw.textbbox((0, 0), subtext, font=font_sub)
        stw = sbbox[2] - sbbox[0]
        stx = x1 + (w - stw) // 2
        sty = y1 + h // 2 + 1
        draw_bubble_text(draw, stx, sty, subtext, font_sub, fill=(255, 250, 180, 255), stroke_fill=border_color, stroke_width=2)
    else:
        tx = x1 + (w - tw) // 2
        ty = y1 + (h - th) // 2 - 2
        draw_bubble_text(draw, tx, ty, text, font, fill=text_color, stroke_fill=border_color, stroke_width=3)

def process_map1():
    """Lâu Đài Moly (Map 1) - Tag 5 in Map_10001.swf & 1.swf"""
    src_img = PROJECT_ROOT / "work" / "exported" / "Map1" / "5.jpg"
    if not src_img.exists():
        return
    im = Image.open(src_img).convert("RGBA")
    
    # Grand Castle Arch Banner: x: 420..540, y: 245..280
    draw_cute_plaque(
        im,
        box=[416, 246, 544, 282],
        text="LÂU ĐÀI MOLY",
        font_size=15,
        fill_color=(255, 185, 25, 255),
        text_color=(255, 255, 255, 255),
        border_color=(120, 45, 0, 255)
    )
    
    out_jpg = WORK_DIR / "map1_bg_vi.jpg"
    im.convert("RGB").save(out_jpg, quality=95)
    print("  [Map 1] Rendered localized castle entrance signboard.")
    
    # Inject into Map_10001.swf and 1.swf
    for dst_name in ["Map_10001.swf", "1.swf"]:
        curr_swf = OVERRIDES_MAP / dst_name if (OVERRIDES_MAP / dst_name).exists() else MIRROR_MAP / dst_name
        tmp_swf = WORK_DIR / f"temp_{dst_name}"
        cmd = [JAVA_EXE, "-jar", FFDEC_JAR, "-replace", str(curr_swf), str(tmp_swf), "5", str(out_jpg)]
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode == 0:
            shutil.copy2(tmp_swf, OVERRIDES_MAP / dst_name)
            print(f"  [Map 1 OK] Injected into {dst_name}")

def process_map2():
    """Quảng Trường Ái Tâm (Map 2) - Tag 57 in Map_10002.swf"""
    src_img = PROJECT_ROOT / "work" / "exported" / "Map2" / "57.jpg"
    if not src_img.exists():
        return
    im = Image.open(src_img).convert("RGBA")
    
    # 1. Police Station (left): x: 125..225, y: 200..235
    draw_cute_plaque(
        im,
        box=[120, 202, 230, 236],
        text="CẢNH SÁT MOLY",
        font_size=12,
        fill_color=(35, 120, 230, 255),
        text_color=(255, 255, 255, 255),
        border_color=(10, 35, 90, 255)
    )
    
    # 2. Hospital / Rescue Clinic (center-left): x: 330..430, y: 155..190
    draw_cute_plaque(
        im,
        box=[325, 158, 435, 192],
        text="BỆNH VIỆN ÁI TÂM",
        font_size=11,
        fill_color=(235, 60, 60, 255),
        text_color=(255, 255, 255, 255),
        border_color=(110, 15, 15, 255)
    )
    
    # 3. Newspaper Office (center-right): x: 550..650, y: 175..210
    draw_cute_plaque(
        im,
        box=[545, 178, 655, 212],
        text="TÒA SOẠN BÁO",
        font_size=12,
        fill_color=(245, 150, 25, 255),
        text_color=(255, 255, 255, 255),
        border_color=(90, 40, 5, 255)
    )
    
    # 4. Post Office (right): x: 770..870, y: 195..230
    draw_cute_plaque(
        im,
        box=[765, 198, 875, 232],
        text="BƯU ĐIỆN MOLY",
        font_size=12,
        fill_color=(60, 175, 50, 255),
        text_color=(255, 255, 255, 255),
        border_color=(15, 75, 20, 255)
    )
    
    out_jpg = WORK_DIR / "map2_bg_vi.jpg"
    im.convert("RGB").save(out_jpg, quality=95)
    print("  [Map 2] Rendered 4 localized civic signboards.")
    
    curr_swf = OVERRIDES_MAP / "Map_10002.swf" if (OVERRIDES_MAP / "Map_10002.swf").exists() else MIRROR_MAP / "Map_10002.swf"
    tmp_swf = WORK_DIR / "temp_Map_10002.swf"
    cmd = [JAVA_EXE, "-jar", FFDEC_JAR, "-replace", str(curr_swf), str(tmp_swf), "57", str(out_jpg)]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode == 0:
        shutil.copy2(tmp_swf, OVERRIDES_MAP / "Map_10002.swf")
        print("  [Map 2 OK] Injected into Map_10002.swf")

def process_map3():
    """Phố Mua Sắm Taotao (Map 3) - Tag 4 in Map_10003.swf"""
    src_img = PROJECT_ROOT / "work" / "exported" / "Map3" / "4.jpg"
    if not src_img.exists():
        return
    im = Image.open(src_img).convert("RGBA")
    
    # 1. Props Store (Rainbow): x: 90..190, y: 145..185
    draw_cute_plaque(
        im,
        box=[85, 148, 195, 185],
        text="TIỆM ĐẠO CỤ",
        font_size=12,
        fill_color=(185, 70, 235, 255),
        text_color=(255, 255, 255, 255),
        border_color=(65, 15, 95, 255)
    )
    
    # 2. Fashion Clothes Store (Silk): x: 335..445, y: 120..160
    draw_cute_plaque(
        im,
        box=[330, 122, 450, 160],
        text="TIỆM THỜI TRANG",
        font_size=12,
        fill_color=(240, 80, 140, 255),
        text_color=(255, 255, 255, 255),
        border_color=(90, 15, 45, 255)
    )
    
    # 3. Lamu Pet Store: x: 575..675, y: 130..170
    draw_cute_plaque(
        im,
        box=[570, 132, 680, 170],
        text="TIỆM LA MỖ",
        font_size=13,
        fill_color=(85, 190, 40, 255),
        text_color=(255, 255, 255, 255),
        border_color=(25, 75, 10, 255)
    )
    
    # 4. Bank / Hua Shen Stand: x: 790..890, y: 185..225
    draw_cute_plaque(
        im,
        box=[785, 188, 895, 225],
        text="NGÂN HÀNG MOLY",
        font_size=11,
        fill_color=(255, 185, 20, 255),
        text_color=(255, 255, 255, 255),
        border_color=(105, 45, 0, 255)
    )
    
    out_jpg = WORK_DIR / "map3_bg_vi.jpg"
    im.convert("RGB").save(out_jpg, quality=95)
    print("  [Map 3] Rendered 4 localized Taotao shopping street signboards.")
    
    curr_swf = OVERRIDES_MAP / "Map_10003.swf" if (OVERRIDES_MAP / "Map_10003.swf").exists() else MIRROR_MAP / "Map_10003.swf"
    tmp_swf = WORK_DIR / "temp_Map_10003.swf"
    cmd = [JAVA_EXE, "-jar", FFDEC_JAR, "-replace", str(curr_swf), str(tmp_swf), "4", str(out_jpg)]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode == 0:
        shutil.copy2(tmp_swf, OVERRIDES_MAP / "Map_10003.swf")
        print("  [Map 3 OK] Injected into Map_10003.swf")

def process_map4():
    """Chân Núi Molylaya (Map 4) - Tag 15 in Map_10004.swf"""
    src_img = PROJECT_ROOT / "work" / "exported" / "Map4" / "15.jpg"
    if not src_img.exists():
        return
    im = Image.open(src_img).convert("RGBA")
    
    # 1. Ski resort cable car (left): x: 230..340, y: 220..255
    draw_cute_plaque(
        im,
        box=[225, 222, 345, 258],
        text="BÃI TRƯỢT TUYẾT",
        font_size=12,
        fill_color=(45, 155, 235, 255),
        text_color=(255, 255, 255, 255),
        border_color=(10, 45, 95, 255)
    )
    
    # 2. Hunter Cabin (right): x: 720..830, y: 225..260
    draw_cute_plaque(
        im,
        box=[715, 228, 835, 264],
        text="NHÀ THỢ SĂN M",
        font_size=12,
        fill_color=(175, 110, 50, 255),
        text_color=(255, 255, 255, 255),
        border_color=(65, 30, 5, 255)
    )
    
    out_jpg = WORK_DIR / "map4_bg_vi.jpg"
    im.convert("RGB").save(out_jpg, quality=95)
    print("  [Map 4] Rendered 2 localized snow mountain signboards.")
    
    curr_swf = OVERRIDES_MAP / "Map_10004.swf" if (OVERRIDES_MAP / "Map_10004.swf").exists() else MIRROR_MAP / "Map_10004.swf"
    tmp_swf = WORK_DIR / "temp_Map_10004.swf"
    cmd = [JAVA_EXE, "-jar", FFDEC_JAR, "-replace", str(curr_swf), str(tmp_swf), "15", str(out_jpg)]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode == 0:
        shutil.copy2(tmp_swf, OVERRIDES_MAP / "Map_10004.swf")
        print("  [Map 4 OK] Injected into Map_10004.swf")

def main():
    print("=" * 65)
    print(" LOCALIZING BUILDING SIGNBOARDS & TEXTURES (CORE MAPS 1, 2, 3, 4)")
    print("=" * 65)
    process_map1()
    process_map2()
    process_map3()
    process_map4()
    print("All core map building textures localized successfully!")

if __name__ == "__main__":
    main()
