import os
import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

OUT_DIR = 'work/login_candidates'
os.makedirs(OUT_DIR, exist_ok=True)

def get_font(size, bold=True):
    font_paths = [
        'C:/Windows/Fonts/tahomabd.ttf' if bold else 'C:/Windows/Fonts/tahoma.ttf',
        'C:/Windows/Fonts/segoeuib.ttf' if bold else 'C:/Windows/Fonts/segoeui.ttf',
        'C:/Windows/Fonts/arialbd.ttf' if bold else 'C:/Windows/Fonts/arial.ttf',
    ]
    for p in font_paths:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                pass
    return ImageFont.load_default()

def draw_3d_text_fast(canvas, cx, cy, text, font, fill_top, fill_bot, stroke_col, stroke_w, extrude_col=None, extrude_h=0, center=True):
    dummy = ImageDraw.Draw(canvas)
    bbox = dummy.textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    
    pad = stroke_w + extrude_h + 10
    mw, mh = tw + pad * 2, th + pad * 2
    
    # 1. Base text mask
    text_mask = Image.new('L', (mw, mh), 0)
    m_draw = ImageDraw.Draw(text_mask)
    text_x = pad - bbox[0]
    text_y = pad - bbox[1]
    m_draw.text((text_x, text_y), text, font=font, fill=255)
    
    # 2. Stroke mask via MaxFilter
    filter_size = max(3, stroke_w * 2 + 1)
    if filter_size % 2 == 0:
        filter_size += 1
    stroke_mask = text_mask.filter(ImageFilter.MaxFilter(filter_size))
    
    target_x = cx - mw // 2 if center else cx - pad
    target_y = cy - mh // 2 if center else cy - pad

    # 3. Extrusion layer
    if extrude_col and extrude_h > 0:
        extrude_layer = Image.new('RGBA', (mw, mh + extrude_h + 4), (0, 0, 0, 0))
        for ey in range(extrude_h, 0, -2):
            ext_img = Image.new('RGBA', (mw, mh), extrude_col)
            ext_img.putalpha(stroke_mask)
            extrude_layer.paste(ext_img, (0, ey), ext_img)
        canvas.paste(extrude_layer, (target_x, target_y), extrude_layer)
        
    # 4. Stroke layer
    if stroke_col and stroke_w > 0:
        stroke_img = Image.new('RGBA', (mw, mh), stroke_col)
        stroke_img.putalpha(stroke_mask)
        canvas.paste(stroke_img, (target_x, target_y), stroke_img)
        
    # 5. Face layer with vertical gradient
    face_img = Image.new('RGBA', (mw, mh), (0, 0, 0, 0))
    f_draw = ImageDraw.Draw(face_img)
    for row in range(max(0, text_y - 2), min(mh, text_y + th + 4)):
        t = (row - text_y) / max(1, th)
        t = max(0.0, min(1.0, t))
        r = int(fill_top[0] * (1 - t) + fill_bot[0] * t)
        g = int(fill_top[1] * (1 - t) + fill_bot[1] * t)
        b = int(fill_top[2] * (1 - t) + fill_bot[2] * t)
        f_draw.line([(0, row), (mw, row)], fill=(r, g, b, 255))
    face_img.putalpha(text_mask)
    canvas.paste(face_img, (target_x, target_y), face_img)


