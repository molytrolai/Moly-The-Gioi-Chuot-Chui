#!/usr/bin/env python3
"""Translate all 1200 server names in Login tag 408 to authentic Vietnamese."""

import sys
import re
import xml.etree.ElementTree as ET
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT_DIR = Path(__file__).resolve().parents[1]
SRC_BIN = ROOT_DIR / "work" / "exported" / "Login_bin" / "408_com.mole.login.LoginServerConfig_ServerName.bin"
OUT_BIN = ROOT_DIR / "work" / "translated_408_server_names.bin"

# Core keyword dictionaries
LOCATIONS = {
    "发明屋": "Xưởng Sáng Chế", "神秘湖": "Hồ Thần Bí", "爱心教堂": "Nhà Thờ Ái Tâm",
    "淘淘乐街": "Phố Taotao", "阳光牧场": "Nông Trại Ánh Dương", "开心农场": "Nông Trại Vui Vẻ",
    "摩尔拉雅山": "Núi Molylaya", "东部游乐场": "Công Viên Phía Đông", "西部游乐场": "Công Viên Phía Tây",
    "蘑菇洞": "Hang Nấm", "魔法马车": "Cỗ Xe Phép Thuật", "摩摩赛车场": "Đường Đua Moly",
    "摩尔足球场": "Sân Bóng Moly", "地下城堡": "Lâu Đài Dưới Đất", "SMC基地": "Căn Cứ SMC",
    "猎人小屋": "Nhà Thợ Săn M", "摩尔餐厅": "Nhà Hàng Moly", "摩尔城堡": "Lâu Đài Moly",
    "摩尔庄园": "Vương Quốc Moly", "摩尔快车道": "Đường Cao Tốc Moly", "游戏小屋": "Nhà Trò Chơi",
    "城堡露台": "Ban Công Lâu Đài", "宠物店": "Tiệm Thú Cưng", "道具店": "Tiệm Đạo Cụ",
    "服装店": "Tiệm Thời Trang", "摩尔滑冰场": "Sân Trượt Băng Moly", "城堡书房": "Thư Viện Lâu Đài",
    "城堡大厅": "Đại Sảnh Lâu Đài", "大榕树舞厅": "Vũ Đài Cây Đa", "神龟许愿池": "Hồ Rùa Thần Ước Nguyện",
    "浆果秘道": "Đường Bí Mật Dâu", "神奇树洞": "Hốc Cây Kỳ Diệu", "快乐叨叨墙": "Bức Tường Tán Gẫu",
    "神秘洞穴": "Hang Động Bí Ẩn", "蚂蚁的家": "Nhà Kiến", "浆果森林": "Rừng Quả Mọng",
    "名画走廊": "Hành Lang Tranh Quý", "皇家骑士团": "Kỵ Sĩ Hoàng Gia", "摩尔警署": "Cảnh Sát Moly",
    "力量之泉": "Suối Sức Mạnh", "彩虹瀑布": "Thác Cầu Vồng", "爱Party": "Tiệc Ái Tâm",
    "摩尔小屋": "Nhà Nhỏ Moly", "南瓜种植园": "Vườn Bí Ngô", "温室小花": "Nhà Kính Hoa Nhỏ",
    "野营之旅": "Chuyến Cắm Trại", "熔岩火山": "Núi Lửa Nham Thạch", "公民管理处": "Cơ Quan Quản Lý",
    "骑士训练场": "Trường Đua Kỵ Sĩ", "咕噜艺术街": "Phố Nghệ Thuật Guru", "黑森林": "Rừng Hắc Ám",
    "摩罗地海": "Biển Morodi", "消防署": "Trạm Cứu Hỏa", "粒粒小广场": "Quảng Trường Lạp Lạp",
    "爱心向导社": "Hội Hướng Dẫn Ái Tâm", "摩尔报社": "Tòa Soạn Báo Moly", "摩尔大剧院": "Nhà Hát Lớn Moly",
    "摩尔爱心医院": "Bệnh Viện Ái Tâm Moly", "摩尔银行": "Ngân Hàng Moly", "拉姆学院": "Học Viện La Mỗ",
    "摩尔大学": "Đại Học Moly", "摩尔时尚街": "Phố Thời Trang Moly", "建设署": "Sở Xây Dựng",
    "摩尔古董店": "Tiệm Cổ Vật Moly", "拉姆运送站": "Trạm Vận Chuyển La Mỗ", "咕噜音乐街": "Phố Âm Nhạc Guru",
}

