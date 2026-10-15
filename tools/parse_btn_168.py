import zlib
from pathlib import Path

swf = Path("archive/clients/local-overrides/mole.61.com/resource/login/LoginHome.swf").read_bytes()
dec = zlib.decompress(swf[8:])

# Skip RECT
# first 5 bits are nbits
nbits = dec[0] >> 3
rect_bits = 5 + nbits * 4
rect_bytes = (rect_bits + 7) // 8
pos = rect_bytes + 4 # 2 bytes frame rate, 2 bytes frame count
print(f"Tags start at offset {pos}, total dec len {len(dec)}")

while pos < len(dec) - 2:
    tag_code_and_len = int.from_bytes(dec[pos:pos+2], "little")
    tag_type = tag_code_and_len >> 6
    tag_len = tag_code_and_len & 0x3F
    header_len = 2
    if tag_len == 0x3F:
        tag_len = int.from_bytes(dec[pos+2:pos+6], "little")
        header_len = 6
    
    if tag_type == 34: # DefineButton2
        bid = int.from_bytes(dec[pos+header_len:pos+header_len+2], "little")
        print(f"Button id={bid} at {pos}")
        if bid == 168:
            print(f"Button 168 found! len={tag_len}")
    pos += header_len + tag_len
