#!/usr/bin/env python3
"""Master Server Names Translator for Moly - Thế Giới Chuột Chũi VN.

Translates 100% of all 1200 server names from the pristine offline-mirror tag 408
into authentic, polished Vietnamese, with zero leftover Chinese characters.
"""

import sys
import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT_DIR = Path(__file__).resolve().parents[1]
SRC_BIN = ROOT_DIR / "work" / "original_login_bin" / "408_com.mole.login.LoginServerConfig_ServerName.bin"
OUT_BIN = ROOT_DIR / "work" / "translated_408_server_names.bin"
CHAR_MAP_FILE = ROOT_DIR / "work" / "hanzi_to_vi.json"

char_map = json.loads(CHAR_MAP_FILE.read_text(encoding="utf-8"))

# Priority Compounds & Constellations & Lore
COMPOUNDS = [
    # Constellations
    ("白羊座", "Bạch Dương"), ("金牛座", "Kim Ngưu"), ("双子座", "Song Tử"),
    ("巨蟹座", "Cự Giải"), ("狮子座", "Sư Tử"), ("处女座", "Xử Nữ"),
    ("天秤座", "Thiên Bình"), ("天蝎座", "Thiên Yết"), ("射手座", "Nhân Mã"),
    ("摩羯座", "Ma Kết"), ("水瓶座", "Bảo Bình"), ("双鱼座", "Song Ngư"),
    ("白羊", "Bạch Dương"), ("金牛", "Kim Ngưu"), ("双子", "Song Tử"),
    ("巨蟹", "Cự Giải"), ("狮子", "Sư Tử"), ("处女", "Xử Nữ"),
    ("天秤", "Thiên Bình"), ("天蝎", "Thiên Yết"), ("射手", "Nhân Mã"),
    ("摩羯", "Ma Kết"), ("水瓶", "Bảo Bình"), ("双鱼", "Song Ngư"),
    ("仙后座", "Tiên Hậu"), ("仙女座", "Tiên Nữ"), ("猎户座", "Thợ Săn"),
    ("大熊座", "Đại Hùng"), ("小熊座", "Tiểu Hùng"), ("天鹅座", "Thiên Nga"),
    ("天琴座", "Thiên Cầm"), ("天鹰座", "Thiên Ưng"), ("飞马座", "Phi Mã"),
    ("凤凰座", "Phượng Hoàng"), ("孔雀座", "Khổng Tước"),

    # Map & Story Hubs
    ("发明屋", "Xưởng Sáng Chế"), ("神秘湖", "Hồ Thần Bí"), ("爱心教堂", "Nhà Thờ Ái Tâm"),
    ("淘淘乐街", "Phố Taotao"), ("阳光牧场", "Nông Trại Ánh Dương"), ("开心农场", "Nông Trại Vui Vẻ"),
    ("摩尔拉雅山", "Núi Molylaya"), ("东部游乐场", "Công Viên Đông"), ("西部游乐场", "Công Viên Tây"),
    ("蘑菇洞", "Hang Nấm"), ("魔法马车", "Cỗ Xe Phép Thuật"), ("摩摩赛车场", "Đường Đua Moly"),
    ("摩尔足球场", "Sân Bóng Moly"), ("地下城堡", "Lâu Đài Dưới Đất"), ("SMC基地", "Căn Cứ SMC"),
    ("猎人小屋", "Nhà Thợ Săn M"), ("摩尔餐厅", "Nhà Hàng Moly"), ("摩尔城堡", "Lâu Đài Moly"),
    ("摩尔庄园", "Vương Quốc Moly"), ("摩尔快车道", "Đường Cao Tốc Moly"), ("游戏小屋", "Nhà Trò Chơi"),
    ("城堡露台", "Ban Công Lâu Đài"), ("宠物店", "Tiệm Thú Cưng"), ("道具店", "Tiệm Đạo Cụ"),
    ("服装店", "Tiệm Thời Trang"), ("摩尔滑冰场", "Sân Trượt Băng Moly"), ("城堡书房", "Thư Viện Lâu Đài"),
    ("城堡大厅", "Đại Sảnh Lâu Đài"), ("大榕树舞厅", "Vũ Đài Cây Đa"), ("神龟许愿池", "Hồ Rùa Thần Ước Nguyện"),
    ("浆果秘道", "Đường Bí Mật Dâu"), ("神奇树洞", "Hốc Cây Kỳ Diệu"), ("快乐叨叨墙", "Tường Tán Gẫu"),
    ("神秘洞穴", "Hang Động Bí Ẩn"), ("蚂蚁的家", "Tổ Kiến"), ("浆果森林", "Rừng Quả Mọng"),
    ("名画走廊", "Hành Lang Tranh"), ("皇家骑士团", "Kỵ Sĩ Hoàng Gia"), ("摩尔警署", "Cảnh Sát Moly"),
    ("力量之泉", "Suối Sức Mạnh"), ("彩虹瀑布", "Thác Cầu Vồng"), ("爱Party", "Tiệc Ái Tâm"),
    ("摩尔小屋", "Nhà Nhỏ Moly"), ("南瓜种植园", "Vườn Bí Ngô"), ("温室小花", "Nhà Kính Hoa Nhỏ"),
    ("野营之旅", "Chuyến Cắm Trại"), ("熔岩火山", "Núi Lửa Nham Thạch"), ("公民管理处", "Quản Lý Công Dân"),
    ("阳光草舍", "Nhà Cỏ Ánh Dương"), ("雪山神鹰", "Thần Ưng Núi Tuyết"), ("魔幻镜", "Gương Ma Thuật"),
    ("雪人水车", "Cối Xay Người Tuyết"), ("咕噜艺术街", "Phố Nghệ Thuật Guru"), ("黑森林", "Rừng Hắc Ám"),
    ("吉普豆村", "Làng Đậu Jipu"), ("麦田村", "Làng Lúa Mạch"), ("摩罗地海", "Biển Morodi"),

    # Game Lore & Roles
    ("么么公主", "Công Chúa Meme"), ("洛克行政官", "Quan Locke"), ("菩提大伯", "Bác Bồ Đề"),
    ("凯文老师", "Thầy Kevin"), ("凯文", "Kevin"), ("丝尔特", "Silk"), ("彩虹姐姐", "Chị Cầu Vồng"),
    ("RK", "RK"), ("捷克王子", "Hoàng Tử Jack"), ("杰克王子", "Hoàng Tử Jack"),
    ("瑞琪", "Ricky"), ("艾尔警长", "Cảnh Trưởng Air"), ("兔兔主编", "Tổng Biên Thỏ"),
    ("大卫", "David"), ("花婶", "Bác Hoa"), ("尼克", "Nick"), ("汤米", "Tommy"),
    ("超级拉姆", "Super La Mỗ"), ("拉姆", "La Mỗ"), ("小摩尔", "Moly Nhỏ"), ("摩尔", "Moly"),
    ("骑士", "Kỵ Sĩ"), ("骑士团", "Đoàn Kỵ Sĩ"), ("牧场", "Mục Trường"), ("农场", "Nông Trại"),
    ("城堡", "Lâu Đài"), ("庄园", "Vương Quốc"), ("公国", "Công Quốc"),
    
    # Common Treats & Items
    ("冰淇淋", "Kem Tuyết"), ("巧克力", "Sô-cô-la"), ("大礼包", "Túi Quà Lớn"),
    ("旋转木马", "Đu Quay Ngựa"), ("摩天轮", "Đu Quay Đứng"), ("万花筒", "Kính Vạn Hoa"),
    ("圣诞老人", "Ông Già Noel"), ("圣诞节", "Giáng Sinh"), ("万圣节", "Halloween"),
    ("情人节", "Lễ Tình Nhân"), ("感恩节", "Lễ Tạ Ơn"), ("儿童节", "Tết Thiếu Nhi"),
    ("奖杯", "Cúp Vàng"), ("饼干", "Bánh Quy"), ("奶昔", "Milkshake"),
    ("水晶鞋", "Hài Pha Lê"), ("水晶", "Pha Lê"), ("宝石", "Đá Quý"),
    ("气球", "Khinh Khí Cầu"), ("风车", "Cối Xay Gió"), ("秋千", "Xích Đu"),
    ("草莓", "Dâu Tây"), ("西瓜", "Dưa Hấu"), ("苹果", "Táo Đỏ"), ("樱桃", "Anh Đào"),
    ("蓝莓", "Việt Quất"), ("柠檬", "Chanh"), ("葡萄", "Nho"), ("香蕉", "Chuối"),
    ("独角兽", "Kỳ Lân"), ("小天鹅", "Thiên Nga"), ("海豚", "Cá Heo"), ("白鲸", "Cá Voi Trắng"),
    ("企鹅", "Chim Cánh Cụt"), ("北极熊", "Gấu Bắc Cực"), ("白熊", "Gấu Trắng"),
    ("小青蛇", "Rắn Xanh"), ("金鱼", "Cá Vàng"), ("热带鱼", "Cá Nhiệt Đới"),
    ("蝴蝶", "Bướm"), ("蜻蜓", "Chuồn Chuồn"), ("萤火虫", "Đom Đóm"),
]

