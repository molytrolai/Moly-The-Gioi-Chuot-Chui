#!/usr/bin/env python3
"""Inspect national symbols and holidays questions."""

import json
from pathlib import Path

data = json.loads(Path("E:/Codex/Projects/Moly-Viet/data/server/classified_questions.json").read_text(encoding="utf-8"))

out_lines = []
out_lines.append("=== SAMPLE NATIONAL / HOLIDAYS / CHINA SPECIFIC QUESTIONS ===")

for idx, q in enumerate(data["national_symbols_holidays"][:30], 1):
    out_lines.append(f"\n[{idx}] File: {q['file']} | ID: {q['id']}")
    out_lines.append(f"Content: {q['content']}")
    out_lines.append(f"A: {q['optionA']} | B: {q['optionB']} | C: {q['optionC']} | D: {q['optionD']}")
    out_lines.append(f"Ans: {q['answer']}")

Path("E:/Codex/Projects/Moly-Viet/data/server/dump_national.txt").write_text("\n".join(out_lines), encoding="utf-8")
print(f"Wrote {len(data['national_symbols_holidays'])} national questions to dump_national.txt")
