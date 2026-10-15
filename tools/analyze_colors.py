from pathlib import Path
from PIL import Image

def analyze_pixels(name, path):
    im = Image.open(path).convert("RGBA")
    colors = im.getcolors(maxcolors=10000)
    # Check dominant colors
    print(f"\n[{name}] size={im.size}")
    if colors:
        sorted_colors = sorted(colors, key=lambda x: x[0], reverse=True)[:5]
        for count, col in sorted_colors:
            if col[3] > 0: # not transparent
                print(f"  color {col}: {count} px")

if __name__ == "__main__":
    p = Path("work/shape_previews")
    for f in sorted(p.glob("*.png")):
        analyze_pixels(f.name, f)
