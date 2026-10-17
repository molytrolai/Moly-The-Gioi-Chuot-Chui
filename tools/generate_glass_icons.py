"""
Generate High-Fidelity Frosted Glassmorphism SVG Icons for Moly Vietnam
Each icon features:
- Translucent frosted glass squircle container with specular reflection arc
- Multi-stop metallic & luminous gradients
- Outer neon aura drop shadow
- Faceted 3D vector artwork with crystal reflections
"""

import os

ICONS_DIR = "web/assets/icons"
os.makedirs(ICONS_DIR, exist_ok=True)

icons = {}

# 1. Glass Dark Lamu (Đậu Siêu Cấp Hắc Ám)
icons["glass-dark.svg"] = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="64" height="64">
  <defs>
    <radialGradient id="darkBgGlow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#a855f7" stop-opacity="0.35"/>
      <stop offset="100%" stop-color="#3b0764" stop-opacity="0.95"/>
    </radialGradient>
    <linearGradient id="darkRim" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#f3e8ff" stop-opacity="0.8"/>
      <stop offset="50%" stop-color="#c084fc" stop-opacity="0.4"/>
      <stop offset="100%" stop-color="#581c87" stop-opacity="0.8"/>
    </linearGradient>
    <linearGradient id="darkWing" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#e879f9"/>
      <stop offset="40%" stop-color="#a21caf"/>
      <stop offset="100%" stop-color="#3b0764"/>
    </linearGradient>
    <radialGradient id="darkOrb" cx="35%" cy="30%" r="65%">
      <stop offset="0%" stop-color="#f5d0fe"/>
      <stop offset="25%" stop-color="#c084fc"/>
      <stop offset="70%" stop-color="#6b21a8"/>
      <stop offset="100%" stop-color="#2e1065"/>
    </radialGradient>
    <linearGradient id="specularHighlight" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0.65"/>
      <stop offset="40%" stop-color="#ffffff" stop-opacity="0.15"/>
      <stop offset="100%" stop-color="#ffffff" stop-opacity="0"/>
    </linearGradient>
    <filter id="purpleGlow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="3" result="blur"/>
      <feComposite in="SourceGraphic" in2="blur" operator="over"/>
    </filter>
  </defs>

  <!-- Ambient Shadow -->
  <rect x="4" y="6" width="56" height="54" rx="18" fill="#1e1b4b" opacity="0.4" filter="url(#purpleGlow)"/>

  <!-- Glass Container -->
  <rect x="4" y="4" width="56" height="56" rx="18" fill="url(#darkBgGlow)" stroke="url(#darkRim)" stroke-width="1.8"/>

  <!-- Specular Curve -->
  <path d="M 6 22 C 6 12 12 6 22 6 L 42 6 C 52 6 58 12 58 22 C 58 26 50 30 32 30 C 14 30 6 26 6 22 Z" fill="url(#specularHighlight)"/>

  <!-- Left Demon Wing -->
  <path d="M 30 35 C 22 28 14 26 8 32 C 10 37 15 39 18 38 C 13 42 12 46 16 48 C 22 47 26 43 30 39 Z" fill="url(#darkWing)" stroke="#f0abfc" stroke-width="0.8"/>

  <!-- Right Demon Wing -->
  <path d="M 34 35 C 42 28 50 26 56 32 C 54 37 49 39 46 38 C 51 42 52 46 48 48 C 42 47 38 43 34 39 Z" fill="url(#darkWing)" stroke="#f0abfc" stroke-width="0.8"/>

  <!-- Central Dark Matter Orb -->
  <circle cx="32" cy="38" r="11" fill="url(#darkOrb)" stroke="#e879f9" stroke-width="1.2"/>

  <!-- Demon Horns -->
  <path d="M 27 29 C 25 22 20 20 18 21 C 21 26 24 28 27 30 Z" fill="#e879f9"/>
  <path d="M 37 29 C 39 22 44 20 46 21 C 43 26 40 28 37 30 Z" fill="#e879f9"/>

  <!-- Core Shine -->
  <ellipse cx="28" cy="34" rx="3.5" ry="2" fill="#ffffff" opacity="0.85"/>
  <polygon points="46,16 47,19 50,20 47,21 46,24 45,21 42,20 45,19" fill="#f5d0fe"/>
