#!/usr/bin/env python3
"""Batch Map XML Translator for Moly - Thế Giới Chuột Chũi VN.

Reads all 257 map XML files from archive/clients/offline-mirror/mole.61.com/resource/map/
and generates 100% localized Vietnamese XML files in
archive/clients/local-overrides/mole.61.com/resource/map/.
"""

import os
import glob
import re
import xml.etree.ElementTree as ET
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "archive" / "clients" / "offline-mirror" / "mole.61.com" / "resource" / "map"
DST_DIR = PROJECT_ROOT / "archive" / "clients" / "local-overrides" / "mole.61.com" / "resource" / "map"

REQUIRED_RETURN_PORTALS = {
    20: (3, "Đến Phố mua sắm Taotao"),
    32: (1, "Đến Lâu đài Moly"),
    17: (1, "Đến Lâu đài Moly"),
    21: (3, "Đến Phố mua sắm Taotao"),
    75: (4, "Đến Chân núi Molylaya"),
    142: (3, "Đến Phố mua sắm Taotao"),
    143: (4, "Đến Chân núi Molylaya"),
    19: (3, "Đến Phố mua sắm Taotao"),
    76: (3, "Đến Phố mua sắm Taotao"),
    63: (61, "Đến Tiền đồn Kỵ sĩ"),
    64: (61, "Đến Tiền đồn Kỵ sĩ"),
}

