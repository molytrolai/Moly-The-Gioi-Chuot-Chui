import os
from PIL import Image

def analyze_topui():
    topui_dir = "work/audit_images/topUI"
    for f in sorted(os.listdir(topui_dir)):
        if f.endswith(".png"):
            p = os.path.join(topui_dir, f)
            im = Image.open(p)
            print(f"{f}: size={im.size}")

if __name__ == "__main__":
    analyze_topui()
