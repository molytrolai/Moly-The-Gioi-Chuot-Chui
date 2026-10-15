import sys
from pathlib import Path
from PIL import Image

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

icon_files = [
    "work/audit_images/ui/3279.png",
    "work/audit_images/ui/6834.png",
    "work/audit_images/ui/6839.png",
    "work/audit_images/ui/6844.png",
    "work/audit_images/ui/6849.png",
    "work/audit_images/ui/6854.png",
    "work/audit_images/ui/6859.png",
    "work/audit_images/ui/6864.png",
    "work/audit_images/ui/6929.png",
]

for f in icon_files:
    p = Path(f)
    if not p.exists(): continue
    im = Image.open(p)
    w, h = im.size
    print(f"\n--- {p.name} ({w}x{h}) ---")
    
    # Sample colors in the bottom half (where text is)
    colors = {}
    for y in range(h // 2, h):
        for x in range(w):
            r, g, b, a = im.getpixel((x, y))
            if a > 50:
                # Group colors slightly
                key = (r // 10 * 10, g // 10 * 10, b // 10 * 10)
                colors[key] = colors.get(key, 0) + 1
    top_cols = sorted(colors.items(), key=lambda x: x[1], reverse=True)[:6]
    for c, count in top_cols:
        print(f"   Color rgb{c}: count={count}")
