from PIL import Image, ImageDraw, ImageFont

# Load base image with Vietnamese sign 'LÂU ĐÀI MOLY'
base_img = Image.open('work/map_buildings/map1_bg_vi.jpg').convert('RGBA')

# The shield position in (960, 560):
# Center x is at x=478, y is from y=168 to y=218
overlay = Image.new('RGBA', base_img.size, (0, 0, 0, 0))
draw = ImageDraw.Draw(overlay)

# Shield coordinates in full 960x560 image:
# x offset: +430, y offset: +150
# shield_pts in zoomed were:
# (24, 18), (72, 18), (74, 32), (72, 46), (48, 64), (24, 46), (22, 32)
# In full image coordinates:
pts = [
    (430 + 24, 150 + 18),
    (430 + 72, 150 + 18),
    (430 + 74, 150 + 32),
    (430 + 72, 150 + 46),
    (430 + 48, 150 + 64),
    (430 + 24, 150 + 46),
    (430 + 22, 150 + 32)
]

# Inner crimson royal background
draw.polygon(pts, fill=(185, 28, 28, 255))

# Golden border rim
draw.polygon(pts, outline=(251, 191, 36, 255), width=2)

# Mini Royal Crown at top of shield
crown_pts = [
    (430 + 40, 150 + 23),
    (430 + 43, 150 + 19),
    (430 + 48, 150 + 21),
    (430 + 53, 150 + 19),
    (430 + 56, 150 + 23),
    (430 + 48, 150 + 25)
]
draw.polygon(crown_pts, fill=(253, 224, 71, 255), outline=(180, 83, 9, 255))

# Font for MOLY
try:
    font = ImageFont.truetype('arialbd.ttf', 13)
except:
    font = ImageFont.load_default()

# Shadow
draw.text((430 + 32, 150 + 33), 'MOLY', font=font, fill=(69, 10, 10, 255))
# Text
draw.text((430 + 31, 150 + 32), 'MOLY', font=font, fill=(254, 240, 138, 255))

# Golden star emblem below text
star_cx = 430 + 48
star_cy = 150 + 53
star_pts = [
    (star_cx, star_cy - 6),
    (star_cx + 2, star_cy - 2),
    (star_cx + 6, star_cy - 2),
    (star_cx + 3, star_cy + 1),
    (star_cx + 4, star_cy + 5),
    (star_cx, star_cy + 2),
    (star_cx - 4, star_cy + 5),
    (star_cx - 3, star_cy + 1),
    (star_cx - 6, star_cy - 2),
    (star_cx - 2, star_cy - 2)
]
draw.polygon(star_pts, fill=(250, 204, 21, 255))

final_img = Image.alpha_composite(base_img, overlay).convert('RGB')

# Save to both locations
final_img.save('web/assets/game_bg_square.jpg', quality=95)
final_img.save('work/map_buildings/map1_bg_vi.jpg', quality=95)
print('Successfully updated game_bg_square.jpg and map1_bg_vi.jpg with MOLY royal crest!')
