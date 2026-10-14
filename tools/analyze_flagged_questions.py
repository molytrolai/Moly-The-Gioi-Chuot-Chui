#!/usr/bin/env python3
"""Detailed analysis and classification of flagged questions."""

import json
from pathlib import Path

raw_data = json.loads(Path("E:/Codex/Projects/Moly-Viet/data/server/flagged_questions.json").read_text(encoding="utf-8"))

# Categorize into:
# 1. SOVEREIGNTY / GEOPOLITICAL (Nam Hải, Hoàng Sa, Trường Sa, lãnh thổ, địa lý TQ)
# 2. EMERGENCY / CIVIC PHONE NUMBERS (110, 119, 120 -> 113, 114, 115)
# 3. NATIONAL / "NƯỚC TA" / TQ NATIONAL SYMBOLS (quốc kỳ 5 sao, quốc huy TQ, ngày lễ TQ)
# 4. CHINESE DYNASTIES / HISTORICAL SPECIFIC TO CHINA
# 5. GENERAL TRIVIA (science, universal facts)

categories = {
    "sovereignty_geopolitical": [],
    "emergency_numbers": [],
    "national_symbols_holidays": [],
    "china_history_politics": [],
    "culture_wordplay": [],
}

for q in raw_data:
    txt = q["content"] + " " + q["optionA"] + " " + q["optionB"] + " " + q["optionC"] + " " + q["optionD"]
    kw = q["keyword"]
    
    if any(k in txt for k in ["南海", "西沙", "南沙", "钓鱼岛", "台湾", "领海", "领土"]):
        categories["sovereignty_geopolitical"].append(q)
    elif any(k in txt for k in ["火警", "报警", "急救", "110", "119", "120"]):
        categories["emergency_numbers"].append(q)
    elif any(k in txt for k in ["国旗", "国徽", "首都", "国歌", "植树节", "我国"]):
        if any(h in txt for h in ["朝代", "皇帝", "唐朝", "清朝", "明朝", "汉朝", "秦"]):
            categories["china_history_politics"].append(q)
        else:
            categories["national_symbols_holidays"].append(q)
    elif any(k in txt for k in ["朝代", "皇帝", "中国"]):
        categories["china_history_politics"].append(q)
    else:
        categories["culture_wordplay"].append(q)

summary = {cat: len(items) for cat, items in categories.items()}
print("Classification Summary:")
for k, v in summary.items():
    print(f"  {k}: {v}")

Path("E:/Codex/Projects/Moly-Viet/data/server/classified_questions.json").write_text(
    json.dumps(categories, ensure_ascii=False, indent=2), encoding="utf-8"
)
print("Saved classified questions to data/server/classified_questions.json")
