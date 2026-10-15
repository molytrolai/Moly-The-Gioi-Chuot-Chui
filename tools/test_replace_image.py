import subprocess
from pathlib import Path
from PIL import Image

JAVA_EXE = r"C:\Program Files\Microsoft\jdk-21.0.12.101-hotspot\bin\java.exe"
FFDEC_JAR = r"tools\ffdec-26.3.0\ffdec-cli.jar"

test_dir = Path("work/test_replace")
test_dir.mkdir(parents=True, exist_ok=True)

# Test 1: Replace Image 226 in LoginHome.swf
# Create a dummy or custom 226.png
img226 = Image.new("RGBA", (122, 156), (0, 255, 0, 255))
img226_path = test_dir / "226.png"
img226.save(img226_path)

in_swf = "archive/clients/local-overrides/mole.61.com/resource/login/LoginHome.swf"
out_swf = str(test_dir / "LoginHome_test.swf")

cmd = [
    JAVA_EXE, "-jar", FFDEC_JAR,
    "-replace",
    in_swf,
    out_swf,
    "226",
    str(img226_path)
]
print("Running command:", " ".join(cmd))
res = subprocess.run(cmd, capture_output=True, text=True)
print("Return code:", res.returncode)
print("Stdout:", res.stdout)
print("Stderr:", res.stderr)
if Path(out_swf).exists():
    print("Success! Output size:", Path(out_swf).stat().st_size)
