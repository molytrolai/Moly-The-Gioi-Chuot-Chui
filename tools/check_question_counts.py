#!/usr/bin/env python3
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from collections import Counter

sys.stdout.reconfigure(encoding="utf-8")

PROJECT_ROOT = Path("E:/Codex/Projects/Moly-Viet")

files = {
    "gamesvr_questions": PROJECT_ROOT / "archive/source/taomee-server-leak-full/mole/gamesvr/conf/questions.xml",
    "class_questions": PROJECT_ROOT / "archive/source/taomee-server-leak-full/mole/online/conf/class_questions.xml",
    "kfc_questions": PROJECT_ROOT / "analysis/decompiled/ClientConfigDLL-binary/4_com.global.staticData.XMLInfo_kfcQuestion_com.global.staticData.XMLInfo_kfcQuestion.bin",
}

for name, path in files.items():
    root = ET.parse(path).getroot()
    questions = root.findall(".//Question")
    print(f"File {name}: {len(questions)} questions")
