import os
from pathlib import Path
from PIL import Image

def find_shapes():
    p = Path("work/exported/LoginHome_full/shapes")
    for f in sorted(p.glob("*.png"), key=lambda x: int(x.stem) if x.stem.isdigit() else 0):
        im = Image.open(f)
        # Check if shape contains colored pixels or text-like features
        # Let's inspect shapes with specific dimensions or inspect all significant ones
        print(f"LoginHome Shape {f.name}: size={im.size}")

if __name__ == "__main__":
    find_shapes()
