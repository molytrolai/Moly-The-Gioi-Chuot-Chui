#!/usr/bin/env python3
"""Scan all Map SWFs in pure Python for Chinese text and report their exact locations."""

import sys
import zlib
import re
import xml.etree.ElementTree as ET
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = Path(__file__).resolve().parents[1]
MAP_DIR = ROOT_DIR / "archive" / "clients" / "offline-mirror" / "mole.61.com" / "resource" / "map"
CONFIG_FILE = ROOT_DIR / "work" / "translated_52_wordMapTipConfig.bin"

# 1. Load Map ID -> Vietnamese Name mapping from world map config
map_names = {}
if CONFIG_FILE.exists():
    try:
        content = CONFIG_FILE.read_text(encoding="utf-8", errors="ignore")
        root = ET.fromstring(content)
        for m in root.findall(".//Map"):
            mid = m.get("ID")
            name = m.get("name")
            if mid and name:
                map_names[int(mid)] = name
    except Exception as e:
        print("Error reading map config:", e)

hanzi_regex = re.compile(r'[\u4e00-\u9fff]{2,}')

def extract_hanzi_from_swf(swf_path):
    raw = swf_path.read_bytes()
    if len(raw) < 8:
        return []
    sig = raw[:3]
    if sig == b'CWS':
        try:
            body = zlib.decompress(raw[8:])
        except:
            return []
    elif sig == b'FWS':
        body = raw[8:]
    else:
        return []
        
    text = body.decode('utf-8', errors='ignore')
    matches = hanzi_regex.findall(text)
    
    # Filter out common ActionScript system symbols if any, keep distinct phrases
    clean_matches = []
    seen = set()
    for m in matches:
        if m not in seen and len(m) >= 2:
            seen.add(m)
            clean_matches.append(m)
    return clean_matches

def scan_all_maps():
    print("======================================================================")
    print("        RÀ SOÁT TẤT CẢ MAP GAME TÌM CHỮ TIẾNG TRUNG CÒN TỒN ĐỌNG      ")
    print("======================================================================")
    
    # We scan all unique map IDs from Map_10001 to Map_10409 and 1.swf to 259.swf
    processed_ids = set()
    map_files = sorted(list(MAP_DIR.glob("Map_*.swf")))
    
    found_maps = []
    
    for mf in map_files:
        # Extract map number from name e.g. Map_10001 -> 1
        m = re.search(r'Map_(\d+)', mf.name)
        if not m:
            continue
        full_num = int(m.group(1))
        short_num = full_num - 10000 if full_num > 10000 else full_num
        
        if short_num in processed_ids:
            continue
        processed_ids.add(short_num)
        
        matches = extract_hanzi_from_swf(mf)
        if matches:
            v_name = map_names.get(short_num, f"Bản đồ {short_num}")
            found_maps.append({
                "id": short_num,
                "full_id": full_num,
                "file": mf.name,
                "path": str(mf.relative_to(ROOT_DIR)),
                "name": v_name,
                "sample_texts": matches[:8],
                "total_phrases": len(matches)
            })

    print(f"\nĐã rà soát {len(processed_ids)} map game.")
    print(f"Phát hiện {len(found_maps)} map có chứa chuỗi chữ tiếng Trung còn lại:\n")
    
    for item in found_maps:
        texts_str = ", ".join([f'"{t}"' for t in item["sample_texts"][:5]])
        print(f"* [Map {item['id']:02d}] {item['name']} ({item['file']}) - {item['total_phrases']} cụm chữ:")
        print(f"   Đường dẫn: {item['path']}")
        print(f"   Chữ mẫu: {texts_str}")
        print()

    # Save to report artifact/json
    return found_maps

if __name__ == "__main__":
    scan_all_maps()
