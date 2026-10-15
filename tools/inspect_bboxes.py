from pathlib import Path
from PIL import Image

def inspect_pngs():
    lh_shapes = Path("work/exported/LoginHome_full/shapes")
    for f in sorted(lh_shapes.glob("*.png"), key=lambda x: int(x.stem) if x.stem.isdigit() else 0):
        im = Image.open(f)
        if im.width > 50 and im.height > 15:
            # Check bounding box of non-zero alpha
            bbox = im.getbbox()
            print(f"LoginHome Shape {f.name}: size={im.size}, bbox={bbox}")

    lg_shapes = Path("work/exported/Login_full/shapes")
    for f in sorted(lg_shapes.glob("*.png"), key=lambda x: int(x.stem) if x.stem.isdigit() else 0):
        im = Image.open(f)
        if im.width > 50 and im.height > 15:
            bbox = im.getbbox()
            print(f"Login Shape {f.name}: size={im.size}, bbox={bbox}")

if __name__ == "__main__":
    inspect_pngs()
