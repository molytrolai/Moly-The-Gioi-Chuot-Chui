import subprocess
from pathlib import Path

JAVA_EXE = r"C:\Program Files\Microsoft\jdk-21.0.12.101-hotspot\bin\java.exe"
FFDEC_JAR = r"tools\ffdec-26.3.0\ffdec-cli.jar"

# Generate path using TextToSvgPath
cmd_path = [JAVA_EXE, "tools/TextToSvgPath.java"]
res_path = subprocess.run(cmd_path, capture_output=True, text=True)

test_dir = Path("work/test_svg_vector")
test_dir.mkdir(parents=True, exist_ok=True)

# Build complete 171.svg with the generated path
# Center "ĐĂNG NHẬP"
svg_content = f'''<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg xmlns:ffdec="https://www.free-decompiler.com/flash" xmlns:xlink="http://www.w3.org/1999/xlink" ffdec:objectType="shape" height="66.4px" width="146.8px" xmlns="http://www.w3.org/2000/svg">
  <g transform="matrix(1.0, 0.0, 0.0, 1.0, 75.2, 26.75)">
    <!-- Outer glossy outline from original 171.svg -->
    <path d="M60.95 -16.3 Q51.3 -25.75 37.65 -25.75 L-41.15 -25.75 Q-54.9 -25.75 -64.55 -16.3 -74.2 -6.95 -74.2 6.45 -74.2 19.8 -64.55 29.2 -54.9 38.65 -41.15 38.65 L37.65 38.65 Q51.3 38.65 60.95 29.2 70.6 19.8 70.6 6.45 70.6 -6.95 60.95 -16.3 Z" fill="none" stroke="url(#gradient0)" stroke-linecap="round" stroke-linejoin="round" stroke-width="2.0"/>
    
    <!-- Vector text: ĐĂNG NHẬP with stroke and gradient fill -->
    <!-- Shadow stroke -->
    <g transform="translate(-62, 14)">
      <path d="{res_path.stdout.split('Generated SVG path: ')[1].strip()}" fill="#fee892" stroke="#a52c0e" stroke-width="6.0" stroke-linecap="round" stroke-linejoin="round"/>
      <path d="{res_path.stdout.split('Generated SVG path: ')[1].strip()}" fill="url(#gradient1)" stroke="url(#gradient4)" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
      <path d="{res_path.stdout.split('Generated SVG path: ')[1].strip()}" fill="#ffffff" fill-opacity="0.8"/>
    </g>
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
    <linearGradient gradientTransform="matrix(0.0, 0.0307, -0.0305, 0.0, 24.2, 7.75)" gradientUnits="userSpaceOnUse" id="gradient4" spreadMethod="pad" x1="-819.2" x2="819.2">
      <stop offset="0.0" stop-color="#e0675a"/>
      <stop offset="0.6" stop-color="#a52c0e"/>
      <stop offset="1.0" stop-color="#c23512"/>
    </linearGradient>
  </defs>
</svg>'''

svg_file = test_dir / "171.svg"
svg_file.write_text(svg_content, encoding="utf-8")

cmd_import = [
    JAVA_EXE, "-jar", FFDEC_JAR,
    "-replace",
    "archive/clients/local-overrides/mole.61.com/resource/login/Login.swf",
    str(test_dir / "Login_vector.swf"),
    "171",
    str(svg_file)
]
res_imp = subprocess.run(cmd_import, capture_output=True, text=True)
print("Import return code:", res_imp.returncode)
print("Stdout:", res_imp.stdout)
print("Stderr:", res_imp.stderr)
