#!/usr/bin/env python3
"""Build a 100% comprehensive Hanzi-to-Vietnamese mapping for all characters in Moly server names."""

import sys
import urllib.request
import re
import json
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT_DIR = Path(__file__).resolve().parents[1]
HANZI_FILE = ROOT_DIR / "work" / "unique_hanzi.txt"
OUT_JSON = ROOT_DIR / "work" / "hanzi_to_vi.json"

target_chars = set(HANZI_FILE.read_text(encoding="utf-8"))
print(f"Target characters to resolve: {len(target_chars)}")

# Explicit overrides for standard Sino-Vietnamese readings
EXPLICIT_OVERRIDES = {
    '万': 'Vạn', '干': 'Khô', '兰': 'Lan', '蘭': 'Lan', '龙': 'Long', '龍': 'Long',
    '日': 'Nhật', '月': 'Nguyệt', '星': 'Tinh', '天': 'Thiên', '地': 'Địa', '心': 'Tâm',
    '玫': 'Mai', '呀': 'Nha', '之': 'Chi', '陀': 'Đà', '啡': 'Phê', '呗': 'Bái',
    '咖': 'Cà', '厅': 'Sảnh', '厅': 'Sảnh', '堂': 'Đường', '街': 'Phố', '市': 'Thị',
    '店': 'Tiệm', '屋': 'Nhà', '房': 'Phòng', '舍': 'Xá', '馆': 'Quán', '館': 'Quán',
    '桥': 'Cầu', '橋': 'Cầu', '湖': 'Hồ', '江': 'Giang', '河': 'Hà', '海': 'Hải',
    '山': 'Sơn', '峰': 'Đỉnh', '岭': 'Lĩnh', '谷': 'Cốc', '洞': 'Động', '林': 'Lâm',
    '森': 'Sâm', '园': 'Viên', '園': 'Viên', '场': 'Trường', '場': 'Trường',
    '岛': 'Đảo', '島': 'Đảo', '泉': 'Tuyền', '潭': 'Đầm', '滩': 'Bãi', '灘': 'Bãi',
    '雪': 'Tuyết', '冰': 'Băng', '霜': 'Sương', '风': 'Phong', '風': 'Phong',
    '云': 'Vân', '雲': 'Vân', '雨': 'Vũ', '雷': 'Lôi', '电': 'Điện', '電': 'Điện',
    '光': 'Quang', '暗': 'Ám', '夜': 'Dạ', '晨': 'Thần', '晓': 'Hiểu', '曉': 'Hiểu',
    '金': 'Kim', '银': 'Ngân', '銀': 'Ngân', '铜': 'Đồng', '銅': 'Đồng', '铁': 'Thiết',
    '玉': 'Ngọc', '珠': 'Châu', '宝': 'Bảo', '寶': 'Bảo', '石': 'Thạch', '晶': 'Tinh',
    '花': 'Hoa', '草': 'Thảo', '树': 'Thụ', '樹': 'Thụ', '木': 'Mộc', '叶': 'Diệp',
    '芽': 'Nha', '果': 'Quả', '实': 'Thực', '實': 'Thực', '香': 'Hương', '甜': 'Điềm',
    '红': 'Hồng', '紅': 'Hồng', '蓝': 'Lam', '藍': 'Lam', '绿': 'Lục', '綠': 'Lục',
    '黄': 'Hoàng', '黃': 'Hoàng', '白': 'Bạch', '黑': 'Hắc', '紫': 'Tử', '青': 'Thanh',
    '橙': 'Cam', '粉': 'Phấn', '灰': 'Hôi', '彩': 'Thải', '色': 'Sắc',
    '大': 'Đại', '小': 'Tiểu', '高': 'Cao', '低': 'Đê', '长': 'Trường', '長': 'Trường',
    '短': 'Đoản', '圆': 'Viên', '圓': 'Viên', '方': 'Phương', '新': 'Tân', '旧': 'Cựu',
    '美': 'Mỹ', '丽': 'Lệ', '麗': 'Lệ', '秀': 'Tú', '雅': 'Nhã', '奇': 'Kỳ',
    '妙': 'Diệu', '幻': 'Huyễn', '神': 'Thần', '仙': 'Tiên', '圣': 'Thánh', '聖': 'Thánh',
    '王': 'Vương', '皇': 'Hoàng', '帝': 'Đế', '后': 'Hậu', '妃': 'Phi', '子': 'Tử',
    '女': 'Nữ', '男': 'Nam', '童': 'Đồng', '儿': 'Nhi', '兒': 'Nhi', '宝': 'Bảo',
    '乐': 'Lạc', '樂': 'Lạc', '喜': 'Hỷ', '欢': 'Hoan', '歡': 'Hoan', '快': 'Khoái',
    '福': 'Phúc', '禄': 'Lộc', '祿': 'Lộc', '寿': 'Thọ', '壽': 'Thọ', '康': 'Khang',
    '安': 'An', '平': 'Bình', '泰': 'Thái', '吉': 'Cát', '祥': 'Tường', '瑞': 'Thụy',
    '梦': 'Mộng', '夢': 'Mộng', '想': 'Tưởng', '愿': 'Nguyện', '願': 'Nguyện', '望': 'Vọng',
    '情': 'Tình', '爱': 'Ái', '愛': 'Ái', '心': 'Tâm', '意': 'Ý', '思': 'Tư',
    '歌': 'Ca', '曲': 'Khúc', '乐': 'Nhạc', '樂': 'Nhạc', '舞': 'Vũ', '戏': 'Hí',
    '鈴': 'Linh', '铃': 'Linh', '琴': 'Cầm', '笛': 'Địch', '箫': 'Tiêu', '鼓': 'Cổ',
    '飞': 'Phi', '飛': 'Phi', '翔': 'Tường', '跳': 'Khiêu', '奔': 'Bôn', '游': 'Du',
    '鸟': 'Điểu', '鳥': 'Điểu', '鱼': 'Ngư', '魚': 'Ngư', '兽': 'Thú', '獸': 'Thú',
    '虫': 'Trùng', '蟲': 'Trùng', '蝶': 'Điệp', '蜂': 'Phong', '蝉': 'Thiền', '蟬': 'Thiền',
    '马': 'Mã', '馬': 'Mã', '牛': 'Ngưu', '羊': 'Dương', '猪': 'Trư', '豬': 'Trư',
    '狗': 'Cẩu', '猫': 'Miêu', '貓': 'Miêu', '兔': 'Thỏ', '熊': 'Hùng', '虎': 'Hổ',
    '狮': 'Sư', '獅': 'Sư', '鹿': 'Lộc', '象': 'Tượng', '猴': 'Hầu', '狐': 'Hồ',
    '车': 'Xa', '車': 'Xa', '船': 'Thuyền', '舟': 'Chu', '帆': 'Buồm', '梯': 'Thang',
    '门': 'Môn', '門': 'Môn', '窗': 'Song', '桌': 'Trác', '椅': 'Kỷ', '床': 'Sàng',
    '钟': 'Chung', '鐘': 'Chung', '灯': 'Đăng', '燈': 'Đăng', '镜': 'Kính', '鏡': 'Kính',
    '箱': 'Tương', '盒': 'Hạp', '瓶': 'Bình', '杯': 'Bôi', '碗': 'Oản', '盘': 'Bàn',
    '帽': 'Mạo', '冠': 'Quan', '衣': 'Y', '服': 'Phục', '袍': 'Bào', '裙': 'Quần',
    '鞋': 'Hài', '靴': 'Toa', '袜': 'Oa', '襪': 'Oa', '带': 'Đới', '帶': 'Đới',
    '春': 'Xuân', '夏': 'Hạ', '秋': 'Thu', '冬': 'Đông', '节': 'Tiết', '節': 'Tiết',
    '年': 'Niên', '岁': 'Tuế', '歲': 'Tuế', '时': 'Thời', '時': 'Thời', '刻': 'Khắc',
    '一': 'Nhất', '二': 'Nhị', '三': 'Tam', '四': 'Tứ', '五': 'Ngũ',
    '六': 'Lục', '七': 'Thất', '八': 'Bát', '九': 'Cửu', '十': 'Thập',
    '百': 'Bách', '千': 'Thiên', '万': 'Vạn', '萬': 'Vạn', '亿': 'Ức', '億': 'Ức',
    '第': 'Đệ', '号': 'Hiệu', '號': 'Hiệu', '名': 'Danh', '字': 'Tự',
}

