import os
from pathlib import Path
from PIL import Image

def examine():
    # LoginHome checks
    lh_shapes = Path("work/exported/LoginHome_full/shapes")
    lh_images = Path("work/exported/LoginHome_full/images")
    
    print("--- LoginHome Images ---")
    for f in lh_images.glob("*.png"):
        print(f, Image.open(f).size)

    # Let's see what is inside LoginHome Shape 169
    # Where is the Start button in LoginHome? Let's check buttons/sprites!
    
if __name__ == "__main__":
    examine()
