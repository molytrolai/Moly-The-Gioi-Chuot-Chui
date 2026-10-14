import os
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

JAVA_EXE = r"C:\Program Files\Microsoft\jdk-21.0.12.101-hotspot\bin\java.exe"
FFDEC_JAR = r"tools\ffdec-26.3.0\ffdec.jar"

PROJECT_ROOT = Path(r"E:\Codex\Projects\Moly-Viet")
OVERRIDES_ROOT = PROJECT_ROOT / "archive" / "clients" / "local-overrides" / "mole.61.com"
OFFLINE_MIRROR = PROJECT_ROOT / "archive" / "clients" / "offline-mirror" / "mole.61.com"

# 1. Localize loadingWord.xml
loading_word_path = OVERRIDES_ROOT / "resource" / "xml" / "logo" / "loadingWord.xml"
loading_word_path.parent.mkdir(parents=True, exist_ok=True)
loading_word_content = "_Chào mừng bạn đến với Moly - Thế Giới Chuột Chũi!_Máy chủ Việt Nam sẵn sàng!_Chúc các cư dân phiêu lưu vui vẻ!_Đậu Đậu Siêu Cấp đồng hành cùng bạn!_"
loading_word_path.write_text(loading_word_content, encoding="utf-8")
print("[OK] Localized loadingWord.xml created.")

# 2. Localize LoginHome.swf
login_home_dir = OVERRIDES_ROOT / "resource" / "login"
login_home_dir.mkdir(parents=True, exist_ok=True)
src_login_home = OFFLINE_MIRROR / "resource" / "login" / "LoginHome.swf"
dst_login_home = login_home_dir / "LoginHome.swf"

# Update text files in work/exported/LoginHome/texts
text_232 = """LƯU Ý DÀNH CHO CƯ DÂN
--- RECORDSEPARATOR ---
1
--- RECORDSEPARATOR ---
. 
--- RECORDSEPARATOR ---
Moly - Thế Giới Chuột Chũi là tựa game cộng đồng nuôi dưỡng tuổi thơ, phù hợp cho
--- RECORDSEPARATOR ---
mọi lứa tuổi
--- RECORDSEPARATOR ---
từ
--- RECORDSEPARATOR ---
8
--- RECORDSEPARATOR ---
tuổi trở lên
--- RECORDSEPARATOR ---
. Chúc các bạn nhỏ có
--- RECORDSEPARATOR ---
những phút giây phiêu lưu bổ ích và vui vẻ.
--- RECORDSEPARATOR ---
2
--- RECORDSEPARATOR ---
. 
--- RECORDSEPARATOR ---
Người chơi hóa thân thành những chú Chuột Chũi Moly đáng yêu, cùng xây dựng gia
--- RECORDSEPARATOR ---
viên, trồng trọt nông trại, chăm sóc Đậu Đậu và kết nối bạn bè khắp nơi. Thế giới
--- RECORDSEPARATOR ---
Moly mang đến không gian giải trí an toàn, lành mạnh và giàu tính giáo dục.
--- RECORDSEPARATOR ---
3
--- RECORDSEPARATOR ---
. 
--- RECORDSEPARATOR ---
Máy chủ Moly Việt Nam hiện mở cửa
--- RECORDSEPARATOR ---
trải nghiệm miễn phí
--- RECORDSEPARATOR ---
,
--- RECORDSEPARATOR ---
hỗ trợ đầy đủ tính năng
--- RECORDSEPARATOR ---
.
--- RECORDSEPARATOR ---
4
--- RECORDSEPARATOR ---
. 
--- RECORDSEPARATOR ---
Hệ thống tài khoản bảo mật và chống gian lận tự động:
--- RECORDSEPARATOR ---
Các cư dân lưu ý
--- RECORDSEPARATOR ---
bảo vệ mật khẩu cá nhân,
--- RECORDSEPARATOR ---
không chia sẻ thông tin cho người khác
--- RECORDSEPARATOR ---
để
--- RECORDSEPARATOR ---
tránh
--- RECORDSEPARATOR ---
mất tài khoản.
--- RECORDSEPARATOR ---
5
--- RECORDSEPARATOR ---
. 
--- RECORDSEPARATOR ---
Hãy cùng nhau xây dựng Vương Quốc Moly văn minh, thân thiện và tràn ngập niềm vui,
--- RECORDSEPARATOR ---
khám phá bao điều kỳ diệu đang đón chờ bạn mỗi ngày!"""

Path(r"work\exported\LoginHome\texts\232.txt").write_text(text_232, encoding="utf-8")