WORDS = [
    # General terms
    ("摩尔", "Moly "), ("拉姆", "La Mỗ "), ("小摩尔", "Moly Nhỏ "), ("么么公主", "Công Chúa Meme "),
    ("洛克行政官", "Quan Hành Chính Locke "), ("菩提大伯", "Bác Bồ Đề "), ("凯文老师", "Thầy Kevin "),
    ("大卫", "David "), ("丝尔特", "Silk "), ("彩虹姐姐", "Chị Cầu Vồng "), ("库鲁", "Kuru "),
    ("RK", "RK "), ("杰克王子", "Hoàng Tử Jack "), ("瑞琪", "Ricky "), ("捷克王子", "Hoàng Tử Jack "),
    ("汉青", "Hán Thanh "), ("尤娜", "Yuna "), ("花婶", "Bác Hoa "), ("尼克", "Nick "),
    ("汤米", "Tommy "), ("艾尔警长", "Cảnh Trưởng Air "), ("茜茜", "Sissi "), ("兔兔主编", "Tổng Biên Thỏ "),
    ("城堡", "Lâu Đài "), ("森林", "Rừng "), ("庄园", "Vương Quốc "), ("花园", "Vườn Hoa "),
    ("秘密", "Bí Mật "), ("神奇", "Kỳ Diệu "), ("快乐", "Vui Vẻ "), ("开心", "Hân Hoan "),
    ("爱心", "Ái Tâm "), ("阳光", "Ánh Dương "), ("彩虹", "Cầu Vồng "), ("天使", "Thiên Thần "),
    ("水晶", "Pha Lê "), ("宝石", "Đá Quý "), ("钻石", "Kim Cương "), ("黄金", "Hoàng Kim "),
    ("骑士", "Kỵ Sĩ "), ("公主", "Công Chúa "), ("王子", "Hoàng Tử "), ("国王", "Quốc Vương "),
    ("派对", "Bữa Tiệc "), ("狂欢", "Lễ Hội "), ("盛典", "Đại Lễ "), ("庆典", "Lễ Kỷ Niệm "),
    ("星空", "Bầu Trời Sao "), ("银河", "Ngân Hà "), ("流星", "Sao Băng "), ("梦境", "Giấc Mơ "),
    ("童话", "Cổ Tích "), ("传说", "Truyền Thuyết "), ("奇迹", "Kỳ Tích "), ("神话", "Thần Thoại "),
    ("冰雪", "Băng Tuyết "), ("雪花", "Hoa Tuyết "), ("冬日", "Mùa Đông "), ("春天", "Mùa Xuân "),
    ("夏日", "Mùa Hè "), ("秋天", "Mùa Thu "), ("金秋", "Mùa Thu Vàng "), ("暖春", "Xuân Ấm "),
    ("玫瑰", "Hoa Hồng "), ("百合", "Hoa Bách Hợp "), ("郁金香", "Hoa Tulip "), ("向日葵", "Hoa Hướng Dương "),
    ("樱花", "Hoa Anh Đào "), ("桃花", "Hoa Đào "), ("荷花", "Hoa Sen "), ("茉莉", "Hoa Lài "),
    ("蝴蝶", "Bướm "), ("蜜蜂", "Ong Vàng "), ("小鸟", "Chim Nhỏ "), ("天鹅", "Thiên Nga "),
    ("海豚", "Cá Heo "), ("鲸鱼", "Cá Voi "), ("白熊", "Gấu Trắng "), ("企鹅", "Chim Cánh Cụt "),
    ("糖果", "Kẹo Ngọt "), ("巧克力", "Sô-cô-la "), ("冰淇淋", "Kem Tuyết "), ("蛋糕", "Bánh Kem "),
    ("气球", "Khinh Khí Cầu "), ("风车", "Cối Xay Gió "), ("秋千", "Xích Đu "), ("旋转木马", "Đu Quay Ngựa "),
    ("南瓜", "Bí Ngô "), ("草莓", "Dâu Tây "), ("西瓜", "Dưa Hấu "), ("苹果", "Táo Đỏ "),
    ("浆果", "Quả Mọng "), ("蓝莓", "Việt Quất "), ("樱桃", "Anh Đào "), ("蜜桃", "Đào Mật "),
    ("星星", "Ngôi Sao "), ("月亮", "Mặt Trăng "), ("太阳", "Mặt Trời "), ("云朵", "Đám Mây "),
    ("晨曦", "Bình Minh "), ("黄昏", "Hoàng Hôn "), ("夜色", "Màn Đêm "), ("清风", "Gió Mát "),
    ("微风", "Gió Thoảng "), ("海洋", "Đại Dương "), ("波浪", "Sóng Biển "), ("海滩", "Bãi Biển "),
    ("珍珠", "Ngọc Trai "), ("珊瑚", "San Hô "), ("贝壳", "Vỏ Sò "), ("海星", "Sao Biển "),
    ("魔法", "Phép Thuật "), ("奇幻", "Kỳ Ảo "), ("幻境", "Ảo Cảnh "), ("探险", "Thám Hiểm "),
    ("冒险", "Phiêu Lưu "), ("寻宝", "Tìm Kho Báu "), ("宝藏", "Kho Báu "), ("藏宝图", "Bản Đồ Kho Báu "),
    ("英雄", "Anh Hùng "), ("勇士", "Dũng Sĩ "), ("卫士", "Vệ Binh "), ("守卫", "Người Canh Gác "),
    ("和平", "Hòa Bình "), ("友谊", "Tình Bạn "), ("希望", "Hy Vọng "), ("温暖", "Ấm Áp "),
    ("幸福", "Hạnh Phúc "), ("甜蜜", "Ngọt Ngào "), ("美梦", "Giấc Mơ Đẹp "), ("愿望", "Điều Ước "),
    ("祝福", "Lời Chúc "), ("礼物", "Món Quà "), ("惊喜", "Bất Ngờ "), ("欢笑", "Tiếng Cười "),
    ("歌声", "Lời Ca "), ("舞步", "Điệu Nhảy "), ("乐章", "Bản Nhạc "), ("旋律", "Giai Điệu "),
    ("铃铛", "Chuông Gió "), ("烟花", "Pháo Hoa "), ("彩带", "Dải Ruy Băng "), ("灯火", "Ánh Đèn "),
    ("座", " "), ("之", " "), ("的", " "), ("大", "Đại "), ("小", "Tiểu "),
]

