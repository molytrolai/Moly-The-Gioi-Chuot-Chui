import sys
from pathlib import Path
import re

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

for fname in ['web/index.html', 'web/play.html']:
    text = Path(fname).read_text(encoding='utf-8')
    print('=== ' + fname + ' ===')
    # search for modal closing logic in scripts
    matches = re.findall(r'[^\n]*modal[^\n]*\.classList\.[^\n]*', text, re.I)
    for m in matches[:10]:
        print('   ', m.strip())
    
    # check if click listener is attached to window, document, or overlays
    overlay_clicks = re.findall(r'[^\n]*(?:overlay|modal)[^\n]*addEventListener[^\n]*', text, re.I)
    print("Overlay click listeners:", overlay_clicks)
