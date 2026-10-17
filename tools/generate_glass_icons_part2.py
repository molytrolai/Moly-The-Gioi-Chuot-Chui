"""
Generate Additional Frosted Glassmorphism SVG Icons for Moly Vietnam
"""

import os

ICONS_DIR = "web/assets/icons"
os.makedirs(ICONS_DIR, exist_ok=True)

icons = {}

# 13. Glass News (Tin Tức)
icons["glass-news.svg"] = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" width="32" height="32">
  <defs>
    <radialGradient id="gn_bg" cx="50%" cy="30%" r="70%">
      <stop offset="0%" stop-color="#38bdf8" stop-opacity="0.9"/>
      <stop offset="60%" stop-color="#0284c7" stop-opacity="0.85"/>
      <stop offset="100%" stop-color="#0c4a6e" stop-opacity="0.95"/>
    </radialGradient>
    <linearGradient id="gn_rim" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0.9"/>
      <stop offset="100%" stop-color="#7dd3fc" stop-opacity="0.4"/>
    </linearGradient>
  </defs>
  <rect x="2" y="2" width="28" height="28" rx="9" fill="url(#gn_bg)" stroke="url(#gn_rim)" stroke-width="1.2"/>
  <path d="M 3 11 C 3 6 6 3 11 3 L 21 3 C 26 3 29 6 29 11 C 29 13 25 15 16 15 C 7 15 3 13 3 11 Z" fill="#ffffff" opacity="0.35"/>
  <!-- Newspaper / Scroll -->
  <rect x="8" y="9" width="16" height="14" rx="2" fill="#ffffff" stroke="#0284c7" stroke-width="0.8"/>
  <rect x="10" y="11" width="5" height="4" fill="#38bdf8" rx="0.5"/>
  <line x1="17" y1="12" x2="22" y2="12" stroke="#0284c7" stroke-width="1.2" stroke-linecap="round"/>
  <line x1="17" y1="14" x2="21" y2="14" stroke="#0284c7" stroke-width="1" stroke-linecap="round"/>
  <line x1="10" y1="17" x2="22" y2="17" stroke="#64748b" stroke-width="1" stroke-linecap="round"/>
  <line x1="10" y1="19.5" x2="19" y2="19.5" stroke="#64748b" stroke-width="1" stroke-linecap="round"/>
</svg>
"""

# 14. Glass Tools (Tiện Ích)
icons["glass-tools.svg"] = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" width="32" height="32">
  <defs>
    <radialGradient id="gt_bg" cx="50%" cy="30%" r="70%">
      <stop offset="0%" stop-color="#fde047" stop-opacity="0.9"/>
      <stop offset="60%" stop-color="#eab308" stop-opacity="0.85"/>
      <stop offset="100%" stop-color="#854d0e" stop-opacity="0.95"/>
    </radialGradient>
    <linearGradient id="gt_rim" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0.9"/>
      <stop offset="100%" stop-color="#fef08a" stop-opacity="0.4"/>
    </linearGradient>
  </defs>
  <rect x="2" y="2" width="28" height="28" rx="9" fill="url(#gt_bg)" stroke="url(#gt_rim)" stroke-width="1.2"/>
  <path d="M 3 11 C 3 6 6 3 11 3 L 21 3 C 26 3 29 6 29 11 C 29 13 25 15 16 15 C 7 15 3 13 3 11 Z" fill="#ffffff" opacity="0.35"/>
  <!-- Lightning Bolt -->
  <polygon points="17,7 10,17 15,17 13,25 22,14 17,14" fill="#ffffff" stroke="#713f12" stroke-width="1"/>
</svg>
"""

