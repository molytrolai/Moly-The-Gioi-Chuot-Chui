#!/usr/bin/env python3
"""Batch Localizer for 12 External Module SWFs (module/external/*.swf).

Translates and re-packs:
- AfuSmallShopPanel.swf
- BubbleMainB2.swf
- MagicSpiritMainPanel.swf
- MoleShop.swf
- NPCDialogPanel.swf
- SuperLamuGiftMain.swf
- SuperLahmIntroPanel.swf
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

JAVA_EXE = r"C:\Program Files\Microsoft\jdk-21.0.12.101-hotspot\bin\java.exe"
PROJECT_ROOT = Path(__file__).resolve().parents[1]
FFDEC_JAR = str(PROJECT_ROOT / "tools" / "ffdec-26.3.0" / "ffdec-cli.jar")

MIRROR_EXT = PROJECT_ROOT / "archive" / "clients" / "offline-mirror" / "mole.61.com" / "module" / "external"
OVERRIDES_EXT = PROJECT_ROOT / "archive" / "clients" / "local-overrides" / "mole.61.com" / "module" / "external"
OVERRIDES_EXT.mkdir(parents=True, exist_ok=True)

TEXTS_BASE = PROJECT_ROOT / "work" / "external_texts"
WORK_DIR = PROJECT_ROOT / "work" / "external_compile"
WORK_DIR.mkdir(parents=True, exist_ok=True)

TRANSLATIONS = {
    "AfuSmallShopPanel": {
        "58.txt": "Đổi Quà",
        "67.txt": "Tên Vật Phẩm",
        "74.txt": "Cần",
        "76.txt": "Bộ",
        "97.txt": "Tiệm Cũ A Phúc",
        "100.txt": "Bấm vào đây để khám phá thêm nhiều điều bất ngờ!",
        "102.txt": "Đổi lại vật phẩm đã sở hữu vẫn tiêu tốn Thẻ Phúc, hãy kiểm tra kỹ trước khi đổi!",
        "99.txt": "Vật phẩm đổi cần:\n--- RECORDSEPARATOR ---\nThẻ Phúc\n--- RECORDSEPARATOR ---\n        \n--- RECORDSEPARATOR ---\nMỗi\n--- RECORDSEPARATOR ---\n4\n--- RECORDSEPARATOR ---\nloại khác nhau\n--- RECORDSEPARATOR ---\nlà\n--- RECORDSEPARATOR ---\n1\n--- RECORDSEPARATOR ---\nđơn vị đổi\n--- RECORDSEPARATOR ---\n(\n--- RECORDSEPARATOR ---\nbộ\n--- RECORDSEPARATOR ---\n)"
    },
    "BubbleMainB2": {
        "156.txt": "Thất",
        "164.txt": "Bại",
        "166.txt": "Rồi",
        "171.txt": "Xem",
        "173.txt": "Thành",
        "175.txt": "Tích",
        "179.txt": "Của",
        "181.txt": "Bạn",
        "184.txt": "Làm",
        "186.txt": "Tốt"
    },
    "MagicSpiritMainPanel": {
        "57.txt": "Tên Cư Dân",
        "170.txt": "Tên Cư Dân",
        "350.txt": "Tên Ma Linh",
        "407.txt": "Đang Tải...",
        "409.txt": "Tên Kỹ Năng",
        "413.txt": "Đang Tải...",
        "414.txt": "Tên Kỹ Năng",
        "12.txt": "LƯU Ý QUAN TRỌNG\n--- RECORDSEPARATOR ---\nSố lượng Ma\n--- RECORDSEPARATOR ---\nLinh\n--- RECORDSEPARATOR ---\ntrong túi\n--- RECORDSEPARATOR ---\nvượt\n--- RECORDSEPARATOR ---\nquá\n--- RECORDSEPARATOR ---\n2330\n--- RECORDSEPARATOR ---\ncon sẽ\n--- RECORDSEPARATOR ---\nkhông\n--- RECORDSEPARATOR ---\nhiển\n--- RECORDSEPARATOR ---\nthị\n--- RECORDSEPARATOR ---\nđược!\n--- RECORDSEPARATOR ---\nHãy\n--- RECORDSEPARATOR ---\ndọn bớt túi."
    },
    "MoleShop": {
        "357.txt": "Trang sau"
    },
    "NPCDialogPanel": {
        "25.txt": "Tượng Nhân Ngư Thần Bí"
    },
    "SuperLamuGiftMain": {
        "298.txt": "Cấp Siêu Đậu Đậu:",
        "299.txt": "Năng lực sở hữu:",
        "300.txt": "Còn thiếu để lên cấp:",
        "301.txt": "Điểm Siêu Cấp:",
        "303.txt": "4 sao",
        "305.txt": "4 ngày",
        "432.txt": "Áo Choàng Chiến Binh Lamu",
        "438.txt": "Sân Trượt Băng Molylaya - Túp Lều Thợ Săn M",
        "439.txt": "   Giúp bạn chống đỡ mọi hiểm nguy trong thế giới Lamu!",
        "440.txt": "   Hiện không thể nhận",
        "444.txt": "Ván Trượt Cực Quang",
        "450.txt": "   Đỉnh núi tuyết Molylaya",
        "451.txt": "   Trải nghiệm trượt tuyết tốc độ cao, trở thành tay trượt cừ khôi nhất!",
        "460.txt": "Mây Tím Gió Linh",
        "466.txt": "   Hồ Thần Bí",
        "467.txt": "   Có thể cưỡi mây bay lượn tự do khắp vương quốc Moly!",
        "476.txt": "Vòng Tay Rắn Lửa",
        "482.txt": "   Rừng Rậm Hắc Ám",
        "483.txt": "   Vật phẩm hộ mệnh chứa đựng ngọn lửa thần kỳ bí ẩn!",
        "492.txt": "Vương Miện Ánh Sáng",
        "498.txt": "   Đại Sảnh Lâu Đài",
        "499.txt": "   Biểu tượng danh dự dành cho cư dân Moly xuất sắc!",
        "508.txt": "Giày Bay Tinh Tú",
        "514.txt": "   Cây Bầu Trời",
        "515.txt": "   Giúp bước chân nhẹ tựa mây bay trên mọi vùng đất!",
        "524.txt": "Cánh Thiên Thần Pha Lê",
        "530.txt": "   Quảng Trường Ái Tâm",
        "531.txt": "   Đôi cánh lung linh tỏa sáng rực rỡ trong đêm!",
        "540.txt": "Đũa Thần Cầu Vồng",
        "546.txt": "   Phố Mua Sắm Taotao",
        "547.txt": "   Phép thuật biến hình những điều kỳ diệu quanh bạn!",
        "556.txt": "Khiên Kỵ Sĩ Hoàng Kim",
        "562.txt": "   Tiền Đồn Kỵ Sĩ",
        "563.txt": "   Bảo vệ sự bình yên và công lý cho toàn vương quốc Moly!",
        "572.txt": "Cung Tên Băng Tuyết",
        "578.txt": "   Đỉnh Núi Molylaya",
        "579.txt": "   Mũi tên băng tinh khiết mang sức mạnh mùa đông vĩnh cửu!"
    },
    "SuperLahmIntroPanel": {
        "273.txt": "Mẹo nhỏ:",
        "274.txt": "Ngôi sao màu sắc Moly nằm ở cỗ xe ma thuật tại Khu vui chơi phía Đông.",
        "291.txt": "Mẹo nhỏ:",
        "292.txt": "Tìm David ở xưởng sáng chế Nông trại Vui vẻ để nhận Sợi dây Thời Gian nhé!",
        "351.txt": "Mỗi đạo cụ thần kỳ đều có công năng vô cùng đặc biệt đấy!",
        "526.txt": "   Qua thời gian dài theo dõi Đậu Đậu Siêu Cấp, tôi phát hiện các Moly và Đậu Đậu có mối gắn kết vô cùng kỳ diệu.",
        "527.txt": "   Chỉ cần trở thành Đậu Đậu Siêu Cấp, điểm Siêu Cấp sẽ tự động tăng 5 điểm mỗi ngày, tích lũy điểm càng cao cấp độ càng tăng!",
        "531.txt": "1-2 tháng",
        "532.txt": "3-5 tháng",
        "533.txt": "6-11 tháng",
        "534.txt": "12 tháng trở lên",
        "535.txt": "Cấp 1",
        "536.txt": "Cấp 2",
        "537.txt": "Cấp 3",
        "538.txt": "Cấp 4",
        "539.txt": "Cấp 5",
        "540.txt": "Điểm Siêu Cấp:",
        "541.txt": "Đặc quyền bay lượn khắp vương quốc",
        "542.txt": "Biến hình thành nhiều hình dáng kỳ thú",
        "543.txt": "Nhận hạt giống quý và đồ trang trí VIP hàng tuần",
        "544.txt": "Quyền vào Câu lạc bộ Siêu Đậu Đậu VIP",
        "545.txt": "Nhận thù lao gấp đôi khi làm thêm tại Nhà Hàng",
        "546.txt": "Giảm giá đặc biệt tại tất cả các cửa tiệm Moly",
        "547.txt": "Hiệu ứng vòng sáng thiên thần lấp lánh",
        "548.txt": "Cấp độ Siêu Cấp tối thượng đồng hành cùng bạn!"
    }
}

def main():
    print("=" * 65)
    print("   LOCALIZING 12 EXTERNAL MODULE SWFs (module/external/*.swf)")
    print("=" * 65)
    
    success_count = 0
    for mod_name, rep_dict in TRANSLATIONS.items():
        swf_name = f"{mod_name}.swf"
        src_swf = MIRROR_EXT / swf_name
        dst_swf = OVERRIDES_EXT / swf_name
        txt_dir = TEXTS_BASE / mod_name
        
        if not src_swf.exists():
            print(f"  [WARN] Source SWF not found: {src_swf}")
            continue
            
        txt_dir.mkdir(parents=True, exist_ok=True)
        # 1. Update text files
        for fname, val in rep_dict.items():
            (txt_dir / fname).write_text(val, encoding="utf-8")
            
        # 2. Recompile SWF with FFDec -importText
        tmp_swf = WORK_DIR / f"temp_{swf_name}"
        cmd = [JAVA_EXE, "-jar", FFDEC_JAR, "-importText", str(src_swf), str(tmp_swf), str(txt_dir)]
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode == 0:
            shutil.copy2(tmp_swf, dst_swf)
            print(f"  [OK] Localized and re-packed {swf_name} ({dst_swf.stat().st_size:,} bytes)")
            success_count += 1
        else:
            print(f"  [FAIL] Failed recompiling {swf_name}:\n{res.stderr}")
            
    print(f"\n[SUMMARY] Successfully localized {success_count}/{len(TRANSLATIONS)} external module SWFs!")

if __name__ == "__main__":
    main()