# ==============================================================================
# 1. BTN_START_168 (LoginHome Start Button: 222x258 px)
# ==============================================================================
def craft_btn_start_168():
    SCALE = 4
    W, H = 222 * SCALE, 258 * SCALE
    
    orig_path = 'data/decompiled/LoginHome/buttons/DefineButton2_168/1_up.png'
    if os.path.exists(orig_path):
        base = Image.open(orig_path).convert('RGBA').resize((W, H), Image.Resampling.LANCZOS)
    else:
        base = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        
    draw = ImageDraw.Draw(base)
    cx, cy = 111 * SCALE, 129 * SCALE
    r = int(57.5 * SCALE)
    
    # Outer dark contour of sphere
    draw.ellipse([cx - r - 2*SCALE, cy - r - 2*SCALE, cx + r + 2*SCALE, cy + r + 2*SCALE], fill=(70, 0, 10, 255))
    # Red crystal body with multi-level smooth radial gradient
    steps = 40
    for s in range(steps):
        cur_r = int(r * (1 - s / steps))
        if cur_r <= 0:
            break
        t = s / steps
        cr = int(140 * (1 - t) + 250 * t)
        cg = int(10 * (1 - t) + 35 * t)
        cb = int(15 * (1 - t) + 40 * t)
        draw.ellipse([cx - cur_r, cy - cur_r - int(t*8*SCALE), cx + cur_r, cy + cur_r - int(t*8*SCALE)], fill=(cr, cg, cb, 255))
        
    # Top curved gloss highlight
    gloss = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    g_draw = ImageDraw.Draw(gloss)
    g_draw.ellipse([cx - int(38*SCALE), cy - int(50*SCALE), cx + int(38*SCALE), cy - int(12*SCALE)], fill=(255, 255, 255, 140))
    g_draw.ellipse([cx - int(24*SCALE), cy - int(48*SCALE), cx + int(24*SCALE), cy - int(26*SCALE)], fill=(255, 255, 255, 200))
    base.alpha_composite(gloss)
    
    # Text "BẮT ĐẦU" in two lines, bold 3D cartoon style
    font_start = get_font(33 * SCALE, bold=True)
    draw_3d_text_fast(base, cx, cy - int(22*SCALE), "BẮT", font_start,
                      fill_top=(255, 255, 190), fill_bot=(255, 185, 0),
                      stroke_col=(105, 0, 8, 255), stroke_w=int(4.5*SCALE),
                      extrude_col=(45, 0, 3, 255), extrude_h=int(4*SCALE))
                 
    draw_3d_text_fast(base, cx, cy + int(18*SCALE), "ĐẦU", font_start,
                      fill_top=(255, 255, 190), fill_bot=(255, 185, 0),
                      stroke_col=(105, 0, 8, 255), stroke_w=int(4.5*SCALE),
                      extrude_col=(45, 0, 3, 255), extrude_h=int(4*SCALE))

    final_im = base.resize((222, 258), Image.Resampling.LANCZOS)
    final_im.save(os.path.join(OUT_DIR, 'btn_start_168.png'))
    print('  - btn_start_168.png crafted')


# ==============================================================================
# 2. BTN_LOGIN_173 (Login Button: 243x220 px) & SHAPE_171 (147x67 px)
# ==============================================================================
def craft_btn_login_173():
    SCALE = 4
    W, H = 243 * SCALE, 220 * SCALE
    
    orig_path = 'data/decompiled/Login/buttons/DefineButton2_173/1_up.png'
    if os.path.exists(orig_path):
        base = Image.open(orig_path).convert('RGBA').resize((W, H), Image.Resampling.LANCZOS)
    else:
        base = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        
    draw = ImageDraw.Draw(base)
    bx1, by1 = int(44 * SCALE), int(78 * SCALE)
    bx2, by2 = int(198 * SCALE), int(142 * SCALE)
    rad = int(32 * SCALE)
    
    # Redraw shiny amber-orange capsule
    draw.rounded_rectangle([bx1 - int(2*SCALE), by1 - int(2*SCALE), bx2 + int(2*SCALE), by2 + int(2*SCALE)],
                           radius=rad + int(2*SCALE), fill=(110, 20, 0, 255))
    steps = 30
    for s in range(steps):
        cur_y = by1 + int((by2 - by1) * s / steps)
        t = s / steps
        cr = int(255 * (1 - t*0.1) + 210 * t*0.1)
        cg = int(175 * (1 - t*0.7) + 50 * t*0.7)
        cb = int(25 * (1 - t))
        draw.rounded_rectangle([bx1, cur_y, bx2, by2], radius=rad, fill=(cr, cg, cb, 255))
        
    # Top curved gloss
    gloss = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    g_draw = ImageDraw.Draw(gloss)
    g_draw.rounded_rectangle([bx1 + int(6*SCALE), by1 + int(4*SCALE), bx2 - int(6*SCALE), by1 + int(28*SCALE)],
                            radius=int(14*SCALE), fill=(255, 255, 255, 140))
    base.alpha_composite(gloss)
    
    # Huge, bold "ĐĂNG NHẬP" text
    font_login = get_font(23 * SCALE, bold=True)
    cx, cy = (bx1 + bx2) // 2, (by1 + by2) // 2 - int(1*SCALE)
    draw_3d_text_fast(base, cx, cy, "ĐĂNG NHẬP", font_login,
                      fill_top=(255, 255, 200), fill_bot=(255, 195, 0),
                      stroke_col=(95, 15, 0, 255), stroke_w=int(3.5*SCALE),
                      extrude_col=(45, 5, 0, 255), extrude_h=int(3*SCALE))
                 
    final_im = base.resize((243, 220), Image.Resampling.LANCZOS)
    final_im.save(os.path.join(OUT_DIR, 'btn_login_173.png'))
    print('  - btn_login_173.png crafted')
    
    # Shape 171 (147x67 px)
    SW, SH = 147 * SCALE, 67 * SCALE
    s_im = Image.new('RGBA', (SW, SH), (0, 0, 0, 0))
    s_font = get_font(21 * SCALE, bold=True)
    draw_3d_text_fast(s_im, SW // 2, SH // 2 - int(2*SCALE), "ĐĂNG NHẬP", s_font,
                      fill_top=(255, 255, 200), fill_bot=(255, 195, 0),
                      stroke_col=(95, 15, 0, 255), stroke_w=int(3.5*SCALE),
                      extrude_col=(45, 5, 0, 255), extrude_h=int(3*SCALE))
    s_final = s_im.resize((147, 67), Image.Resampling.LANCZOS)
    s_final.save(os.path.join(OUT_DIR, 'shape_171.png'))
    print('  - shape_171.png crafted')


