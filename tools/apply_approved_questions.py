#!/usr/bin/env python3
"""Comprehensive Minigame Question Audit & Sanitizer for Moly-Viet."""

import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path

PROJECT_ROOT = Path("E:/Codex/Projects/Moly-Viet")

QUESTION_FILES = {
    "gamesvr_questions": PROJECT_ROOT / "archive/source/taomee-server-leak-full/mole/gamesvr/conf/questions.xml",
    "online_questions": PROJECT_ROOT / "archive/source/taomee-server-leak-full/mole/online/conf/questions.xml",
    "class_questions": PROJECT_ROOT / "archive/source/taomee-server-leak-full/mole/online/conf/class_questions.xml",
    "tv_question": PROJECT_ROOT / "archive/source/taomee-server-leak-full/mole/online/conf/tv_question.xml",
    "kfc_questions": PROJECT_ROOT / "analysis/decompiled/ClientConfigDLL-binary/4_com.global.staticData.XMLInfo_kfcQuestion_com.global.staticData.XMLInfo_kfcQuestion.bin",
}

# 1. First: Apply approved replacements to gamesvr_questions, online_questions, class_questions
APPROVED_REPLACEMENTS_QUESTIONS = {
    "1": {
        "Content": "Khi phát hiện có đám cháy hoặc hỏa hoạn, số điện thoại khẩn cấp gọi Cứu hỏa tại Việt Nam là gì?",
        "OptionA": "113",
        "OptionB": "114",
        "OptionC": "115",
        "OptionD": "112",
        "Answer": "2",
        "Reason": "Sửa số báo cháy cứu hỏa từ 119 (Trung Quốc) thành 114 (Việt Nam)",
    },
    "6": {
        "Content": "Biển nào sau đây có diện tích lớn nhất trên thế giới?",
        "OptionA": "Biển Caribe",
        "OptionB": "Biển Đen",
        "OptionC": "Biển San Hô (Coral Sea)",
        "OptionD": "Biển Đỏ",
        "Answer": "3",
        "Reason": "Loại bỏ lựa chọn cài cắm chủ quyền 'Biển Nam Hải của Trung Quốc'",
    },
    "7": {
        "Content": "Phong trào 'Tết trồng cây' đầy ý nghĩa tại Việt Nam vào mỗi dịp đầu xuân được khởi xướng bởi ai?",
        "OptionA": "Chủ tịch Hồ Chí Minh",
        "OptionB": "Đại tướng Võ Nguyên Giáp",
        "OptionC": "Nhà giáo Chu Văn An",
        "OptionD": "Danh y Tuệ Tĩnh",
        "Answer": "1",
        "Reason": "Thay ngày Tết trồng cây TQ 12/3 bằng Tết trồng cây mùa xuân của Bác Hồ",
    },
    "10": {
        "Content": "Hòn đảo tự nhiên lớn nhất thế giới hiện nay là hòn đảo nào?",
        "OptionA": "Đảo Greenland",
        "OptionB": "Đảo Madagascar",
        "OptionC": "Đảo Borneo",
        "OptionD": "Đảo New Guinea",
        "Answer": "1",
        "Reason": "Thay câu hỏi so sánh đảo nội địa TQ bằng kiến thức địa lý thế giới chuẩn xác",
    },
    "27": {
        "Content": "Hồ nước ngọt tự nhiên trên núi lớn nhất của Việt Nam là hồ nào?",
        "OptionA": "Hồ Tây (Hà Nội)",
        "OptionB": "Hồ Ba Bể (Bắc Kạn)",
        "OptionC": "Hồ Tơ Nưng (Gia Lai)",
        "OptionD": "Hồ Dầu Tiếng",
        "Answer": "2",
        "Reason": "Thay hồ Thanh Hải TQ bằng Hồ Ba Bể Việt Nam",
    },
    "52": {
        "Content": "Vườn quốc gia đầu tiên được thành lập tại Việt Nam (năm 1962) là vườn quốc gia nào?",
        "OptionA": "Vườn quốc gia Ba Vì",
        "OptionB": "Vườn quốc gia Cát Tiên",
        "OptionC": "Vườn quốc gia Cúc Phương",
        "OptionD": "Vườn quốc gia Phong Nha - Kẻ Bàng",
        "Answer": "3",
        "Reason": "Thay Trương Gia Giới TQ bằng Vườn quốc gia Cúc Phương",
    },
    "68": {
        "Content": "Tại Việt Nam, ba đầu số khẩn cấp 113 - 114 - 115 lần lượt phục vụ mục đích gì?",
        "OptionA": "Cứu hỏa - Công an - Cấp cứu",
        "OptionB": "Cảnh sát - Cứu hỏa - Cấp cứu y tế",
        "OptionC": "Cấp cứu - Cứu hỏa - Điện lực",
        "OptionD": "Bưu điện - Cứu hỏa - Cảnh sát",
        "Answer": "2",
        "Reason": "Chuẩn hóa chức năng các đầu số khẩn cấp quốc gia tại Việt Nam",
    },
    "86": {
        "Content": "Thác nước tự nhiên lớn và hùng vĩ nhất Việt Nam nằm trên biên giới tại tỉnh Cao Bằng tên là gì?",
        "OptionA": "Thác Cam Ly",
        "OptionB": "Thác Bản Giốc",
        "OptionC": "Thác Pongour",
        "OptionD": "Thác Datanla",
        "Answer": "2",
        "Reason": "Thay thác Hoàng Quả Thụ TQ bằng Thác Bản Giốc Việt Nam",
    },
    "136": {
        "Content": "Vận động viên đầu tiên mang về Huy chương Vàng Olympic lịch sử cho thể thao Việt Nam (năm 2016) là ai?",
        "OptionA": "Hoàng Xuân Vinh (Bắn súng)",
        "OptionB": "Trần Hiếu Ngân (Taekwondo)",
        "OptionC": "Hoàng Anh Tuấn (Cử tạ)",
        "OptionD": "Nguyễn Thị Ánh Viên (Bơi lội)",
        "Answer": "1",
        "Reason": "Thay vận động viên TQ bằng xạ thủ Hoàng Xuân Vinh",
    },
    "260": {
        "Content": "Nơi nào trên Trái Đất từng ghi nhận nhiệt độ tự nhiên cao kỷ lục lên tới 56.7°C?",
        "OptionA": "Thung lũng Chết (Death Valley, Mỹ)",
        "OptionB": "Sa mạc Sahara",
        "OptionC": "Cao nguyên Tây Tạng",
        "OptionD": "Rừng rậm nhiệt đới Amazon",
        "Answer": "1",
        "Reason": "Loại bỏ lựa chọn cài cắm 'Quần đảo Nam Sa' vi phạm chủ quyền",
    },
    "459": {
        "Content": "Đại dương nào có diện tích lớn nhất trên hành tinh Trái Đất?",
        "OptionA": "Đại Tây Dương",
        "OptionB": "Ấn Độ Dương",
        "OptionC": "Thái Bình Dương",
        "OptionD": "Bắc Băng Dương",
        "Answer": "3",
        "Reason": "Loại bỏ câu hỏi quy nạp 'bốn vùng biển nước ta gồm Nam Hải'",
    },
    "580": {
        "Content": "Nếu phát hiện có người bị điện giật, bước quan trọng đầu tiên cần làm ngay là gì?",
        "OptionA": "Dùng tay không kéo nạn nhân ra",
        "OptionB": "Nhanh chóng ngắt cầu dao/nguồn điện an toàn",
        "OptionC": "Đổ nước vào người nạn nhân",
        "OptionD": "Đứng yên quan sát",
        "Answer": "2",
        "Reason": "Thay lựa chọn gọi 110 TQ bằng kỹ năng sơ cứu điện giật chuẩn",
    },
}