# Hanzi to Sino-Vietnamese / Pinyin translation table for remaining characters
SINO_VIET = {
    "一": "Nhất", "二": "Nhị", "三": "Tam", "四": "Tứ", "五": "Ngũ", "六": "Lục", "七": "Thất", "八": "Bát", "九": "Cửu", "十": "Thập",
    "百": "Bách", "千": "Thiên", "万": "Vạn", "亿": "Ức", "天": "Thiên", "地": "Địa", "人": "Nhân", "山": "Sơn", "水": "Thủy", "火": "Hỏa",
    "风": "Phong", "雷": "Lôi", "电": "Điện", "雨": "Vũ", "雪": "Tuyết", "光": "Quang", "暗": "Ám", "明": "Minh", "月": "Nguyệt", "日": "Nhật",
    "红": "Hồng", "黄": "Hoàng", "蓝": "Lam", "绿": "Lục", "青": "Thanh", "白": "Bạch", "黑": "Hắc", "紫": "Tử", "金": "Kim", "银": "Ngân",
    "玉": "Ngọc", "珠": "Châu", "花": "Hoa", "草": "Thảo", "树": "Thụ", "木": "Mộc", "林": "Lâm", "森": "Sâm", "石": "Thạch", "泉": "Tuyền",
    "河": "Hà", "江": "Giang", "湖": "Hồ", "海": "Hải", "洋": "Dương", "谷": "Cốc", "洞": "Động", "城": "Thành", "堡": "Bảo", "国": "Quốc",
    "家": "Gia", "园": "Viên", "居": "Cư", "堂": "Đường", "阁": "Các", "楼": "Lâu", "殿": "Điện", "塔": "Tháp", "门": "Môn", "道": "Đạo",
    "路": "Lộ", "桥": "Kiều", "舟": "Chu", "船": "Thuyền", "车": "Xa", "马": "Mã", "龙": "Long", "凤": "Phụng", "虎": "Hổ", "狮": "Sư",
    "熊": "Hùng", "鹿": "Lộc", "鹤": "Hạc", "鹰": "Ưng", "鱼": "Ngư", "鸟": "Điểu", "蝶": "Điệp", "蜂": "Phong", "蝉": "Thiền", "蛙": "Oa",
    "春": "Xuân", "夏": "Hạ", "秋": "Thu", "冬": "Đông", "晨": "Thần", "暮": "Mộ", "夜": "Dạ", "晓": "Hiểu", "晴": "Tình", "阴": "Âm",
    "吉": "Cát", "祥": "Tường", "如": "Như", "意": "Ý", "安": "An", "康": "Khang", "福": "Phúc", "禄": "Lộc", "寿": "Thọ", "喜": "Hỷ",
    "庆": "Khánh", "乐": "Lạc", "欢": "Hoan", "欣": "Hân", "荣": "Vinh", "华": "Hoa", "富": "Phú", "贵": "Quý", "盛": "Thịnh", "丰": "Phong",
    "长": "Trường", "久": "Cửu", "永": "Vĩnh", "恒": "Hằng", "真": "Chân", "善": "Thiện", "美": "Mỹ", "纯": "Thuần", "洁": "Khiết", "雅": "Nhã",
    "清": "Thanh", "静": "Tĩnh", "宁": "Ninh", "灵": "Linh", "神": "Thần", "仙": "Tiên", "圣": "Thánh", "皇": "Hoàng", "帝": "Đế", "王": "Vương",
    "君": "Quân", "卿": "Khanh", "相": "Tương", "将": "Tướng", "帅": "Soái", "士": "Sĩ", "侠": "Hiệp", "客": "Khách", "友": "Hữu", "朋": "Bằng",
    "伴": "Bạn", "侣": "Lữ", "心": "Tâm", "情": "Tình", "意": "Ý", "思": "Tư", "想": "Tưởng", "念": "Niệm", "怀": "Hoài", "梦": "Mộng",
    "幻": "Huyễn", "忆": "Ức", "缘": "Duyên", "份": "Phận", "韵": "Vận", "律": "Luật", "歌": "Ca", "曲": "Khúc", "琴": "Cầm", "棋": "Kỳ",
    "书": "Thư", "画": "Họa", "诗": "Thi", "词": "Từ", "墨": "Mặc", "香": "Hương", "味": "Vị", "色": "Sắc", "声": "Thanh", "影": "Ảnh",
    "姿": "Tư", "容": "Dung", "颜": "Nhan", "态": "Thái", "风": "Phong", "采": "Thải", "韵": "Vận", "致": "Trí", "趣": "Thú", "味": "Vị",
}

