import os
from pathlib import Path
from PIL import Image

def scan_text_and_features():
    print("=== LOGINHOME IMAGES ===")
    p_lh_img = Path("work/exported/LoginHome_full/images")
    if p_lh_img.exists():
        for f in p_lh_img.glob("*.png"):
            im = Image.open(f)
            print(f"LoginHome Image {f.name}: {im.size}")

    print("\n=== LOGINHOME SHAPES (Key shapes) ===")
    p_lh_shapes = Path("work/exported/LoginHome_full/shapes")
    # Let's check some shapes: 20, 57, 58, 60, 62, 64, 66, 68, 172, 174, 176, 178, 183, 184, 186, 203, 205, 207, 209, 211, 213, 228
    for sid in [20, 55, 57, 58, 60, 62, 64, 66, 68, 169, 170, 172, 174, 176, 178, 183, 184, 186, 202, 203, 205, 207, 209, 211, 213, 228]:
        sf = p_lh_shapes / f"{sid}.png"
        if sf.exists():
            im = Image.open(sf)
            print(f"LoginHome Shape {sf.name}: size={im.size}")

    print("\n=== LOGIN IMAGES ===")
    p_lg_img = Path("work/exported/Login_full/images")
    if p_lg_img.exists():
        for f in p_lg_img.glob("*.png"):
            im = Image.open(f)
            print(f"Login Image {f.name}: {im.size}")

    print("\n=== LOGIN SHAPES ===")
    p_lg_shapes = Path("work/exported/Login_full/shapes")
    for sid in [29, 71, 72, 73, 123, 150, 157, 158, 161, 164, 167, 170, 171, 174, 180, 182, 185, 187, 190]:
        sf = p_lg_shapes / f"{sid}.png"
        if sf.exists():
            im = Image.open(sf)
            print(f"Login Shape {sf.name}: size={im.size}")

if __name__ == "__main__":
    scan_text_and_features()
