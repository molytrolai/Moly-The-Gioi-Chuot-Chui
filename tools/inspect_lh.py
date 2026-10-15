import os
from pathlib import Path
from PIL import Image

def inspect_lh():
    lh_img = Path("work/exported/LoginHome_full/images")
    for f in lh_img.glob("*.*"):
        im = Image.open(f)
        print(f"LoginHome Image: {f.name}, size={im.size}, mode={im.mode}")
        
    lh_shapes = Path("work/exported/LoginHome_full/shapes")
    for sid in [169, 172, 174, 183, 184, 186, 202, 228]:
        p = lh_shapes / f"{sid}.png"
        if p.exists():
            im = Image.open(p)
            print(f"LoginHome Shape {sid}: size={im.size}")

if __name__ == "__main__":
    inspect_lh()