text_234 = """QUY ƯỚC CƯ DÂN VĂN MINH
--- RECORDSEPARATOR ---
•
--- RECORDSEPARATOR ---
BẢO VỆ TÀI KHOẢN
--- RECORDSEPARATOR ---
•
--- RECORDSEPARATOR ---
 
--- RECORDSEPARATOR ---
TRẢI
--- RECORDSEPARATOR ---
NGHIỆM
--- RECORDSEPARATOR ---
LÀNH MẠNH
--- RECORDSEPARATOR ---
•
--- RECORDSEPARATOR ---
 
--- RECORDSEPARATOR ---
PHÂN BỔ
--- RECORDSEPARATOR ---
THỜI GIAN
--- RECORDSEPARATOR ---
 
--- RECORDSEPARATOR ---
HỢP
--- RECORDSEPARATOR ---
LÝ
--- RECORDSEPARATOR ---
VÀ
--- RECORDSEPARATOR ---
TẬN HƯỞNG
--- RECORDSEPARATOR ---
NIỀM
--- RECORDSEPARATOR ---
VUI
--- RECORDSEPARATOR ---
CÙNG
--- RECORDSEPARATOR ---
MOLY
--- RECORDSEPARATOR ---
VIỆT
--- RECORDSEPARATOR ---
 
--- RECORDSEPARATOR ---
NAM
--- RECORDSEPARATOR ---
!"""

Path(r"work\exported\LoginHome\texts\234.txt").write_text(text_234, encoding="utf-8")

# Also create modern graphics for 171.png (publisher logo) and 236.png (header notice badge)
img_dir = Path(r"work\exported\LoginHome\images")
img_dir.mkdir(parents=True, exist_ok=True)

# 171.png: (114, 37) - Moly Viet brand badge
img_171 = Image.new("RGBA", (114, 37), (0, 0, 0, 0))
draw = ImageDraw.Draw(img_171)
draw.rounded_rectangle([(2, 2), (111, 34)], radius=8, fill=(234, 88, 12, 230), outline=(254, 215, 170, 255), width=2)
# Draw text
draw.text((16, 9), "MOLY VIỆT", fill=(255, 255, 255))
img_171.save(img_dir / "171.png")

# 236.png: (135, 41) - Notice button
img_236 = Image.new("RGBA", (135, 41), (0, 0, 0, 0))
draw = ImageDraw.Draw(img_236)
draw.rounded_rectangle([(2, 2), (132, 38)], radius=8, fill=(30, 41, 59, 230), outline=(59, 130, 246, 255), width=2)
draw.text((14, 11), "Lưu Ý Cư Dân", fill=(255, 255, 255))
img_236.save(img_dir / "236.png")

# Import texts into LoginHome.swf
subprocess.run([
    JAVA_EXE, "-jar", FFDEC_JAR,
    "-importText",
    str(src_login_home),
    str(dst_login_home),
    r"work\exported\LoginHome\texts"
], check=True)

# Import images into LoginHome.swf
subprocess.run([
    JAVA_EXE, "-jar", FFDEC_JAR,
    "-importImages",
    str(dst_login_home),
    str(dst_login_home),
    r"work\exported\LoginHome\images"
], check=True)

print(f"[OK] Localized LoginHome.swf generated: {dst_login_home} ({dst_login_home.stat().st_size} bytes)")

# 3. Localize Login.swf
dst_login = login_home_dir / "Login.swf"
src_login = OFFLINE_MIRROR / "resource" / "login" / "Login.swf"

login_texts_dir = Path(r"work\exported\Login\texts")
(login_texts_dir / "37.txt").write_text("Đổi mã khác", encoding="utf-8")
(login_texts_dir / "39.txt").write_text("Đổi mã khác", encoding="utf-8")
(login_texts_dir / "138.txt").write_text("Đổi mã khác", encoding="utf-8")
(login_texts_dir / "141.txt").write_text("Đổi mã khác", encoding="utf-8")
(login_texts_dir / "192.txt").write_text("Đổi mã khác", encoding="utf-8")
(login_texts_dir / "151.txt").write_text("© 2026 Moly Việt. Thế Giới Chuột Chũi.", encoding="utf-8")
(login_texts_dir / "215.txt").write_text("Nhập tên máy chủ...", encoding="utf-8")
(login_texts_dir / "275.txt").write_text("Sân Băng Moly", encoding="utf-8")
(login_texts_dir / "287.txt").write_text("Mã xác thực không đúng, vui lòng nhập lại!", encoding="utf-8")
(login_texts_dir / "50.txt").write_text("Tôi đã đọc và đồng ý với 《\n--- RECORDSEPARATOR ---\n                  \n--- RECORDSEPARATOR ---\nĐiều khoản Cư Dân Moly》", encoding="utf-8")

subprocess.run([
    JAVA_EXE, "-jar", FFDEC_JAR,
    "-importText",
    str(src_login),
    str(dst_login),
    str(login_texts_dir)
], check=True)

print(f"[OK] Localized Login.swf generated: {dst_login} ({dst_login.stat().st_size} bytes)")
