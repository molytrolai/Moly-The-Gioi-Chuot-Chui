import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

test_str = "BẠN BÈ ĐỘNG TÁC TÚI ĐỒ BẢN ĐỒ THIÊN SỨ GIA VIÊN"
fonts = [
    ("Arial Bold", "C:/Windows/Fonts/arialbd.ttf"),
    ("Tahoma Bold", "C:/Windows/Fonts/tahomabd.ttf"),
    ("Segoe UI Bold", "C:/Windows/Fonts/segoeuib.ttf"),
    ("Arial Black", "C:/Windows/Fonts/ariblk.ttf"),
]

for name, path in fonts:
    f = ImageFont.truetype(path, 20)
    im = Image.new("RGBA", (500, 50), (255, 255, 255, 255))
    draw = ImageDraw.Draw(im)
    draw.text((10, 10), test_str, font=f, fill=(0, 0, 0, 255))
    bbox = draw.textbbox((10, 10), test_str, font=f)
    print(f"Font {name}: renders width {bbox[2]-bbox[0]}px")
