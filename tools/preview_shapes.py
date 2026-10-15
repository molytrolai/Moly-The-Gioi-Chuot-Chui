from pathlib import Path
from PIL import Image

def make_contact_sheet():
    out_dir = Path("work/shape_previews")
    out_dir.mkdir(parents=True, exist_ok=True)
    
    # 1. Login
    for name in ["29", "123", "150", "157", "158", "161", "164", "167", "171", "174", "182", "187"]:
        p = Path(f"work/exported/Login_full/shapes/{name}.png")
        if p.exists():
            im = Image.open(p)
            im.save(out_dir / f"login_shape_{name}.png")
            print(f"login_shape_{name}.png: {im.size}")
            
    p148 = Path("work/exported/Login_full/images/148.png")
    if p148.exists():
        im = Image.open(p148)
        im.save(out_dir / "login_image_148.png")
        print(f"login_image_148.png: {im.size}")
        
    # 2. LoginHome
    for name in ["16", "171", "226", "236"]:
        p = Path(f"work/exported/LoginHome_full/images/{name}.png")
        if p.exists():
            im = Image.open(p)
            im.save(out_dir / f"loginhome_image_{name}.png")
            print(f"loginhome_image_{name}.png: {im.size}")

    for name in ["20", "55", "57", "58", "60", "62", "64", "66", "68", "169", "172", "174", "176", "178", "183", "184", "186", "202", "203", "205", "207", "209", "211", "213", "228"]:
        p = Path(f"work/exported/LoginHome_full/shapes/{name}.png")
        if p.exists():
            im = Image.open(p)
            im.save(out_dir / f"loginhome_shape_{name}.png")
            print(f"loginhome_shape_{name}.png: {im.size}")

if __name__ == "__main__":
    make_contact_sheet()
