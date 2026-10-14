#!/usr/bin/env python3
"""Batch SWF Localizer and Compiler for Moly - Thế Giới Chuột Chũi VN.

Compiles:
1. ui.swf -> archive/clients/local-overrides/mole.61.com/resource/ui/ui.swf
2. topUI.swf -> archive/clients/local-overrides/mole.61.com/resource/ui/topUI.swf
3. NPCDialogPanel.swf -> archive/clients/local-overrides/mole.61.com/module/external/NPCDialogPanel.swf
4. Map_10005.swf & 5.swf -> archive/clients/local-overrides/mole.61.com/resource/map/
5. Map_10006.swf & 6.swf -> archive/clients/local-overrides/mole.61.com/resource/map/
6. Map_10007.swf & 7.swf -> archive/clients/local-overrides/mole.61.com/resource/map/
7. Map_10061.swf & 61.swf -> archive/clients/local-overrides/mole.61.com/resource/map/
"""

import os
import sys
import subprocess
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

JAVA_EXE = r"C:\Program Files\Microsoft\jdk-21.0.12.101-hotspot\bin\java.exe"
PROJECT_ROOT = Path(__file__).resolve().parents[1]
FFDEC_JAR = str(PROJECT_ROOT / "tools" / "ffdec-26.3.0" / "ffdec-cli.jar")

MIRROR_ROOT = PROJECT_ROOT / "archive" / "clients" / "offline-mirror" / "mole.61.com"
OVERRIDES_ROOT = PROJECT_ROOT / "archive" / "clients" / "local-overrides" / "mole.61.com"
WORK_DIR = PROJECT_ROOT / "work" / "exported"

TARGETS = [
    # 1. UI.SWF
    {
        "name": "ui.swf",
        "src": MIRROR_ROOT / "resource" / "ui" / "ui.swf",
        "dst_list": [OVERRIDES_ROOT / "resource" / "ui" / "ui.swf"],
        "text_dir": WORK_DIR / "ui_texts",
        "replacements": {
            "265.txt": "Moly Chuột Chũi",
            "1252.txt": "Bạn có chắc muốn xóa bạn này không?\nXóa xong sẽ không còn là bạn bè nữa nhé.",
            "1268.txt": "Mười Vạn Câu Hỏi Vì Sao",
            "1698.txt": "Bạn có muốn kết bạn cùng người này không?",
            "2400.txt": "Vui lòng nhập ID Đội nhóm:",
            "2411.txt": "Vui lòng nhập lời nhắn gia nhập:",
            "2755.txt": "Công chúa Meme",
            "2950.txt": "Bạn có chắc muốn thêm người này vào danh sách chặn?",
            "3276.txt": "1 giây",
            "3526.txt": "Moly Chuột Chũi",
            "3926.txt": "Vui lòng nhập ID Moly của bạn bè:",
            "4054.txt": "Độ đói:",
            "4055.txt": "Độ khát:",
            "4056.txt": "Vệ sinh:",
            "4057.txt": "Tâm trạng:",
            "4061.txt": "Giờ",
            "4062.txt": "Tuổi:",
            "4077.txt": "Độ đói:",
            "4113.txt": "Sở Thích",
            "4143.txt": "Tôi muốn Đậu Đậu Siêu Cấp",
            "4144.txt": "Tìm hiểu Đặc quyền Siêu Cấp",
            "4385.txt": "Chúc mừng!\nBạn và người ấy đã trở thành bạn bè thân thiết.",
            "4425.txt": "Đang trò chuyện cùng bạn bè",
            "4448.txt": "Avatar Bạn Bè",
            "4449.txt": "Avatar Của Tôi",
            "4478.txt": "Nhấn Enter gửi tin",
            "4479.txt": "Ctrl+Enter gửi tin",
            "4638.txt": "Danh sách chặn những người làm phiền bạn.",
            "6544.txt": "Sử dụng tên không văn minh",
            "6545.txt": "Dùng ngôn từ xúc phạm/thiếu văn minh",
            "6546.txt": "Hỏi thăm hoặc làm lộ thông tin cá nhân",
            "6547.txt": "Sử dụng phần mềm gian lận (Hack/Cheat)",
            "6646.txt": "Tuyệt đối không chia sẻ mật khẩu cho người khác nhé!",
            "6655.txt": "Bạn nhận được lời mời cùng tham gia trò chơi!",
            "6666.txt": "Người này đã từ chối lời mời kết bạn.",
            "6749.txt": "Hiện bạn đang có",
            "6750.txt": "Bạn có chắc muốn đổi",
        }
    },
    # 2. TOPUI.SWF
    {
        "name": "topUI.swf",
        "src": MIRROR_ROOT / "resource" / "ui" / "topUI.swf",
        "dst_list": [OVERRIDES_ROOT / "resource" / "ui" / "topUI.swf"],
        "text_dir": WORK_DIR / "topui_texts",
        "replacements": {
            "81.txt": "Lâu Đài Moly",
            "442.txt": "Phúc Lợi & Sự Kiện",
            "447.txt": "Nông Sản Chung Vui",
            "452.txt": "Tiệm A Phúc",
            "216.txt": "Lần này\n--- RECORDSEPARATOR ---\nĐổi\n--- RECORDSEPARATOR ---\nkhi\n--- RECORDSEPARATOR ---\nmáy\n--- RECORDSEPARATOR ---\nchủ\n--- RECORDSEPARATOR ---\nkhởi\n--- RECORDSEPARATOR ---\nđộng\n--- RECORDSEPARATOR ---\nlại\n--- RECORDSEPARATOR ---\nsẽ\n--- RECORDSEPARATOR ---\ncó\n--- RECORDSEPARATOR ---\nhiệu\n--- RECORDSEPARATOR ---\nlực!"
        }
    },
    # 3. NPCDIALOGPANEL.SWF
    {
        "name": "NPCDialogPanel.swf",
        "src": MIRROR_ROOT / "module" / "external" / "NPCDialogPanel.swf",
        "dst_list": [OVERRIDES_ROOT / "module" / "external" / "NPCDialogPanel.swf"],
        "text_dir": WORK_DIR / "dialog_texts",
        "replacements": {
            "25.txt": "Tượng Đá Nàng Tiên Cá Thần Bí"
        }
    },
    # 4. MAP 5 (Nông trại vui vẻ)
    {
        "name": "Map_10005.swf",
        "src": MIRROR_ROOT / "resource" / "map" / "Map_10005.swf",
        "dst_list": [OVERRIDES_ROOT / "resource" / "map" / "Map_10005.swf"],
        "text_dir": WORK_DIR / "Map_10005_texts",
        "replacements": {
            "108.txt": "Trò chơi Băng Tuyết Vui Vẻ"
        }
    },
    # 5. MAP 6 (Đồng cỏ Ánh dương)
    {
        "name": "Map_10006.swf",
        "src": MIRROR_ROOT / "resource" / "map" / "Map_10006.swf",
        "dst_list": [OVERRIDES_ROOT / "resource" / "map" / "Map_10006.swf"],
        "text_dir": WORK_DIR / "Map_10006_texts",
        "replacements": {
            "96.txt": "Trò chơi Đĩa Trái Cây Vui Vẻ"
        }
    },
    # 6. MAP 7 (Học viện Lamu)
    {
        "name": "Map_10007.swf",
        "src": MIRROR_ROOT / "resource" / "map" / "Map_10007.swf",
        "dst_list": [OVERRIDES_ROOT / "resource" / "map" / "Map_10007.swf"],
        "text_dir": WORK_DIR / "Map_10007_texts",
        "replacements": {
            "133.txt": "Trò chơi Vũ Điệu Moly",
            "145.txt": "Thực phẩm an toàn bổ dưỡng, các bé Lamu cứ yên tâm thưởng thức nhé!",
            "147.txt": "Bé Thỏ Ngọc trên cung trăng buồn quá, ước gì được bay lên chơi cùng.",
            "149.txt": "Hóa ra chú Ỉn lại từng là Nguyên Soái oai phong, thật bất ngờ quá đi!",
            "151.txt": "Các bé Lamu cũng thích ăn bánh ngọt lắm, vui ghê!",
            "153.txt": "Bánh ngọt thơm phức làm ấm lòng cư dân vương quốc Moly.",
            "472.txt": "Vào Trò Chơi"
        }
    },
    # 7. MAP 61 (Tiền đồn Kỵ sĩ)
    {
        "name": "Map_10061.swf",
        "src": MIRROR_ROOT / "resource" / "map" / "Map_10061.swf",
        "dst_list": [OVERRIDES_ROOT / "resource" / "map" / "Map_10061.swf"],
        "text_dir": WORK_DIR / "Map_10061_texts",
        "replacements": {
            "105.txt": "Mau tham gia  Chiến Đấu Thiên Sứ!",
            "119.txt": "Vào Căn Cứ Bí Mật Kỵ Sĩ"
        }
    }
]

