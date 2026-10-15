import sys
from pathlib import Path
import re

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

for fname in ['web/index.html', 'web/play.html']:
    text = Path(fname).read_text(encoding='utf-8')
    print('=== ' + fname + ' ===')
    # Find each modal-overlay div and extract its entire header and any back/close buttons
    matches = re.finditer(r'<div\s+id=[\'"]([^\'"]+)[\'"]\s+class=[\'"][^\'"]*modal-overlay[^\'"]*[\'"](.*?)</div>\s*<!--\s*==', text, re.DOTALL)
    for m in re.finditer(r'<div\s+id=[\'"]([^\'"]+)[\'"]\s+class=[\'"][^\'"]*modal-overlay[^\'"]*[\'"]', text):
        mid = m.group(1)
        start = m.start()
        # Find the modal-box inside it
        box_match = text[start:start+4000]
        # find header
        header = re.search(r'<div class="modal-header">.*?</div>', box_match, re.DOTALL)
        print(f"Modal: {mid}")
        if header:
            print("  Header:", header.group(0).replace('\n', ' '))
        else:
            print("  NO HEADER!")
            
        # check if it has back button
        has_back = "trở lại" in box_match.lower() or "quay lại" in box_match.lower()
        has_x = "modal-close" in box_match or "&times;" in box_match or "✕" in box_match
        print(f"  Has back button: {has_back}, Has X close: {has_x}")

