import sys
from pathlib import Path
import re

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

for fname in ['web/index.html', 'web/play.html', 'web/admin.html']:
    text = Path(fname).read_text(encoding='utf-8')
    print('=== ' + fname + ' ===')
    
    # 1. Search for all divs with class containing modal, popup, dialog, alert, or overlay
    divs = re.findall(r'<div[^>]+(?:class|id)=[\'"][^\'"]*(?:modal|popup|dialog|overlay|drawer|dropdown-menu)[^\'"]*[\'"][^>]*>', text, re.I)
    print(f"Total matching divs: {len(divs)}")
    for d in divs:
        print("  ", d)
