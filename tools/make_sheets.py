import os
from PIL import Image, ImageDraw, ImageFont

def make_sheet(folder, out_name):
    files = sorted([f for f in os.listdir(folder) if f.endswith(".png") and not f.startswith("sheet")])
    if not files: return
    
    font = ImageFont.load_default()
    cols = 6
    cell_w = 160
    cell_h = 100
    rows = (len(files) + cols - 1) // cols
    sheet = Image.new("RGBA", (cols * cell_w, rows * cell_h), (40, 44, 52, 255))
    draw = ImageDraw.Draw(sheet)
    
    for idx, f in enumerate(files):
        c = idx % cols
        r = idx // cols
        x = c * cell_w
        y = r * cell_h
        
        # draw border
        draw.rectangle([x+2, y+2, x+cell_w-2, y+cell_h-2], outline=(70, 75, 85))
        draw.text((x+6, y+4), f, fill=(220, 220, 220), font=font)
        
        p = os.path.join(folder, f)
        try:
            im = Image.open(p).convert("RGBA")
            # scale if needed to fit 120x70
            max_w, max_h = 130, 70
            scale = min(max_w / im.width, max_h / im.height, 2.0)
            target_size = (int(im.width * scale), int(im.height * scale))
            im_resized = im.resize(target_size, Image.Resampling.NEAREST if scale >= 1 else Image.Resampling.LANCZOS)
            
            paste_x = x + (cell_w - target_size[0]) // 2
            paste_y = y + 20 + (cell_h - 20 - target_size[1]) // 2
            sheet.alpha_composite(im_resized, (paste_x, paste_y))
        except Exception as e:
            draw.text((x+6, y+30), f"Err: {e}", fill=(255, 100, 100), font=font)
            
    sheet.save(out_name)
    print(f"Saved {out_name}: {sheet.size}")

make_sheet("work/audit_images/topUI", "work/topui_overview.png")
make_sheet("work/audit_images/ui", "work/ui_overview.png")
