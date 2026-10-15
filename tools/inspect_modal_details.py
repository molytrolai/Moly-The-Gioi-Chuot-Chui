import sys
import os
from pathlib import Path
import re

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

for fname in ['web/index.html', 'web/play.html']:
    text = Path(fname).read_text(encoding='utf-8')
    print('=== ' + fname + ' ===')
    matches = re.finditer(r'<div\s+id=[\'"]([^\'"]+)[\'"]\s+class=[\'"][^\'"]*modal-overlay[^\'"]*[\'"]', text)
    for m in matches:
        modal_id = m.group(1)
        start = m.start()
        # Find next 2000 chars to see header and content
        snippet = text[start:start+2000]
        print(f'\n--- Modal ID: {modal_id} ---')
        header_m = re.search(r'<div class="modal-header">.*?</div>', snippet, re.DOTALL)
        if header_m:
            print("Header snippet:")
            print(header_m.group(0)[:300])
        else:
            print("NO MODAL-HEADER FOUND!")
            
        closes = re.findall(r'onclick=[\'"]([^\'"]*close[^\'"]*)[\'"]', snippet, re.I)
        print("Close onclicks found in modal:", closes)

