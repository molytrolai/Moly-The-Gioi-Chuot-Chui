#!/usr/bin/env python3
"""Scanner for questions with sensitive, geopolitical, or culturally biased content."""

import xml.etree.ElementTree as ET
from pathlib import Path
import json

files = [
    Path("E:/Codex/Projects/Moly-Viet/archive/source/taomee-server-leak-full/mole/gamesvr/conf/questions.xml"),
    Path("E:/Codex/Projects/Moly-Viet/archive/source/taomee-server-leak-full/mole/online/conf/questions.xml"),
    Path("E:/Codex/Projects/Moly-Viet/archive/source/taomee-server-leak-full/mole/online/conf/class_questions.xml"),
]

keywords = [
    "南海", "西沙", "南沙", "钓鱼岛", "我国", "中国", "台湾", "火警", "报警", "急救", "首都", "国旗", "国徽"
]

flagged = []

for f in files:
    if not f.exists():
        continue
    try:
        content = f.read_text(encoding="utf-8", errors="ignore")
        root = ET.fromstring(content)
        for q in root.findall(".//Question"):
            qid = q.attrib.get("ID")
            text = q.attrib.get("Content", "")
            oa = q.attrib.get("OptionA", "")
            ob = q.attrib.get("OptionB", "")
            oc = q.attrib.get("OptionC", "")
            od = q.attrib.get("OptionD", "")
            ans = q.attrib.get("Answer", "")
            full = f"{text} {oa} {ob} {oc} {od}"
            for kw in keywords:
                if kw in full:
                    flagged.append({
                        "file": f.name,
                        "id": qid,
                        "keyword": kw,
                        "content": text,
                        "optionA": oa,
                        "optionB": ob,
                        "optionC": oc,
                        "optionD": od,
                        "answer": ans,
                    })
                    break
    except Exception as e:
        print("Error reading", f, e)

output_path = Path("E:/Codex/Projects/Moly-Viet/data/server/flagged_questions.json")
output_path.write_text(json.dumps(flagged, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"Total flagged questions: {len(flagged)}")
