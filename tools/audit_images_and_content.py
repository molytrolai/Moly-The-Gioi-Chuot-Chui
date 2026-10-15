import os
from pathlib import Path
import subprocess
import json

PROJECT_ROOT = Path(__file__).resolve().parents[1]

def audit_web_assets():
    print("=== 1. AUDIT WEB ASSETS (web/assets/) ===")
    web_assets = PROJECT_ROOT / "web" / "assets"
    if not web_assets.is_dir():
        print("web/assets not found")
        return
    for item in sorted(web_assets.iterdir()):
        if item.is_file():
            print(f"  - {item.name}: {item.stat().st_size:,} bytes")

def audit_override_images():
    print("\n=== 2. AUDIT LOCAL-OVERRIDES IMAGES ===")
    overrides = PROJECT_ROOT / "archive" / "clients" / "local-overrides"
    image_exts = {".png", ".jpg", ".jpeg", ".gif", ".bmp"}
    found_images = []
    for root, dirs, files in os.walk(overrides):
        for f in files:
            p = Path(root) / f
            if p.suffix.lower() in image_exts:
                rel = p.relative_to(overrides)
                found_images.append((str(rel), p.stat().st_size))
    print(f"Total override images found: {len(found_images)}")
    for rel, sz in found_images:
        print(f"  - {rel}: {sz:,} bytes")

def audit_core_swfs_status():
    print("\n=== 3. AUDIT COMPILED CORE SWFS STATUS ===")
    overrides = PROJECT_ROOT / "archive" / "clients" / "local-overrides" / "mole.61.com"
    core_swfs = [
        "Client.swf",
        "resource/login/Login.swf",
        "resource/login/LoginHome.swf",
        "resource/ui/ui.swf",
        "resource/ui/topUI.swf",
        "module/external/NPCDialogPanel.swf",
        "module/external/logo/randomMC.swf",
        "resource/ui/main_resource.swf",
        "resource/map/Map_10005.swf",
        "resource/map/Map_10006.swf",
        "resource/map/Map_10007.swf",
        "resource/map/Map_10061.swf",
    ]
    for rel in core_swfs:
        p = overrides / rel
        if p.is_file():
            print(f"  [EXISTS] {rel} ({p.stat().st_size:,} bytes)")
        else:
            print(f"  [MISSING IN OVERRIDES] {rel}")

def main():
    audit_web_assets()
    audit_override_images()
    audit_core_swfs_status()

if __name__ == "__main__":
    main()