# ==============================================================================
# 3. ACTION LINKS (Đăng Ký, Quên MK, Đổi MK, Bảo Mật)
# ==============================================================================
def craft_action_links():
    SCALE = 4
    actions = [
        ('btn_reg_169.png', 88, 18, 'Đăng Ký', 13.5),
        ('btn_forgot_160.png', 64, 18, 'Quên MK', 12.5),
        ('btn_change_163.png', 64, 18, 'Đổi MK', 12.5),
        ('btn_protect_166.png', 64, 18, 'Bảo Mật', 12.5),
    ]
    
    for filename, w, h, text, font_sz in actions:
        SW, SH = w * SCALE, h * SCALE
        im = Image.new('RGBA', (SW, SH), (0, 0, 0, 0))
        font = get_font(int(font_sz * SCALE), bold=True)
        
        cx, cy = SW // 2, SH // 2 - int(1 * SCALE)
        draw_3d_text_fast(im, cx, cy, text, font,
                          fill_top=(255, 255, 40), fill_bot=(255, 185, 0),
                          stroke_col=(120, 20, 10, 255), stroke_w=int(2.2 * SCALE),
                          extrude_col=(50, 5, 2, 255), extrude_h=int(1.5 * SCALE))
                     
        final_im = im.resize((w, h), Image.Resampling.LANCZOS)
        final_im.save(os.path.join(OUT_DIR, filename))
        print(f'  - {filename} crafted')


# ==============================================================================
# 4. BTN_CLEAR_109 (Clear Saved Records Button: 133x49 px)
# ==============================================================================
def craft_btn_clear_109():
    SCALE = 4
    W, H = 133 * SCALE, 49 * SCALE
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(im)
    
    bx1, by1 = int(6 * SCALE), int(6 * SCALE)
    bx2, by2 = int(127 * SCALE), int(43 * SCALE)
    rad = int(12 * SCALE)
    
    # Shadow & border
    draw.rounded_rectangle([bx1, by1 + int(3*SCALE), bx2, by2 + int(3*SCALE)], radius=rad, fill=(40, 0, 0, 180))
    draw.rounded_rectangle([bx1 - int(1.5*SCALE), by1 - int(1.5*SCALE), bx2 + int(1.5*SCALE), by2 + int(1.5*SCALE)],
                           radius=rad + int(1.5*SCALE), fill=(110, 10, 10, 255))
    steps = 20
    for s in range(steps):
        cur_y = by1 + int((by2 - by1) * s / steps)
        t = s / steps
        cr = int(235 * (1 - t*0.25) + 160 * t*0.25)
        cg = int(50 * (1 - t*0.7) + 15 * t*0.7)
        cb = int(50 * (1 - t*0.7) + 15 * t*0.7)
        draw.rounded_rectangle([bx1, cur_y, bx2, by2], radius=rad, fill=(cr, cg, cb, 255))
        
    # Top gloss
    gloss = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    g_draw = ImageDraw.Draw(gloss)
    g_draw.rounded_rectangle([bx1 + int(4*SCALE), by1 + int(2*SCALE), bx2 - int(4*SCALE), by1 + int(16*SCALE)],
                            radius=int(8*SCALE), fill=(255, 255, 255, 110))
    im.alpha_composite(gloss)
    
    font = get_font(18 * SCALE, bold=True)
    cx, cy = (bx1 + bx2) // 2, (by1 + by2) // 2 - int(1*SCALE)
    draw_3d_text_fast(im, cx, cy, "Xóa Lưu", font,
                      fill_top=(255, 255, 200), fill_bot=(255, 200, 0),
                      stroke_col=(90, 10, 5, 255), stroke_w=int(2.8 * SCALE),
                      extrude_col=(40, 0, 0, 255), extrude_h=int(2 * SCALE))
                 
    final_im = im.resize((133, 49), Image.Resampling.LANCZOS)
    final_im.save(os.path.join(OUT_DIR, 'btn_clear_109.png'))
    print('  - btn_clear_109.png crafted')


