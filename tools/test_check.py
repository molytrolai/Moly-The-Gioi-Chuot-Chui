from pathlib import Path
from PIL import Image

def test():
    im148 = Image.open("work/exported/Login_full/images/148.png")
    print(f"Login Image 148: {im148.size}, {im148.mode}")
    im149 = Image.open("work/exported/Login_full/images/149.png")
    print(f"Login Image 149: {im149.size}, {im149.mode}")
    im150 = Image.open("work/exported/Login_full/shapes/150.png")
    print(f"Login Shape 150: {im150.size}")
    im171 = Image.open("work/exported/Login_full/shapes/171.png")
    print(f"Login Shape 171: {im171.size}")
    im182 = Image.open("work/exported/Login_full/shapes/182.png")
    print(f"Login Shape 182: {im182.size}")
    im187 = Image.open("work/exported/Login_full/shapes/187.png")
    print(f"Login Shape 187: {im187.size}")
    im123 = Image.open("work/exported/Login_full/shapes/123.png")
    print(f"Login Shape 123: {im123.size}")
    im157 = Image.open("work/exported/Login_full/shapes/157.png")
    print(f"Login Shape 157: {im157.size}")
    im29 = Image.open("work/exported/Login_full/shapes/29.png")
    print(f"Login Shape 29: {im29.size}")

if __name__ == "__main__":
    test()
