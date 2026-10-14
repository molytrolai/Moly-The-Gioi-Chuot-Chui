#!/usr/bin/env python3
"""Translate TaskSummary.xml to Vietnamese for Moly-Viet."""

from pathlib import Path
import re

src_path = Path("E:/Codex/Projects/Moly-Viet/archive/clients/offline-mirror/mole.61.com/resource/xml/task/TaskSummary.xml")
dst_path = Path("E:/Codex/Projects/Moly-Viet/archive/clients/local-overrides/mole.61.com/resource/xml/task/TaskSummary.xml")
dst_path.parent.mkdir(parents=True, exist_ok=True)

content = src_path.read_text(encoding="utf-8")

group_replacements = {
    'Name="真王觉醒之路"': 'Name="Con Đường Thức Tỉnh Chân Vương"',
    'Name="王子与黑猫"': 'Name="Hoàng Tử và Mèo Đen"',
    'Name="到月亮上去"': 'Name="Hành Trình Lên Mặt Trăng"',
    'Name="庄园小夜曲"': 'Name="Khúc Dạ Hành Vương Quốc"',
    'Name="少女情怀总是诗"': 'Name="Tâm Tình Thiếu Nữ"',
    'Name="其它任务"': 'Name="Nhiệm Vụ Khác"',
    'Name="摩灵传说"': 'Name="Truyền Thuyết Linh Hồn Moly"',
    'Name="摩利亚之歌"': 'Name="Khúc Ca Moria"',
    'Name="格历尔传说"': 'Name="Truyền Thuyết Griel"',
    'Name="每日打工"': 'Name="Công Việc Hằng Ngày (SMC)"',
    'Name="摩尔成长"': 'Name="Quá Trình Trưởng Thành Moly"',
    'Name="寻回骰子"': 'Name="Tìm Lại Xúc Xắc"',
    'Name="库拉流浪记"': 'Name="Hành Trình Lưu Lạc Của Kula"',
    'Name="王子复仇记"': 'Name="Hoàng Tử Phục Thù"',
    'Name="田园浪漫季"': 'Name="Mùa Lãng Mạn Điền Viên"',
    'Name="例外任务"': 'Name="Nhiệm Vụ Đặc Biệt"',
}

for k, v in group_replacements.items():
    content = content.replace(k, v)

# Common lock message replacement
content = re.sub(r'需要完成“(.*?)”任务才能解锁哦！', r'Cần hoàn thành nhiệm vụ “\1” để mở khóa nhé!', content)
content = content.replace("摩尔豆", "Đậu Moly")
content = content.replace("么么公主", "Công chúa Meme")
content = content.replace("小摩尔", "Chuột Chũi")
content = content.replace("庄园", "Vương quốc")

# Replace top quest names
task_name_map = {
    'Name="真王觉醒"': 'Name="Chân Vương Thức Tỉnh"',
    'Name="塞拉是你吗？"': 'Name="Có Phải Là Sera Không?"',
    'Name="黑影的目标"': 'Name="Mục Tiêu Của Bóng Đen"',
    'Name="瞬间流逝的光阴"': 'Name="Thời Gian Trôi Mau"',
    'Name="万圣之夜"': 'Name="Đêm Halloween"',
    'Name="黑魔法学院"': 'Name="Học Viện Ma Pháp Hắc Ám"',
    'Name="目标是摩尔之眼"': 'Name="Mục Tiêu Là Con Mắt Moly"',
    'Name="猫怪来袭"': 'Name="Mèo Quái Dị Tấn Công"',
    'Name="塞拉的新世界"': 'Name="Thế Giới Mới Của Sera"',
    'Name="巧克力中剑"': 'Name="Thanh Kiếm Trong Socola"',
    'Name="月亮是个奶油蛋糕？"': 'Name="Mặt Trăng Là Bánh Kem?"',
    'Name="伟大的登月计划"': 'Name="Kế Hoạch Vĩ Đại Lên Mặt Trăng"',
    'Name="大大的礼物"': 'Name="Món Quà To Lớn"',
}

for k, v in task_name_map.items():
    content = content.replace(k, v)

dst_path.write_text(content, encoding="utf-8")
print("Successfully generated Vietnamese TaskSummary.xml in local-overrides!")