# 15. Glass Download (Tải Về)
icons["glass-download.svg"] = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" width="32" height="32">
  <defs>
    <radialGradient id="gdl_bg" cx="50%" cy="30%" r="70%">
      <stop offset="0%" stop-color="#34d399" stop-opacity="0.9"/>
      <stop offset="60%" stop-color="#059669" stop-opacity="0.85"/>
      <stop offset="100%" stop-color="#064e3b" stop-opacity="0.95"/>
    </radialGradient>
    <linearGradient id="gdl_rim" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0.9"/>
      <stop offset="100%" stop-color="#a7f3d0" stop-opacity="0.4"/>
    </linearGradient>
  </defs>
  <rect x="2" y="2" width="28" height="28" rx="9" fill="url(#gdl_bg)" stroke="url(#gdl_rim)" stroke-width="1.2"/>
  <path d="M 3 11 C 3 6 6 3 11 3 L 21 3 C 26 3 29 6 29 11 C 29 13 25 15 16 15 C 7 15 3 13 3 11 Z" fill="#ffffff" opacity="0.35"/>
  <!-- Down Arrow -->
  <path d="M 16 8 L 16 18 M 11 14 L 16 19 L 21 14" fill="none" stroke="#ffffff" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>
  <!-- Base Tray -->
  <path d="M 9 21 L 9 23 L 23 23 L 23 21" fill="none" stroke="#ffffff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
</svg>
"""

# 16. Glass Stats (Tổng Quan Admin)
icons["glass-stats.svg"] = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" width="32" height="32">
  <defs>
    <radialGradient id="gst_bg" cx="50%" cy="30%" r="70%">
      <stop offset="0%" stop-color="#38bdf8" stop-opacity="0.9"/>
      <stop offset="60%" stop-color="#0284c7" stop-opacity="0.85"/>
      <stop offset="100%" stop-color="#075985" stop-opacity="0.95"/>
    </radialGradient>
    <linearGradient id="gst_rim" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0.9"/>
      <stop offset="100%" stop-color="#7dd3fc" stop-opacity="0.4"/>
    </linearGradient>
  </defs>
  <rect x="2" y="2" width="28" height="28" rx="9" fill="url(#gst_bg)" stroke="url(#gst_rim)" stroke-width="1.2"/>
  <path d="M 3 11 C 3 6 6 3 11 3 L 21 3 C 26 3 29 6 29 11 C 29 13 25 15 16 15 C 7 15 3 13 3 11 Z" fill="#ffffff" opacity="0.35"/>
  <!-- Bar chart -->
  <rect x="8" y="18" width="3.5" height="5" rx="1" fill="#bae6fd"/>
  <rect x="14" y="13" width="3.5" height="10" rx="1" fill="#fde047"/>
  <rect x="20" y="9" width="3.5" height="14" rx="1" fill="#ffffff"/>
</svg>
"""

# 17. Glass Shield (Hệ Thống Admin / SMC)
icons["glass-shield.svg"] = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" width="32" height="32">
  <defs>
    <radialGradient id="gsh_bg" cx="50%" cy="30%" r="70%">
      <stop offset="0%" stop-color="#a855f7" stop-opacity="0.9"/>
      <stop offset="60%" stop-color="#7e22ce" stop-opacity="0.85"/>
      <stop offset="100%" stop-color="#3b0764" stop-opacity="0.95"/>
    </radialGradient>
    <linearGradient id="gsh_rim" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0.9"/>
      <stop offset="100%" stop-color="#d8b4fe" stop-opacity="0.4"/>
    </linearGradient>
  </defs>
  <rect x="2" y="2" width="28" height="28" rx="9" fill="url(#gsh_bg)" stroke="url(#gsh_rim)" stroke-width="1.2"/>
  <path d="M 3 11 C 3 6 6 3 11 3 L 21 3 C 26 3 29 6 29 11 C 29 13 25 15 16 15 C 7 15 3 13 3 11 Z" fill="#ffffff" opacity="0.35"/>
  <!-- Shield Shape -->
  <path d="M 16 8 L 22 10.5 C 22 17 19 21.5 16 23.5 C 13 21.5 10 17 10 10.5 Z" fill="#ffffff" stroke="#581c87" stroke-width="0.8"/>
  <polygon points="16,11 17.5,14.5 21,15 18,17.5 19,21 16,19 13,21 14,17.5 11,15 14.5,14.5" fill="#fde047"/>
</svg>
"""

# Write all SVG files
for filename, content in icons.items():
    path = os.path.join(ICONS_DIR, filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip())
    print(f"Generated {filename}")

print(f"Successfully generated {len(icons)} additional glassmorphism icons!")
