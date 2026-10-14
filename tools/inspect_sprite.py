import zlib
import sys
import os

sys.stdout.reconfigure(encoding='utf-8')

swf_path = os.path.join('archive', 'clients', 'offline-mirror', 'mole.61.com', 'resource', 'login', 'LoginHome.swf')

with open(swf_path, 'rb') as f:
    data = f.read()

if data[:3] == b'CWS':
    data = data[:8] + zlib.decompress(data[8:])

pos = 8
nbits = data[pos] >> 3
nbits_total = 5 + nbits * 4
bytes_rect = (nbits_total + 7) // 8
pos += bytes_rect
pos += 4

tags = {}
sprites = {}
texts = {}
while pos < len(data):
    if pos + 2 > len(data):
        break
    tag_and_len = int.from_bytes(data[pos:pos+2], 'little')
    pos += 2
    tag_code = tag_and_len >> 6
    tag_len = tag_and_len & 0x3f
    if tag_len == 0x3f:
        if pos + 4 > len(data):
            break
        tag_len = int.from_bytes(data[pos:pos+4], 'little')
        pos += 4
    tag_data = data[pos:pos+tag_len]
    tags[pos] = (tag_code, tag_len)
    if tag_code == 39: # DefineSprite
        sprite_id = int.from_bytes(tag_data[:2], 'little')
        sprites[sprite_id] = tag_data[2:]
    elif tag_code in (11, 33): # DefineText
        text_id = int.from_bytes(tag_data[:2], 'little')
        texts[text_id] = tag_data[2:]
    pos += tag_len

print(f'Found {len(sprites)} sprites, {len(texts)} texts')

if 239 in sprites:
    sp_data = sprites[239]
    frame_count = int.from_bytes(sp_data[:2], 'little')
    print(f'Sprite 239: frame_count={frame_count}, len={len(sp_data)}')
    sp_pos = 2
    while sp_pos < len(sp_data):
        st_and_len = int.from_bytes(sp_data[sp_pos:sp_pos+2], 'little')
        sp_pos += 2
        st_code = st_and_len >> 6
        st_len = st_and_len & 0x3f
        if st_len == 0x3f:
            st_len = int.from_bytes(sp_data[sp_pos:sp_pos+4], 'little')
            sp_pos += 4
        sdata = sp_data[sp_pos:sp_pos+st_len]
        if st_code in (4, 26, 70): # PlaceObject
            # check character id
            has_char = (sdata[0] & 0x02) != 0
            if has_char:
                char_id = int.from_bytes(sdata[3:5], 'little')
                print(f'  PlaceObject {st_code}: char_id={char_id}')
        elif st_code == 1:
            print('  ShowFrame')
        sp_pos += st_len
