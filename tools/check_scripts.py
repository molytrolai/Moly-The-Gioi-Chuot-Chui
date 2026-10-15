import sys
from pathlib import Path
import re

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

for fname in ['web/index.html', 'web/play.html']:
    text = Path(fname).read_text(encoding='utf-8')
    print('=== ' + fname + ' ===')
    # Check for any obvious syntax issues or where event listeners are defined
    scripts = re.findall(r'<script>(.*?)</script>', text, re.DOTALL)
    print(f"Total <script> tags: {len(scripts)}")
    for i, s in enumerate(scripts):
        print(f"Script {i}: length {len(s)}")
        # Check if contains closeAccountModal
        if "closeAccountModal" in s:
            print(f"  Contains closeAccountModal (len={len(s)})")
        if "addEventListener" in s:
            print(f"  Contains addEventListener")
