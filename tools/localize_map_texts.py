#!/usr/bin/env python3
"""Master Map Localizer & Asset Injector for Moly - Thế Giới Chuột Chũi VN.

Combines background signboard image injection and dialogue/navigation text localization
for all core maps, saving to both Map_1000X.swf and X.swf in archive/clients/local-overrides.
"""

import os
import sys
import shutil
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
WORK_DIR = PROJECT_ROOT / "work" / "map_build_temp"
WORK_DIR.mkdir(parents=True, exist_ok=True)

MAP_CONFIGS = [
    {
        "name": "Map 1 (Lâu Đài Moly)",
        "src": OFFLINE_MAP / "Map_10001.swf",
        "dst_list": [OVERRIDES_MAP / "Map_10001.swf", OVERRIDES_MAP / "1.swf"],
        "image_replace": ("5", PROJECT_ROOT / "work" / "exported" / "Map1" / "5.jpg"),
        "text_dir": PROJECT_ROOT / "work" / "exported" / "Map1_texts",
        "texts": {
            "234.txt": "Hòm thư đây, bấm vào tôi để nhận và gửi thư nhé!",
            "173.txt": "Bé Ngoan",
            "195.txt": "Lili",
        }
    },
    {
        "name": "Map 2 (Quảng Trường Ái Tâm)",
        "src": OFFLINE_MAP / "Map_10002.swf",
        "dst_list": [OVERRIDES_MAP / "Map_10002.swf", OVERRIDES_MAP / "2.swf"],
        "image_replace": ("57", PROJECT_ROOT / "work" / "exported" / "Map2" / "57.jpg"),
        "text_dir": PROJECT_ROOT / "work" / "exported" / "Map2_texts",
        "texts": {
            "43.txt": "Đây là Hồ Ước Nguyện Thần Quy kỳ diệu! Bạn có muốn gửi điều ước vào lọ ước nguyện không?",
            "23.txt": "Bây giờ hãy thả một ít đậu vào Hồ ước nguyện nào! Tôi muốn ném        Đậu Moly cho Thần Quy!",
            "8.txt": "Bây giờ mình đã giúp bạn đặt điều ước vào lọ, bạn cần đợi một ngày. Ngày mai (trong vòng 7 ngày) hãy quay lại xem điều ước đã thành hiện thực chưa nhé~ Nếu bạn thấy có lọ trong hồ phát sáng kỳ diệu, có thể điều ước của bạn đã thành hiện thực rồi đấy!",
        }
    },
    {
        "name": "Map 3 (Phố Mua Sắm Taotao)",
        "src": OFFLINE_MAP / "Map_10003.swf",
        "dst_list": [OVERRIDES_MAP / "Map_10003.swf", OVERRIDES_MAP / "3.swf"],
        "image_replace": ("4", PROJECT_ROOT / "work" / "map_buildings" / "map3_bg_vi.jpg"),
        "text_dir": PROJECT_ROOT / "work" / "exported" / "Map3_texts",
        "texts": {
            "341.txt": "Cô Hoa",
            "188.txt": "Hì hì~ Quà tặng miễn phí đây, ghé qua nhận ngay kẻo lỡ nhé!",
            "441.txt": "Oa oa, oa oa~ Ném bom nước vào tượng đá có cơ hội gọi Công chúa Nhân Ngư đấy!",
            "45.txt": "Mone",
        }
    },
    {
        "name": "Map 4 (Bãi Trượt Tuyết Molylaya)",
        "src": OFFLINE_MAP / "Map_10004.swf",
        "dst_list": [OVERRIDES_MAP / "Map_10004.swf", OVERRIDES_MAP / "4.swf"],
        "image_replace": ("15", PROJECT_ROOT / "work" / "exported" / "Map4" / "15.jpg"),
        "text_dir": None,
        "texts": {}
    },
    {
        "name": "Map 10 (Sở Giao Thông / Tiệm Bánh)",
        "src": OFFLINE_MAP / "Map_10010.swf",
        "dst_list": [OVERRIDES_MAP / "Map_10010.swf", OVERRIDES_MAP / "10.swf"],
        "image_replace": None,
        "text_dir": PROJECT_ROOT / "work" / "exported" / "Map10_texts",
        "texts": {
            "117.txt": "Tham gia trò chơi",
            "121.txt": "A! Bạn tìm được quà Giáng Sinh David tặng tôi rồi, là một linh kiện mới tinh!",
            "124.txt": "Quà của David, bánh răng, haha! Vui quá đi!",
            "126.txt": "Cảm ơn bạn đã tìm giúp quà David tặng tôi, Giáng Sinh vui vẻ!",
            "398.txt": "A Thất",
            "44.txt": "Vào Sở Giao Thông",
            "451.txt": "Kẻ xấu, lại đến trêu trứng của tôi",
            "454.txt": "Ghét ghê á!",
            "482.txt": "Ăn nhanh lên, bạn chậm nhất đấy!",
            "488.txt": "Ăn xong về nhà sớm kẻo gặp sói xám",
            "51.txt": "Vào Nhà Ba Anh Em",
            "527.txt": "Chúng mình tuyệt đối không dùng chất bảo quản, các bé Đậu Đậu cứ yên tâm thưởng thức nhé.",
            "529.txt": "Chị Hằng Nga ở cung trăng buồn quá, ước gì được lên chơi cùng chị.",
            "531.txt": "Hóa ra Trư Bát Giới từng là Thiên Bồng Nguyên Soái, bất ngờ ghê nha.",
            "533.txt": "Các bé Đậu Đậu cũng thích ăn bánh trung thu, vui thật đấy.",
            "535.txt": "Nghe nói anh bạn bánh thập cẩm đã bị loại khỏi đội bánh rồi.",
            "604.txt": "Phim điện ảnh Thế Giới Chuột Chũi: Chuyến Tàu Phép Thuật!",
            "755.txt": "Phim điện ảnh Thế Giới Chuột Chũi: Chuyến Tàu Phép Thuật!",
        }
    },
    {
        "name": "Map 17 (Nhà Hàng Moly)",
        "src": OFFLINE_MAP / "Map_10017.swf",
        "dst_list": [OVERRIDES_MAP / "Map_10017.swf", OVERRIDES_MAP / "17.swf"],
        "image_replace": None,
        "text_dir": PROJECT_ROOT / "work" / "exported" / "Map17_texts",
        "texts": {
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
    },
    {
        "name": "Map 18 (Nhà Thờ Moly)",
        "src": OFFLINE_MAP / "Map_10018.swf",
        "dst_list": [OVERRIDES_MAP / "Map_10018.swf", OVERRIDES_MAP / "18.swf"],
        "image_replace": None,
        "text_dir": PROJECT_ROOT / "work" / "exported" / "Map18_texts",
        "texts": {
            "138.txt": "Mục sư Claw",
            "213.txt": "Món quà từ bầu trời",
            "44.txt": "Tôi là mục sư Claw, trong chuyến thám hiểm Rừng Rậm Đen, tôi đã phát hiện ra bí mật của Đậu Đậu Siêu Cấp. Hóa ra Đậu Đậu Siêu Cấp thần kỳ chỉ mở khóa khi kích hoạt đặc quyền VIP, bạn có muốn sở hữu ngay bây giờ không?",
            "45.txt": "http://127.0.0.1:18080/recharge",
            "46.txt": "Mở liên kết nạp VIP:",
        }
    }
]

def build_maps():
    print("======================================================================")
    print("      BUILDING LOCALIZED MAPS WITH USER BACKGROUNDS & TEXTS           ")
    print("======================================================================")
    
    for cfg in MAP_CONFIGS:
        name = cfg["name"]
        src = cfg["src"]
        dst_list = cfg["dst_list"]
        print(f"\n[Processing] {name}...")
        
        if not src.exists():
            print(f"  [ERROR] Source SWF not found: {src}")
            continue
            
        curr_file = src
        temp_img_out = WORK_DIR / f"temp_{src.stem}_img.swf"
        temp_txt_out = WORK_DIR / f"temp_{src.stem}_txt.swf"
        
        # 1. Image Replacement if configured
        if cfg["image_replace"]:
            tag_id, img_path = cfg["image_replace"]
            if img_path.exists():
                print(f"  Replacing Tag {tag_id} with {img_path.name}...")
                cmd = [JAVA_EXE, "-jar", FFDEC_JAR, "-replace", str(curr_file), str(temp_img_out), str(tag_id), str(img_path)]
                res = subprocess.run(cmd, capture_output=True, text=True)
                if res.returncode == 0:
                    curr_file = temp_img_out
                    print(f"  [Image OK] Injected {img_path.name}")
                else:
                    print(f"  [Image FAIL] {res.stderr}")
            else:
                print(f"  [WARN] Image file not found: {img_path}")
                
        # 2. Text Replacement if configured
        if cfg["texts"] and cfg["text_dir"]:
            text_dir = cfg["text_dir"]
            text_dir.mkdir(parents=True, exist_ok=True)
            for fname, content in cfg["texts"].items():
                (text_dir / fname).write_text(content, encoding="utf-8")
                
            print(f"  Importing {len(cfg['texts'])} localized texts...")
            cmd = [JAVA_EXE, "-jar", FFDEC_JAR, "-importText", str(curr_file), str(temp_txt_out), str(text_dir)]
            res = subprocess.run(cmd, capture_output=True, text=True)
            if res.returncode == 0:
                curr_file = temp_txt_out
                print(f"  [Text OK] Imported texts from {text_dir.name}")
            else:
                print(f"  [Text FAIL] {res.stderr}")
                
        # 3. Save to all destination aliases
        for dst in dst_list:
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(curr_file, dst)
            print(f"  [SAVED] {dst.name} ({dst.stat().st_size:,} bytes)")
            
    print("\n======================================================================")
    print("      ALL MAPS COMPILED & LOCALIZED SUCCESSFULLY!                     ")
    print("======================================================================")

if __name__ == "__main__":
    build_maps()
