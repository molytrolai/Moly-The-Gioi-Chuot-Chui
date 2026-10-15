import os
from PIL import Image, ImageDraw, ImageFont

def make_login_sheet():
    pairs = [
        # (id, name, orig_path, current_loc_path)
        ("128", "NÚT BẮT ĐẦU (LoginHome)", "work/exported/LoginHome_full/shapes/128.png", "scratch/localized_assets/shape_128.png"),
        ("171", "NÚT ĐĂNG NHẬP (Login)", "work/exported/Login_full/shapes/171.png", "scratch/localized_assets/shape_171.png"),
        ("158", "NÚT ĐĂNG KÝ", "work/exported/Login_full/shapes/158.png", "scratch/localized_assets/btn_reg_169.png"),
        ("161", "NÚT QUÊN MK", "work/exported/Login_full/shapes/161.png", "scratch/localized_assets/btn_forgot_160.png"),
        ("164", "NÚT ĐỔI MK", "work/exported/Login_full/shapes/164.png", "scratch/localized_assets/btn_change_163.png"),
        ("167", "NÚT BẢO MẬT", "work/exported/Login_full/shapes/167.png", "scratch/localized_assets/btn_protect_166.png"),
        ("174", "NÚT TÀI KHOẢN LƯU", "work/exported/Login_full/shapes/174.png", "scratch/localized_assets/btn_system_174.png"),
        ("182", "NHÃN TÀI KHOẢN:", "work/exported/Login_full/shapes/182.png", "scratch/localized_assets/shape_182.png"),
        ("187", "NHÃN MẬT KHẨU:", "work/exported/Login_full/shapes/187.png", "scratch/localized_assets/shape_187.png"),
        ("123", "GHI NHỚ (CHECKBOX)", "work/exported/Login_full/shapes/123.png", "scratch/localized_assets/shape_123.png"),
    ]
    
    font = ImageFont.load_default()
    
    # 2 columns per item: Original vs Current
    cols = 2
    row_h = 100
    col_w = 400
    total_w = cols * col_w
    total_h = len(pairs) * row_h + 50
    
    sheet = Image.new("RGBA", (total_w, total_h), (30, 41, 59, 255))
    draw = ImageDraw.Draw(sheet)
    
    draw.text((20, 15), "SO SÁNH CÁC NÚT & ICON NGOÀI MÀN HÌNH ĐĂNG NHẬP (GỐC VS HIỆN TẠI)", fill=(255, 215, 0), font=font)
    draw.line([(0, 40), (total_w, 40)], fill=(71, 85, 105), width=2)
    
    for idx, (cid, name, orig, curr) in enumerate(pairs):
        y = 50 + idx * row_h
        
        # Row line
        draw.line([(0, y + row_h), (total_w, y + row_h)], fill=(51, 65, 85), width=1)
        
        # Col 1: Original
        draw.text((15, y + 10), f"[{cid}] {name} - GỐC (TRUNG QUỐC)", fill=(148, 163, 184), font=font)
        if os.path.exists(orig):
            imo = Image.open(orig).convert("RGBA")
            sheet.alpha_composite(imo, (20, y + 30))
        else:
            draw.text((20, y + 35), "Không tìm thấy file gốc", fill=(239, 68, 68), font=font)
            
        # Col 2: Current
        draw.text((col_w + 15, y + 10), f"[{cid}] {name} - BẢN HIỆN TẠI (SCRATCH)", fill=(250, 204, 21), font=font)
        if os.path.exists(curr):
            imc = Image.open(curr).convert("RGBA")
            sheet.alpha_composite(imc, (col_w + 20, y + 30))
        else:
            draw.text((col_w + 20, y + 35), "Chưa có file", fill=(239, 68, 68), font=font)
            
    sheet.save("work/login_buttons_comparison.png")
    print("Saved work/login_buttons_comparison.png")

make_login_sheet()
