import sys
from pathlib import Path
from PIL import Image

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

icon_files = [
    "work/audit_images/ui/3279.png",
    "work/audit_images/ui/6834.png",
    "work/audit_images/ui/6836.png",
    "work/audit_images/ui/6839.png",
    "work/audit_images/ui/6841.png",
    "work/audit_images/ui/6844.png",
    "work/audit_images/ui/6846.png",
    "work/audit_images/ui/6849.png",
    "work/audit_images/ui/6851.png",
    "work/audit_images/ui/6854.png",
    "work/audit_images/ui/6856.png",
    "work/audit_images/ui/6859.png",
    "work/audit_images/ui/6861.png",
    "work/audit_images/ui/6864.png",
    "work/audit_images/ui/6866.png",
    "work/audit_images/ui/6929.png",
    "work/audit_images/ui/6931.png",
    "work/audit_images/topUI/82.png",
    "work/audit_images/topUI/366.png"
]

for f in icon_files:
    p = Path(f)
    if not p.exists(): continue
    im = Image.open(p)
    w, h = im.size
    # Find where the golden/red text starts from the bottom
    text_y_start = h
    for y in range(h // 2, h):
        found = False
        for x in range(w):
            r, g, b, a = im.getpixel((x, y))
            # Golden yellow rgb(240, 180, 0) or red rgb(140, 20, 20)
            if a > 150 and ((r > 200 and g > 150 and b < 50) or (r > 100 and g < 40 and b < 40)):
                text_y_start = y
                found = True
                break
        if found:
            break
    print(f"{p.name} ({w}x{h}): Text starts around y={text_y_start} (height remaining: {h - text_y_start}px)")