</svg>
"""

# 2. Glass Cosmic Lamu (Đậu Siêu Cấp Vũ Trụ)
icons["glass-cosmic.svg"] = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="64" height="64">
  <defs>
    <radialGradient id="cosmicBgGlow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#38bdf8" stop-opacity="0.35"/>
      <stop offset="100%" stop-color="#082f49" stop-opacity="0.95"/>
    </radialGradient>
    <linearGradient id="cosmicRim" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#e0f2fe" stop-opacity="0.85"/>
      <stop offset="50%" stop-color="#38bdf8" stop-opacity="0.45"/>
      <stop offset="100%" stop-color="#0284c7" stop-opacity="0.8"/>
    </linearGradient>
    <radialGradient id="cosmicPlanet" cx="30%" cy="28%" r="70%">
      <stop offset="0%" stop-color="#ffffff"/>
      <stop offset="20%" stop-color="#7dd3fc"/>
      <stop offset="60%" stop-color="#0284c7"/>
      <stop offset="100%" stop-color="#082f49"/>
    </radialGradient>
    <linearGradient id="cosmicRing" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#fef08a" stop-opacity="0.9"/>
      <stop offset="50%" stop-color="#38bdf8" stop-opacity="0.8"/>
      <stop offset="100%" stop-color="#c084fc" stop-opacity="0.9"/>
    </linearGradient>
    <linearGradient id="cosmicSpec" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0.7"/>
      <stop offset="45%" stop-color="#ffffff" stop-opacity="0.15"/>
      <stop offset="100%" stop-color="#ffffff" stop-opacity="0"/>
    </linearGradient>
  </defs>

  <!-- Ambient Glow -->
  <rect x="4" y="6" width="56" height="54" rx="18" fill="#0369a1" opacity="0.3"/>

  <!-- Glass Container -->
  <rect x="4" y="4" width="56" height="56" rx="18" fill="url(#cosmicBgGlow)" stroke="url(#cosmicRim)" stroke-width="1.8"/>

  <!-- Specular Arc -->
  <path d="M 6 22 C 6 12 12 6 22 6 L 42 6 C 52 6 58 12 58 22 C 58 26 50 30 32 30 C 14 30 6 26 6 22 Z" fill="url(#cosmicSpec)"/>

  <!-- Back of Planetary Ring -->
  <path d="M 12 37 C 14 31 38 23 52 27 C 48 31 24 39 12 37 Z" fill="url(#cosmicRing)" opacity="0.5"/>

  <!-- Planet Sphere -->
  <circle cx="32" cy="36" r="13" fill="url(#cosmicPlanet)" stroke="#38bdf8" stroke-width="1"/>

  <!-- Planet Surface Swirl / Cloud Band -->
  <path d="M 21 34 C 26 31 38 33 44 38 C 42 41 33 39 21 34 Z" fill="#bae6fd" opacity="0.35"/>

  <!-- Front of Planetary Ring -->
  <path d="M 10 39 C 14 47 48 45 54 33 C 51 32 46 36 34 38 C 22 40 13 38 10 39 Z" fill="url(#cosmicRing)"/>

  <!-- Shiny Sparkles -->
  <polygon points="48,15 49,18 52,19 49,20 48,23 47,20 44,19 47,18" fill="#ffffff"/>
  <circle cx="16" cy="22" r="1.5" fill="#fde047"/>
  <circle cx="48" cy="48" r="1.2" fill="#7dd3fc"/>
</svg>
"""

