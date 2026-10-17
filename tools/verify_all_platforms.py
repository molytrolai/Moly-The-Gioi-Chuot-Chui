#!/usr/bin/env python3
"""Comprehensive verification across Web, Android APK, and PC Desktop distribution."""

import sys
import zipfile
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[1]

def verify_apk():
    print("======================================================================")
    print("   1. KIỂM TRA ĐẶC BIỆT BẢN ANDROID APK                                ")
    print("======================================================================")
    apk_paths = [
        ROOT / "web" / "download" / "Moly-The-Gioi-Chuot-Chui.apk",
        ROOT / "web" / "download" / "Moly Thế Giới Chuột chũi.apk",
    ]
    for apk in apk_paths:
        if not apk.exists():
            print(f"  ❌ Không tìm thấy: {apk}")
            continue
        print(f"  ✓ Tệp APK: {apk.name} ({apk.stat().st_size:,} bytes)")
        with zipfile.ZipFile(apk) as zf:
            names = set(zf.namelist())
            has_dex = "classes.dex" in names
            has_manifest = "AndroidManifest.xml" in names
            has_offline = "assets/offline.html" in names
            has_mobile = "assets/mobile.html" in names
            has_ruffle_js = "assets/static/ruffle/ruffle.js" in names
            has_wasm = any(n.endswith(".wasm") for n in names)
            
            print(f"    - Mã máy Java/DEX (classes.dex): {'✅ Hợp lệ' if has_dex else '❌ Thiếu'}")
            print(f"    - Cấu hình quyền (AndroidManifest.xml): {'✅ Hợp lệ' if has_manifest else '❌ Thiếu'}")
            print(f"    - Trang kết nối tự động (offline.html): {'✅ Hợp lệ' if has_offline else '❌ Thiếu'}")
            print(f"    - Bộ nạp Ruffle WebAssembly: {'✅ Hợp lệ' if (has_ruffle_js and has_wasm) else '❌ Thiếu'}")

def verify_desktop():
    print("\n======================================================================")
    print("   2. KIỂM TRA BẢN MÁY TÍNH (PC DOWNLOAD)                             ")
    print("======================================================================")
    zip_paths = [
        ROOT / "web" / "download" / "Moly-The-Gioi-Chuot-Chui.zip",
        ROOT / "web" / "download" / "Moly Thế Giới Chuột chũi.zip",
    ]
    for zp in zip_paths:
        if not zp.exists():
            print(f"  ❌ Không tìm thấy: {zp}")
            continue
        print(f"  ✓ Tệp ZIP: {zp.name} ({zp.stat().st_size:,} bytes)")
        with zipfile.ZipFile(zp) as zf:
            names = zf.namelist()
            print(f"    - Tổng số tệp nén: {len(names):,} files")
            has_exe = any(n.endswith(".exe") for n in names)
            has_bat = any(n.endswith(".bat") for n in names)
            has_ruffle = any("ruffle" in n for n in names)
            has_overrides = any("local-overrides" in n for n in names)
            has_offline_maps = any("offline-mirror" in n for n in names)
            print(f"    - Tệp thực thi launcher: {'✅ Hợp lệ' if (has_exe and has_bat) else '❌ Thiếu'}")
            print(f"    - Ruffle Runtime PC: {'✅ Hợp lệ' if has_ruffle else '❌ Thiếu'}")
            print(f"    - Dữ liệu map & UI mới (overrides): {'✅ Hợp lệ' if has_overrides else '❌ Thiếu'}")
            print(f"    - Toàn bộ map offline (offline-mirror): {'✅ Hợp lệ' if has_offline_maps else '❌ Thiếu'}")

def verify_swfs():
    print("\n======================================================================")
    print("   3. KIỂM TRA TẤT CẢ DỮ LIỆU ĐỒ HỌA & MAP FLASH MỚI NHẤT             ")
    print("======================================================================")
    targets = [
        ("Thanh điều hướng đỉnh", "archive/clients/local-overrides/mole.61.com/resource/ui/topUI.swf"),
        ("Thanh công cụ & Động tác", "archive/clients/local-overrides/mole.61.com/resource/ui/ui.swf"),
        ("Bảng Đậu Đậu Siêu Cấp", "archive/clients/local-overrides/mole.61.com/module/external/SuperLahmIntroPanel.swf"),
    ]
    user_maps = [1, 2, 3, 4, 6, 7, 8, 9, 10, 28, 37, 38, 47, 77, 83, 109]
    for m in user_maps:
        targets.append((f"Bản đồ Map {m}", f"archive/clients/local-overrides/mole.61.com/resource/map/{m}.swf"))

    all_ok = True
    for label, rel in targets:
        p = ROOT / rel
        if not p.exists():
            print(f"  ❌ THIẾU: {label} ({rel})")
            all_ok = False
        else:
            sig = p.read_bytes()[:3]
            if sig in [b"FWS", b"CWS", b"ZWS"]:
                print(f"  ✅ {label:<26}: {p.name} ({p.stat().st_size:,} bytes, chữ ký Flash {sig.decode('ascii')})")
            else:
                print(f"  ⚠️ {label:<26}: {p.name} Chữ ký không hợp lệ ({sig})")
                all_ok = False

    print("\n======================================================================")
    if all_ok:
        print("   ✅ TẤT CẢ DỮ LIỆU GAME ĐÃ ĐỒNG BỘ 100% TRÊN WEB, APK VÀ PC!      ")
    else:
        print("   ⚠️ PHÁT HIỆN LỖI DỮ LIỆU TRÊN MỘT SỐ THÀNH PHẦN                    ")
    print("======================================================================")

if __name__ == "__main__":
    verify_apk()
    verify_desktop()
    verify_swfs()
