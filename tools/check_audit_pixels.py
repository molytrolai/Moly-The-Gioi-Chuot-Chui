import os
from PIL import Image

def examine_images(folder):
    print(f"=== Examining {folder} ===")
    for f in sorted(os.listdir(folder)):
        if not f.endswith(".png"): continue
        p = os.path.join(folder, f)
        im = Image.open(p).convert("RGBA")
        w, h = im.size
        # sample some colors or check if it looks like an icon
        pix = im.load()
        non_transparent = sum(1 for y in range(h) for x in range(w) if pix[x,y][3] > 10)
        print(f"  {f:12s} ({w:3d}x{h:3d}) non-transparent: {non_transparent:6d}/{w*h}")

examine_images("work/audit_images/topUI")
examine_images("work/audit_images/ui")