# 3. Glass Mythic Lamu (Đậu Siêu Cấp Thần Thoại)
icons["glass-mythic.svg"] = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="64" height="64">
  <defs>
    <radialGradient id="mythicBgGlow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#fbbf24" stop-opacity="0.4"/>
      <stop offset="100%" stop-color="#451a03" stop-opacity="0.95"/>
    </radialGradient>
    <linearGradient id="mythicRim" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#fef3c7" stop-opacity="0.9"/>
      <stop offset="50%" stop-color="#fbbf24" stop-opacity="0.5"/>
      <stop offset="100%" stop-color="#b45309" stop-opacity="0.8"/>
    </linearGradient>
    <linearGradient id="goldWing" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#ffffff"/>
      <stop offset="30%" stop-color="#fde047"/>
      <stop offset="70%" stop-color="#f59e0b"/>
      <stop offset="100%" stop-color="#b45309"/>
    </linearGradient>
    <radialGradient id="sunburstCore" cx="40%" cy="40%" r="60%">
      <stop offset="0%" stop-color="#ffffff"/>
      <stop offset="35%" stop-color="#fde047"/>
      <stop offset="75%" stop-color="#f59e0b"/>
      <stop offset="100%" stop-color="#d97706"/>
    </radialGradient>
    <linearGradient id="mythicSpec" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0.75"/>
      <stop offset="40%" stop-color="#ffffff" stop-opacity="0.2"/>
      <stop offset="100%" stop-color="#ffffff" stop-opacity="0"/>
    </linearGradient>
  </defs>

  <!-- Ambient Glow -->
  <rect x="4" y="6" width="56" height="54" rx="18" fill="#78350f" opacity="0.3"/>

  <!-- Glass Container -->
  <rect x="4" y="4" width="56" height="56" rx="18" fill="url(#mythicBgGlow)" stroke="url(#mythicRim)" stroke-width="1.8"/>

  <!-- Specular Arc -->
  <path d="M 6 22 C 6 12 12 6 22 6 L 42 6 C 52 6 58 12 58 22 C 58 26 50 30 32 30 C 14 30 6 26 6 22 Z" fill="url(#mythicSpec)"/>

  <!-- Angelic Wings Left -->
  <path d="M 30 36 C 22 26 12 24 8 28 C 9 34 14 37 17 38 C 11 41 11 46 15 48 C 22 47 26 43 30 38 Z" fill="url(#goldWing)" stroke="#fef08a" stroke-width="0.8"/>

  <!-- Angelic Wings Right -->
  <path d="M 34 36 C 42 26 52 24 56 28 C 55 34 50 37 47 38 C 53 41 53 46 49 48 C 42 47 38 43 34 38 Z" fill="url(#goldWing)" stroke="#fef08a" stroke-width="0.8"/>

  <!-- Celestial Halo -->
  <ellipse cx="32" cy="24" rx="12" ry="3.5" fill="none" stroke="#fde047" stroke-width="1.8" opacity="0.85"/>

  <!-- Radiant 8-Point Holy Star -->
  <polygon points="32,23 34.5,31.5 43,34 34.5,36.5 32,45 29.5,36.5 21,34 29.5,31.5" fill="url(#sunburstCore)" stroke="#fff" stroke-width="0.8"/>

  <!-- Prismatic Gems -->
  <circle cx="32" cy="34" r="3.2" fill="#ffffff"/>
  <polygon points="17,16 18,18 20,19 18,20 17,22 16,20 14,19 16,18" fill="#ffffff"/>
  <polygon points="47,44 48,46 50,47 48,48 47,50 46,48 44,47 46,46" fill="#fef08a"/>
