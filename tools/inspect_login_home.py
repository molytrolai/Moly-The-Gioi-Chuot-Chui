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

tags = []
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
    tags.append((tag_code, pos, tag_len))
    pos += tag_len

for code, offset, length in tags:
    tag_data = data[offset:offset+length]
    if code in (75, 88): # DefineFont3, DefineFontName
        font_id = int.from_bytes(tag_data[:2], 'little')
        print(f'Font tag {code} id={font_id} len={length}: {tag_data[2:40]}')
    elif code in (11, 33): # DefineText
        text_id = int.from_bytes(tag_data[:2], 'little')
        print(f'DefineText {code} id={text_id} len={length}')
    elif code == 76: # SymbolClass
        print(f'SymbolClass at {offset}, len={length}')
        num_symbols = int.from_bytes(tag_data[:2], 'little')
        sp = 2
        for _ in range(num_symbols):
            sym_id = int.from_bytes(tag_data[sp:sp+2], 'little')
            sp += 2
            end = tag_data.find(b'\x00', sp)
            sym_name = tag_data[sp:end].decode('latin1', errors='ignore')
            sp = end + 1
            print(f'  Symbol {sym_id}: {sym_name}')