def translate_name(ch_name):
    if ch_name in LOCATIONS:
        return LOCATIONS[ch_name]
    
    res = ch_name
    for ch_word, vi_word in WORDS:
        res = res.replace(ch_word, vi_word)
        
    # Check if there are still Hanzi characters
    chars = []
    for c in res:
        if '\u4e00' <= c <= '\u9fff':
            chars.append(SINO_VIET.get(c, c))
        else:
            chars.append(c)
    out = "".join(chars)
    # Clean whitespace
    out = re.sub(r'\s+', ' ', out).strip()
    return out

def main():
    print(f"Reading {SRC_BIN}...")
    content = SRC_BIN.read_text(encoding="utf-8")
    root = ET.fromstring(content)
    
    count = 0
    translated_map = {}
    for elem in root.findall("List"):
        sid = elem.get("ID")
        ch_name = elem.get("Name")
        vi_name = translate_name(ch_name)
        elem.set("Name", vi_name)
        translated_map[sid] = vi_name
        count += 1
        
    out_xml = ET.tostring(root, encoding="utf-8").decode("utf-8")
    # Add newline after XML declaration if needed
    header = '<?xml version="1.0" encoding="utf-8"?>\n'
    if not out_xml.startswith("<?xml"):
        out_xml = header + out_xml
        
    OUT_BIN.write_text(out_xml, encoding="utf-8")
    print(f"Successfully translated {count} server names to {OUT_BIN}")
    
    # Also write a copy to work/exported/Login_bin so it stays in sync
    SRC_BIN.write_text(out_xml, encoding="utf-8")
    print(f"Updated {SRC_BIN}")
    
    # Print sample
    print("\n--- SAMPLE TRANSLATED SERVERS ---")
    for sid in ["1", "2", "3", "4", "5", "10", "15", "18", "25", "30", "100", "200", "500", "1000", "1200"]:
        if sid in translated_map:
            print(f"Server {sid:4s}: {translated_map[sid]}")

if __name__ == "__main__":
    main()