</svg>
"""

# 4. Glass VIP Crown (Thẻ Tháng VIP 1 -> 19)
icons["glass-vip.svg"] = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="64" height="64">
  <defs>
    <radialGradient id="vipBgGlow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#34d399" stop-opacity="0.35"/>
      <stop offset="100%" stop-color="#022c22" stop-opacity="0.95"/>
    </radialGradient>
    <linearGradient id="vipRim" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#a7f3d0" stop-opacity="0.85"/>
      <stop offset="50%" stop-color="#34d399" stop-opacity="0.45"/>
      <stop offset="100%" stop-color="#059669" stop-opacity="0.8"/>
    </linearGradient>
    <linearGradient id="goldCrown" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#fef08a"/>
      <stop offset="35%" stop-color="#facc15"/>
      <stop offset="70%" stop-color="#eab308"/>
      <stop offset="100%" stop-color="#ca8a04"/>
    </linearGradient>
    <radialGradient id="rubyGem" cx="35%" cy="30%" r="65%">
      <stop offset="0%" stop-color="#fca5a5"/>
      <stop offset="35%" stop-color="#ef4444"/>
      <stop offset="100%" stop-color="#7f1d1d"/>
    </radialGradient>
    <linearGradient id="vipSpec" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0.75"/>
      <stop offset="40%" stop-color="#ffffff" stop-opacity="0.2"/>
      <stop offset="100%" stop-color="#ffffff" stop-opacity="0"/>
    </linearGradient>
  </defs>

  <!-- Ambient Glow -->
  <rect x="4" y="6" width="56" height="54" rx="18" fill="#064e3b" opacity="0.35"/>

  <!-- Glass Container -->
  <rect x="4" y="4" width="56" height="56" rx="18" fill="url(#vipBgGlow)" stroke="url(#vipRim)" stroke-width="1.8"/>

  <!-- Specular Arc -->
  <path d="M 6 22 C 6 12 12 6 22 6 L 42 6 C 52 6 58 12 58 22 C 58 26 50 30 32 30 C 14 30 6 26 6 22 Z" fill="url(#vipSpec)"/>

  <!-- Royal Imperial Crown (5 Peaks) -->
  <path d="M 16 44 L 14 28 L 22 34 L 32 23 L 42 34 L 50 28 L 48 44 Z" fill="url(#goldCrown)" stroke="#fef08a" stroke-width="1"/>

  <!-- Crown Base Velvet Cushion Band -->
  <rect x="15" y="42" width="34" height="6" rx="3" fill="#047857" stroke="#fbbf24" stroke-width="1"/>

  <!-- Crown Peak Jewels -->
  <circle cx="14" cy="27" r="2.2" fill="#38bdf8"/>
  <circle cx="22" cy="33" r="2" fill="#a7f3d0"/>
  <circle cx="32" cy="22" r="3" fill="#ffffff" stroke="#facc15" stroke-width="0.8"/>
  <circle cx="42" cy="33" r="2" fill="#a7f3d0"/>
  <circle cx="50" cy="27" r="2.2" fill="#38bdf8"/>

  <!-- Central Faceted Ruby Heart -->
  <polygon points="32,32 36,36 32,41 28,36" fill="url(#rubyGem)" stroke="#fef08a" stroke-width="0.6"/>

  <!-- Crown Sparkles -->
  <polygon points="46,16 47,19 50,20 47,21 46,24 45,21 42,20 45,19" fill="#fef08a"/>
</svg>
"""

# 5. Glass Game Controller (Chơi Ngay / Vào Game)
icons["glass-game.svg"] = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" width="32" height="32">
  <defs>
    <radialGradient id="gg_bg" cx="50%" cy="30%" r="70%">
      <stop offset="0%" stop-color="#38bdf8" stop-opacity="0.9"/>
      <stop offset="50%" stop-color="#0284c7" stop-opacity="0.8"/>
      <stop offset="100%" stop-color="#0369a1" stop-opacity="0.95"/>
    </radialGradient>
    <linearGradient id="gg_rim" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0.9"/>
      <stop offset="100%" stop-color="#38bdf8" stop-opacity="0.4"/>
    </linearGradient>
  </defs>
  <rect x="2" y="2" width="28" height="28" rx="9" fill="url(#gg_bg)" stroke="url(#gg_rim)" stroke-width="1.2"/>
  <path d="M 3 11 C 3 6 6 3 11 3 L 21 3 C 26 3 29 6 29 11 C 29 13 25 15 16 15 C 7 15 3 13 3 11 Z" fill="#ffffff" opacity="0.35"/>
  <!-- Gamepad Shape -->
  <path d="M 8 13 C 8 10 12 9 16 9 C 20 9 24 10 24 13 C 24 18 22 23 20 23 C 18.5 23 18 20 16 20 C 14 20 13.5 23 12 23 C 10 23 8 18 8 13 Z" fill="#0f172a" stroke="#7dd3fc" stroke-width="0.8"/>
  <!-- D-Pad -->
  <rect x="10.5" y="13" width="3" height="1" fill="#fde047" rx="0.5"/>
  <rect x="11.5" y="12" width="1" height="3" fill="#fde047" rx="0.5"/>
  <!-- AB Buttons -->
  <circle cx="19.5" cy="12.5" r="0.9" fill="#f43f5e"/>
  <circle cx="21.5" cy="14" r="0.9" fill="#10b981"/>
