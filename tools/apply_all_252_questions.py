#!/usr/bin/env python3
"""Apply all 252 audited questions to game server and client configuration files."""

import sys
import json
import xml.etree.ElementTree as ET
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

PROJECT_ROOT = Path("E:/Codex/Projects/Moly-Viet")

JSON_AUDIT = PROJECT_ROOT / "data/server/moly_minigame_questions_audit.json"
audited_data = json.loads(JSON_AUDIT.read_text(encoding="utf-8"))

print(f"Loaded {len(audited_data)} audited questions from JSON.")

# Target paths
TARGET_FILES = {
    "gamesvr_questions.xml": [
        PROJECT_ROOT / "archive/source/taomee-server-leak-full/mole/gamesvr/conf/questions.xml",
        PROJECT_ROOT / "archive/source/taomee-server-leak-full/mole/online/conf/questions.xml",
        PROJECT_ROOT / "archive/clients/local-overrides/mole.61.com/resource/xml/question/questions.xml",
    ],
    "class_questions.xml": [
        PROJECT_ROOT / "archive/source/taomee-server-leak-full/mole/online/conf/class_questions.xml",
        PROJECT_ROOT / "archive/clients/local-overrides/mole.61.com/resource/xml/question/class_questions.xml",
    ],
    "kfc_questions.bin": [
        PROJECT_ROOT / "analysis/decompiled/ClientConfigDLL-binary/4_com.global.staticData.XMLInfo_kfcQuestion_com.global.staticData.XMLInfo_kfcQuestion.bin",
    ],
}

# Ensure destination directories exist
for target_list in TARGET_FILES.values():
    for p in target_list:
        p.parent.mkdir(parents=True, exist_ok=True)

# Organize replacements by source_file and question_id
replacements = {}
for item in audited_data:
    src = item["source_file"]
    qid = str(item["question_id"])
    if src not in replacements:
        replacements[src] = {}
    replacements[src][qid] = item

total_updated = 0

for src_name, file_targets in TARGET_FILES.items():
    if src_name not in replacements:
        continue
    items_for_src = replacements[src_name]
    print(f"\nProcessing {src_name} ({len(items_for_src)} replacements)...")

    for target_path in file_targets:
        if not target_path.exists():
            print(f"  Target does not exist: {target_path}")
            continue

        try:
            content = target_path.read_text(encoding="utf-8", errors="ignore")
            root = ET.fromstring(content)
            modified_count = 0

            for q in root.findall(".//Question"):
                qid = str(q.attrib.get("ID", ""))
                if qid in items_for_src:
                    rep = items_for_src[qid]
                    q.attrib["Content"] = rep["proposed_question_vi"]
                    q.attrib["OptionA"] = rep["proposed_options_vi"]["A"]
                    q.attrib["OptionB"] = rep["proposed_options_vi"]["B"]
                    q.attrib["OptionC"] = rep["proposed_options_vi"]["C"]
                    q.attrib["OptionD"] = rep["proposed_options_vi"]["D"]
                    q.attrib["Answer"] = str(rep["proposed_answer"])
                    modified_count += 1

            # Format and save XML with clean declaration
            xml_str = ET.tostring(root, encoding="utf-8").decode("utf-8")
            if not xml_str.startswith("<?xml"):
                xml_str = '<?xml version="1.0" encoding="utf-8"?>\n' + xml_str
            target_path.write_text(xml_str, encoding="utf-8")
            print(f"  [OK] Updated {modified_count} questions in: {target_path.relative_to(PROJECT_ROOT)}")
            total_updated += modified_count
        except Exception as e:
            print(f"  [ERROR] Updating {target_path}: {e}")

print(f"\nCompleted! Total question nodes updated across all files: {total_updated}")