APPROVED_REPLACEMENTS_CLASS = {
    "1": {
        "Content": "Vừa gà vừa chó, bó lại cho tròn, 36 con, 100 chân chẵn. Hỏi có bao nhiêu con gà và bao nhiêu con chó?",
        "OptionA": "22 gà, 14 chó",
        "OptionB": "24 gà, 12 chó",
        "OptionC": "20 gà, 16 chó",
        "OptionD": "18 gà, 18 chó",
        "Answer": "1",
        "Reason": "Thay câu đố thành ngữ chữ Hán bằng toán đố dân gian vui Việt Nam",
    },
    "13": {
        "Content": "Một chú ốc sên leo lên cây cau cao 10m. Ban ngày leo 3m, ban đêm tụt 2m. Hỏi sau bao nhiêu ngày ốc sên chạm đỉnh cây?",
        "OptionA": "10 ngày",
        "OptionB": "8 ngày",
        "OptionC": "7 ngày",
        "OptionD": "9 ngày",
        "Answer": "2",
        "Reason": "Thay câu đố chiết tự chữ Hán bằng câu đố tư duy logic",
    },
    "173": {
        "Content": "Hòn đảo có diện tích tự nhiên lớn nhất của Việt Nam là đảo nào?",
        "OptionA": "Đảo Cát Bà",
        "OptionB": "Đảo Phú Quốc",
        "OptionC": "Đảo Côn Sơn",
        "OptionD": "Đảo Lý Sơn",
        "Answer": "2",
        "Reason": "Thay câu hỏi chính trị đảo Đài Loan bằng Đảo Phú Quốc Việt Nam",
    },
}

def apply_replacements(xml_file: Path, replacements: dict):
    if not xml_file.exists():
        return 0
    content = xml_file.read_text(encoding="utf-8", errors="ignore")
    root = ET.fromstring(content)
    modified = 0
    for q in root.findall(".//Question"):
        qid = q.attrib.get("ID")
        if qid in replacements:
            rep = replacements[qid]
            q.attrib["Content"] = rep["Content"]
            q.attrib["OptionA"] = rep["OptionA"]
            q.attrib["OptionB"] = rep["OptionB"]
            q.attrib["OptionC"] = rep["OptionC"]
            q.attrib["OptionD"] = rep["OptionD"]
            q.attrib["Answer"] = rep["Answer"]
            modified += 1
    if modified > 0:
        new_xml = ET.tostring(root, encoding="utf-8", xml_declaration=True).decode("utf-8")
        xml_file.write_text(new_xml, encoding="utf-8")
    return modified

# Run initial application
count1 = apply_replacements(QUESTION_FILES["online_questions"], APPROVED_REPLACEMENTS_QUESTIONS)
count2 = apply_replacements(QUESTION_FILES["gamesvr_questions"], APPROVED_REPLACEMENTS_QUESTIONS)
count3 = apply_replacements(QUESTION_FILES["class_questions"], APPROVED_REPLACEMENTS_CLASS)
print(f"Applied approved replacements: online={count1}, gamesvr={count2}, class={count3}")

# Copy sanitized online_questions & class_questions to local-overrides if needed
overrides_dir = PROJECT_ROOT / "archive/clients/local-overrides/mole.61.com/resource/xml/question"
overrides_dir.mkdir(parents=True, exist_ok=True)
if QUESTION_FILES["online_questions"].exists():
    (overrides_dir / "questions.xml").write_bytes(QUESTION_FILES["online_questions"].read_bytes())
if QUESTION_FILES["class_questions"].exists():
    (overrides_dir / "class_questions.xml").write_bytes(QUESTION_FILES["class_questions"].read_bytes())
print("Mirrored sanitized questions into local-overrides.")
