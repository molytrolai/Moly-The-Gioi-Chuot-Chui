import os
import sys
from PIL import Image, ImageDraw, ImageFont

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

def get_font(size, bold=True):
    paths = [
        "C:/Windows/Fonts/tahomabd.ttf",
        "C:/Windows/Fonts/segoeuib.ttf",
        "C:/Windows/Fonts/arialbd.ttf"
    ]
    for p in paths:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                pass
    return ImageFont.load_default()

def make_comparison_sheet():
    # Items to compare:
    # 1. 3279: Bản đồ (Map)
    # 2. 6834: Động tác (Action)
    # 3. 6839: Ném (Throw)
    # 4. 6844: Túi đồ / Ba lô (Backpack)
    # 5. 6849: Bạn bè (Friends)
    # 6. 6854: Thiên sứ (Angel)
    # 7. 6859: Gia viên / Vườn (Homestead)
    # 8. 6864: Shop / Cửa hàng (Shop)
    # 9. 6929: Nhà ở (House)
    # 10. TopUI 82: Quà tặng (Gift)
    # 11. TopUI 361: Hoạt hình (Animation)
    # 12. TopUI 366: Gia viên mới (New Homestead)
    
    items = [
        {
            "id": "3279",
            "name": "BẢN ĐỒ (Map)",
            "orig": "work/audit_images/ui/3279.png",
            "old_badge": "scratch/localized_assets/ui_3279.png",
            "cand_1": "work/icon_candidates/3279_bando_ai.png",
            "cand_1_lbl": "Option 1: 3D AI Master Island",
            "cand_2": "work/icon_candidates/3279_bando.png",
            "cand_2_lbl": "Option 2: Authentic Golden Glow",
        },
        {
            "id": "6834",
            "name": "ĐỘNG TÁC (Action)",
            "orig": "work/audit_images/ui/6834.png",
            "old_badge": "scratch/localized_assets/ui_6834.png",
            "cand_1": "work/icon_candidates/6834_dongtac_v3.png",
            "cand_1_lbl": "Option 1: 2 Tầng 'ĐỘNG/TÁC'",
            "cand_2": "work/icon_candidates/6834_dongtac_ai.png",
            "cand_2_lbl": "Option 2: 3D AI Jumping Mole",
        },
        {
            "id": "6839",
            "name": "NÉM (Throw)",
            "orig": "work/audit_images/ui/6839.png",
            "old_badge": "scratch/localized_assets/ui_6839.png",
            "cand_1": "work/icon_candidates/6839_nem_v3.png",
            "cand_1_lbl": "Option 1: Chữ Lớn 'NÉM' (11pt)",
            "cand_2": "work/icon_candidates/6841_nem_v3.png",
            "cand_2_lbl": "Hover State (6841)",
        },
        {
            "id": "6844",
            "name": "TÚI ĐỒ / BA LÔ (Bag)",
            "orig": "work/audit_images/ui/6844.png",
            "old_badge": "scratch/localized_assets/ui_6844.png",
            "cand_1": "work/icon_candidates/6844_tuido_v3.png",
            "cand_1_lbl": "Option 1: 'TÚI ĐỒ' Chuẩn Game",
            "cand_2": "work/icon_candidates/6844_balo_v3.png",
            "cand_2_lbl": "Option 2: 'BA LÔ' Chữ To",
        },
        {
            "id": "6849",
            "name": "BẠN BÈ (Friends)",
            "orig": "work/audit_images/ui/6849.png",
            "old_badge": "scratch/localized_assets/ui_6849.png",
            "cand_1": "work/icon_candidates/6849_banbe_v3.png",
            "cand_1_lbl": "Option 1: 'BẠN BÈ' Giữ Nụ Cười",
            "cand_2": "work/icon_candidates/6851_banbe_v3.png",
            "cand_2_lbl": "Hover State (6851)",
        },
        {
            "id": "6854",
            "name": "THIÊN SỨ (Angel)",
            "orig": "work/audit_images/ui/6854.png",
            "old_badge": "scratch/localized_assets/ui_6854.png",
            "cand_1": "work/icon_candidates/6854_thiensu_v3.png",
            "cand_1_lbl": "Option 1: Ngang 'THIÊN SỨ'",
            "cand_2": "work/icon_candidates/6854_thiensu_stack_v3.png",
            "cand_2_lbl": "Option 2: 2 Tầng 'THIÊN/SỨ'",
        },
        {
            "id": "6859",
            "name": "GIA VIÊN (Homestead)",
            "orig": "work/audit_images/ui/6859.png",
            "old_badge": "scratch/localized_assets/ui_6859.png",
            "cand_1": "work/icon_candidates/6859_giavien_v3.png",
            "cand_1_lbl": "Option 1: 'GIA VIÊN' Chuẩn Gốc",
            "cand_2": "work/icon_candidates/6859_vuon_v3.png",
            "cand_2_lbl": "Option 2: 'VƯỜN' Chữ Cực Rõ",
        },
        {
            "id": "6864",
            "name": "SHOP (Store)",
            "orig": "work/audit_images/ui/6864.png",
            "old_badge": "scratch/localized_assets/ui_6864.png",
            "cand_1": "work/icon_candidates/6864_shop_v3.png",
            "cand_1_lbl": "Option 1: 'SHOP' Phong Cách Cute",
            "cand_2": "work/icon_candidates/6864_cuahang_v3.png",
            "cand_2_lbl": "Option 2: 'CỬA HÀNG'",
        },
        {
            "id": "6929",
            "name": "NHÀ Ở (House)",
            "orig": "work/audit_images/ui/6929.png",
            "old_badge": "scratch/localized_assets/ui_6929.png",
            "cand_1": "work/icon_candidates/6929_nhao_v3.png",
            "cand_1_lbl": "Option 1: 'NHÀ Ở' 3D Viền Đỏ",
            "cand_2": "work/icon_candidates/6931_nhao_v3.png",
            "cand_2_lbl": "Hover State (6931)",
        },
        {
            "id": "topui_82",
            "name": "QUÀ TẶNG (Top Gift)",
            "orig": "work/audit_images/topUI/82.png",
            "old_badge": "scratch/localized_assets/topui_82.png",
            "cand_1": "work/icon_candidates/topui_82_quatang_clean.png",
            "cand_1_lbl": "Option 1: 'QUÀ TẶNG'",
            "cand_2": "work/icon_candidates/topui_82_quatuan.png",
            "cand_2_lbl": "Option 2: 'QUÀ TUẦN'",
        },
        {
            "id": "topui_361",
            "name": "HOẠT HÌNH (Animation)",
            "orig": "work/audit_images/topUI/361.png",
            "old_badge": "work/audit_images/topUI/361.png",
            "cand_1": "work/icon_candidates/topui_361_hoathinh.png",
            "cand_1_lbl": "Option 1: 'HOẠT HÌNH' Nơ Đỏ",
            "cand_2": "work/icon_candidates/topui_361_hoathinh.png",
            "cand_2_lbl": "Khử Sạch Chữ Trung",
        },
        {
            "id": "topui_366",
            "name": "GIA VIÊN MỚI (Cat Girl)",
            "orig": "work/audit_images/topUI/366.png",
            "old_badge": "scratch/localized_assets/topui_366.png",
            "cand_1": "work/icon_candidates/topui_366_giavienmoi.png",
            "cand_1_lbl": "Option 1: 'GIA VIÊN MỚI'",
            "cand_2": "work/icon_candidates/topui_366_giavienmoi.png",
            "cand_2_lbl": "Chữ Đỏ Nền Gỗ",
        },
    ]

    # Grid layout:
    # 12 rows, each row has:
    # Col 0: Title & Info (width 180)
    # Col 1: Original Chinese (width 180)
    # Col 2: Old Temporary Badge (width 180)
    # Col 3: Candidate 1 (width 260)
    # Col 4: Candidate 2 (width 260)
    
    col_widths = [190, 170, 180, 280, 280]
    total_w = sum(col_widths)
    header_h = 60
    row_h = 135
    total_h = header_h + len(items) * row_h + 30
    
    sheet = Image.new("RGBA", (total_w, total_h), (24, 28, 36, 255))
    draw = ImageDraw.Draw(sheet)
    
    font_title = get_font(18, bold=True)
    font_header = get_font(12, bold=True)
    font_row_title = get_font(13, bold=True)
    font_label = get_font(11, bold=False)
    font_sub = get_font(10, bold=False)
    
    # Draw Sheet Header
    draw.rectangle([0, 0, total_w, header_h], fill=(15, 23, 42, 255))
    draw.text((20, 18), "BẢNG SO SÁNH ĐỐI CHIẾU ICON VIỆT HÓA THEO YÊU CẦU DUYỆT (MOLY VN)", fill=(255, 215, 0), font=font_title)
    
    # Column Headers
    headers = [
        "TÊN ICON & CHỨC NĂNG",
        "BẢN GỐC (TIẾNG TRUNG)",
        "BẢN TẠM CŨ (BADGE)",
        "ĐỀ XUẤT 1 (3D CUTE / AI)",
        "ĐỀ XUẤT 2 (LỰA CHỌN PHỤ)"
    ]
    
    hy = header_h - 22
    cx = 0
    for i, w in enumerate(col_widths):
        draw.text((cx + 12, hy), headers[i], fill=(148, 163, 184), font=font_header)
        cx += w
        
    draw.line([(0, header_h), (total_w, header_h)], fill=(51, 65, 85), width=2)
    
    # Draw Each Row
    for idx, item in enumerate(items):
        ry = header_h + idx * row_h
        bg_col = (30, 41, 59, 255) if idx % 2 == 0 else (24, 28, 36, 255)
        draw.rectangle([0, ry, total_w, ry + row_h], fill=bg_col)
        draw.line([(0, ry + row_h), (total_w, ry + row_h)], fill=(51, 65, 85), width=1)
        
        # Col 0: Name & Info
        draw.text((15, ry + 25), item["name"], fill=(255, 255, 255), font=font_row_title)
        draw.text((15, ry + 55), f"ID: {item['id']}", fill=(148, 163, 184), font=font_sub)
        draw.text((15, ry + 75), "Độ phân giải 2x zoom", fill=(100, 116, 139), font=font_sub)
        
        # Helper to draw icon box
        def draw_box(col_idx, img_path, label_text):
            box_x = sum(col_widths[:col_idx])
            box_w = col_widths[col_idx]
            
            # Label
            draw.text((box_x + 12, ry + 12), label_text, fill=(203, 213, 225), font=font_label)
            
            # Image Container
            cx_center = box_x + box_w // 2
            cy_center = ry + 75
            
            # draw dark inset box
            bx1 = cx_center - 55
            by1 = ry + 36
            bx2 = cx_center + 55
            by2 = ry + 116
            draw.rectangle([bx1, by1, bx2, by2], fill=(15, 23, 42, 255), outline=(71, 85, 105))
            
            if img_path and os.path.exists(img_path):
                try:
                    im = Image.open(img_path).convert("RGBA")
                    # Zoom factor: 2.0x (or 1.8x if large)
                    zoom = 2.0
                    if im.width > 60 or im.height > 60:
                        zoom = 1.2
                    tw = int(im.width * zoom)
                    th = int(im.height * zoom)
                    if tw > 100 or th > 72:
                        s = min(100 / tw, 72 / th)
                        tw = int(tw * s)
                        th = int(th * s)
                    im_scaled = im.resize((tw, th), Image.Resampling.NEAREST if zoom >= 1.5 else Image.Resampling.LANCZOS)
                    sheet.alpha_composite(im_scaled, (cx_center - tw // 2, cy_center - th // 2))
                except Exception as e:
                    draw.text((cx_center - 40, cy_center - 8), "Error", fill=(239, 68, 68), font=font_sub)
            else:
                draw.text((cx_center - 40, cy_center - 8), "Chưa có", fill=(100, 116, 139), font=font_sub)

        # Draw Columns
        draw_box(1, item["orig"], "Gốc tiếng Trung")
        draw_box(2, item["old_badge"], "Bản cũ (tạm)")
        draw_box(3, item["cand_1"], item["cand_1_lbl"])
        draw_box(4, item["cand_2"], item["cand_2_lbl"])

    out_sheet_path = "work/icon_candidates/comparison_sheet.png"
    sheet.save(out_sheet_path)
    print(f"Comparison sheet successfully generated at: {out_sheet_path} ({sheet.size})")

if __name__ == "__main__":
    make_comparison_sheet()
