import os
import subprocess
from pathlib import Path

JAVA_EXE = r"C:\Program Files\Microsoft\jdk-21.0.12.101-hotspot\bin\java.exe"
FFDEC_JAR = r"tools\ffdec-26.3.0\ffdec.jar"

src_swf = r"archive\clients\offline-mirror\mole.61.com\resource\login\LoginHome.swf"
dst_dir = Path(r"archive\clients\local-overrides\mole.61.com\resource\login")
dst_dir.mkdir(parents=True, exist_ok=True)
dst_swf = str(dst_dir / "LoginHome.swf")
texts_dir = r"work\exported\LoginHome\texts"

# Write localized 232.txt
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

# Write localized 234.txt
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

# Write localized 197.txt
text_197 = """Phiên bản Moly Việt
--- RECORDSEPARATOR ---
[2026]
--- RECORDSEPARATOR ---
v1.0
--- RECORDSEPARATOR ---
Máy chủ nội bộ
--- RECORDSEPARATOR ---
Cộng
--- RECORDSEPARATOR ---
đồng
--- RECORDSEPARATOR ---
Tuổi thơ
--- RECORDSEPARATOR ---
[2026]MOLY-VN
--- RECORDSEPARATOR ---
VN"""

Path(r"work\exported\LoginHome\texts\197.txt").write_text(text_197, encoding="utf-8")

print("Importing texts into LoginHome.swf...")
cmd = [
    JAVA_EXE, "-jar", FFDEC_JAR,
    "-importText",
    src_swf,
    dst_swf,
    texts_dir
]

res = subprocess.run(cmd, capture_output=True, text=True)
print("Return code:", res.returncode)
print("Stdout:", res.stdout)
print("Stderr:", res.stderr)
if os.path.exists(dst_swf):
    print(f"Generated {dst_swf} successfully! Size: {os.path.getsize(dst_swf)} bytes")