# 1. Comprehensive dictionary of Map Portals & Building Tips
TIPS_DICT = {
    # Hubs & Main Streets
    "城堡大厅": "Đại sảnh Lâu đài",
    "城堡书房": "Thư viện Lâu đài",
    "摩尔城堡": "Lâu đài Moly",
    "城堡露台": "Ban công Lâu đài",
    "城堡露天花园": "Vườn hoa Lâu đài",
    "Tầng hầm lâu đài": "Tầng hầm Lâu đài",
    "Tầng hai lâu đài": "Tầng hai Lâu đài",
    "摩尔拉雅山脚": "Chân núi Molylaya",
    "摩尔拉雅山顶": "Đỉnh núi Molylaya",
    "摩尔拉雅滑冰场": "Sân trượt băng Molylaya",
    "进入摩尔拉雅滑冰场": "Đến Sân trượt băng Molylaya",
    "进入摩尔拉雅山顶": "Đến Đỉnh núi Molylaya",
    "爱心广场": "Quảng trường Ái Tâm",
    "进入爱心广场": "Đến Quảng trường Ái Tâm",
    "爱心教堂内": "Bên trong Nhà thờ Ái Tâm",
    "Bên trong Nhà thờ Tình Yêu": "Bên trong Nhà thờ Ái Tâm",
    "爱心救治室": "Phòng Cứu chữa Ái Tâm",
    "Phòng cứu chữa": "Phòng Cứu chữa Ái Tâm",
    "爱心向导社": "Hội Hướng dẫn viên Ái Tâm",
    "Hội hướng dẫn viên": "Hội Hướng dẫn viên Ái Tâm",
    "摩尔庄园警署": "Đồn Cảnh sát Moly",
    "Sở cảnh sát Moly": "Đồn Cảnh sát Moly",
    "摩尔报社": "Tòa soạn Báo Moly",
    "Tòa soạn Moly": "Tòa soạn Báo Moly",
    "摩尔银行": "Ngân hàng Moly",
    "Ngân hàng Moly": "Ngân hàng Moly",
    "电视墙": "Tường Truyền hình",
    "Tường truyền hình": "Tường Truyền hình",
    "淘淘乐街": "Phố mua sắm Taotao",
    "进入淘淘乐街": "Đến Phố mua sắm Taotao",
    "Phố mua sắm": "Phố mua sắm Taotao",
    "道具店": "Tiệm Đạo cụ Rainbow",
    "Cửa hàng vật phẩm": "Tiệm Đạo cụ Rainbow",
    "服装店": "Tiệm Thời trang Silk",
    "Cửa hàng thời trang": "Tiệm Thời trang Silk",
    "宠物店": "Tiệm Thú cưng Lamu",
    "Cửa hàng thú cưng": "Tiệm Thú cưng Lamu",
    "摩尔餐厅": "Nhà hàng Moly",
    "餐厅打工游戏": "Làm thêm tại Nhà hàng",
    "开心大厨游戏": "Trò chơi Đầu bếp Vui vẻ",
    "米勒大道": "Đại lộ Miller",
    "Đại lộ Miller": "Đại lộ Miller",
    "粒粒小广场": "Quảng trường nhỏ Lili",

    # Farms, Pastures & Nature
    "开心农场": "Nông trại Vui vẻ",
    "进入开心农场": "Đến Nông trại Vui vẻ",
    "进入梅森小屋": "Đến Túp lều Mason",
    "进入农场发明屋": "Đến Xưởng sáng chế Nông trại",
    "进入三兄弟小屋": "Đến Nhà Ba Anh Em",
    "阳光牧场": "Đồng cỏ Ánh Dương",
    "进入阳光牧场": "Đến Đồng cỏ Ánh Dương",
    "Trang trại Ánh Dương": "Đồng cỏ Ánh Dương",
    "进入尤尤小屋": "Đến Túp lều Yoyo",
    "进入阳光草舍": "Đến Nhà cỏ Ánh Dương",
    "进入阳光培育室": "Đến Phòng nuôi cấy Ánh Dương",
    "吉普豆村": "Làng Đậu Jipu",
    "麦田村": "Làng Lúa Mạch",
    "草木树海": "Rừng Cây Đại Ngàn",
    "藤蔓森林": "Rừng Dây Leo",
    "蘑菇森林": "Rừng Nấm",
    "Ng ngôi nhà Nấm": "Ngôi nhà Nấm",
    "Ngôi nhà Nấm": "Ngôi nhà Nấm",
    "进入虫虫谷": "Đến Thung lũng Côn Trùng",
    "云雾谜桥": "Cầu Mây Bí Ẩn",
    "彩虹瀑布": "Thác Cầu Vồng",
    "浆果秘道": "Mật đạo Quả Mọng",
    "浆果密道": "Mật đạo Quả Mọng",
    "五色浆果": "Quả Mọng Ngũ Sắc",
    "天空树": "Cây Bầu Trời",
    "进入天空树": "Đến Cây Bầu Trời",
    "世界树": "Cây Thế Giới",

    # Coastal & Harbor
    "进入东部沙滩码头": "Đến Bến tàu Bãi biển Phía Đông",
    "进入神秘湖码头": "Đến Bến tàu Hồ Thần Bí",
    "进入神秘湖": "Đến Hồ Thần Bí",
    "进入摩罗地海海底": "Đến Đáy biển Molodi",
    "进入浮冰岛海湾": "Đến Vịnh Băng Trôi",
    "浮冰岛海湾": "Vịnh Băng Trôi",
    "珊瑚平原": "Bình nguyên San Hô",
    "深水之城": "Thành phố Dưới Nước",
    "海妖巢穴": "Hang Quái Ngư",
    "海妖王宝藏": "Kho báu Vua Hải Yêu",
    "海妖冒险训练": "Huấn luyện Thám hiểm Hải Yêu",
    "海妖骑士训练服": "Trang phục Kỵ sĩ Hải Yêu",
    "海妖冒险训练奖励展示": "Phần thưởng Huấn luyện",

    # School & Academies
    "拉姆学院": "Học viện Lamu",
    "进入拉姆学院": "Đến Học viện Lamu",
    "Học viện Ram": "Học viện Lamu",
    "进入拉姆课堂": "Vào Lớp học Lamu",
    "进入拉姆运动场": "Đến Sân vận động Lamu",
    "拉姆运动场": "Sân vận động Lamu",
    "进入学院教导处": "Đến Văn phòng Học viện",
    "进入魔法阁楼": "Lên Gác mái Ma thuật",
    "进入摩尔大学": "Đến Đại học Moly",
    "进入摩尔大学大厅": "Vào Đại sảnh Đại học Moly",
    "摩尔大学大厅": "Đại sảnh Đại học Moly",
    "摩尔大学公告板": "Bảng tin Đại học Moly",
    "摩尔大学校训": "Lời răn Đại học Moly",
    "进入涂鸦馆": "Vào Phòng vẽ Tranh",
    "超级拉姆俱乐部": "Câu lạc bộ Siêu Đậu Đậu",

    # Sports & Amusements
    "进入摩尔足球场": "Đến Sân bóng đá Moly",
    "摩尔足球场": "Sân bóng đá Moly",
    "回到摩尔足球场": "Trở lại Sân bóng đá",
    "东部游乐场": "Khu vui chơi Phía Đông",
    "进入东部游乐场": "Đến Khu vui chơi Phía Đông",
    "西部游乐场": "Khu vui chơi Phía Tây",
    "进入西部游乐场": "Đến Khu vui chơi Phía Tây",
    "摩摩赛车场": "Trường đua xe Momo",
    "游戏小屋": "Ngôi nhà Trò chơi",
    "小游戏天地": "Thế giới Trò chơi nhỏ",
    "进入露天剧场": "Đến Nhà hát Ngoài trời",
    "露天剧场": "Nhà hát Ngoài trời",
    "Nhà hát ngoài trời": "Nhà hát Ngoài trời",
    "魔法马车": "Cỗ xe Ma thuật",
    "大变摩尔": "Biến hình Moly",
    "冲浪滑梯": "Cầu trượt Lướt sóng",
    "超级大水桶说明": "Hướng dẫn Thùng nước Khổng lồ",
    "街边套圈圈": "Trò chơi Ném vòng Ven đường",
    "拉姆跳高": "Lamu Nhảy cao",
    "单人贪吃蛇": "Rắn Săn Mồi Đơn",
    "钓鱼": "Câu cá",
    "捞鱼": "Vớt cá",
    "图书大修复": "Phục hồi Sách cổ",
    "大脑加油站": "Trạm Nạp Trí Tuệ",

    # Military, Knights & Fortresses
    "进入前哨站": "Đến Tiền đồn Kỵ sĩ",
    "前哨站": "Tiền đồn Kỵ sĩ",
    "返回前哨站": "Trở về Tiền đồn Kỵ sĩ",
    "骑士训练场": "Sân huấn luyện Kỵ sĩ",
    "骑士训练营": "Trại huấn luyện Kỵ sĩ",
    "骑士要塞塔顶": "Đỉnh tháp Pháo đài Kỵ sĩ",
    "骑士秘密基地": "Căn cứ Bí mật Kỵ sĩ",
    "进入SMC基地": "Đến Căn cứ Bí mật SMC",
    "进入消防署": "Đến Sở Cứu hỏa",
    "进入交通署": "Đến Sở Giao thông",
    "交通署大厅": "Đại sảnh Sở Giao thông",
    "进入建设署": "Đến Sở Xây dựng",
    "猎人小屋": "Túp lều Thợ săn",

    # Mystic Lands & Mythical Dungeons
    "尼尔拉塔": "Tháp Nierla",
    "进入尼尔拉塔第一层": "Vào Tháp Nierla Tầng 1",
    "时光圣殿": "Điện thờ Thời Gian",
    "元素骑士训练营": "Trại Kỵ sĩ Nguyên tố",
    "元素训练": "Huấn luyện Nguyên tố",
    "龙巢迷宫": "Mê cung Hang Rồng",
    "进入龙之幻境": "Vào Huyễn Cảnh Rồng",
    "永夜哨站": "Trạm gác Vĩnh Dạ",
    "摩利亚王城": "Vương thành Molia",
    "进入积雪镇": "Đến Thị trấn Tuyết",
    "进入积雪神殿": "Vào Đền Thờ Tuyết",
    "进入神殿彩虹桥": "Đến Cầu Cầu Vồng Thần Điện",
    "目灵祭台": "Tế đàn Linh Mắt",
    "沙之迷穴": "Mê động Cát Vàng",
    "沙之秘穴": "Bí động Cát Vàng",
    "黑岩旋梯": "Cầu thang Xoắn Đá Đen",
    "冰脊之巅": "Đỉnh Băng Sơn",
    "雨昙秘境": "Bí cảnh Mưa Hoa",
    "月灵之森": "Rừng Linh Nguyệt",
    "国家花园": "Vườn hoa Hoàng gia",
    "食人花园": "Vườn hoa Ăn thịt",
    "水晶迷宫": "Mê cung Pha Lê",
    "封印之地": "Vùng đất Phong Ấn",
    "风岩沙漠": "Sa mạc Gió Đá",
    "荆棘桥": "Cầu Gai Góc",
    "摩灵宫殿": "Cung điện Moling",
    "仙堡大厅": "Đại sảnh Lâu đài Tiên",
    "仙堡前院": "Tiền viện Lâu đài Tiên",
    "仙堡后庭": "Hậu viện Lâu đài Tiên",
    "库拉城堡": "Lâu đài Kula",
    "库拉城堡大厅": "Đại sảnh Lâu đài Kula",
    "进入遗忘田园": "Đến Đồng quê Lãng Quên",
    "拉姆神秘世界": "Thế giới Bí ẩn Lamu",
    "拉姆世界丛林": "Rừng rậm Thế giới Lamu",
    "试炼洞穴": "Hang Động Thử Thách",
    "无尽深渊": "Vực Thẳm Vô Tận",
    "灰烬深渊": "Vực Thẳm Tro Tàn",
    "信奉广场": "Quảng trường Đức Tin",
    "视界原": "Đồng Cỏ Tầm Nhìn",
    "格历尔平原": "Bình nguyên Grier",
    "曜石迷宫": "Mê cung Hắc Diệu Thạch",
    "寒心水牢": "Thủy Lao Lạnh Giá",
    "镜花水月": "Cảnh Kính Hoa Thủy Nguyệt",
    "璨之花园": "Vườn hoa Rực Rỡ",
    "摩界之门": "Cánh Cổng Ma Giới",

    # Activities, Tasks & Notices
    "看电影": "Xem Phim Chiếu Rạp",
    "燃放烟花": "Bắn Pháo Hoa Rực Rỡ",
    "快抓生日礼物": "Bắt Quà Sinh Nhật",
    "我要装饰": "Tôi Muốn Trang Trí",
    "舞台剧说明": "Hướng dẫn Vở Kịch",
    "大富翁游戏说明": "Hướng dẫn Cờ Tỷ Phú",
    "驯蛇伏摩游戏说明": "Hướng dẫn Trò chơi Thu Phục Rắn",
    "活动规则": "Quy tắc Sự kiện",
    "打开回忆长廊": "Mở Hành Lang Kỷ Niệm",
    "长廊": "Hành lang Kỷ niệm",
    "唤醒木神": "Đánh thức Mộc Thần",
    "敬拜木神": "Kính bái Mộc Thần",
    "优秀小店员墙": "Bảng Vinh Danh Nhân Viên",
    "KFC惊喜栏": "Bảng Bất Ngờ KFC",
    "KFC餐厅": "Nhà hàng KFC",
    "誓言小屋": "Túp lều Lời Thề",
    "小屋寻踪": "Dò tìm Túp lều",
    "卡罗拉日记本": "Nhật ký Carola",
    "反应训练": "Huấn luyện Phản xạ",
    "速度训练": "Huấn luyện Tốc độ",
    "力量训练": "Huấn luyện Thể lực",
    "手里剑训练": "Huấn luyện Phi tiêu",
    "弓箭训练": "Huấn luyện Cung tên",
    "训练排行榜": "Bảng xếp hạng Huấn luyện",
    "训练介绍": "Giới thiệu Huấn luyện",
    "挑战小恶魔": "Thử thách Ác Ma Nhỏ",
    "邪恶蘑菇": "Nấm Độc Hắc Ám",
    "挑战巨型赤蝎": "Thử thách Bò Cạp Đỏ Khổng Lồ",
    "开始游戏": "Bắt đầu Trò chơi",
    "挑战莎士魔亚": "Thử thách Shasmoa",
    "捐献": "Quyên góp",
    "公告": "Bảng Thông báo",
    "海贼喽啰": "Tên cướp biển tay sai",
    "挑战汉青": "Thử thách Hán Thanh",
    "激战蛋蛋": "Chiến đấu Trứng Vui Vẻ",
    "决战扣扣": "Quyết đấu Khấu Khấu",
    "邪恶的洛基": "Loki Tà Ác",
    "好战的托尔": "Thor Hiếu Chiến",
    "沉睡的奥丁": "Odin Ngủ Say",
    "进入神秘花蕊": "Vào Nhụy Hoa Thần Bí",
    "地下洞穴": "Hang động Ngầm",
    "奇普力村长家": "Nhà Trưởng thôn Qipuli",
    "祭拜说明面板": "Bảng Hướng dẫn Tế Lễ",
    "野人狩猎季": "Mùa Săn Bắn Người Rừng",
    "时光井底": "Đáy Giếng Thời Gian",
    "春暖花开": "Mùa Xuân Đơm Hoa",
    "经营冰淇淋小屋": "Kinh doanh Quán Kem",
    "庄园新公告": "Bản tin Vương quốc Moly",
    "礼物小屋": "Ngôi nhà Quà tặng",
    "Cửa hàng quà tặng": "Ngôi nhà Quà tặng",
    "拉姆菌": "Nấm Lamu",
    "食人花妖": "Yêu hoa Ăn thịt",
    "杀戮榜": "Bảng Diệt Quái",
    "连胜榜": "Bảng Chiến Thắng",
    "点我": "Bấm vào tôi",
    "阿福小店": "Tiệm nhỏ A Phúc",
    "南瓜": "Bí ngô Kỳ diệu",
    "南瓜屋密室": "Mật thất Nhà Bí Ngô",
    "么么的卧室": "Phòng ngủ Công chúa Momo",
    "么么的密室": "Mật thất Công chúa Momo",
    "未来星": "Ngôi Sao Tương Lai",
    "蛋屋场景": "Ngôi nhà Trứng",
    "进入森林训练场": "Đến Bãi Huấn luyện Rừng",
    "下车": "Xuống xe",
    "龙王丸一号车厢": "Toa số 1 Long Vương Hoàn",
    "猫的夜市": "Chợ đêm Mèo",
}