</svg>
"""

# 6. Glass Home (Trang Chủ)
icons["glass-home.svg"] = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" width="32" height="32">
  <defs>
    <radialGradient id="gh_bg" cx="50%" cy="30%" r="70%">
      <stop offset="0%" stop-color="#fbbf24" stop-opacity="0.9"/>
      <stop offset="60%" stop-color="#d97706" stop-opacity="0.85"/>
      <stop offset="100%" stop-color="#78350f" stop-opacity="0.95"/>
    </radialGradient>
    <linearGradient id="gh_rim" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0.9"/>
      <stop offset="100%" stop-color="#fbbf24" stop-opacity="0.4"/>
    </linearGradient>
  </defs>
  <rect x="2" y="2" width="28" height="28" rx="9" fill="url(#gh_bg)" stroke="url(#gh_rim)" stroke-width="1.2"/>
  <path d="M 3 11 C 3 6 6 3 11 3 L 21 3 C 26 3 29 6 29 11 C 29 13 25 15 16 15 C 7 15 3 13 3 11 Z" fill="#ffffff" opacity="0.35"/>
  <!-- Fantasy Castle / Home -->
  <path d="M 16 8 L 8 15 L 10 15 L 10 23 L 22 23 L 22 15 L 24 15 Z" fill="#fff" stroke="#451a03" stroke-width="1"/>
  <!-- Door Arch -->
  <path d="M 14 23 L 14 18 C 14 16.8 15 16 16 16 C 17 16 18 16.8 18 18 L 18 23 Z" fill="#d97706"/>
</svg>
"""

# 7. Glass Diamond (Nạp Đậu / Cửa Hàng)
icons["glass-diamond.svg"] = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" width="32" height="32">
  <defs>
    <radialGradient id="gd_bg" cx="50%" cy="30%" r="70%">
      <stop offset="0%" stop-color="#22d3ee" stop-opacity="0.9"/>
      <stop offset="60%" stop-color="#0891b2" stop-opacity="0.85"/>
      <stop offset="100%" stop-color="#164e63" stop-opacity="0.95"/>
    </radialGradient>
    <linearGradient id="gd_rim" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0.9"/>
      <stop offset="100%" stop-color="#67e8f9" stop-opacity="0.4"/>
    </linearGradient>
  </defs>
  <rect x="2" y="2" width="28" height="28" rx="9" fill="url(#gd_bg)" stroke="url(#gd_rim)" stroke-width="1.2"/>
  <path d="M 3 11 C 3 6 6 3 11 3 L 21 3 C 26 3 29 6 29 11 C 29 13 25 15 16 15 C 7 15 3 13 3 11 Z" fill="#ffffff" opacity="0.35"/>
  <!-- Diamond Shape -->
  <polygon points="11,12 21,12 25,17 16,24 7,17" fill="#cffafe" stroke="#ffffff" stroke-width="0.8"/>
  <polygon points="11,12 21,12 18,17 14,17" fill="#67e8f9"/>
  <polygon points="14,17 18,17 16,24" fill="#06b6d4"/>