def compile_all():
    print("=== STARTING COMPILATION OF ALL CORE SWF ASSETS ===")
    success_count = 0
    total_count = len(TARGETS)

    for item in TARGETS:
        name = item["name"]
        src = item["src"]
        dst_list = item["dst_list"]
        text_dir = item["text_dir"]
        replacements = item["replacements"]

        print(f"\n[Compiling] {name}...")
        if not src.exists():
            print(f"  [ERROR] Source SWF not found: {src}")
            continue

        text_dir.mkdir(parents=True, exist_ok=True)
        for fname, text_val in replacements.items():
            tpath = text_dir / fname
            tpath.write_text(text_val, encoding="utf-8")
            print(f"  -> Prepared text {fname}: {repr(text_val[:35])}")

        primary_dst = dst_list[0]
        primary_dst.parent.mkdir(parents=True, exist_ok=True)

        cmd = [
            JAVA_EXE, "-jar", FFDEC_JAR,
            "-importText",
            str(src),
            str(primary_dst),
            str(text_dir)
        ]
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode == 0:
            sz = primary_dst.stat().st_size
            print(f"  [OK] Successfully compiled {primary_dst.name} ({sz:,} bytes)")
            for alias in dst_list[1:]:
                alias.parent.mkdir(parents=True, exist_ok=True)
                alias.write_bytes(primary_dst.read_bytes())
                print(f"  [ALIAS] Copied to {alias.name}")
            success_count += 1
        else:
            print(f"  [FAIL] Compilation error on {name}:\n{res.stderr}")

    print(f"\n=== COMPLETED: {success_count}/{total_count} CORE SWFs COMPILED SUCCESSFULLY ===")

if __name__ == "__main__":
    compile_all()