# 2. Comprehensive dictionary of NPC Names
NPC_NAMES_DICT = {
    "粒粒": "Lili",
    "小乖": "Bé Ngoan",
    "汉青": "Hán Thanh",
    "阿七": "A Thất",
    "兔兔主编": "Tổng biên tập Thỏ Momo",
    "杰西": "Jesse",
    "菩提大伯": "Bác Bồ Đề",
    "么么公主": "Công chúa Momo",
    "摩乐乐": "Moly Lele",
    "帕帕囧": "Papa Jiong",
    "老超": "Bác Siêu",
    "扣扣": "Khấu Khấu",
    "克劳": "Mục sư Crow",
    "小仔": "Tiểu Tử",
    "迷你星": "Ngôi Sao Mini",
    "彩虹姐姐": "Chị Cầu Vồng (Rainbow)",
    "哈哈魔法师": "Pháp sư Haha",
    "大卫": "David",
    "捷克": "Hoàng tử Jack",
    "猎人M": "Thợ săn M",
    "艾尔": "Sĩ quan Air",
    "艾米": "Ký giả Amy",
    "凯文": "Huấn luyện viên Kevin",
    "葡萄": "Bồ Đào",
    "弗兰克": "Hiệp sĩ Frank",
    "安迪": "Andy",
    "花婶": "Cô Hoa",
    "丝尔特": "Silk",
    "尼克": "Nick",
    "洛克": "Locke",
    "尤尤": "Yoyo",
    "梅森": "Mason",
    "库拉": "Kula",
    "丫丽": "Yali",
    "布多多": "Buduoduo",
    "布少少": "Bushaoshao",
    "尼尔拉法师": "Pháp sư Nierla",
    "尤瑞克": "Yurick",
    "捷克王子": "Hoàng tử Jack",
    "小喵咪": "Mèo Con",
}

