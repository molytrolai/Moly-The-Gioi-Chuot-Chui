#!/usr/bin/env python3
"""Inspect specific sensitive questions."""

import json
from pathlib import Path

data = json.loads(Path("E:/Codex/Projects/Moly-Viet/data/server/classified_questions.json").read_text(encoding="utf-8"))

out_lines = []

out_lines.append("=== SOVEREIGNTY & GEOPOLITICAL (6 questions) ===")
for idx, q in enumerate(data["sovereignty_geopolitical"], 1):
    out_lines.append(f"\n[{idx}] File: {q['file']} | ID: {q['id']}")
    out_lines.append(f"Content: {q['content']}")
    out_lines.append(f"A: {q['optionA']} | B: {q['optionB']} | C: {q['optionC']} | D: {q['optionD']}")
    out_lines.append(f"Ans: {q['answer']}")

out_lines.append("\n=== EMERGENCY NUMBERS (9 questions) ===")
for idx, q in enumerate(data["emergency_numbers"], 1):
    out_lines.append(f"\n[{idx}] File: {q['file']} | ID: {q['id']}")
    out_lines.append(f"Content: {q['content']}")
    out_lines.append(f"A: {q['optionA']} | B: {q['optionB']} | C: {q['optionC']} | D: {q['optionD']}")
    out_lines.append(f"Ans: {q['answer']}")

Path("E:/Codex/Projects/Moly-Viet/data/server/dump_sensitive.txt").write_text("\n".join(out_lines), encoding="utf-8")
print("Wrote dump_sensitive.txt successfully!")
