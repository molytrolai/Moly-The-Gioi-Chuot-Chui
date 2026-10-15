import subprocess
import base64
from pathlib import Path
from PIL import Image

JAVA_EXE = r"C:\Program Files\Microsoft\jdk-21.0.12.101-hotspot\bin\java.exe"
FFDEC_JAR = r"tools\ffdec-26.3.0\ffdec-cli.jar"

test_dir = Path("work/test_svg_embed")
test_dir.mkdir(parents=True, exist_ok=True)

# Generate a PNG of "ĐĂNG NHẬP"
# Create 147x67 image
png_path = test_dir / "btn_test.png"
im = Image.new("RGBA", (147, 67), (255, 0, 0, 255))
im.save(png_path)
with open(png_path, "rb") as f:
    b64 = base64.b64encode(f.read()).decode("ascii")

# Test A: SVG with embedded image
svg_content = f'''<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg xmlns:ffdec="https://www.free-decompiler.com/flash" xmlns:xlink="http://www.w3.org/1999/xlink" ffdec:objectType="shape" height="67px" width="147px" xmlns="http://www.w3.org/2000/svg">
  <g transform="matrix(1.0, 0.0, 0.0, 1.0, 73.5, 33.5)">
    <image x="-73.5" y="-33.5" width="147" height="67" xlink:href="data:image/png;base64,{b64}"/>
  </g>
</svg>'''

svg_path = test_dir / "171.svg"
svg_path.write_text(svg_content, encoding="utf-8")

in_swf = "archive/clients/local-overrides/mole.61.com/resource/login/Login.swf"
out_swf = str(test_dir / "Login_test_svg.swf")

cmd = [
    JAVA_EXE, "-jar", FFDEC_JAR,
    "-importShapes",
    in_swf,
    out_swf,
    str(test_dir)
]
res = subprocess.run(cmd, capture_output=True, text=True)
print("ImportShapes with embedded image return code:", res.returncode)
print("Stdout:", res.stdout)
print("Stderr:", res.stderr)