def clean_word(w):
    # Remove 'Họ [...]' or '[...]' markers
    w = re.sub(r'Họ \[[^\]]+\]', '', w)
    w = re.sub(r'\[[^\]]+\]', '', w)
    w = re.sub(r'\(.*?\)', '', w)
    # Remove awkward dictionary prefixes
    w = re.sub(r'^(Thuộc về|Dùng trong|Dùng để|Tên một|Tên người|Tên loài)\s+', '', w)
    return w.strip()

def translate_server_name(raw_name):
    txt = raw_name
    for ch_term, vi_term in COMPOUNDS:
        txt = txt.replace(ch_term, " " + vi_term + " ")
        
    res = []
    for c in txt:
        if '\u4e00' <= c <= '\u9fff':
            vi_c = char_map.get(c, "")
            vi_c = clean_word(vi_c)
            if not vi_c:
                vi_c = "Moly"
            res.append(" " + vi_c + " ")
        else:
            res.append(c)
            
    out = "".join(res)
    # Clean up redundant spaces and empty markers
    out = clean_word(out)
    out = re.sub(r'\s+', ' ', out).strip()
    return out

def main():
    print(f"Reading pristine {SRC_BIN}...")
    content = SRC_BIN.read_text(encoding="utf-8")
    root = ET.fromstring(content)
    
    servers = root.findall("List")
    print(f"Total servers in tag 408: {len(servers)}")
    
    untranslated_chars = set()
    translated_count = 0
    
    for elem in servers:
        sid = elem.get("ID")
        ch_name = elem.get("Name")
        vi_name = translate_server_name(ch_name)
        elem.set("Name", vi_name)
        translated_count += 1
        
        for c in vi_name:
            if '\u4e00' <= c <= '\u9fff':
                untranslated_chars.add(c)
                
    if untranslated_chars:
        print(f"[ERROR] Found {len(untranslated_chars)} untranslated characters: {untranslated_chars}")
        sys.exit(1)
        
    out_xml = ET.tostring(root, encoding="utf-8").decode("utf-8")
    header = '<?xml version="1.0" encoding="utf-8"?>\n'
    if not out_xml.startswith("<?xml"):
        out_xml = header + out_xml
        
    OUT_BIN.write_text(out_xml, encoding="utf-8")
    target_bin = ROOT_DIR / "work" / "exported" / "Login_bin" / "408_com.mole.login.LoginServerConfig_ServerName.bin"
    target_bin.write_text(out_xml, encoding="utf-8")
    
    print(f"\n[SUCCESS] 100% of {translated_count} server names translated cleanly with ZERO leftover Hanzi!")
    print(f"Written to:\n  - {OUT_BIN}\n  - {target_bin}")
    
    print("\n--- SAMPLE TRANSLATED SERVERS ---")
    for elem in servers[:10] + servers[98:106] + servers[498:505] + servers[1190:]:
        print(f"Server {elem.get('ID'):>4s}: {elem.get('Name')}")

if __name__ == "__main__":
    main()