</svg>
"""

# 8. Glass Gift Box (Giftcode)
icons["glass-gift.svg"] = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" width="32" height="32">
  <defs>
    <radialGradient id="gf_bg" cx="50%" cy="30%" r="70%">
      <stop offset="0%" stop-color="#f43f5e" stop-opacity="0.9"/>
      <stop offset="60%" stop-color="#be123c" stop-opacity="0.85"/>
      <stop offset="100%" stop-color="#881337" stop-opacity="0.95"/>
    </radialGradient>
    <linearGradient id="gf_rim" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0.9"/>
      <stop offset="100%" stop-color="#fda4af" stop-opacity="0.4"/>
    </linearGradient>
  </defs>
  <rect x="2" y="2" width="28" height="28" rx="9" fill="url(#gf_bg)" stroke="url(#gf_rim)" stroke-width="1.2"/>
  <path d="M 3 11 C 3 6 6 3 11 3 L 21 3 C 26 3 29 6 29 11 C 29 13 25 15 16 15 C 7 15 3 13 3 11 Z" fill="#ffffff" opacity="0.35"/>
  <!-- Gift Box Base -->
  <rect x="9" y="16" width="14" height="8" rx="1.5" fill="#fecdd3" stroke="#fff" stroke-width="0.6"/>
  <!-- Gift Box Lid -->
  <rect x="8" y="13" width="16" height="4" rx="1" fill="#ffe4e6" stroke="#fff" stroke-width="0.6"/>
  <!-- Gold Ribbon -->
  <rect x="14.5" y="13" width="3" height="11" fill="#fde047"/>
  <!-- Ribbon Bow -->
  <path d="M 16 13 C 14 10 11 11 13 13 C 11 11 14 9 16 13 Z" fill="#fde047"/>
  <path d="M 16 13 C 18 10 21 11 19 13 C 21 11 18 9 16 13 Z" fill="#fde047"/>
</svg>
"""

# 9. Glass User / Account (Tài Khoản / Cư Dân)
icons["glass-user.svg"] = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" width="32" height="32">
  <defs>
    <radialGradient id="gu_bg" cx="50%" cy="30%" r="70%">
      <stop offset="0%" stop-color="#818cf8" stop-opacity="0.9"/>
      <stop offset="60%" stop-color="#4f46e5" stop-opacity="0.85"/>
      <stop offset="100%" stop-color="#312e81" stop-opacity="0.95"/>
    </radialGradient>
    <linearGradient id="gu_rim" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0.9"/>
      <stop offset="100%" stop-color="#c7d2fe" stop-opacity="0.4"/>
    </linearGradient>
  </defs>
  <rect x="2" y="2" width="28" height="28" rx="9" fill="url(#gu_bg)" stroke="url(#gu_rim)" stroke-width="1.2"/>
  <path d="M 3 11 C 3 6 6 3 11 3 L 21 3 C 26 3 29 6 29 11 C 29 13 25 15 16 15 C 7 15 3 13 3 11 Z" fill="#ffffff" opacity="0.35"/>
  <!-- User Head -->
  <circle cx="16" cy="12" r="4" fill="#ffffff" stroke="#312e81" stroke-width="0.8"/>
  <!-- User Shoulders -->
  <path d="M 9 23 C 9 18 13 17 16 17 C 19 17 23 18 23 23 Z" fill="#ffffff" stroke="#312e81" stroke-width="0.8"/>
</svg>
"""

# 10. Glass Sound (Âm Thanh)
icons["glass-sound.svg"] = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" width="32" height="32">
  <defs>
    <radialGradient id="gs_bg" cx="50%" cy="30%" r="70%">
      <stop offset="0%" stop-color="#a855f7" stop-opacity="0.9"/>
      <stop offset="60%" stop-color="#7e22ce" stop-opacity="0.85"/>
      <stop offset="100%" stop-color="#581c87" stop-opacity="0.95"/>
    </radialGradient>
    <linearGradient id="gs_rim" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0.9"/>
      <stop offset="100%" stop-color="#e9d5ff" stop-opacity="0.4"/>
    </linearGradient>
  </defs>
  <rect x="2" y="2" width="28" height="28" rx="9" fill="url(#gs_bg)" stroke="url(#gs_rim)" stroke-width="1.2"/>
  <path d="M 3 11 C 3 6 6 3 11 3 L 21 3 C 26 3 29 6 29 11 C 29 13 25 15 16 15 C 7 15 3 13 3 11 Z" fill="#ffffff" opacity="0.35"/>
  <!-- Speaker Cone -->
  <polygon points="10,13 13,13 17,9 17,23 13,19 10,19" fill="#ffffff"/>
  <!-- Sound Waves -->
  <path d="M 20 12 C 21.5 13.5 21.5 18.5 20 20" fill="none" stroke="#fde047" stroke-width="1.5" stroke-linecap="round"/>
  <path d="M 23 9 C 25.5 11.5 25.5 20.5 23 23" fill="none" stroke="#fde047" stroke-width="1.5" stroke-linecap="round"/>
</svg>
"""

