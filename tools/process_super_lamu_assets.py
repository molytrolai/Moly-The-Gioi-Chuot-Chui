#!/usr/bin/env python3
"""Tool to process, auto-remove background, resize, and compose Super Lamu assets for game integration.

Usage:
  python tools/process_super_lamu_assets.py --input-dir scratch/raw_lamu --output-dir chinh_sua_icon_game/19_dau_dau_sieu_cap_moi
"""

import sys
import shutil
from pathlib import Path
from PIL import Image, ImageDraw, ImageOps

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "scratch" / "raw_lamu"
OUTPUT_DIR = ROOT / "chinh_sua_icon_game" / "19_dau_dau_sieu_cap_moi"

def remove_background_auto(img: Image.Image) -> Image.Image:
    """Tự động tách nền: thử rembg trước, nếu chưa cài thì dùng bóc tách màu nền trắng/đen."""
    try:
        import rembg
        return rembg.remove(img)
    except ImportError:
        # Fallback tách nền thông minh dựa trên màu biên (border sampling)
        img = img.convert("RGBA")
        datas = img.getdata()
        
        # Lấy mẫu màu góc trên bên trái làm màu nền
        corner_color = img.getpixel((0, 0))
        cr, cg, cb, ca = corner_color
        
        new_data = []
        for item in datas:
            r, g, b, a = item
            # Nếu màu rất gần với màu nền góc (dung sai 25 đơn vị)
            if abs(r - cr) < 28 and abs(g - cg) < 28 and abs(b - cb) < 28:
                new_data.append((255, 255, 255, 0))
            else:
                new_data.append(item)
                
        img.putdata(new_data)
        return img

def process_single_species(raw_image_path: Path, species_id: int, species_name: str):
    """Xử lý tạo đủ 4 tệp cho 1 chủng loài từ 1 ảnh thô."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    prefix = f"{species_id:02d}_{species_name}"
    
    img = Image.open(raw_image_path)
    img_transparent = remove_background_auto(img)
    
    # 1. Tệp toàn thân 512x512
    bbox = img_transparent.getbbox()
    if bbox:
        cropped = img_transparent.crop(bbox)
        # Giữ tỉ lệ và căn giữa vào khung 512x512
        cropped.thumbnail((470, 470), Image.Resampling.LANCZOS)
        fullbody_512 = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
        offset_x = (512 - cropped.width) // 2
        offset_y = (512 - cropped.height) // 2
        fullbody_512.paste(cropped, (offset_x, offset_y), cropped)
        full_path = OUTPUT_DIR / f"{prefix}_toan_than_512.png"
        fullbody_512.save(full_path, "PNG")
        print(f"  ✓ Đã xuất: {full_path.name}")
        
        # 2. Tệp huy hiệu 128x128
        badge_128 = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
        badge_thumb = cropped.copy()
        badge_thumb.thumbnail((110, 110), Image.Resampling.LANCZOS)
        bx = (128 - badge_thumb.width) // 2
        by = (128 - badge_thumb.height) // 2
        badge_128.paste(badge_thumb, (bx, by), badge_thumb)
        badge_path = OUTPUT_DIR / f"{prefix}_huy_hieu_128.png"
        badge_128.save(badge_path, "PNG")
        print(f"  ✓ Đã xuất: {badge_path.name}")

def compose_lineup_showcase():
    """Ghép 6 chủng loài thành 1 bảng Lineup Showcase 16:9 (1920x1080)."""
    fullbody_files = sorted(OUTPUT_DIR.glob("*_toan_than_512.png"))
    if len(fullbody_files) < 6:
        print(f"  [Thông báo] Hiện có {len(fullbody_files)}/6 ảnh toàn thân, chưa đủ để ghép Lineup.")
        return
        
    lineup = Image.new("RGBA", (1920, 1080), (15, 23, 42, 255))
    step = 1920 // 6
    for idx, f in enumerate(fullbody_files[:6]):
        sp = Image.open(f)
        sp.thumbnail((280, 280), Image.Resampling.LANCZOS)
        x = idx * step + (step - sp.width) // 2
        y = (1080 - sp.height) // 2
        lineup.paste(sp, (x, y), sp)
        
    out_lineup = OUTPUT_DIR / "master_showcase_lineup_16x9.png"
    lineup.save(out_lineup, "PNG")
    print(f"  ✓ Đã xuất bảng tổng hợp: {out_lineup.name} (1920x1080)")

def main():
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    raw_files = sorted(RAW_DIR.glob("*.*"))
    print("======================================================================")
    print("   BỘ CÔNG CỤ TỰ ĐỘNG TÁCH NỀN & XỬ LÝ ĐỒ HỌA ĐẬU ĐẬU SIÊU CẤP        ")
    print("======================================================================")
    if not raw_files:
        print(f"[*] Thư mục chờ ảnh thô: {RAW_DIR}")
        print("[*] Hãy lưu ảnh thô từ AI vào thư mục này để công cụ tự động tách nền và resize!")
        return

    species_names = ["hac_am", "vu_tru", "than_thoai", "bang_hoa", "co_khi", "toi_thuong"]
    for idx, f in enumerate(raw_files[:6]):
        sname = species_names[idx] if idx < len(species_names) else f"species_{idx+1}"
        process_single_species(f, idx + 1, sname)
        
    compose_lineup_showcase()
    print("======================================================================")

if __name__ == "__main__":
    main()
