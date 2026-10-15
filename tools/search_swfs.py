import zlib
from pathlib import Path

ROOT = Path("archive/clients/local-overrides/mole.61.com")

def decompress_swf(data):
    if len(data) < 8:
        return b""
    sig = data[:3]
    if sig == b"FWS": # uncompressed
        return data[8:]
    elif sig == b"CWS": # zlib compressed
        try:
            return zlib.decompress(data[8:])
        except:
            return b""
    elif sig == b"ZWS": # lzma compressed
        import lzma
        try:
            return lzma.decompress(data[12:])
        except:
            return b""
    return data

def search_text_in_swfs():
    for swf in ROOT.glob("**/*.swf"):
        try:
            raw = swf.read_bytes()
            dec = decompress_swf(raw)
            if b"\xe5\xbc\x80\xe5\xa7\x8b" in dec: # 开始
                print(f"[FOUND 开始] {swf.name}")
            if b"\xe6\x91\xa9\xe5\xb0\x94\xe5\xba\x84\xe5\x9b\xad" in dec: # 摩尔庄园
                print(f"[FOUND 摩尔庄园] {swf.name}")
            if b"\xe9\x80\x82\xe9\xbe\x84\xe6\x8f\x90\xe7\xa4\xba" in dec: # 适龄提示
                print(f"[FOUND 适龄提示] {swf.name}")
            if b"Taomee" in dec:
                print(f"[FOUND Taomee] {swf.name}")
            if b"account.61.com" in dec:
                print(f"[FOUND account.61.com] {swf.name}")
        except Exception as e:
            pass

if __name__ == "__main__":
    search_text_in_swfs()
