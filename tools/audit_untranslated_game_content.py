#!/usr/bin/env python3
"""Comprehensive Translation & Localization Audit for Moly - Thế Giới Chuột Chũi VN."""

import os
import re
import sys
from pathlib import Path

CHINESE_PATTERN = re.compile(r'[\u4e00-\u9fff]+')
MIRROR_ROOT = Path("archive/clients/offline-mirror/mole.61.com")
OVERRIDES_ROOT = Path("archive/clients/local-overrides/mole.61.com")

def audit_xml_configs():
    xml_files = list(MIRROR_ROOT.rglob("*.xml"))
    total_xml = len(xml_files)
    chinese_xml_files = []
    
    for p in xml_files:
        try:
            content = p.read_text(encoding="utf-8")
        except:
            try:
                content = p.read_text(encoding="gbk", errors="ignore")
            except:
                continue
        matches = CHINESE_PATTERN.findall(content)
        if matches:
            chinese_xml_files.append((p.relative_to(MIRROR_ROOT), len(matches), matches[:5]))
            
    return total_xml, chinese_xml_files

def audit_map_swfs():
    map_dir = MIRROR_ROOT / "resource" / "map"
    map_swfs = list(map_dir.glob("*.swf"))
    
    # Categorize common maps
    core_maps = []
    for p in map_swfs:
        name = p.stem
        core_maps.append(name)
    return len(map_swfs), core_maps

def audit_ui_swfs():
    ui_swfs = list((MIRROR_ROOT / "resource" / "ui").glob("*.swf"))
    ext_swfs = list((MIRROR_ROOT / "module" / "external").glob("*.swf"))
    dll_swfs = list((MIRROR_ROOT / "dll").glob("*.swf"))
    return [p.name for p in ui_swfs], [p.name for p in ext_swfs], [p.name for p in dll_swfs]

def main():
    total_xml, zh_xmls = audit_xml_configs()
    total_maps, map_names = audit_map_swfs()
    ui_list, ext_list, dll_list = audit_ui_swfs()
    
    print(f"Total XMLs: {total_xml}, With Chinese: {len(zh_xmls)}")
    print(f"Total Maps: {total_maps}")
    print(f"UI SWFs: {ui_list}")
    print(f"External SWFs: {ext_list}")
    print(f"DLL SWFs: {dll_list}")

if __name__ == "__main__":
    main()
