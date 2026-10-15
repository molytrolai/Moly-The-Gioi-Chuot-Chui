import os
import subprocess
from pathlib import Path
from PIL import Image

JAVA_EXE = r"C:\Program Files\Microsoft\jdk-21.0.12.101-hotspot\bin\java.exe"
PROJECT_ROOT = Path(__file__).resolve().parents[1]
FFDEC_JAR = str(PROJECT_ROOT / "tools" / "ffdec-26.3.0" / "ffdec-cli.jar")

SWF_DIR = PROJECT_ROOT / "archive" / "clients" / "local-overrides" / "mole.61.com"
MIRROR_DIR = PROJECT_ROOT / "archive" / "clients" / "offline-mirror" / "mole.61.com"
EXPORT_DIR = PROJECT_ROOT / "work" / "audit_images"
EXPORT_DIR.mkdir(parents=True, exist_ok=True)

swfs_to_audit = [
    ("LoginHome.swf", SWF_DIR / "resource" / "login" / "LoginHome.swf"),
    ("Login.swf", SWF_DIR / "resource" / "login" / "Login.swf"),
    ("topUI.swf", SWF_DIR / "resource" / "ui" / "topUI.swf"),
    ("main_resource.swf", MIRROR_DIR / "resource" / "ui" / "main_resource.swf"),
    ("NPCDialogPanel.swf", SWF_DIR / "module" / "external" / "NPCDialogPanel.swf"),
    ("randomMC.swf", MIRROR_DIR / "module" / "external" / "logo" / "randomMC.swf")
]

def export_and_inspect():
    for name, swf_path in swfs_to_audit:
        if not swf_path.is_file():
            print(f"[SKIP] {name} not found at {swf_path}")
            continue
        out_dir = EXPORT_DIR / name.replace(".swf", "")
        out_dir.mkdir(parents=True, exist_ok=True)
        img_dir = out_dir / "images"
        if not img_dir.is_dir() or len(list(img_dir.iterdir())) == 0:
            print(f"Exporting images from {name}...")
            cmd = [JAVA_EXE, "-jar", FFDEC_JAR, "-export", "image", str(out_dir), str(swf_path)]
            subprocess.run(cmd, capture_output=True, text=True)

        imgs = list(img_dir.glob("*.*")) if img_dir.is_dir() else []
        print(f"[{name}] Exported {len(imgs)} images:")
        for img in sorted(imgs, key=lambda x: x.stat().st_size, reverse=True)[:5]:
            try:
                with Image.open(img) as im:
                    print(f"    - {img.name}: {im.size}, {im.format}, {img.stat().st_size:,} bytes")
            except Exception as e:
                print(f"    - {img.name}: error opening ({e})")

if __name__ == "__main__":
    export_and_inspect()
