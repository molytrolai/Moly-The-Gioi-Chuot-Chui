import sys
from PIL import Image, ImageDraw, ImageFont

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

for name, path in [
    ("Arial Black", "C:/Windows/Fonts/ariblk.ttf"),
    ("Arial Bold", "C:/Windows/Fonts/arialbd.ttf"),
    ("Tahoma Bold", "C:/Windows/Fonts/tahomabd.ttf"),
    ("Segoe UI Bold", "C:/Windows/Fonts/segoeuib.ttf"),
]:
    f = ImageFont.truetype(path, 30)
    im = Image.new("RGBA", (150, 50), (255, 255, 255, 255))
    draw = ImageDraw.Draw(im)
    draw.text((10, 5), "BẠN", font=f, fill=(0, 0, 0, 255))
    im.save(f"work/test_{name.replace(' ', '_')}.png")
    print(f"Saved work/test_{name.replace(' ', '_')}.png")
