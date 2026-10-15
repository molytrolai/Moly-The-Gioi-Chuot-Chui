import sys
from pathlib import Path
import re

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

for fname in ['web/index.html', 'web/play.html']:
    text = Path(fname).read_text(encoding='utf-8')
    print('=== ' + fname + ' ===')
    lines = text.splitlines()
    for idx, l in enumerate(lines):
        if 'addEventListener("click"' in l and ('overlay' in l or 'modal' in l):
            start = max(0, idx - 5)
            end = min(len(lines), idx + 15)
            print(f"Around line {idx+1}:")
            for i in range(start, end):
                print(f"  {i+1}: {lines[i]}")