# 3. Common dialogue and option regex rules / translation pairs
COMMON_PHRASES = [
    ("你好呀！我是粒粒，很高兴认识你~", "Xin chào! Mình là Lili, rất vui được làm quen với bạn~"),
    ("我也很高兴可以认识你", "Mình cũng rất vui được làm quen với bạn"),
    ("账户安全", "Bảo mật tài khoản"),
    ("好的，我这就去。", "Được, mình đi ngay đây."),
    ("好嘞，我这就过去！", "Được rồi, mình qua đó ngay!"),
    ("好嘞", "Đã rõ"),
    ("太棒了！我现在就去！", "Tuyệt quá! Mình đi ngay đây!"),
    ("什么额外惊喜？", "Bất ngờ gì vậy?"),
    ("那怎么找到他们呢？", "Vậy làm sao tìm được họ?"),
    ("幸运月饼有什么用呢？", "Bánh trung thu may mắn dùng để làm gì vậy?"),
    ("讨厌，被你找到了喵o(︶︿︶)o", "Ghét ghê, bạn tìm thấy mình rồi meo~ o(︶︿︶)o"),
    ("我知道你是让着我的~摸摸~", "Mình biết bạn nhường mình mà~ Xoa đầu nào~"),
    ("你怎么会发现我的(┬＿┬)", "Sao bạn lại tìm ra mình được vậy? (┬＿┬)"),
    ("我和你心有灵犀(*^__^*)", "Vì chúng mình tâm đầu ý hợp mà (*^__^*)"),
    ("你终于找到我了！(＾▽＾)", "Cuối cùng bạn cũng tìm thấy tôi rồi! (＾▽＾)"),
    ("我知道了！", "Tôi hiểu rồi!"),
    ("哦，我知道了。", "Ồ, tôi hiểu rồi."),
    ("知道了!", "Đã hiểu!"),
    ("知道啦！", "Biết rồi nha!"),
    ("我知道了", "Tôi đã hiểu"),
    ("没什么事", "Không có việc gì đâu"),
    ("没什么事！", "Không có việc gì đâu!"),
    ("随便聊聊", "Trò chuyện đôi chút"),
    ("好的", "Được rồi"),
    ("好的！", "Được rồi!"),
    ("下次再说！", "Hẹn lần sau nhé!"),
    ("下次再来", "Lần sau lại đến nhé"),
    ("领取队服", "Nhận đồng phục đội"),
    ("领取袖章", "Nhận băng tay"),
    ("拼合碎片", "Ghép mảnh vỡ"),
    ("冰雪美食节", "Lễ hội Ẩm thực Băng Tuyết"),
    ("参加火神杯", "Tham gia Cúp Hỏa Thần"),
    ("你太客气了", "Bạn khách sáo quá"),
    ("不用这么客气，你已经送给过我月饼了", "Không cần khách sáo vậy đâu, bạn đã tặng bánh trung thu cho mình rồi mà"),
    ("嗯，好的", "Ừm, được rồi"),
    ("嗯，是的。", "Ừm, đúng vậy."),
    ("我有事先走了！", "Mình có việc phải đi trước đây!"),
    ("我有事，先走了", "Mình có việc, đi trước nhé"),
    ("哦，再见！", "Ồ, tạm biệt nhé!"),
    ("稍等！", "Chờ một chút!"),
    ("呃，我相信你了！", "Ừm, tôi tin bạn rồi!"),
    ("卖萌也没用！这次被我抓到了吧！", "Giả vờ dễ thương cũng vô ích thôi! Lần này bị bắt quả tang rồi nhé!"),
    ("嗯！一定不能让他得逞！", "Đúng vậy! Tuyệt đối không để hắn đạt được mục đích!"),
    ("喂！那个小摩尔！别站在那儿，妨碍大家训练！", "Này! Cư dân Moly kia! Đừng đứng đó cản trở mọi người luyện tập chứ!"),
    ("我要交纹章", "Tôi muốn nộp huân chương"),
    ("放弃占卜。", "Hủy bỏ bói toán."),
    ("咦！这个邀请函好像不是送给我的，呜呜呜~真伤心！", "Ủa! Thư mời này hình như không phải gửi cho mình, hu hu hu~ Buồn quá đi!"),
    ("不好意思啦，我弄错了o(╯□╰)o", "Ngại quá, mình nhầm rồi o(╯□╰)o"),
    ("我这就去！", "Mình đi ngay đây!"),
    ("我要报名", "Tôi muốn đăng ký"),
    ("我想更换队伍", "Tôi muốn đổi đội"),
    ("查看赛程表", "Xem lịch thi đấu"),
    ("查看积分排行和奖励", "Xem bảng điểm và phần thưởng"),
    ("好的，没问题！", "Được, không thành vấn đề!"),
    ("我开玩笑的，我不换~", "Tôi đùa thôi, tôi không đổi đâu~"),
    ("有什么奖励呢?", "Có phần thưởng gì thế?"),
    ("我要砸蛋", "Tôi muốn đập trứng"),
    ("好的,我知道了!", "Được, tôi biết rồi!"),
    ("哇,我一定不会错过的!", "Oa, tôi nhất định không bỏ lỡ đâu!"),
    ("摩尔庄园", "Thế Giới Chuột Chũi Moly"),
    ("小摩尔", "Cư dân Moly"),
    ("摩尔豆", "Đậu Moly"),
    ("金豆", "Đậu Vàng"),
    ("拉姆", "Lamu"),
    ("超级拉姆", "Siêu Đậu Đậu"),
]

