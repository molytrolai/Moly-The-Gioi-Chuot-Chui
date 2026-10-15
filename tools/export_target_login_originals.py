import os
import subprocess
from pathlib import Path

JAVA = r"C:\Program Files\Microsoft\jdk-21.0.12.101-hotspot\bin\java.exe"
FFDEC = r"tools/ffdec-26.3.0/ffdec-cli.jar"

out_dir = Path("work/target_login_originals")
out_dir.mkdir(parents=True, exist_ok=True)

# 1. randomMC.swf
subprocess.run([JAVA, "-jar", FFDEC, "-export", "image", str(out_dir / "randomMC"), "archive/clients/offline-mirror/mole.61.com/module/external/logo/randomMC.swf"], capture_output=True)

# 2. Login.swf images & shapes (especially 148, 171, 158, 161, 164, 167, 174, 176, 109, 168)
subprocess.run([JAVA, "-jar", FFDEC, "-export", "image", str(out_dir / "login_images"), "archive/clients/offline-mirror/mole.61.com/resource/login/Login.swf"], capture_output=True)

# 3. LoginHome.swf images & shapes
subprocess.run([JAVA, "-jar", FFDEC, "-export", "image", str(out_dir / "loginhome_images"), "archive/clients/offline-mirror/mole.61.com/resource/login/LoginHome.swf"], capture_output=True)

print("Export finished! Listing files:")
for sub in ["randomMC", "login_images", "loginhome_images"]:
    p = out_dir / sub
    if p.exists():
        print(f"[{sub}]:", os.listdir(p))
