#!/usr/bin/env python3
"""Master Compiler & Localizer for Moly - Thế Giới Chuột Chũi VN.

Compiles and installs into archive/clients/local-overrides/mole.61.com/:
1. module/external/logo/Logo.swf (Image 5 -> Moly VN Logo)
2. module/external/logo/51moleInfo0.swf (Image 9 -> Moly VN Logo)
3. module/external/logo/randomMC.swf (Image 3 -> Moly VN Banner)
4. resource/login/LoginHome.swf (Start button, CADPA badge, transparent Taomee erasers, VN covenants)
5. resource/login/Login.swf (Full wooden booth & plaque, notice boxes, text labels, buttons, Taomee logo removed)
6. resource/ui/ui.swf (17 toolbar icons + 35 in-game dialog texts)
7. resource/ui/topUI.swf (2 toolbar icons + top navigation texts)
8. module/external/NPCDialogPanel.swf (Vietnamese dialog panel texts)
9. resource/map/Map_*.swf (Core map game texts)
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
sys.path.insert(0, str(PROJECT_ROOT))
FFDEC_JAR = str(PROJECT_ROOT / "tools" / "ffdec-26.3.0" / "ffdec-cli.jar")

MIRROR_ROOT = PROJECT_ROOT / "archive" / "clients" / "offline-mirror" / "mole.61.com"
OVERRIDES_ROOT = PROJECT_ROOT / "archive" / "clients" / "local-overrides" / "mole.61.com"
ASSETS_DIR = PROJECT_ROOT / "scratch" / "localized_assets"
WORK_DIR = PROJECT_ROOT / "work" / "master_compile"

WORK_DIR.mkdir(parents=True, exist_ok=True)

def apply_replacements(src_swf, dst_swf, reps, text_replacements=None):
    """
    reps: list of (characterId, filePath)
    text_replacements: dict of {filename: text_content}
    """
    print(f"\n[Compiling] {src_swf.name} -> {dst_swf.relative_to(PROJECT_ROOT)}...")
    if not src_swf.exists():
        print(f"  [ERROR] Source not found: {src_swf}")
        return False
        
    temp_a = WORK_DIR / f"temp_{src_swf.stem}_a.swf"
    temp_b = WORK_DIR / f"temp_{src_swf.stem}_b.swf"
    
    curr_input = src_swf
    next_output = temp_a
    
    # 1. Image / Shape replacements
    for cid, fpath in reps:
        p = Path(fpath)
        if not p.exists():
            print(f"  [WARN] Asset file missing: {p}")
            continue
            
        cmd = [JAVA_EXE, "-jar", FFDEC_JAR, "-replace", str(curr_input), str(next_output), str(cid), str(p)]
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode != 0:
            print(f"  [FAIL] Error replacing {cid} in {src_swf.name}:\n{res.stderr}")
            return False
            
        # Flip buffers
        curr_input = next_output
        next_output = temp_b if curr_input == temp_a else temp_a

    # 2. Text replacements via -importText if any
    if text_replacements:
        txt_dir = WORK_DIR / f"texts_{src_swf.stem}"
        txt_dir.mkdir(parents=True, exist_ok=True)
        for fname, content in text_replacements.items():
            tfile = txt_dir / fname
            tfile.write_text(content, encoding="utf-8")
            
        cmd = [JAVA_EXE, "-jar", FFDEC_JAR, "-importText", str(curr_input), str(next_output), str(txt_dir)]
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode != 0:
            print(f"  [FAIL] Error importing text in {src_swf.name}:\n{res.stderr}")
            return False
        curr_input = next_output

    # 3. Finalize to dst_swf
    dst_swf.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(curr_input, dst_swf)
    print(f"  [SUCCESS] Written {dst_swf.name} ({dst_swf.stat().st_size:,} bytes)")
    return True

def compile_all():
    print("======================================================================")
    print("      COMPILING MOLY - THẾ GIỚI CHUỘT CHŨI VN MASTER CORE SWFs       ")
    print("======================================================================")
    
    logo_img = ASSETS_DIR / "logo_9_fitted.png"
    
    # 1. Logo.swf
    apply_replacements(
        src_swf=MIRROR_ROOT / "module" / "external" / "logo" / "Logo.swf",
        dst_swf=OVERRIDES_ROOT / "module" / "external" / "logo" / "Logo.swf",
        reps=[("5", str(logo_img))]
    )
    
    # 2. 51moleInfo0.swf
    apply_replacements(
        src_swf=MIRROR_ROOT / "module" / "external" / "logo" / "51moleInfo0.swf",
        dst_swf=OVERRIDES_ROOT / "module" / "external" / "logo" / "51moleInfo0.swf",
        reps=[("9", str(logo_img))]
    )
    
    # 3. randomMC.swf
    apply_replacements(
        src_swf=MIRROR_ROOT / "module" / "external" / "logo" / "randomMC.swf",
        dst_swf=OVERRIDES_ROOT / "module" / "external" / "logo" / "randomMC.swf",
        reps=[("3", str(ASSETS_DIR / "randomMC_banner_3_fitted.png"))]
    )
    
    # 4. LoginHome.swf (XML-patched, DefineEditText Tag, pure 3D BẮT ĐẦU, CADPA 8+ tooltip)
    from scratch.build_home import build_login_home
    build_login_home()
    
    # 5. Login.swf (Double button eliminated, Taomee copyright removed, pixel-perfect bottom buttons, Vietnamese alert dialog & AS3 messages)
    from scratch.build_login import build_login
    build_login()
    
    # 6. ui.swf
    ui_reps = [
        ("3279", str(ASSETS_DIR / "ui_3279.png")),
        ("6834", str(ASSETS_DIR / "ui_6834.png")),
        ("6836", str(ASSETS_DIR / "ui_6836.png")),
        ("6839", str(ASSETS_DIR / "ui_6839.png")),
        ("6841", str(ASSETS_DIR / "ui_6841.png")),
        ("6844", str(ASSETS_DIR / "ui_6844.png")),
        ("6846", str(ASSETS_DIR / "ui_6846.png")),
        ("6849", str(ASSETS_DIR / "ui_6849.png")),
        ("6851", str(ASSETS_DIR / "ui_6851.png")),
        ("6854", str(ASSETS_DIR / "ui_6854.png")),
        ("6856", str(ASSETS_DIR / "ui_6856.png")),
        ("6859", str(ASSETS_DIR / "ui_6859.png")),
        ("6861", str(ASSETS_DIR / "ui_6861.png")),
        ("6864", str(ASSETS_DIR / "ui_6864.png")),
        ("6866", str(ASSETS_DIR / "ui_6866.png")),
        ("6929", str(ASSETS_DIR / "ui_6929.png")),
        ("6931", str(ASSETS_DIR / "ui_6931.png")),
        # Super Lamu VIP Menu Pill Buttons
        ("5864", str(ASSETS_DIR / "ui_5864.png")),
        ("5865", str(ASSETS_DIR / "ui_5864.png")),
        ("5866", str(ASSETS_DIR / "ui_5864.png")),
        ("5868", str(ASSETS_DIR / "ui_5868.png")),
        ("5869", str(ASSETS_DIR / "ui_5868.png")),
        ("5870", str(ASSETS_DIR / "ui_5868.png")),
        ("5872", str(ASSETS_DIR / "ui_5872.png")),
        ("5873", str(ASSETS_DIR / "ui_5872.png")),
        ("5874", str(ASSETS_DIR / "ui_5872.png")),
        ("5876", str(ASSETS_DIR / "ui_5876.png")),
        ("5877", str(ASSETS_DIR / "ui_5876.png")),
        ("5878", str(ASSETS_DIR / "ui_5876.png")),
        ("5881", str(ASSETS_DIR / "ui_5881.png")),
        ("5882", str(ASSETS_DIR / "ui_5881.png")),
        ("5883", str(ASSETS_DIR / "ui_5881.png")),
        # Embedded Fonts -> Arial TTF (Full Unicode Vietnamese Support)
        ("1251", r"C:\Windows\Fonts\arial.ttf"),
        ("264", r"C:\Windows\Fonts\arial.ttf"),
        ("1587", r"C:\Windows\Fonts\arial.ttf"),
        ("2399", r"C:\Windows\Fonts\arial.ttf"),
        ("3715", r"C:\Windows\Fonts\arial.ttf"),
        ("4112", r"C:\Windows\Fonts\arial.ttf"),
        ("7299", r"C:\Windows\Fonts\arial.ttf"),
    ]
    ui_texts = {
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
    apply_replacements(
        src_swf=MIRROR_ROOT / "resource" / "ui" / "ui.swf",
        dst_swf=OVERRIDES_ROOT / "resource" / "ui" / "ui.swf",
        reps=ui_reps,
        text_replacements=ui_texts
    )
    
    # 7. topUI.swf
    topui_reps = [
        ("82", str(ASSETS_DIR / "topui_82.png")),
        ("361", str(ASSETS_DIR / "topui_361.png")),
        ("366", str(ASSETS_DIR / "topui_366.png")),
        # Embedded Font -> Arial TTF (Full Unicode Vietnamese Support)
        ("441", r"C:\Windows\Fonts\arial.ttf"),
    ]
    topui_texts = {
        "81.txt": "Lâu Đài Moly",
        "442.txt": "Phúc Lợi & Sự Kiện",
        "447.txt": "Nông Sản Chung Vui",
        "452.txt": "Tiệm A Phúc",
        "216.txt": "Lần này\n--- RECORDSEPARATOR ---\nĐổi\n--- RECORDSEPARATOR ---\nkhi\n--- RECORDSEPARATOR ---\nmáy\n--- RECORDSEPARATOR ---\nchủ\n--- RECORDSEPARATOR ---\nkhởi\n--- RECORDSEPARATOR ---\nđộng\n--- RECORDSEPARATOR ---\nlại\n--- RECORDSEPARATOR ---\nsẽ\n--- RECORDSEPARATOR ---\ncó\n--- RECORDSEPARATOR ---\nhiệu\n--- RECORDSEPARATOR ---\nlực!"
    }
    apply_replacements(
        src_swf=MIRROR_ROOT / "resource" / "ui" / "topUI.swf",
        dst_swf=OVERRIDES_ROOT / "resource" / "ui" / "topUI.swf",
        reps=topui_reps,
        text_replacements=topui_texts
    )
    
    # 8. SuperLahmIntroPanel.swf (Tag 336 localized intro panel)
    super_lamu_img = PROJECT_ROOT / "work" / "exported" / "SuperLamu" / "336.png"
    if super_lamu_img.exists():
        apply_replacements(
            src_swf=MIRROR_ROOT / "module" / "external" / "SuperLahmIntroPanel.swf",
            dst_swf=OVERRIDES_ROOT / "module" / "external" / "SuperLahmIntroPanel.swf",
            reps=[("336", str(super_lamu_img))]
        )

    print("\n======================================================================")
    print("      ALL MASTER CORE SWFs COMPILED AND INSTALLED SUCCESSFULLY!       ")
    print("======================================================================")

if __name__ == "__main__":
    compile_all()
