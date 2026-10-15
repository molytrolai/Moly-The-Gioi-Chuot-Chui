import os
import subprocess
from pathlib import Path

JAVA_EXE = r"C:\Program Files\Microsoft\jdk-21.0.12.101-hotspot\bin\java.exe"
PROJECT_ROOT = Path(__file__).resolve().parents[1]
FFDEC_JAR = str(PROJECT_ROOT / "tools" / "ffdec-26.3.0" / "ffdec-cli.jar")
OVERRIDES_ROOT = PROJECT_ROOT / "archive" / "clients" / "local-overrides" / "mole.61.com"
VERIF_DIR = PROJECT_ROOT / "work" / "verification"

VERIF_DIR.mkdir(parents=True, exist_ok=True)

def verify_swf(swf_path, out_subfolder, select_ids, export_type="shape"):
    out_dir = VERIF_DIR / out_subfolder
    out_dir.mkdir(parents=True, exist_ok=True)
    cmd = [
        JAVA_EXE, "-jar", FFDEC_JAR,
        "-selectid", ",".join(str(i) for i in select_ids),
        "-format", f"{export_type}:png",
        "-export", export_type,
        str(out_dir),
        str(swf_path)
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    print(f"Export {swf_path.name} ({export_type}): {res.returncode}")

def main():
    print("=== EXPORTING VERIFICATION PREVIEWS ===")
    
    # 1. Login.swf: shapes 150, 157, 182, 187, 171, image 148
    verify_swf(
        OVERRIDES_ROOT / "resource" / "login" / "Login.swf",
        "login_shapes",
        [150, 157, 182, 187, 171],
        "shape"
    )
    verify_swf(
        OVERRIDES_ROOT / "resource" / "login" / "Login.swf",
        "login_images",
        [148],
        "image"
    )
    
    # 2. LoginHome.swf: shape 128, images 226, 171, 236
    verify_swf(
        OVERRIDES_ROOT / "resource" / "login" / "LoginHome.swf",
        "lh_shapes",
        [128],
        "shape"
    )
    verify_swf(
        OVERRIDES_ROOT / "resource" / "login" / "LoginHome.swf",
        "lh_images",
        [226, 171, 236],
        "image"
    )
    
    # 3. Logo.swf: image 5
    verify_swf(
        OVERRIDES_ROOT / "module" / "external" / "logo" / "Logo.swf",
        "logo_images",
        [5],
        "image"
    )
    
    # 4. ui.swf: images 3279, 6834, 6844, 6849
    verify_swf(
        OVERRIDES_ROOT / "resource" / "ui" / "ui.swf",
        "ui_images",
        [3279, 6834, 6844, 6849, 6864],
        "image"
    )
    
    print("=== EXPORT COMPLETE! ===")

if __name__ == "__main__":
    main()
