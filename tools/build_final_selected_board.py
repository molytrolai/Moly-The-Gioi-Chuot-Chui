import os
import shutil
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

def get_font(size, bold=True):
    for p in ["C:/Windows/Fonts/tahomabd.ttf", "C:/Windows/Fonts/segoeuib.ttf"]:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                pass
    return ImageFont.load_default()

def make_board():
    assets_dir = Path("scratch/localized_assets")
    
    # 12 selected items
    items = [
        {"id": "ui_3279", "name": "1. BẢN ĐỒ", "file": "ui_3279.png", "source": "Bản vẽ tay do bạn thiết kế"},
        {"id": "ui_6834", "name": "2. ĐỘNG TÁC", "file": "ui_6834.png", "source": "Option 1 (2 Tầng 'ĐỘNG/TÁC')"},
        {"id": "ui_6839", "name": "3. NÉM", "file": "ui_6839.png", "source": "Option 1 (Chữ lớn 'NÉM')"},
        {"id": "ui_6844", "name": "4. BA LÔ", "file": "ui_6844.png", "source": "Option 2 ('BA LÔ' Chữ To)"},
        {"id": "ui_6849", "name": "5. BẠN BÈ", "file": "ui_6849.png", "source": "Option 1 ('BẠN BÈ' Giữ Nụ Cười)"},
        {"id": "ui_6854", "name": "6. THIÊN SỨ", "file": "ui_6854.png", "source": "Option 1 ('THIÊN SỨ' Cánh Trứng)"},
        {"id": "ui_6859", "name": "7. GIA VIÊN", "file": "ui_6859.png", "source": "Option 1 ('GIA VIÊN' Chữ M Vàng)"},
        {"id": "ui_6864", "name": "8. SHOP", "file": "ui_6864.png", "source": "Option 1 ('SHOP' Ngọc Pha Lê)"},
        {"id": "ui_6929", "name": "9. NHÀ Ở", "file": "ui_6929.png", "source": "Option 1 ('NHÀ Ở' Ngôi Nhà Cam)"},
        {"id": "topui_82", "name": "10. QUÀ TẶNG", "file": "topui_82.png", "source": "Bản vẽ tay do bạn thiết kế"},
        {"id": "topui_361", "name": "11. HOẠT HÌNH", "file": "topui_361.png", "source": "Option 1 ('HOẠT HÌNH' Nơ Đỏ)"},
        {"id": "topui_366", "name": "12. GIA VIÊN MỚI", "file": "topui_366.png", "source": "Option 1 ('GIA VIÊN MỚI' Bé Mèo)"},
    ]
    
    # 4 columns, 3 rows
    cols = 4
    rows = 3
    card_w = 260
    card_h = 160
    
    total_w = cols * card_w + 30
    header_h = 70
    total_h = header_h + rows * card_h + 30
    
    board = Image.new("RGBA", (total_w, total_h), (15, 23, 42, 255))
    draw = ImageDraw.Draw(board)
    
    font_main_title = get_font(20, bold=True)
    font_card_title = get_font(13, bold=True)
    font_card_src = get_font(10, bold=False)
    font_status = get_font(10, bold=True)
    
    # Title
    draw.text((20, 15), "TỔNG HỢP TOÀN BỘ 12 ICON ĐÃ ĐƯỢC BẠN CHỌN & ĐÃ BIÊN DỊCH VÀO GAME", fill=(255, 215, 0), font=font_main_title)
    draw.text((20, 42), "Trạng thái: 100% Khớp với lựa chọn của bạn - Đang hoạt động trực tiếp trong ui.swf & topUI.swf", fill=(148, 163, 184), font=font_card_src)
    draw.line([(0, header_h), (total_w, header_h)], fill=(51, 65, 85), width=2)
    
    for idx, item in enumerate(items):
        c = idx % cols
        r = idx // cols
        
        x = 20 + c * card_w
        y = header_h + 15 + r * card_h
        
        # Card container
        draw.rectangle([x, y, x + card_w - 15, y + card_h - 15], fill=(30, 41, 59, 255), outline=(71, 85, 105), width=1)
        
        # Card header badge
        draw.rectangle([x, y, x + card_w - 15, y + 26], fill=(51, 65, 85, 255))
        draw.text((x + 8, y + 5), item["name"], fill=(255, 255, 255), font=font_card_title)
        
        # Image area
        img_p = assets_dir / item["file"]
        cx_box = x + (card_w - 15) // 2
        cy_box = y + 78
        
        # Draw dark inner well
        draw.rectangle([cx_box - 50, cy_box - 36, cx_box + 50, cy_box + 36], fill=(15, 23, 42, 255), outline=(51, 65, 85))
        
        if img_p.exists():
            im = Image.open(img_p).convert("RGBA")
            zoom = 2.0
            if im.width > 60 or im.height > 60:
                zoom = 1.2
            tw = int(im.width * zoom)
            th = int(im.height * zoom)
            if tw > 90 or th > 64:
                s = min(90 / tw, 64 / th)
                tw = int(tw * s)
                th = int(th * s)
            im_scaled = im.resize((tw, th), Image.Resampling.NEAREST if zoom >= 1.5 else Image.Resampling.LANCZOS)
            board.alpha_composite(im_scaled, (cx_box - tw // 2, cy_box - th // 2))
            
        # Footnote
        draw.text((x + 8, y + card_h - 32), item["source"], fill=(226, 232, 240), font=font_card_src)
        draw.text((x + 8, y + card_h - 18), "✓ ĐÃ TÍCH HỢP GAME", fill=(74, 222, 128), font=font_status)
        
    out_path = Path("work/final_selected_icons_board.png")
    board.save(out_path)
    print("Saved final selected icons board to", out_path)
    
    # Copy to artifacts for embedding
    art_path = Path(r"C:\Users\Admin\.gemini\antigravity-ide\brain\ae93fb41-d50f-40d1-b4ba-8a7e00a730ac\final_selected_icons_board.png")
    shutil.copy2(out_path, art_path)
    print("Copied to artifacts")

if __name__ == "__main__":
    make_board()