# ==============================================================================
# 5. BTN_SYSTEM_174 (147x43 px) & BTN_SYSTEM_176 (154x45 px)
# ==============================================================================
def craft_btn_system():
    SCALE = 4
    buttons = [
        ('btn_system_174.png', 147, 43),
        ('btn_system_176.png', 154, 45)
    ]
    for filename, w, h in buttons:
        W, H = w * SCALE, h * SCALE
        im = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        draw = ImageDraw.Draw(im)
        
        bx1, by1 = int(4 * SCALE), int(3 * SCALE)
        bx2, by2 = int((w - 4) * SCALE), int((h - 3) * SCALE)
        rad = int(14 * SCALE)
        
        draw.rounded_rectangle([bx1, by1 + int(2*SCALE), bx2, by2 + int(2*SCALE)], radius=rad, fill=(50, 15, 0, 160))
        draw.rounded_rectangle([bx1 - int(1.5*SCALE), by1 - int(1.5*SCALE), bx2 + int(1.5*SCALE), by2 + int(1.5*SCALE)],
                               radius=rad + int(1.5*SCALE), fill=(120, 45, 5, 255))
        steps = 20
        for s in range(steps):
            cur_y = by1 + int((by2 - by1) * s / steps)
            t = s / steps
            cr = int(255 * (1 - t*0.15) + 215 * t*0.15)
            cg = int(160 * (1 - t*0.5) + 80 * t*0.5)
            cb = int(25 * (1 - t))
            draw.rounded_rectangle([bx1, cur_y, bx2, by2], radius=rad, fill=(cr, cg, cb, 255))
            
        gloss = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        g_draw = ImageDraw.Draw(gloss)
        g_draw.rounded_rectangle([bx1 + int(4*SCALE), by1 + int(2*SCALE), bx2 - int(4*SCALE), by1 + int(15*SCALE)],
                                radius=int(8*SCALE), fill=(255, 255, 255, 120))
        im.alpha_composite(gloss)
        
        font = get_font(15 * SCALE, bold=True)
        cx, cy = (bx1 + bx2) // 2, (by1 + by2) // 2 - int(1*SCALE)
        draw_3d_text_fast(im, cx, cy, "Tài Khoản Lưu", font,
                          fill_top=(255, 255, 230), fill_bot=(255, 215, 80),
                          stroke_col=(95, 30, 0, 255), stroke_w=int(2.5 * SCALE),
                          extrude_col=(45, 10, 0, 255), extrude_h=int(2 * SCALE))
                     
        final_im = im.resize((w, h), Image.Resampling.LANCZOS)
        final_im.save(os.path.join(OUT_DIR, filename))
        print(f'  - {filename} crafted')


