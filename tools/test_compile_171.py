import subprocess
from pathlib import Path

JAVA_EXE = r"C:\Program Files\Microsoft\jdk-21.0.12.101-hotspot\bin\java.exe"
FFDEC_JAR = r"tools\ffdec-26.3.0\ffdec-cli.jar"

# Pass ĐĂNG NHẬP via UTF-8 stdin
p = subprocess.Popen([JAVA_EXE, "tools/TextToSvgPath.java", "Arial", "bold", "21", "true"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
stdout, stderr = p.communicate(input="ĐĂNG NHẬP".encode("utf-8"))
out_str = stdout.decode("utf-8")

lines = out_str.splitlines()
path_str = ""
for l in lines:
    if l.startswith("PATH:"):
        path_str = l[5:]

test_dir = Path("work/test_svg_vector")
test_dir.mkdir(parents=True, exist_ok=True)

svg_content = f'''<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg xmlns:ffdec="https://www.free-decompiler.com/flash" xmlns:xlink="http://www.w3.org/1999/xlink" ffdec:objectType="shape" height="66.4px" width="146.8px" xmlns="http://www.w3.org/2000/svg">
  <g transform="matrix(1.0, 0.0, 0.0, 1.0, 73.4, 33.2)">
    <path d="M60.95 -16.3 Q51.3 -25.75 37.65 -25.75 L-41.15 -25.75 Q-54.9 -25.75 -64.55 -16.3 -74.2 -6.95 -74.2 6.45 -74.2 19.8 -64.55 29.2 -54.9 38.65 -41.15 38.65 L37.65 38.65 Q51.3 38.65 60.95 29.2 70.6 19.8 70.6 6.45 70.6 -6.95 60.95 -16.3 Z" fill="none" stroke="url(#gradient0)" stroke-linecap="round" stroke-linejoin="round" stroke-width="2.0"/>
    <path d="{path_str}" fill="#fee892" stroke="#a52c0e" stroke-width="6.0" stroke-linecap="round" stroke-linejoin="round"/>
    <path d="{path_str}" fill="url(#gradient1)" stroke="#c23512" stroke-width="2.0" stroke-linecap="round" stroke-linejoin="round"/>
    <path d="{path_str}" fill="#ffffff" fill-opacity="0.6"/>
  </g>
  <defs>
    <linearGradient gradientTransform="matrix(0.0, 0.0457, -0.0754, 0.0, 408.25, 7.65)" gradientUnits="userSpaceOnUse" id="gradient0" spreadMethod="pad" x1="-819.2" x2="819.2">
      <stop offset="0.0" stop-color="#ffffec" stop-opacity="0.498"/>
      <stop offset="1.0" stop-color="#fffff3" stop-opacity="0.207"/>
    </linearGradient>
    <linearGradient gradientTransform="matrix(0.0, 0.0229, -0.024, 0.0, 26.7, 6.3)" gradientUnits="userSpaceOnUse" id="gradient1" spreadMethod="pad" x1="-819.2" x2="819.2">
      <stop offset="0.0" stop-color="#ffff00"/>
      <stop offset="1.0" stop-color="#ff9900"/>
    </linearGradient>
  </defs>
</svg>'''

(test_dir / "171.svg").write_text(svg_content, encoding="utf-8")

subprocess.run([
    JAVA_EXE, "-jar", FFDEC_JAR,
    "-replace",
    "archive/clients/local-overrides/mole.61.com/resource/login/Login.swf",
    str(test_dir / "Login_vector.swf"),
    "171",
    str(test_dir / "171.svg")
], check=True)

subprocess.run([
    JAVA_EXE, "-jar", FFDEC_JAR,
    "-selectid", "171",
    "-format", "shape:png",
    "-export", "shape",
    str(test_dir),
    str(test_dir / "Login_vector.swf")
], check=True)

print("SUCCESS: UTF-8 Vietnamese vector shape compiled!")
