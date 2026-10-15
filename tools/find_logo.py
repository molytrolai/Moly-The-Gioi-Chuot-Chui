from pathlib import Path
from PIL import Image

def find_logo():
    # Search all exported shapes/images in work
    for f in Path("work").glob("**/*.png"):
        if "logo" in f.name.lower() or f.name in ["9.png", "29.png"]:
            try:
                im = Image.open(f)
                print(f, im.size)
            except:
                pass

if __name__ == "__main__":
    find_logo()
