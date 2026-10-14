#!/usr/bin/env python3
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from collections import defaultdict

sys.stdout.reconfigure(encoding="utf-8")

PROJECT_ROOT = Path("E:/Codex/Projects/Moly-Viet")

files = {
    "gamesvr_questions": PROJECT_ROOT / "archive/source/taomee-server-leak-full/mole/gamesvr/conf/questions.xml",
    "class_questions": PROJECT_ROOT / "archive/source/taomee-server-leak-full/mole/online/conf/class_questions.xml",
    "kfc_questions": PROJECT_ROOT / "analysis/decompiled/ClientConfigDLL-binary/4_com.global.staticData.XMLInfo_kfcQuestion_com.global.staticData.XMLInfo_kfcQuestion.bin",
}

# Accurate patterns
PATTERNS = {
    "sovereignty": ["南海", "西沙", "南沙", "钓鱼岛", "台湾", "领海", "领土"],
    "emergency": ["110", "119", "120", "火警", "急救", "报警"],
    "national_identity": ["我国", "中国", "国旗", "国徽", "国歌", "建军节", "植树节", "少先队", "少先队员", "共青团", "共产主义"],
    "dynasty_history": ["朝代", "皇帝", "唐朝", "宋朝", "元朝", "明朝", "清朝", "汉朝", "秦朝", "秦始皇", "李世民", "赵匡胤", "乾隆", "康熙", "雍正", "朱元璋", "刘邦", "项羽"],
    "hanzi_riddles": ["成语", "字谜", "猜字", "汉字", "偏旁", "部首", "笔画", "笔顺"],
}

results = defaultdict(list)

for fname, fpath in files.items():
    root = ET.parse(fpath).getroot()
    for q in root.findall(".//Question"):
        qid = q.attrib.get("ID", "")
        content = q.attrib.get("Content", "")
        oa = q.attrib.get("OptionA", "")
        ob = q.attrib.get("OptionB", "")
        oc = q.attrib.get("OptionC", "")
        od = q.attrib.get("OptionD", "")
        ans = q.attrib.get("Answer", "")
        full = f"{content} {oa} {ob} {oc} {od}"
        
        matched_category = None
        matched_word = None
        for cat, words in PATTERNS.items():
            for w in words:
                if w in full:
                    matched_category = cat
                    matched_word = w
                    break
            if matched_category:
                break
        
        if matched_category:
            results[matched_category].append({
                "file": fname,
                "id": qid,
                "matched_word": matched_word,
                "content": content,
                "options": [oa, ob, oc, od],
                "answer": ans,
            })

for cat, items in results.items():
    print(f"\nCategory: {cat} -> {len(items)} items")
    by_file = defaultdict(int)
    for it in items:
        by_file[it["file"]] += 1
    for f, c in by_file.items():
        print(f"  {f}: {c}")

print(f"\nTotal flagged questions: {sum(len(items) for items in results.values())}")
