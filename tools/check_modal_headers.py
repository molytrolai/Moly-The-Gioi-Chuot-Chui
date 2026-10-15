import sys
from pathlib import Path
import re

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

for fname in ['web/index.html', 'web/play.html']:
    text = Path(fname).read_text(encoding='utf-8')
    print('=== ' + fname + ' ===')
    pattern = r'<div\s+id=[\'"]([^\'"]+)[\'"]\s+class=[\'"][^\'"]*modal-overlay[^\'"]*[\'"].*?<div class="modal-header">(.*?)</div>'
    for m in re.finditer(pattern, text, re.DOTALL):
        print(f"Modal ID: {m.group(1)}")
        print(m.group(2).strip())
        print('-'*40)

    # Also check if backdrop click or escape key handlers exist
    has_backdrop = "modal-overlay" in text and "e.target === overlay" in text
    has_escape = "Escape" in text or "keyCode === 27" in text
    print(f"Has backdrop click: {has_backdrop}")
    print(f"Has Escape key handler: {has_escape}")
