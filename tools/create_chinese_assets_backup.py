#!/usr/bin/env python3
"""Bundle all original raw Chinese text dumps, unedited map templates, and loose comparison images
into a single clean ZIP archive (archive/bo_tai_nguyen_goc_tieng_trung_luu_tru.zip)
and clean up loose clutter to keep the project pristine.
"""

import os
import sys
import zipfile
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parents[1]
BACKUP_ZIP = ROOT / "archive" / "bo_tai_nguyen_goc_tieng_trung_luu_tru.zip"
BACKUP_ZIP.parent.mkdir(parents=True, exist_ok=True)

# List of folders/files to archive
SOURCES = [
    ROOT / "work" / "exported",
    ROOT / "scratch" / "cac_map_can_sua",
]

# Patterns of loose test comparison images in scratch
SCRATCH_IMG_PATTERNS = [
    "check_Map*.png",
    "crop_*.png",
    "extracted_*.png",
    "login_buttons_montage*.png",
    "shapes_montage.png",
    "so_sanh_*.png",
    "thumb_map_*.png",
    "preview_*.png",
    "map10_*.png",
]

def create_archive():
    print(f"Creating archive: {BACKUP_ZIP}...")
    with zipfile.ZipFile(BACKUP_ZIP, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        # 1. Add directories
        for src in SOURCES:
            if src.exists():
                for root, dirs, files in os.walk(src):
                    for f in files:
                        p = Path(root) / f
                        arcname = p.relative_to(ROOT)
                        zf.write(p, arcname=str(arcname))
                        print(f"  + Added: {arcname}")

        # 2. Add scratch comparison/test images
        scratch = ROOT / "scratch"
        if scratch.exists():
            for pat in SCRATCH_IMG_PATTERNS:
                for img in scratch.glob(pat):
                    arcname = img.relative_to(ROOT)
                    zf.write(img, arcname=str(arcname))
                    print(f"  + Added: {arcname}")

    print(f"\nSUCCESS: Archive created at {BACKUP_ZIP} ({BACKUP_ZIP.stat().st_size:,} bytes)")

def cleanup_clutter():
    print("\nCleaning up loose clutter from scratch...")
    scratch = ROOT / "scratch"
    if scratch.exists():
        for pat in SCRATCH_IMG_PATTERNS:
            for img in scratch.glob(pat):
                try:
                    img.unlink()
                    print(f"  - Removed loose clutter: {img.name}")
                except Exception as e:
                    print(f"  ! Error removing {img.name}: {e}")

if __name__ == "__main__":
    create_archive()
    cleanup_clutter()
