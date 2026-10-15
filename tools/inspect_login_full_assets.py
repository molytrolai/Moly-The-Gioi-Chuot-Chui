import os
from pathlib import Path
from PIL import Image

def analyze_dir(base_dir):
    print(f"=== ANALYZING {base_dir} ===")
    p = Path(base_dir)
    images_dir = p / "images"
    shapes_dir = p / "shapes"
    texts_dir = p / "texts"
    
    if images_dir.exists():
        print(f"\n--- IMAGES ({len(list(images_dir.glob('*')))}) ---")
        for f in sorted(images_dir.glob("*.png"), key=lambda x: int(x.stem) if x.stem.isdigit() else 0):
            try:
                im = Image.open(f)
                print(f"Image {f.name}: size={im.size}, mode={im.mode}")
            except Exception as e:
                print(f"Image {f.name}: error {e}")
                
    if shapes_dir.exists():
        print(f"\n--- SHAPES ({len(list(shapes_dir.glob('*')))}) ---")
        for f in sorted(shapes_dir.glob("*.png"), key=lambda x: int(x.stem) if x.stem.isdigit() else 0):
            try:
                im = Image.open(f)
                # Print larger shapes that might be banners, buttons, text badges
                if im.width > 30 and im.height > 10:
                    print(f"Shape {f.name}: size={im.size}")
            except Exception as e:
                pass

    if texts_dir.exists():
        print(f"\n--- TEXTS ({len(list(texts_dir.glob('*')))}) ---")
        for f in sorted(texts_dir.glob("*.txt"), key=lambda x: int(x.stem) if x.stem.isdigit() else 0):
            try:
                txt = f.read_text(encoding="utf-8", errors="replace").strip()
                preview = txt.replace("\n", " ")[:60]
                print(f"Text {f.name}: {preview}")
            except Exception as e:
                pass

if __name__ == "__main__":
    analyze_dir("work/exported/LoginHome_full")
    analyze_dir("work/exported/Login_full")