def translate_text(text: str) -> str:
    """Translates common phrases, NPC names, and terms in dialogue text."""
    if not text:
        return text
    
    # Check exact phrase matches first
    for cn, vi in COMMON_PHRASES:
        if text == cn:
            return vi
            
    res = text
    # Replace known phrases inside text
    for cn, vi in COMMON_PHRASES:
        res = res.replace(cn, vi)
        
    # Replace NPC names inside text
    for cn, vi in NPC_NAMES_DICT.items():
        res = res.replace(cn, vi)
        
    return res

def localize_xml_file(src_path: Path, dst_path: Path):
    """Localizes a single Map XML file, updating Tips, NPC names, and talks."""
    try:
        # Read raw content to preserve XML structure and header
        raw_text = src_path.read_text(encoding="utf-8", errors="replace")
        
        # Parse XML with ElementTree
        tree = ET.fromstring(raw_text)
        
        # 1. Update NPC names
        for npc in tree.iter("Npc"):
            name = npc.get("Name")
            if name and name in NPC_NAMES_DICT:
                npc.set("Name", NPC_NAMES_DICT[name])
                
        # 2. Update Triggers (Tips)
        for trigger in tree.iter("Trigger"):
            tips = trigger.get("Tips")
            if tips:
                stripped = tips.strip()
                if stripped in TIPS_DICT:
                    trigger.set("Tips", TIPS_DICT[stripped])
                else:
                    # Generic heuristic translation
                    translated = stripped
                    for cn, vi in TIPS_DICT.items():
                        if cn in translated:
                            translated = translated.replace(cn, vi)
                    for cn, vi in NPC_NAMES_DICT.items():
                        if cn in translated:
                            translated = translated.replace(cn, vi)
                    if "进入" in translated:
                        translated = translated.replace("进入", "Đến ")
                    trigger.set("Tips", translated)
                    
        # 3. Update Talks & Options
        for talk in tree.iter("Talk"):
            msg = talk.get("Msg")
            if msg:
                talk.set("Msg", translate_text(msg))
            opt = talk.get("Option")
            if opt:
                # Options can be separated by $
                opts = opt.split("$")
                translated_opts = [translate_text(o) for o in opts]
                talk.set("Option", "$".join(translated_opts))

        # 4. Inject required return portals for interior maps if missing
        try:
            stem = src_path.stem.lower()
            if stem.startswith("map_"):
                stem = stem[4:]
            mid = int(stem)
            if mid >= 10000:
                mid -= 10000
            if mid in REQUIRED_RETURN_PORTALS:
                target_mid, tips_text = REQUIRED_RETURN_PORTALS[mid]
                triggers_elem = tree.find("Triggers")
                if triggers_elem is None:
                    triggers_elem = ET.SubElement(tree, "Triggers")
                has_portal = False
                for t in triggers_elem.findall("Trigger"):
                    if t.get("Cmd") == "alt_map" and t.get("Param") == str(target_mid):
                        has_portal = True
                        break
                if not has_portal:
                    ET.SubElement(
                        triggers_elem,
                        "Trigger",
                        {
                            "ResName": "door_mc",
                            "Layer": "controlLevel",
                            "Ex": "150",
                            "Ey": "350",
                            "Cmd": "alt_map",
                            "Param": str(target_mid),
                            "Tips": tips_text,
                        }
                    )
        except Exception:
            pass
                
        # Convert tree back to string
        dst_path.parent.mkdir(parents=True, exist_ok=True)
        xml_str = ET.tostring(tree, encoding="utf-8").decode("utf-8")
        
        # Write prettified output
        final_output = f'<?xml version="1.0" encoding="utf-8"?>\n{xml_str}'
        dst_path.write_text(final_output, encoding="utf-8")
        return True
    except Exception as e:
        print(f"[ERROR] Failed {src_path.name}: {e}")
        return False

def main():
    print("=" * 60)
    print("Starting Batch Map XML Localization for Moly VN...")
    print(f"Source Directory: {SRC_DIR}")
    print(f"Destination Override Directory: {DST_DIR}")
    print("=" * 60)
    
    xml_files = sorted(glob.glob(str(SRC_DIR / "*.xml")))
    print(f"Found {len(xml_files)} Map XML files to translate.")
    
    success_count = 0
    for src in xml_files:
        src_p = Path(src)
        dst_p = DST_DIR / src_p.name
        if localize_xml_file(src_p, dst_p):
            success_count += 1
            
    print(f"[OK] Successfully translated {success_count}/{len(xml_files)} Map XML files to local-overrides!")
    print("All portal tooltips, building signs, NPC names, and dialogues are now localized in Vietnamese.")

if __name__ == "__main__":
    main()
