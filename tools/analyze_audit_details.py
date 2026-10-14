#!/usr/bin/env python3
import json
import sys
from collections import defaultdict
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

data_path = Path("E:/Codex/Projects/Moly-Viet/data/server/moly_minigame_questions_audit.json")
data = json.loads(data_path.read_text(encoding="utf-8"))

print("Total audited entries:", len(data))

by_cat = defaultdict(list)
for item in data:
    by_cat[item["category"]].append(item)

for cat, items in by_cat.items():
    print(f"\n=== CATEGORY: {cat} ({len(items)} items) ===")
    for it in items[:5]:
        print(f"  [{it['source_file']} ID {it['question_id']}] {it['old_question']}")