# 11. Glass PC (.exe)
icons["glass-pc.svg"] = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" width="32" height="32">
  <defs>
    <radialGradient id="gpc_bg" cx="50%" cy="30%" r="70%">
      <stop offset="0%" stop-color="#64748b" stop-opacity="0.9"/>
      <stop offset="60%" stop-color="#334155" stop-opacity="0.85"/>
      <stop offset="100%" stop-color="#0f172a" stop-opacity="0.95"/>
    </radialGradient>
    <linearGradient id="gpc_rim" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0.9"/>
      <stop offset="100%" stop-color="#94a3b8" stop-opacity="0.4"/>
    </linearGradient>
  </defs>
  <rect x="2" y="2" width="28" height="28" rx="9" fill="url(#gpc_bg)" stroke="url(#gpc_rim)" stroke-width="1.2"/>
  <path d="M 3 11 C 3 6 6 3 11 3 L 21 3 C 26 3 29 6 29 11 C 29 13 25 15 16 15 C 7 15 3 13 3 11 Z" fill="#ffffff" opacity="0.35"/>
  <!-- Monitor -->
  <rect x="8" y="9" width="16" height="11" rx="1.5" fill="#1e293b" stroke="#38bdf8" stroke-width="1"/>
  <circle cx="16" cy="14.5" r="2.5" fill="#38bdf8" opacity="0.6"/>
  <!-- Stand -->
  <rect x="14" y="20" width="4" height="2.5" fill="#94a3b8"/>
  <rect x="12" y="22.5" width="8" height="1.5" rx="0.5" fill="#cbd5e1"/>
</svg>
"""

# 12. Glass Android (.apk)
icons["glass-android.svg"] = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" width="32" height="32">
  <defs>
    <radialGradient id="gan_bg" cx="50%" cy="30%" r="70%">
      <stop offset="0%" stop-color="#4ade80" stop-opacity="0.9"/>
      <stop offset="60%" stop-color="#16a34a" stop-opacity="0.85"/>
      <stop offset="100%" stop-color="#14532d" stop-opacity="0.95"/>
    </radialGradient>
    <linearGradient id="gan_rim" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0.9"/>
      <stop offset="100%" stop-color="#86efac" stop-opacity="0.4"/>
    </linearGradient>
  </defs>
  <rect x="2" y="2" width="28" height="28" rx="9" fill="url(#gan_bg)" stroke="url(#gan_rim)" stroke-width="1.2"/>
  <path d="M 3 11 C 3 6 6 3 11 3 L 21 3 C 26 3 29 6 29 11 C 29 13 25 15 16 15 C 7 15 3 13 3 11 Z" fill="#ffffff" opacity="0.35"/>
  <!-- Android Head -->
  <path d="M 11 16 C 11 12 13 9 16 9 C 19 9 21 12 21 16 Z" fill="#ffffff"/>
  <!-- Antennae -->
  <line x1="12" y1="10" x2="10" y2="7.5" stroke="#ffffff" stroke-width="1" stroke-linecap="round"/>
  <line x1="20" y1="10" x2="22" y2="7.5" stroke="#ffffff" stroke-width="1" stroke-linecap="round"/>
  <!-- Eyes -->
  <circle cx="13.5" cy="13.5" r="0.8" fill="#15803d"/>
  <circle cx="18.5" cy="13.5" r="0.8" fill="#15803d"/>
  <!-- Body -->
  <rect x="11" y="17.5" width="10" height="5.5" rx="1" fill="#ffffff"/>
</svg>
"""

# Write all SVG files
for filename, content in icons.items():
    path = os.path.join(ICONS_DIR, filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip())
    print(f"Generated {filename}")

print(f"Successfully generated {len(icons)} glassmorphism icons!")