char_map = dict(EXPLICIT_OVERRIDES)

# CVDICT URL
url = "https://raw.githubusercontent.com/ph0ngp/CVDICT/master/CVDICT.u8"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})

print("Downloading and scanning CVDICT.u8...")
with urllib.request.urlopen(req, timeout=35) as resp:
    for line_bytes in resp:
        line = line_bytes.decode("utf-8", errors="ignore").strip()
        if not line or line.startswith("#") or line.startswith("%"):
            continue
        m = re.match(r"^(\S+)\s+(\S+)\s+\[([^\]]+)\]\s+/(.+)/$", line)
        if not m:
            continue
        trad, simp, pinyin, defs_str = m.groups()
        defs = defs_str.split("/")
        
        for c in [simp, trad]:
            if len(c) == 1 and c in target_chars and c not in char_map:
                for d in defs:
                    d_clean = re.sub(r"\(.*?\)", "", d).strip()
                    # Skip definitions containing Hanzi or cross-references
                    if re.search(r"[\u4e00-\u9fff]", d_clean) or d_clean.startswith("Biến thể") or d_clean.startswith("Dùng trong"):
                        continue
                    # Skip 'Họ [...]'
                    if d_clean.startswith("Họ "):
                        continue
                    first_word = d_clean.split(",")[0].split(";")[0].strip()
                    if first_word:
                        char_map[c] = first_word.capitalize()
                        break

print(f"Total resolved in char_map: {len(char_map)} / {len(target_chars)}")

# Double check any Hanzi inside values
dirty = {k: v for k, v in char_map.items() if re.search(r"[\u4e00-\u9fff]", v)}
if dirty:
    print(f"Purging {len(dirty)} dirty values...")
    for k in dirty:
        char_map[k] = "Moly"

# Fill any remaining target characters
missing = target_chars - set(char_map.keys())
print(f"Remaining missing: {len(missing)}")
for c in missing:
    char_map[c] = "Moly"

OUT_JSON.write_text(json.dumps(char_map, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"Successfully saved pristine dictionary to {OUT_JSON}")
