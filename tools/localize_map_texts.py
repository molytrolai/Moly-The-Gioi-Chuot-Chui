#!/usr/bin/env python3
"""Localize DefineText and DefineEditText in core Map SWFs.

Updates:
- Map 1 (Lâu Đài Moly): Map_10001.swf & 1.swf
- Map 2 (Quảng Trường Ái Tâm): Map_10002.swf
- Map 3 (Phố Mua Sắm Taotao): Map_10003.swf
- Map 17 (Nhà Hàng Moly): Map_10017.swf & 17.swf
"""

import os
import sys
import subprocess
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

JAVA_EXE = r"C:\Program Files\Microsoft\jdk-21.0.12.101-hotspot\bin\java.exe"
FFDEC_JAR = r"tools\ffdec-26.3.0\ffdec-cli.jar"
PROJECT_ROOT = Path(__file__).resolve().parents[1]
OFFLINE_MAP = PROJECT_ROOT / "archive" / "clients" / "offline-mirror" / "mole.61.com" / "resource" / "map"
OVERRIDES_MAP = PROJECT_ROOT / "archive" / "clients" / "local-overrides" / "mole.61.com" / "resource" / "map"
OVERRIDES_MAP.mkdir(parents=True, exist_ok=True)

MAPS_TO_LOCALIZE = [
    {
        "src": OFFLINE_MAP / "Map_10001.swf",
        "dst_list": [OVERRIDES_MAP / "Map_10001.swf", OVERRIDES_MAP / "1.swf"],
        "text_dir": PROJECT_ROOT / "work" / "exported" / "Map1_texts",
        "replacements": {
            "234.txt": "Hòm thư đây, bấm vào tôi để nhận và gửi thư nhé!",
            "173.txt": "Bé Ngoan",
            "195.txt": "Lili",
        }
    },
    {
        "src": OFFLINE_MAP / "Map_10002.swf",
        "dst_list": [OVERRIDES_MAP / "Map_10002.swf"],
        "text_dir": PROJECT_ROOT / "work" / "exported" / "Map2_texts",
        "replacements": {
            "43.txt": "Đây là Hồ Ước Nguyện Thần Quy kỳ diệu! Bạn có muốn gửi điều ước vào lọ ước nguyện không?",
            "23.txt": "Bây giờ hãy thả một ít đậu vào Hồ ước nguyện nào! Tôi muốn ném        Đậu Moly cho Thần Quy!",
            "8.txt": "Bây giờ mình đã giúp bạn đặt điều ước vào lọ, bạn cần đợi một ngày. Ngày mai (trong vòng 7 ngày) hãy quay lại xem điều ước đã thành hiện thực chưa nhé~ Nếu bạn thấy có lọ trong hồ phát sáng kỳ diệu, có thể điều ước của bạn đã thành hiện thực rồi đấy!",
        }
    },
    {
        "src": OFFLINE_MAP / "Map_10003.swf",
        "dst_list": [OVERRIDES_MAP / "Map_10003.swf"],
        "text_dir": PROJECT_ROOT / "work" / "exported" / "Map3_texts",
        "replacements": {
            "341.txt": "Cô Hoa",
            "188.txt": "Hì hì~ Quà tặng miễn phí đây, ghé qua nhận ngay kẻo lỡ nhé!",
            "441.txt": "Oa oa, oa oa~ Ném bom nước vào tượng đá có cơ hội gọi Công chúa Nhân Ngư đấy!",
            "45.txt": "Mone",
        }
    },
    {
        "src": OFFLINE_MAP / "Map_10017.swf",
        "dst_list": [OVERRIDES_MAP / "Map_10017.swf", OVERRIDES_MAP / "17.swf"],
        "text_dir": PROJECT_ROOT / "work" / "exported" / "Map17_texts",
        "replacements": {
            "246.txt": "Vào Lâu Đài Moly",
            "373.txt": "Nick",
            "459.txt": "Vào làm thêm tại Nhà Hàng",
            "464.txt": "Trò chơi Đầu Bếp Vui Vẻ",
            "467.txt": "Trò chơi Làm Thêm Nhà Hàng",
            "61.txt": "Này bạn! Muốn làm thêm không? Mặc đồng phục phục vụ, chăm chỉ làm việc 5 phút là bạn sẽ nhận được phần thù lao xứng đáng. Nhắc bạn nhé: làm việc phải chuyên tâm, bỏ chạy giữa chừng là tôi không trả lương đâu đấy.",
            "73.txt": "Chọn xong công việc rồi thì mau rời máy tính, đi giúp mẹ làm việc nhà đi nhé! Lát nữa quay lại.",
            "87.txt": "Nấu bánh ú như thế nào?",
            "98.txt": "Tôi là chiếc nồi 'Cháy hết lòng mình, sưởi ấm dạ dày bạn', chuyên trách nấu bánh ú thơm ngon.",
        }
    }
]

def main():
    print("Localizing Core Map SWF texts...")
    for item in MAPS_TO_LOCALIZE:
        src = item["src"]
        text_dir = item["text_dir"]
        text_dir.mkdir(parents=True, exist_ok=True)
        
        # 1. Update text files
        for fname, content in item["replacements"].items():
            fpath = text_dir / fname
            fpath.write_text(content, encoding="utf-8")
            print(f"  [Text] {item['src'].name} -> {fname}: {content[:35]}...")
            
        # 2. Import into SWF
        primary_dst = item["dst_list"][0]
        cmd = [
            JAVA_EXE, "-jar", FFDEC_JAR,
            "-importText",
            str(src),
            str(primary_dst),
            str(text_dir)
        ]
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode == 0:
            print(f"  [SWF OK] Compiled {primary_dst.name} ({os.path.getsize(primary_dst)} bytes)")
            # Copy to alias destinations (e.g. 1.swf, 17.swf)
            content_bytes = primary_dst.read_bytes()
            for alias in item["dst_list"][1:]:
                alias.write_bytes(content_bytes)
                print(f"  [SWF ALIAS] Copied to {alias.name}")
        else:
            print(f"  [SWF ERROR] {primary_dst.name}: {res.stderr}")

if __name__ == "__main__":
    main()
