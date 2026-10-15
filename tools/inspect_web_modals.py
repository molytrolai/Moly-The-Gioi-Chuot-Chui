import re
from pathlib import Path

def inspect_file(filepath):
    p = Path(filepath)
    if not p.exists():
        print(f"File not found: {filepath}")
        return
    text = p.read_text(encoding="utf-8")
    print(f"\n=== INSPECTING {filepath} ({len(text)} bytes, {len(text.splitlines())} lines) ===")
    
    # Find all elements that look like popups, modals, overlays, panels, or lightboxes
    patterns = [
        r'(<div[^>]+id=["\'][^"\']*(?:modal|popup|overlay|dialog|box|window|panel|form|login|register)[^"\']*["\'][^>]*>)',
        r'(<dialog[^>]*>)',
        r'(\.modal[^{]*\{[^}]*\})',
        r'(\.popup[^{]*\{[^}]*\})',
        r'(\.overlay[^{]*\{[^}]*\})',
    ]
    for pat in patterns:
        m = re.findall(pat, text, re.I)
        if m:
            print(f"Pattern {pat[:30]}... found {len(m)} matches:")
            for item in m[:10]:
                print(f"   {item.strip()[:100]}")

    # Let's search for functions that open/close windows or modals
    funcs = re.findall(r'function\s+([a-zA-Z0-9_]*(?:Modal|Popup|Dialog|Open|Close|Show|Hide)[a-zA-Z0-9_]*)\s*\(', text, re.I)
    print("Related JS Functions:", list(set(funcs)))
    
    # Also find all IDs in text
    all_ids = re.findall(r'id=["\']([^"\']+)["\']', text)
    interesting_ids = [i for i in all_ids if any(k in i.lower() for k in ['modal', 'pop', 'dialog', 'overlay', 'panel', 'box', 'window', 'recharge', 'gift', 'login', 'reg'])]
    print("Interesting IDs:", interesting_ids)

inspect_file("web/index.html")
inspect_file("web/play.html")
inspect_file("web/admin.html")
