import sys
from pathlib import Path
from PIL import Image

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

images = [
    "work/audit_images/ui/6808.png",
    "work/audit_images/ui/6810.png",
    "work/audit_images/ui/6939.png",
    "work/audit_images/ui/6946.png",
    "work/audit_images/ui/6948.png",
    "work/audit_images/topUI/78.png",
    "work/audit_images/topUI/98.png",
    "work/audit_images/topUI/99.png",
    "work/audit_images/Login/71.png",
    "work/audit_images/Login/72.png",
]

for img in images:
    p = Path(img)
    if p.exists():
        im = Image.open(p)
        print(f"{p.name} in {p.parent.name}: {im.size}, mode={im.mode}")
