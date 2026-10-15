import sys
from pathlib import Path
from PIL import Image

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

audit_dir = Path("work/audit_images")
if not audit_dir.exists():
    print("No audit_images dir")
    sys.exit(0)

for p in sorted(audit_dir.glob("**/*.*")):
    if p.is_file() and p.suffix.lower() in [".png", ".jpg", ".jpeg"]:
        rel = p.relative_to(audit_dir)
        try:
            with Image.open(p) as im:
                print(f"{rel} | size: {im.size} | {p.stat().st_size:,} bytes")
        except Exception as e:
            print(f"{rel} | error: {e}")
