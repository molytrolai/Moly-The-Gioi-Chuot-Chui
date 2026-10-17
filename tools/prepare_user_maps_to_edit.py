import shutil
import sys
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "scratch" / "cac_map_can_sua"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# List of maps to provide to user for editing:
# (Map_ID, Vietnamese_Name, Source_SWF_Name, Tag_ID, Source_Extracted_Path)
MAP_EXPORT_LIST = [
    (6, "khu_vui_choi_mien_tay", "Map_10006.swf", "3", ROOT / "scratch/map_audit_bgs/map_6/3.png"),
    (7, "khu_vui_choi_mien_dong", "Map_10007.swf", "5", ROOT / "scratch/map_audit_bgs/map_7/5.png"),
    (8, "ho_than_bi", "Map_10008.swf", "14", ROOT / "scratch/map_audit_bgs/map_8/14.jpg"),
    (9, "trang_trai_anh_duong", "Map_10009.swf", "7", ROOT / "scratch/map_audit_bgs/map_9/7.jpg"),
    (10, "nong_trai_vui_ve", "Map_10010.swf", "15", ROOT / "scratch/map_audit_bgs/map_10/15.jpg"),
    (28, "hoc_vien_lamu", "Map_10028.swf", "7", ROOT / "scratch/map_audit_bgs/map_28/7.jpg"),
    (37, "dinh_nui_molylaya", "37.swf", "139", ROOT / "scratch/map_audit_bgs/map_37/139.png"),
    (38, "san_bong_da_moly", "Map_10038.swf", "26", ROOT / "scratch/map_audit_bgs/map_38/26.png"),
    (47, "quang_truong_hat_nho", "Map_10047.swf", "3", ROOT / "scratch/map_audit_bgs/map_47/3.png"),
    (77, "dai_hoc_moly", "Map_10077.swf", "5", ROOT / "scratch/map_audit_bgs/map_77/5.jpg"),
    (83, "so_giao_thong", "Map_10083.swf", "7", ROOT / "scratch/map_audit_bgs/map_83/7.jpg"),
    (109, "vuon_lau_dai", "Map_10109.swf", "5", ROOT / "scratch/map_audit_bgs/map_109/5.jpg"),
]

print("=== CHUẨN BỊ THƯ MỤC CÁC MAP CẦN SỬA CHO USER ===")
for mid, name, swf, tag, src in MAP_EXPORT_LIST:
    if src.exists():
        ext = src.suffix
        dst = OUT_DIR / f"map_{mid:02d}_{name}_tag_{tag}{ext}"
        shutil.copy2(src, dst)
        print(f"  [OK] Đã xuất: {dst.name} ({src.stat().st_size:,} bytes)")
    else:
        print(f"  [MISSING] Không tìm thấy file: {src}")

# Write README.txt
readme_text = """THƯ MỤC TỔNG HỢP CÁC BẢN ĐỒ CẦN SỬA CHỮ TIẾNG TRUNG
Dự án: Moly - Thế Giới Chuột Chũi
Đường dẫn: scratch/cac_map_can_sua/

1. DANH SÁCH BẢN ĐỒ ĐÃ ĐƯỢC BẠN SỬA TRƯỚC ĐÂY (ĐÃ NẠP VÀO GAME KHÔNG GHI ĐÈ):
- Map 01: Lâu Đài Moly (work/exported/Map1/5.jpg - Có BOOK, MOLY)
- Map 02: Quảng Trường Ái Tâm (work/exported/Map2/57.jpg)
- Map 03: Phố Mua Sắm Taotao (work/exported/Map3/4.jpg - Có GIFTS, PETS, DRESS)
- Map 04: Chân Núi Molylaya / Bãi Trượt Tuyết (work/exported/Map4/15.jpg)
-> Cả 4 map này đã được giữ nguyên vẹn 100% bản vẽ của bạn, ĐÃ GỠ BỎ TOÀN BỘ các ô chữ nổi gây xấu map!

2. DANH SÁCH CÁC MAP GỐC CHƯA SỬA ĐƯỢC TỔNG HỢP TẠI ĐÂY:
- map_06_khu_vui_choi_mien_tay_tag_3.png
- map_07_khu_vui_choi_mien_dong_tag_5.png
- map_08_ho_than_bi_tag_14.jpg
- map_09_trang_trai_anh_duong_tag_7.jpg
- map_10_nong_trai_vui_ve_tag_15.jpg
- map_28_hoc_vien_lamu_tag_7.jpg (Cổng trường Học Viện Lamu)
- map_37_dinh_nui_molylaya_tag_139.png (Khu cáp treo / Suối nước nóng)
- map_38_san_bong_da_moly_tag_26.png
- map_47_quang_truong_hat_nho_tag_3.png
- map_77_dai_hoc_moly_tag_5.jpg
- map_83_so_giao_thong_tag_7.jpg
- map_109_vuon_lau_dai_tag_5.jpg

3. CÁCH SỬA & NẠP VÀO GAME:
- Bạn chỉ cần mở file ảnh trong thư mục này bằng Photoshop / Canva / Paint, sửa trực tiếp lên hình ảnh.
- Sau khi lưu đè lên file, chạy lệnh:
    python tools/pack_all_user_maps.py
  Hệ thống sẽ tự động nạp thẳng vào game SWF mà KHÔNG chèn bất kỳ khung chữ hay ô nổi nào!
"""
(OUT_DIR / "README.txt").write_text(readme_text, encoding="utf-8")
print("\nĐã tạo thành công thư mục và file README.txt tại scratch/cac_map_can_sua/")
