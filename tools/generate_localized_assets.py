import os
import sys
from PIL import Image, ImageDraw, ImageFont

def get_font(size, bold=True):
    font_paths = [
        'C:/Windows/Fonts/arialbd.ttf' if bold else 'C:/Windows/Fonts/arial.ttf',
        'C:/Windows/Fonts/tahomabd.ttf' if bold else 'C:/Windows/Fonts/tahoma.ttf',
        'C:/Windows/Fonts/segoeuib.ttf' if bold else 'C:/Windows/Fonts/segoeui.ttf',
    ]
    for p in font_paths:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                pass
    return ImageFont.load_default()

def draw_bubble_text(draw, x, y, text, font, fill, stroke_fill, stroke_width):
    for dx in range(-stroke_width, stroke_width + 1):
        for dy in range(-stroke_width, stroke_width + 1):
            if dx*dx + dy*dy <= stroke_width*stroke_width:
                draw.text((x + dx, y + dy), text, font=font, fill=stroke_fill)
    draw.text((x, y), text, font=font, fill=fill)

def create_logo_9():
    """Top-left Moly logo for 51moleInfo0.swf (346x180)"""
    w, h = 346, 180
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(im)

    font_main = get_font(56, bold=True)
    font_sub = get_font(16, bold=True)
    font_vn = get_font(13, bold=True)

    # 1. Main MOLY letters
    bbox_moly = draw.textbbox((0, 0), 'MOLY', font=font_main)
    moly_w = bbox_moly[2] - bbox_moly[0]
    moly_x = (w - moly_w) // 2 - 10
    moly_y = 12

    # Shadow & outline
    draw_bubble_text(draw, moly_x, moly_y, 'MOLY', font_main, (255, 245, 170, 255), (70, 35, 10, 255), 7)
    draw.text((moly_x + 2, moly_y + 2), 'MOLY', font=font_main, fill=(255, 255, 255, 240))

    # 2. Cute red mole nose on the 'O'
    # Letter 'M' is ~45px wide, 'O' starts around moly_x + 50
    nose_x = moly_x + 72
    nose_y = moly_y + 16
    nose_r = 16
    draw.ellipse([nose_x - nose_r - 3, nose_y - nose_r - 3, nose_x + nose_r + 3, nose_y + nose_r + 3], fill=(60, 15, 10, 255))
    draw.ellipse([nose_x - nose_r, nose_y - nose_r, nose_x + nose_r, nose_y + nose_r], fill=(235, 25, 25, 255))
    draw.ellipse([nose_x - 6, nose_y - 8, nose_x - 1, nose_y - 3], fill=(255, 255, 255, 240))

    # 3. Subtitle ribbon banner
    banner_w = 260
    banner_h = 36
    bx = (w - banner_w) // 2
    by = 92
    draw.rounded_rectangle([bx, by, bx + banner_w, by + banner_h], radius=14, fill=(245, 140, 20, 255), outline=(70, 35, 10, 255), width=3)
    draw.rounded_rectangle([bx + 3, by + 2, bx + banner_w - 3, by + banner_h // 2], radius=11, fill=(255, 200, 100, 150))
    sub_bbox = draw.textbbox((0, 0), 'THẾ GIỚI CHUỘT CHŨI', font=font_sub)
    sub_w = sub_bbox[2] - sub_bbox[0]
    draw_bubble_text(draw, bx + (banner_w - sub_w) // 2, by + 7, 'THẾ GIỚI CHUỘT CHŨI', font_sub, (255, 255, 255, 255), (70, 35, 10, 255), 2)

    # 4. VN badge
    vn_w = 48
    vn_h = 24
    vx = (w - vn_w) // 2
    vy = 136
    draw.rounded_rectangle([vx, vy, vx + vn_w, vy + vn_h], radius=7, fill=(225, 35, 35, 255), outline=(255, 255, 255, 255), width=2)
    vn_bbox = draw.textbbox((0, 0), 'VN', font=font_vn)
    vn_tw = vn_bbox[2] - vn_bbox[0]
    draw_bubble_text(draw, vx + (vn_w - vn_tw) // 2, vy + 4, 'VN', font_vn, (255, 255, 255, 255), (90, 10, 10, 255), 1)

    return im

def create_start_button():
    """LoginHome Start button 168 (222x258)"""
    # We can load the original 1_up.png as base to keep the outer glow & golden ring, and replace the text
    orig_path = 'data/decompiled/LoginHome/buttons/DefineButton2_168/1_up.png'
    if os.path.exists(orig_path):
        im = Image.open(orig_path).convert('RGBA')
    else:
        im = Image.new('RGBA', (222, 258), (0, 0, 0, 0))

    # Erase the center "开始" area (roughly circle around center (111, 129), radius ~50)
    draw = ImageDraw.Draw(im)
    # Redraw shiny central sphere
    cx, cy, r = 111, 129, 58
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(220, 25, 30, 255))
    # Inner radial gradient simulation
    draw.ellipse([cx - r + 8, cy - r + 8, cx + r - 8, cy + r - 8], fill=(245, 60, 50, 255))
    draw.ellipse([cx - r + 16, cy - r + 12, cx + r - 16, cy + 5], fill=(255, 130, 70, 200))
    draw.ellipse([cx - 25, cy - r + 8, cx + 25, cy - r + 28], fill=(255, 255, 255, 160))

    font_start = get_font(25, bold=True)
    # Text "BẮT ĐẦU" in two lines or single line
    # "BẮT"
    draw_bubble_text(draw, cx - 24, cy - 26, 'BẮT', font_start, (255, 250, 160, 255), (120, 30, 0, 255), 4)
    draw.text((cx - 23, cy - 25), 'BẮT', font=font_start, fill=(255, 255, 255, 230))
    # "ĐẦU"
    draw_bubble_text(draw, cx - 25, cy + 3, 'ĐẦU', font_start, (255, 250, 160, 255), (120, 30, 0, 255), 4)
    draw.text((cx - 24, cy + 4), 'ĐẦU', font=font_start, fill=(255, 255, 255, 230))

    return im

def create_cadpa_badge():
    """LoginHome CADPA 8+ badge (122x156)"""
    w, h = 122, 156
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(im)

    # White card with black border and rounded corners
    draw.rounded_rectangle([2, 2, w - 3, h - 3], radius=16, fill=(255, 255, 255, 255), outline=(30, 30, 30, 255), width=3)
    # Green inner block
    draw.rounded_rectangle([10, 10, w - 11, 115], radius=12, fill=(88, 178, 38, 255))

    font_8 = get_font(56, bold=True)
    font_sub = get_font(13, bold=True)
    font_bot = get_font(12, bold=True)

    draw.text((28, 14), '8+', font=font_8, fill=(255, 255, 255, 255))
    draw.text((27, 85), 'PHÙ HỢP', font=font_sub, fill=(255, 255, 255, 255))
    draw.text((16, 126), 'MỌI LỨA TUỔI', font=font_bot, fill=(30, 30, 30, 255))

    return im

def create_login_button_173():
    """Login.swf big Login button 173 (243x220)"""
    orig_path = 'data/decompiled/Login/buttons/DefineButton2_173/1_up.png'
    if os.path.exists(orig_path):
        im = Image.open(orig_path).convert('RGBA')
    else:
        im = Image.new('RGBA', (243, 220), (0, 0, 0, 0))

    draw = ImageDraw.Draw(im)
    # Erase the center "登录" text inside the inner orange capsule
    # Capsule center is roughly x: 121, y: 110, width: 140, height: 70
    draw.rounded_rectangle([45, 78, 198, 142], radius=32, fill=(245, 120, 15, 255), outline=(220, 70, 0, 255), width=2)
    # Gloss highlight
    draw.rounded_rectangle([52, 82, 191, 105], radius=14, fill=(255, 180, 80, 180))

    font_login = get_font(23, bold=True)
    draw_bubble_text(draw, 56, 96, 'ĐĂNG NHẬP', font_login, (255, 245, 180, 255), (130, 30, 0, 255), 4)
    draw.text((57, 97), 'ĐĂNG NHẬP', font=font_login, fill=(255, 255, 255, 230))

    return im

def create_shape_171():
    """Login.swf shape 171 (147x67) - the '登录' text shape in the button"""
    im = Image.new('RGBA', (147, 67), (0, 0, 0, 0))
    draw = ImageDraw.Draw(im)
    font_login = get_font(22, bold=True)
    draw_bubble_text(draw, 4, 18, 'ĐĂNG NHẬP', font_login, (255, 245, 180, 255), (130, 30, 0, 255), 4)
    draw.text((5, 19), 'ĐĂNG NHẬP', font=font_login, fill=(255, 255, 255, 230))
    return im

def create_shape_182():
    """Login.swf shape 182 - '淘米账号:' label"""
    # Size from export is roughly 120x35
    orig_path = 'scratch/login_shapes_png/182.png'
    if os.path.exists(orig_path):
        base = Image.open(orig_path)
        w, h = max(base.width, 140), max(base.height, 35)
    else:
        w, h = 140, 35
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(im)
    font = get_font(20, bold=True)
    draw_bubble_text(draw, 5, 4, 'Tài Khoản:', font, (255, 245, 160, 255), (140, 40, 0, 255), 3)
    draw.text((6, 5), 'Tài Khoản:', font=font, fill=(255, 255, 255, 230))
    return im

def create_shape_187():
    """Login.swf shape 187 - '密码:' label"""
    orig_path = 'scratch/login_shapes_png/187.png'
    if os.path.exists(orig_path):
        base = Image.open(orig_path)
        w, h = max(base.width, 130), max(base.height, 35)
    else:
        w, h = 130, 35
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(im)
    font = get_font(20, bold=True)
    draw_bubble_text(draw, 5, 4, 'Mật Khẩu:', font, (255, 245, 160, 255), (140, 40, 0, 255), 3)
    draw.text((6, 5), 'Mật Khẩu:', font=font, fill=(255, 255, 255, 230))
    return im

def create_shape_123():
    """Login.swf shape 123 - '记住' label"""
    orig_path = 'scratch/login_shapes_png/123.png'
    if os.path.exists(orig_path):
        base = Image.open(orig_path)
        w, h = max(base.width, 70), max(base.height, 25)
    else:
        w, h = 70, 25
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(im)
    font = get_font(15, bold=True)
    draw_bubble_text(draw, 2, 2, 'Ghi nhớ', font, (255, 245, 160, 255), (140, 40, 0, 255), 2)
    draw.text((3, 3), 'Ghi nhớ', font=font, fill=(255, 255, 255, 230))
    return im

def create_pill_button(w, h, text, font_size=13, fill_color=(250, 130, 15, 255), text_color=(255, 255, 255, 255), outline_color=(120, 40, 0, 255)):
    """Generic cute pill button with rounded corners and glossy highlight"""
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(im)
    r = min(h // 2, 16)
    draw.rounded_rectangle([1, 1, w - 2, h - 2], radius=r, fill=fill_color, outline=outline_color, width=2)
    # Gloss
    draw.rounded_rectangle([3, 2, w - 4, h // 2], radius=r - 1, fill=(255, 255, 255, 80))
    font = get_font(font_size, bold=True)
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    tx = (w - tw) // 2
    ty = (h - th) // 2 - 2
    draw_bubble_text(draw, tx, ty, text, font, text_color, outline_color, 2)
    return im

def create_shape_157():
    """Login.swf shape 157 (900x96) - the two grey notice boxes at the bottom"""
    w, h = 870, 96
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(im)

    box_w = 273
    box_h = 96
    # Left box
    draw.rounded_rectangle([0, 0, box_w, box_h], radius=18, fill=(35, 45, 55, 200), outline=(255, 255, 255, 80), width=1)
    # Right box
    draw.rounded_rectangle([w - box_w, 0, w, box_h], radius=18, fill=(35, 45, 55, 200), outline=(255, 255, 255, 80), width=1)

    font_title = get_font(13, bold=True)
    font_body = get_font(11, bold=False)

    # Left text
    draw.text((15, 12), 'Moly - Thế Giới Chuột Chũi VN', font=font_title, fill=(255, 220, 80, 255))
    draw.text((15, 34), 'Khám phá vương quốc tuổi thơ,', font=font_body, fill=(240, 240, 240, 255))
    draw.text((15, 52), 'nông trại vui vẻ và kết nối bạn bè!', font=font_body, fill=(240, 240, 240, 255))
    draw.text((15, 72), 'Cộng đồng Việt Nam thân thiện.', font=font_body, fill=(180, 230, 255, 255))

    # Right text
    rx = w - box_w + 15
    draw.text((rx, 12), 'Hỗ Trợ & Hướng Dẫn', font=font_title, fill=(255, 220, 80, 255))
    draw.text((rx, 34), 'Đăng ký tài khoản nhanh trên web.', font=font_body, fill=(240, 240, 240, 255))
    draw.text((rx, 52), 'Hỗ trợ lưu đăng nhập tiện lợi.', font=font_body, fill=(240, 240, 240, 255))
    draw.text((rx, 72), 'Chúc bạn chơi game vui vẻ!', font=font_body, fill=(180, 255, 180, 255))

    return im

def create_shape_150():
    """Login.swf shape 150 - booth and fence, clean out the Taomee logo on the fence"""
    orig_path = 'scratch/all_login_shapes/150.png'
    if not os.path.exists(orig_path):
        orig_path = 'data/decompiled/Login/images/150.png'
    im = Image.open(orig_path).convert('RGBA')
    draw = ImageDraw.Draw(im)

    # Taomee logo on fence is at bottom center: x: ~385..610, y: ~495..545
    # Replace with cute wooden plaque "Moly VN"
    plaque_box = [382, 492, 610, 545]
    draw.rounded_rectangle(plaque_box, radius=14, fill=(225, 140, 40, 255), outline=(70, 35, 10, 255), width=3)
    draw.rounded_rectangle([386, 495, 606, 518], radius=10, fill=(255, 190, 90, 180))

    font_plaque = get_font(24, bold=True)
    draw_bubble_text(draw, 420, 504, 'Moly - VN', font_plaque, (255, 255, 255, 255), (80, 35, 10, 255), 3)

    return im

def create_image_148():
    """Login.swf image 148 - Taomee logo at bottom center (900x200)"""
    w, h = 900, 200
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(im)

    # Beautiful centered "Moly - Thế Giới Chuột Chũi VN"
    font_logo = get_font(52, bold=True)
    font_sub = get_font(24, bold=True)

    draw_bubble_text(draw, 220, 45, 'Moly - Thế Giới Chuột Chũi', font_logo, (255, 150, 0, 255), (255, 255, 255, 255), 5)
    draw_bubble_text(draw, 410, 115, 'VIỆT NAM', font_sub, (230, 40, 40, 255), (255, 255, 255, 255), 3)

    return im

def main():
    out_dir = 'scratch/localized_assets'
    os.makedirs(out_dir, exist_ok=True)
    print('Generating localized assets...')

    # 1. 51moleInfo0 logo
    logo9 = create_logo_9()
    logo9.save(os.path.join(out_dir, 'logo_9.png'))
    print('  - logo_9.png created')

    # 2. LoginHome Start Button
    btn_start = create_start_button()
    btn_start.save(os.path.join(out_dir, 'btn_start_168.png'))
    print('  - btn_start_168.png created')

    # 3. CADPA badge
    cadpa = create_cadpa_badge()
    cadpa.save(os.path.join(out_dir, 'cadpa_226.png'))
    print('  - cadpa_226.png created')

    # 4. Login button 173
    btn_login = create_login_button_173()
    btn_login.save(os.path.join(out_dir, 'btn_login_173.png'))
    print('  - btn_login_173.png created')

    # 5. Shape 171
    s171 = create_shape_171()
    s171.save(os.path.join(out_dir, 'shape_171.png'))
    print('  - shape_171.png created')

    # 6. Labels
    s182 = create_shape_182()
    s182.save(os.path.join(out_dir, 'shape_182.png'))
    s187 = create_shape_187()
    s187.save(os.path.join(out_dir, 'shape_187.png'))
    s123 = create_shape_123()
    s123.save(os.path.join(out_dir, 'shape_123.png'))
    print('  - labels 182, 187, 123 created')

    # 7. Small buttons: Đăng Ký (169), Quên MK (160), Đổi MK (163), Bảo Mật (166), Tài Khoản Lưu (174, 176, 177)
    create_pill_button(88, 20, 'Đăng Ký', 12, fill_color=(240, 110, 20, 255)).save(os.path.join(out_dir, 'btn_reg_169.png'))
    create_pill_button(64, 20, 'Quên MK', 11, fill_color=(255, 180, 20, 255), text_color=(80, 30, 0, 255)).save(os.path.join(out_dir, 'btn_forgot_160.png'))
    create_pill_button(64, 20, 'Đổi MK', 11, fill_color=(255, 180, 20, 255), text_color=(80, 30, 0, 255)).save(os.path.join(out_dir, 'btn_change_163.png'))
    create_pill_button(64, 20, 'Bảo Mật', 11, fill_color=(255, 180, 20, 255), text_color=(80, 30, 0, 255)).save(os.path.join(out_dir, 'btn_protect_166.png'))
    create_pill_button(147, 43, 'Tài Khoản Lưu', 15, fill_color=(245, 140, 20, 255)).save(os.path.join(out_dir, 'btn_system_174.png'))
    create_pill_button(154, 45, 'Tài Khoản Lưu', 16, fill_color=(245, 140, 20, 255)).save(os.path.join(out_dir, 'btn_system_176.png'))
    create_pill_button(133, 49, 'Xóa Lưu', 15, fill_color=(235, 70, 70, 255)).save(os.path.join(out_dir, 'btn_clear_109.png'))
    print('  - small action buttons created')

    # 8. Notice boxes shape 157
    s157 = create_shape_157()
    s157.save(os.path.join(out_dir, 'shape_157.png'))
    print('  - shape_157.png created')

    # 9. Plaque on fence shape 150
    s150 = create_shape_150()
    s150.save(os.path.join(out_dir, 'shape_150.png'))
    print('  - shape_150.png created')

    # 10. Taomee logo image 148
    im148 = create_image_148()
    im148.save(os.path.join(out_dir, 'image_148.png'))
    print('  - image_148.png created')

    print('All localized assets generated successfully!')

if __name__ == '__main__':
    main()
