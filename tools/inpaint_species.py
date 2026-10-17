from PIL import Image, ImageFilter
import random
import os

im = Image.open('web/assets/super_lamu_species.jpg').copy()
w, h = im.size

def inpaint_box(img, x1, y1, x2, y2):
    pix = img.load()
    bw = x2 - x1 + 1
    bh = y2 - y1 + 1
    
    random.seed(42)
    for y in range(y1, y2 + 1):
        v_ratio = (y - y1) / float(max(1, bh - 1))
        for x in range(x1, x2 + 1):
            h_ratio = (x - x1) / float(max(1, bw - 1))
            
            top_col = pix[x, max(0, y1 - 2)]
            bot_col = pix[x, min(h - 1, y2 + 2)]
            left_col = pix[max(0, x1 - 2), y]
            right_col = pix[min(w - 1, x2 + 2), y]
            
            vert = [int(top_col[i] * (1 - v_ratio) + bot_col[i] * v_ratio) for i in range(3)]
            horiz = [int(left_col[i] * (1 - h_ratio) + right_col[i] * h_ratio) for i in range(3)]
            blended = [int((vert[i] + horiz[i]) / 2) for i in range(3)]
            
            noise = random.randint(-3, 3)
            final_c = tuple(max(0, min(255, blended[i] + noise)) for i in range(3))
            pix[x, y] = final_c

# Inpaint left logo (25, 10, 330, 130)
inpaint_box(im, 25, 10, 330, 130)
# Inpaint right logo (680, 15, 1160, 130)
inpaint_box(im, 680, 15, 1160, 130)

# Smooth edges
box1 = im.crop((20, 5, 335, 135)).filter(ImageFilter.GaussianBlur(radius=1.5))
im.paste(box1, (20, 5))
box2 = im.crop((675, 10, 1165, 135)).filter(ImageFilter.GaussianBlur(radius=1.5))
im.paste(box2, (675, 10))

im.save('web/assets/super_lamu_species.jpg', quality=95)
print('Inpainted and overwritten super_lamu_species.jpg successfully!')