# ==============================================================================
# 6. RANDOMMC_BANNER_3 (Announcement Banner: 328x238 px)
# ==============================================================================
def craft_randommc_banner_3():
    SCALE = 4
    W, H = 328 * SCALE, 238 * SCALE
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(im)
    
    pad = int(4 * SCALE)
    rad_out = int(18 * SCALE)
    
    # Outer drop shadow & scroll body
    draw.rounded_rectangle([pad + int(2*SCALE), pad + int(4*SCALE), W - pad - int(2*SCALE), H - pad + int(2*SCALE)],
                           radius=rad_out, fill=(0, 0, 0, 180))
    draw.rounded_rectangle([pad, pad, W - pad, H - pad], radius=rad_out, fill=(255, 215, 0, 255))
    draw.rounded_rectangle([pad + int(3*SCALE), pad + int(3*SCALE), W - pad - int(3*SCALE), H - pad - int(3*SCALE)],
                           radius=rad_out - int(2*SCALE), fill=(185, 20, 25, 255))
    draw.rounded_rectangle([pad + int(6*SCALE), pad + int(6*SCALE), W - pad - int(6*SCALE), H - pad - int(6*SCALE)],
                           radius=rad_out - int(4*SCALE), outline=(255, 225, 100, 255), width=int(1.5*SCALE))
                           
    # Header Area
    font_title = get_font(16 * SCALE, bold=True)
    draw_3d_text_fast(im, W // 2, int(26 * SCALE), "MOLY - THẾ GIỚI CHUỘT CHŨI", font_title,
                      fill_top=(255, 255, 180), fill_bot=(255, 190, 0),
                      stroke_col=(90, 10, 15, 255), stroke_w=int(3 * SCALE),
                      extrude_col=(45, 0, 5, 255), extrude_h=int(2 * SCALE))
                 
    draw = ImageDraw.Draw(im)
    font_sub = get_font(10.5 * SCALE, bold=True)
    draw.text((W // 2, int(46 * SCALE)), "PHIÊN BẢN TIẾNG VIỆT 2026", font=font_sub,
              fill=(255, 235, 150, 255), anchor="mm")
              
    # Center Parchment Card
    cx1, cy1 = int(18 * SCALE), int(60 * SCALE)
    cx2, cy2 = W - int(18 * SCALE), int(172 * SCALE)
    c_rad = int(12 * SCALE)
    
    draw.rounded_rectangle([cx1, cy1 + int(2*SCALE), cx2, cy2 + int(2*SCALE)], radius=c_rad, fill=(70, 0, 10, 140))
    draw.rounded_rectangle([cx1, cy1, cx2, cy2], radius=c_rad, fill=(255, 252, 240, 255),
                           outline=(210, 180, 140, 255), width=int(1.5*SCALE))
                           
    font_body = get_font(10.5 * SCALE, bold=True)
    font_body_reg = get_font(9.5 * SCALE, bold=False)
    
    draw.text((cx1 + int(14 * SCALE), cy1 + int(13 * SCALE)), "★ Vương Quốc Tuổi Thơ Độc Lập & Hoàn Chỉnh",
              font=font_body, fill=(160, 20, 20, 255))
    draw.text((cx1 + int(14 * SCALE), cy1 + int(34 * SCALE)), "• Chăm sóc Lặt Vặt, xây dựng Nông trại & Gia viên.",
              font=font_body_reg, fill=(50, 30, 20, 255))
    draw.text((cx1 + int(14 * SCALE), cy1 + int(54 * SCALE)), "• Hệ thống nhiệm vụ, trò chơi & kết nối bạn bè 4 phương.",
              font=font_body_reg, fill=(50, 30, 20, 255))
    draw.text((cx1 + int(14 * SCALE), cy1 + int(74 * SCALE)), "• Máy chủ riêng độc lập, trải nghiệm mượt mà không giới hạn!",
              font=font_body_reg, fill=(20, 100, 30, 255))
              
    # Bottom Emerald Green 3D Button "VÀO GAME NGAY"
    bx1, by1 = (W - int(180 * SCALE)) // 2, int(183 * SCALE)
    bx2, by2 = bx1 + int(180 * SCALE), by1 + int(38 * SCALE)
    b_rad = int(19 * SCALE)
    
    draw.rounded_rectangle([bx1, by1 + int(3*SCALE), bx2, by2 + int(3*SCALE)], radius=b_rad, fill=(0, 0, 0, 160))
    draw.rounded_rectangle([bx1 - int(1.5*SCALE), by1 - int(1.5*SCALE), bx2 + int(1.5*SCALE), by2 + int(1.5*SCALE)],
                           radius=b_rad + int(1.5*SCALE), fill=(0, 80, 35, 255))
    steps = 20
    for s in range(steps):
        cur_y = by1 + int((by2 - by1) * s / steps)
        t = s / steps
        cr = 0
        cg = int(230 * (1 - t*0.35) + 140 * t*0.35)
        cb = int(115 * (1 - t*0.5) + 50 * t*0.5)
        draw.rounded_rectangle([bx1, cur_y, bx2, by2], radius=b_rad, fill=(cr, cg, cb, 255))
        
    gloss = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    g_draw = ImageDraw.Draw(gloss)
    g_draw.rounded_rectangle([bx1 + int(8*SCALE), by1 + int(3*SCALE), bx2 - int(8*SCALE), by1 + int(16*SCALE)],
                            radius=int(9*SCALE), fill=(255, 255, 255, 140))
    im.alpha_composite(gloss)
    
    font_btn = get_font(14 * SCALE, bold=True)
    draw_3d_text_fast(im, W // 2, (by1 + by2) // 2 - int(1*SCALE), "VÀO GAME NGAY", font_btn,
                      fill_top=(255, 255, 255), fill_bot=(255, 230, 150),
                      stroke_col=(0, 60, 25, 255), stroke_w=int(2.8 * SCALE),
                      extrude_col=(0, 30, 10, 255), extrude_h=int(2.5 * SCALE))
                 
    final_im = im.resize((328, 238), Image.Resampling.LANCZOS)
    final_im.save(os.path.join(OUT_DIR, 'randomMC_banner_3.png'))
    print('  - randomMC_banner_3.png crafted')


# ==============================================================================
# 7. IMAGE_148 (Login Screen Main Logo: 900x200 px)
# ==============================================================================
def craft_image_148():
    SCALE = 4
    W, H = 900 * SCALE, 200 * SCALE
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    
    # Line 1: "Moly - Thế Giới Chuột Chũi"
    font_logo = get_font(46 * SCALE, bold=True)
    cx, cy = W // 2, int(68 * SCALE)
    
    draw_3d_text_fast(im, cx, cy, "Moly - Thế Giới Chuột Chũi", font_logo,
                      fill_top=(255, 240, 140), fill_bot=(255, 145, 0),
                      stroke_col=(255, 255, 255, 255), stroke_w=int(5.5 * SCALE),
                      extrude_col=(140, 20, 0, 255), extrude_h=int(6 * SCALE))
                 
    # Cute red mole nose
    draw = ImageDraw.Draw(im)
    bbox_moly = draw.textbbox((0, 0), "Moly - Thế Giới Chuột Chũi", font=font_logo)
    start_x = cx - (bbox_moly[2] - bbox_moly[0]) // 2
    nose_x = start_x + int(76 * SCALE)
    nose_y = cy - int(2 * SCALE)
    nr = int(14 * SCALE)
    draw.ellipse([nose_x - nr - 3*SCALE, nose_y - nr - 3*SCALE, nose_x + nr + 3*SCALE, nose_y + nr + 3*SCALE],
                 fill=(70, 10, 5, 255))
    draw.ellipse([nose_x - nr, nose_y - nr, nose_x + nr, nose_y + nr], fill=(235, 25, 25, 255))
    draw.ellipse([nose_x - int(5*SCALE), nose_y - int(7*SCALE), nose_x - int(1*SCALE), nose_y - int(3*SCALE)],
                 fill=(255, 255, 255, 240))
                 
    # Subtitle Ribbon Badge: "VIỆT NAM"
    rib_w = int(220 * SCALE)
    rib_h = int(38 * SCALE)
    rx1, ry1 = (W - rib_w) // 2, int(136 * SCALE)
    rx2, ry2 = rx1 + rib_w, ry1 + rib_h
    
    draw.rounded_rectangle([rx1, ry1 + int(3*SCALE), rx2, ry2 + int(3*SCALE)], radius=int(14*SCALE), fill=(0, 0, 0, 150))
    draw.rounded_rectangle([rx1, ry1, rx2, ry2], radius=int(14*SCALE), fill=(255, 215, 0, 255))
    draw.rounded_rectangle([rx1 + int(2.5*SCALE), ry1 + int(2.5*SCALE), rx2 - int(2.5*SCALE), ry2 - int(2.5*SCALE)],
                           radius=int(12*SCALE), fill=(215, 25, 30, 255))
                           
    font_vn = get_font(15 * SCALE, bold=True)
    draw_3d_text_fast(im, W // 2, (ry1 + ry2) // 2 - int(1*SCALE), "★  VIỆT NAM  ★", font_vn,
                      fill_top=(255, 255, 255), fill_bot=(255, 235, 160),
                      stroke_col=(110, 15, 10, 255), stroke_w=int(2.5 * SCALE),
                      extrude_col=(50, 0, 0, 255), extrude_h=int(2 * SCALE))
                 
    final_im = im.resize((900, 200), Image.Resampling.LANCZOS)
    final_im.save(os.path.join(OUT_DIR, 'image_148.png'))
    print('  - image_148.png crafted')


def main():
    print("Crafting all authentic login candidates with 4x supersampling...")
    craft_btn_start_168()
    craft_btn_login_173()
    craft_action_links()
    craft_btn_clear_109()
    craft_btn_system()
    craft_randommc_banner_3()
    craft_image_148()
    print("All authentic candidates created successfully!")

if __name__ == '__main__':
    main()
