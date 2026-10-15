import os
from PIL import Image, ImageDraw, ImageFont

BOARD_PATH = 'work/login_candidates/login_comparison_board.png'

items = [
    ('1. Nút BẮT ĐẦU (LoginHome - btn_start_168)',
     'work/audit_original_comparison/168_start_orig.png',
     'scratch/localized_assets/btn_start_168.png',
     'work/login_candidates/btn_start_168.png'),

    ('2. Nút ĐĂNG NHẬP (Login.swf - btn_login_173)',
     'work/audit_original_comparison/173_login_orig.png',
     'scratch/localized_assets/btn_login_173.png',
     'work/login_candidates/btn_login_173.png'),

    ('3. Chữ Đăng Ký (btn_reg_169 / Shape 158)',
     'work/audit_original_comparison/169_reg_orig.png',
     'scratch/localized_assets/btn_reg_169.png',
     'work/login_candidates/btn_reg_169.png'),

    ('4. Chữ Quên MK (btn_forgot_160 / Shape 161)',
     'work/audit_original_comparison/160_forgot_orig.png',
     'scratch/localized_assets/btn_forgot_160.png',
     'work/login_candidates/btn_forgot_160.png'),

    ('5. Chữ Đổi MK (btn_change_163 / Shape 164)',
     'work/audit_original_comparison/163_change_orig.png',
     'scratch/localized_assets/btn_change_163.png',
     'work/login_candidates/btn_change_163.png'),

    ('6. Chữ Bảo Mật (btn_protect_166 / Shape 167)',
     'work/audit_original_comparison/166_protect_orig.png',
     'scratch/localized_assets/btn_protect_166.png',
     'work/login_candidates/btn_protect_166.png'),

    ('7. Nút Xóa Lưu (btn_clear_109)',
     'work/audit_original_comparison/109_clear_orig.png',
     'scratch/localized_assets/btn_clear_109.png',
     'work/login_candidates/btn_clear_109.png'),

    ('8. Nút Tài Khoản Lưu (btn_system_174 / 176)',
     'work/audit_original_comparison/176_system_orig.png',
     'scratch/localized_assets/btn_system_176.png',
     'work/login_candidates/btn_system_176.png'),

    ('9. Bảng Giới Thiệu / Banner (randomMC_banner_3)',
     'work/audit_original_comparison/banner_3_orig.png',
     'scratch/localized_assets/randomMC_banner_3.png',
     'work/login_candidates/randomMC_banner_3.png'),

    ('10. Logo Moly VN (image_148)',
     'work/audit_original_comparison/image_148_orig.png',
     'scratch/localized_assets/image_148.png',
     'work/login_candidates/image_148.png'),
]

font_title = ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf', 26)
font_sec = ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf', 18)
font_header = ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf', 16)
font_label = ImageFont.truetype('C:/Windows/Fonts/arial.ttf', 14)

# Canvas dimensions
BOARD_W = 1200
# Calculate height dynamically
ROW_H_MAP = {
    0: 270,  # 168
    1: 235,  # 173
    2: 75,   # 169
    3: 75,   # 160
    4: 75,   # 163
    5: 75,   # 166
    6: 95,   # 109
    7: 95,   # 176
    8: 260,  # banner 3
    9: 220,  # image 148
}

total_h = 130 + sum(ROW_H_MAP[i] + 45 for i in range(len(items))) + 60
board = Image.new('RGBA', (BOARD_W, total_h), (24, 26, 31, 255))
draw = ImageDraw.Draw(board)

# Header Banner
draw.rectangle([0, 0, BOARD_W, 100], fill=(18, 20, 24, 255))
draw.text((BOARD_W // 2, 35), "BẢNG SO SÁNH NÚT & BANNER MÀN HÌNH ĐĂNG NHẬP (MOLY VN)",
          font=font_title, fill=(255, 215, 0, 255), anchor="mm")
draw.text((BOARD_W // 2, 75), "Đối chiếu: Bản Gốc Trung Quốc | Bản Tạm Cũ (Người dùng chụp) | Bản Mới Làm Lại Chuẩn Phong Cách",
          font=font_label, fill=(200, 210, 225, 255), anchor="mm")

# Column X coordinates
COL1_X = 50    # Item Name
COL2_X = 360   # Original
COL3_X = 630   # Old Flat
COL4_X = 900   # New Authentic

# Table Header
y = 115
draw.rectangle([30, y - 5, BOARD_W - 30, y + 25], fill=(35, 39, 47, 255))
draw.text((COL1_X, y), "THÀNH PHẦN", font=font_header, fill=(255, 220, 100, 255))
draw.text((COL2_X, y), "1. BẢN GỐC TRUNG", font=font_header, fill=(160, 200, 255, 255))
draw.text((COL3_X, y), "2. BẢN CŨ TẠM", font=font_header, fill=(255, 120, 120, 255))
draw.text((COL4_X, y), "3. BẢN MỚI LÀM LẠI (TO RÕ)", font=font_header, fill=(120, 255, 150, 255))

y += 40

for idx, (title, orig_p, curr_p, new_p) in enumerate(items):
    row_h = ROW_H_MAP[idx]
    
    # Row background
    bg_color = (28, 31, 38, 255) if idx % 2 == 0 else (22, 24, 29, 255)
    draw.rounded_rectangle([30, y - 5, BOARD_W - 30, y + row_h + 30], radius=8, fill=bg_color, outline=(50, 55, 65, 255))
    
    # Title
    draw.text((COL1_X, y + 10), title, font=font_sec, fill=(255, 255, 255, 255))
    
    # Process Images
    sub_y = y + 40
    for col_x, p, label in [(COL2_X, orig_p, "Gốc"), (COL3_X, curr_p, "Bản cũ"), (COL4_X, new_p, "Bản mới")]:
        if os.path.exists(p):
            im = Image.open(p)
            w, h = im.size
            
            # Bound image box
            max_w, max_h = 240, row_h - 15
            scale = min(max_w / max(1, w), max_h / max(1, h), 1.0)
            disp_w, disp_h = int(w * scale), int(h * scale)
            im_disp = im.resize((disp_w, disp_h), Image.Resampling.LANCZOS)
            
            # Checkerboard background for transparent areas
            box_x = col_x
            box_y = sub_y
            draw.rectangle([box_x, box_y, box_x + disp_w, box_y + disp_h], fill=(45, 48, 56, 255), outline=(70, 75, 88, 255))
            
            board.paste(im_disp, (box_x, box_y), im_disp if im_disp.mode == 'RGBA' else None)
            draw.text((box_x, box_y + disp_h + 4), f"{w}x{h} px", font=font_label, fill=(150, 160, 175, 255))
        else:
            draw.text((col_x, sub_y + 10), "Không có tệp", font=font_label, fill=(255, 80, 80, 255))
            
    y += row_h + 45

os.makedirs('work/login_candidates', exist_ok=True)
board.save(BOARD_PATH)
print(f"Comparison board created successfully at: {BOARD_PATH}")
