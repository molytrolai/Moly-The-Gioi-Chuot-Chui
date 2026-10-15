import zlib
from pathlib import Path

swf = Path("archive/clients/local-overrides/mole.61.com/resource/login/LoginHome.swf").read_bytes()
dec = zlib.decompress(swf[8:])

pos = 103560
# tag header: len 6
tag_len = 1876
data = dec[pos+6 : pos+6+tag_len]

# bid = data[0:2] -> 168
trackAsMenu = data[2]
actionOffset = int.from_bytes(data[3:5], "little")

# ButtonRecords start at index 5
idx = 5
rec_num = 0
while idx < len(data):
    flags = data[idx]
    if flags == 0:
        print("End of button records at", idx)
        break
    chid = int.from_bytes(data[idx+1:idx+3], "little")
    depth = int.from_bytes(data[idx+3:idx+5], "little")
    print(f"Record {rec_num}: flags=0x{flags:02x} (Up={bool(flags&1)}, Over={bool(flags&2)}, Down={bool(flags&4)}, Hit={bool(flags&8)}) -> chid={chid}, depth={depth}")
    
    # We want to skip Matrix and Cxform to get to next record
    # Instead of full bit parsing, let's just search for next candidate or parse bits
    rec_num += 1
    # Move forward a bit or parse matrix
    idx += 5
    # Matrix: hasScale (1 bit), hasRotate (1 bit), nbits (5 bits)...
    # Let's inspect raw slice
    # Or we can just find all chids!
    break

# Let's search all 2-byte numbers in data that correspond to existing shape/sprite IDs!
valid_shapes = set(range(1, 250))
print("\nScanning for possible character references in Button 168 data:")
found_chids = set()
for i in range(len(data)-1):
    val = int.from_bytes(data[i:i+2], "little")
    if val in [20, 55, 57, 58, 60, 62, 64, 66, 68, 164, 166, 167, 169, 170, 171, 172, 174, 176, 178, 180, 181, 183, 184, 186, 187, 189, 190, 192]:
        found_chids.add(val)
print("Found potential chids referenced:", sorted(found_chids))
