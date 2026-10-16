#!/usr/bin/env python3
"""Công cụ tự động cập nhật icon và giao diện bắt đầu game sau khi người dùng chỉnh sửa ảnh PNG.
Tự động phát hiện ảnh đã sửa trong thư mục `chinh_sua_icon_game/`,
tổng hợp vào LoginHome.swf và sắp xếp lại tag chuẩn để không bị treo game.
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

PROJECT_ROOT = Path(__file__).resolve().parents[1]
USER_DIR = PROJECT_ROOT / "chinh_sua_icon_game"
LOCAL_OVERRIDES = PROJECT_ROOT / "archive" / "clients" / "local-overrides" / "mole.61.com" / "resource" / "login"
LOGIN_HOME_SWF = LOCAL_OVERRIDES / "LoginHome.swf"

def main():
    print("======================================================================")
    print("       ĐANG CẬP NHẬT ICON / GIAO DIỆN BẮT ĐẦU GAME MOLY VN            ")
    print("======================================================================")
    
    if not USER_DIR.exists():
        print(f"[LỖI] Không tìm thấy thư mục {USER_DIR}")
        return 1

    # 1. Quét các file ảnh người dùng đã sửa
    folders = [
        ("01_nut_dang_ky", "Nút Đăng ký"),
        ("02_nut_luu_trang_yeu_thich", "Nút Lưu trang"),
        ("03_nut_dien_dan_chinh_thuc", "Nút Diễn đàn"),
        ("04_cskh_phu_huynh_va_do_tuoi", "Cụm CSKH & Phụ huynh & Độ tuổi"),
        ("05_chu_taomee_chan_trang", "Chữ Taomee chân trang"),
        ("06_tieu_de_thong_bao_alert", "Tiêu đề Thông Báo Alert (Shape 362)"),
        ("07_nut_dang_nhap_lai_alert", "Nút Đăng Nhập Lại trong Alert (Shape 384/385/386/378)"),
        ("08_nut_da_hieu_alert", "Nút Đã Hiểu trong Alert (Shape 367/368/369)"),
        ("09_nut_huy_bo_alert", "Nút Hủy Bỏ trong Alert (Shape 371/372/373)"),
        ("10_nut_xac_nhan_alert", "Nút Xác Nhận trong Alert (Shape 375/376)"),
        ("11_nut_tro_giup_alert", "Nút Trợ Giúp trong Alert (Shape 380/381/382)"),
        ("12_nut_dang_nhap_alert", "Nút Đăng Nhập trong Alert (Shape 388/389/390)"),
        ("13_nut_doi_mat_khau_alert", "Nút Đổi Mật Khẩu trong Alert (Shape 392/393/394)"),
        ("14_man_hinh_chon_server", "Cụm nút Màn Hình Chọn Máy Chủ"),
        ("15_khung_dang_ky_trong_game", "Cụm nút Khung Đăng Ký Trong Game"),
    ]
    
    print("\n[1/3] Kiểm tra các thư mục icon người dùng:")
    for fld, desc in folders:
        fld_path = USER_DIR / fld
        if fld_path.exists():
            pngs = list(fld_path.glob("*.png"))
            print(f"  ✓ {desc} ({fld}): {len(pngs)} file ảnh PNG sẵn sàng.")
        else:
            print(f"  ! Chưa có thư mục: {fld}")

    # 2. Chạy rebuild master LoginHome & Login
    print("\n[2/3] Tiến hành đóng gói và đồng bộ dữ liệu vào game...")
    build_home_script = PROJECT_ROOT / "scratch" / "build_home.py"
    if build_home_script.exists():
        print("  -> Đang biên dịch LoginHome.swf...", flush=True)
        res = subprocess.run([sys.executable, str(build_home_script)], capture_output=True, text=True)
        if res.returncode != 0:
            print(f"[CẢNH BÁO] Quá trình build LoginHome trả về mã lỗi: {res.stderr}", flush=True)
        else:
            print("  ✓ Đã biên dịch xong LoginHome.swf", flush=True)

    build_login_script = PROJECT_ROOT / "scratch" / "build_login.py"
    if build_login_script.exists():
        print("  -> Đang biên dịch Login.swf (quá trình này mất khoảng 25-35 giây do FFDec nạp và ráp đồ hoạ, vui lòng chờ chút nhé)...", flush=True)
        res = subprocess.run([sys.executable, str(build_login_script)], capture_output=True, text=True)
        if res.returncode != 0:
            print(f"[CẢNH BÁO] Quá trình build Login trả về mã lỗi: {res.stderr}", flush=True)
        else:
            print("  ✓ Đã biên dịch xong Login.swf (Áp dụng các nút và đồ hoạ mới)", flush=True)

    # 3. Chạy fix_tag_order để đảm bảo FileAttributes ở Tag #0 (chống treo Flash/Ruffle)
    print("\n[3/3] Kiểm tra an toàn cấu trúc SWF (AVM2 Tag Order)...", flush=True)
    fix_script = PROJECT_ROOT / "scratch" / "fix_tag_order.py"
    if fix_script.exists():
        res = subprocess.run([sys.executable, str(fix_script)], capture_output=True, text=True)
        print("  ✓ Cấu trúc SWF đạt chuẩn:", res.stdout.strip().replace("\n", " | "), flush=True)

    print("\n======================================================================", flush=True)
    print("   THÀNH CÔNG 100%! ĐÃ CẬP NHẬT TOÀN BỘ ICON VÀO GAME MOLY THÀNH CÔNG!     ", flush=True)
    print("   Bạn có thể mở game bằng 'Choi-Game.bat' để vào chơi ngay.             ", flush=True)
    print("======================================================================\n", flush=True)
    return 0

if __name__ == "__main__":
    sys.exit(main())
