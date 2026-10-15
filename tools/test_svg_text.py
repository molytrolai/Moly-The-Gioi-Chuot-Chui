import subprocess
from pathlib import Path

JAVA_EXE = r"C:\Program Files\Microsoft\jdk-21.0.12.101-hotspot\bin\java.exe"
FFDEC_JAR = r"tools\ffdec-26.3.0\ffdec-cli.jar"

test_dir = Path("work/test_svg_text")
test_dir.mkdir(parents=True, exist_ok=True)

# Test SVG with <text>
svg_content = '''<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg xmlns:ffdec="https://www.free-decompiler.com/flash" xmlns:xlink="http://www.w3.org/1999/xlink" ffdec:objectType="shape" height="67px" width="147px" xmlns="http://www.w3.org/2000/svg">
  <g transform="matrix(1.0, 0.0, 0.0, 1.0, 73.5, 33.5)">
    <rect x="-70" y="-30" width="140" height="60" rx="15" ry="15" fill="#f5780f" stroke="#dc4600" stroke-width="3"/>
    <text x="0" y="8" font-family="Arial" font-size="22" font-weight="bold" text-anchor="middle" fill="#ffffff">ĐĂNG NHẬP</text>
  </g>
</svg>'''

svg_path = test_dir / "171.svg"
svg_path.write_text(svg_content, encoding="utf-8")

cmd = [
    JAVA_EXE, "-jar", FFDEC_JAR,
    "-replace",
    "archive/clients/local-overrides/mole.61.com/resource/login/Login.swf",
    str(test_dir / "Login_out.swf"),
    "171",
    str(svg_path)
]
res = subprocess.run(cmd, capture_output=True, text=True)
print("Replace return code:", res.returncode)
print("Stdout:", res.stdout)
print("Stderr:", res.stderr)
