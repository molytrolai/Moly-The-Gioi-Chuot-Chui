#!/usr/bin/env python3
"""Translate World Map Tips XML (tag 52) in ClientConfigDLL."""

import sys
import xml.etree.ElementTree as ET
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT_DIR = Path(__file__).resolve().parents[1]
SRC_BIN = ROOT_DIR / "work" / "exported" / "ClientConfigDLL" / "52_com.global.staticData.XMLInfo_wordMapTipConfig_com.global.staticData.XMLInfo_wordMapTipConfig.bin"
OUT_BIN = ROOT_DIR / "work" / "translated_52_wordMapTipConfig.bin"

TIPS_TRANSLATIONS = {
    # Headers & Lists
    "庄园明星": "Ngôi sao Vương quốc",
    "庄园游戏": "Trò chơi Vương quốc",
    "区域场景": "Khu vực & Địa điểm",
    "世界地图tips数据": "Dữ liệu Hướng dẫn Bản đồ Thế giới",
    
    # Map Names
    "摩尔城堡": "Lâu đài Moly", "开心农场": "Nông trại Vui vẻ", "浆果丛林": "Rừng Quả Mọng",
    "黑森林": "Rừng Hắc Ám", "爱心广场": "Quảng trường Ái Tâm", "库拉城堡": "Lâu đài Kula",
    "阳光牧场": "Đồng cỏ Ánh Dương", "神秘湖": "Hồ Thần Bí", "淘淘乐街": "Phố Mua sắm Taotao",
    "东部游乐场": "Công viên Phía Đông", "摩尔拉雅山": "Núi Molylaya", "吉普豆村": "Làng Đậu Jipu",
    "前哨战": "Tiền đồn Kỵ sĩ", "西部游乐场": "Công viên Phía Tây", "虫虫谷": "Thung lũng Côn Trùng",
    
    # Locations
    "城堡大厅": "Đại sảnh Lâu đài", "城堡书房": "Thư viện Lâu đài", "城堡露台": "Ban công Lâu đài",
    "城堡二楼": "Tầng hai Lâu đài", "城堡露天花园": "Vườn hoa Lâu đài", "么么的卧室": "Phòng ngủ Meme",
    "摩尔餐厅": "Nhà hàng Moly", "超级拉姆俱乐部": "Câu lạc bộ Super Lamu", "城堡地下": "Tầng hầm Lâu đài",
    "梅森小屋": "Túp lều Mason", "农场发明屋": "Xưởng sáng chế Nông trại", "彩虹瀑布": "Thác Cầu Vồng",
    "天空树": "Cây Bầu Trời", "遗忘田园": "Đồng quê Lãng Quên", "神秘花海": "Biển Hoa Thần Bí",
    "誓言小屋": "Túp lều Thề Nguyện", "摩摩训练场": "Trường Đua Moly", "森林训练场": "Trường Luyện Tập Rừng",
    "骑士训练营": "Trại Huấn luyện Kỵ sĩ", "元素骑士训练营": "Trại Huấn luyện Nguyên Tố",
    "云雾谜桥": "Cầu Mây Bí Ẩn", "拉姆世界丛林": "Rừng Thế giới Lamu", "藏宝神殿": "Đền Thần Kho Báu",
    "拉姆神秘世界": "Thế giới Bí ẩn Lamu", "时光圣殿": "Đền Thần Thời Gian", "藤蔓森林": "Rừng Dây Leo",
    "爱心教堂内": "Bên trong Nhà thờ Ái Tâm", "爱心救治室": "Phòng Cứu chữa Ái Tâm",
    "爱心向导社": "Hội Hướng dẫn viên Ái Tâm", "摩尔报社": "Tòa soạn Báo Moly",
    "摩尔电视台": "Đài Truyền hình Moly", "摩尔庄园警署": "Đồn Cảnh sát Moly", "摩尔银行": "Ngân hàng Moly",
    
    # NPC Names
    "粒粒": "Lili", "小乖": "Tiểu Quai", "洛克": "Locke", "尼克": "Nick", "捷克": "Jack",
    "么么": "Meme", "梅森": "Mason", "大卫": "David", "摩乐乐": "Molele", "丫丽": "Yali",
    "布多多": "Buduoduo", "布少少": "Bushaoshao", "尤瑞克": "Yurick", "吉娜": "Gina",
    "土林长老": "Trưởng lão Tulin", "克劳神父": "Mục sư Clau", "安迪": "Andy",
    "杰西": "Jessie", "兔兔": "Thỏ TuTu", "艾米": "Amy", "拉小菲": "Laxiofei", "艾尔": "Air",
    
    # Mini-game Names
    "经营冰激凌小屋": "Kinh doanh Tiệm Kem", "拼图大师": "Bậc thầy Ghép hình",
    "五子棋": "Cờ Caro", "摩罗斯方块": "Xếp hình Moly", "开心大厨": "Đầu bếp Vui vẻ",
    "餐厅打工": "Làm thêm Nhà hàng", "包饺子": "Gói sủi cảo", "摩尔小农夫": "Nông dân Moly",
    "捉萤火虫": "Bắt đom đóm", "摘果实": "Hái quả ngọt", "漂流": "Thuyền trôi sông",
    "天使卡罗拉": "Thiên thần Corolla", "猜尤瑞克喜欢": "Đoán ý Yurick", "小屋寻踪": "Tìm dấu vết",
    "弓箭训练": "Bắn cung", "攀爬训练": "Leo núi", "敏捷训练": "Nhanh nhẹn",
    "反应训练": "Phản xạ", "速度训练": "Tốc độ", "元素训练": "Nguyên tố",
    "救治拉姆": "Chữa bệnh cho Lamu", "零花钱大作战": "Đại chiến Tiền tiết kiệm",
    "营救人质": "Giải cứu con tin", "射击训练": "Tập bắn súng",
}

def translate_tips_text(txt):
    res = txt
    for k, v in TIPS_TRANSLATIONS.items():
        res = res.replace(k, v)
    return res

def main():
    content = SRC_BIN.read_text(encoding="utf-8")
    root = ET.fromstring(content)
    
    # Translate attributes
    for elem in root.iter():
        for attr in ["info", "type_name", "list_name", "list_msg"]:
            if attr in elem.attrib:
                elem.attrib[attr] = translate_tips_text(elem.attrib[attr])
                
    out_xml = ET.tostring(root, encoding="utf-8").decode("utf-8")
    header = '<?xml version="1.0" encoding="UTF-8"?>\n'
    if not out_xml.startswith("<?xml"):
        out_xml = header + out_xml
        
    OUT_BIN.write_text(out_xml, encoding="utf-8")
    SRC_BIN.write_text(out_xml, encoding="utf-8")
    print(f"Successfully translated World Map Tips XML to {OUT_BIN} and updated {SRC_BIN}!")

if __name__ == "__main__":
    main()
