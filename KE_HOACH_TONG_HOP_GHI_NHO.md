# 📋 KẾ HOẠCH TỔNG HỢP & GHI NHỚ TOÀN DIỆN DỰ ÁN
## GAME: MOLY - THẾ GIỚI CHUỘT CHŨI VN
*Tài liệu đối chiếu, rà soát và lưu trữ ghi nhớ tiến độ dự án (Tự động cập nhật để dự phòng mất kết nối)*
*Thời gian cập nhật: 14/10/2026*

---

## 📌 I. TỔNG QUAN ĐỊNH HƯỚNG & YÊU CẦU CỐT LÕI TỪ BẠN

1. **Độc lập máy chủ 100%:**
   - Game chạy máy chủ độc lập hoàn toàn (`account_system.py`, `moly_probe_server.py`), **tuyệt đối không dùng chung hay phụ thuộc vào server Trung Quốc / Đài Loan**.
   - Dữ liệu người chơi, nhân vật, tài sản, Đậu Vàng, VIP Siêu LaMu, nhà cửa và vườn tược được lưu độc lập tại cơ sở dữ liệu (SQLite cục bộ / Neon Cloud PostgreSQL).
2. **Đổi tên thương hiệu chuẩn:**
   - Tên chính thức duy nhất: **"Moly - Thế Giới Chuột Chũi VN"** (Đã xóa bỏ tên cũ "Moly Việt").
   - Gỡ sạch toàn bộ logo bản quyền cũ của Taomee, xóa mọi quảng cáo, banner sự kiện cũ của Trung Quốc.
3. **Bảo mật tuyệt đối:**
   - File `README.md` trên GitHub chỉ chứa thông tin giới thiệu game và hướng dẫn người chơi, **đã xóa sạch toàn bộ API key, mật khẩu quản trị, endpoint nhạy cảm**.
4. **Quy trình Việt hóa Icon / Đồ họa:**
   - Tiêu chí: **Giống bản gốc nhất**, chỉ khác chữ tiếng Việt. Chữ phải **to rõ, dễ đọc, thẩm mỹ 3D hoạt hình dễ thương (cute)** thay vì dán đè khung chữ nhật thô hay chữ quá bé.
   - **Nguyên tắc duyệt:** Báo cáo bảng so sánh chi tiết cho bạn xem và duyệt trước khi thay thế vào file SWF của game.
   - Dùng trình tạo ảnh chất lượng cao đối với các icon chi tiết (Bản đồ đảo nổi, động tác, ba lô), kết hợp render font siêu mẫu (supersampling) 3 lớp: Mặt ## 📌 II. TIẾN ĐỘ THIẾT KẾ & ĐỒ HỌA MÀN HÌNH ĐĂNG NHẬP (NGOÀI GAME)

Đã hoàn thành toàn bộ 10 thành phần hình ảnh theo ảnh chụp màn hình yêu cầu của bạn, được render siêu mẫu 4x với phong cách 2D hoạt hình Chuột Chũi chuẩn nguyên bản:
1. **`btn_start_168.png` & `shape_128.png`:** Nút Bắt Đầu khối cầu pha lê đỏ ruby 3D, chữ "BẮT ĐẦU" 2 tầng vàng kim viền đỏ thẫm cực to rõ.
2. **`btn_login_173.png` & `shape_171.png`:** Nút Đăng Nhập viên thuốc cam bóng 3D, chữ "ĐĂNG NHẬP" hoạt hình vàng kim viền hạt dẻ đậm.
3. **`btn_reg_169.png` (Shape 158):** Chữ "Đăng Ký" hoạt hình vàng kim viền đỏ, xóa sạch hộp xám/cam giả tạo, nền trong suốt 100%.
4. **`btn_forgot_160.png` (Shape 161):** Chữ "Quên MK" vàng kim viền đỏ đậm, nền trong suốt 100%.
5. **`btn_change_163.png` (Shape 164):** Chữ "Đổi MK" vàng kim viền đỏ đậm, nền trong suốt 100%.
6. **`btn_protect_166.png` (Shape 167):** Chữ "Bảo Mật" vàng kim viền đỏ đậm, nền trong suốt 100%.
7. **`btn_clear_109.png`:** Nút "Xóa Lưu" bo góc tròn màu đỏ ruby mềm mại, đổ bóng 3D, chữ vàng kim viền đỏ.
8. **`btn_system_174.png` & `btn_system_176.png`:** Nút "Tài Khoản Lưu" viên thuốc cam hổ phách ấm áp, chữ to rõ.
9. **`randomMC_banner_3.png`:** Bảng thông báo 328x238 px khung cuốn hoàng gia viền chỉ vàng, nội dung tiếng Việt sắc nét, nút ngọc lục bảo 3D "VÀO GAME NGAY".
10. **`image_148.png`:** Logo chính giữa 900x200 px (nền trong suốt), chữ 3D bóng bẩy "Moly - Thế Giới Chuột Chũi" viền trắng kép, chóp mũi đỏ chú chuột chũi và dải ruy băng "★ VIỆT NAM ★".

---

## 💻 III. TRẠNG THÁI NÂNG CẤP GIAO DIỆN WEB & POPUP

Đã rà soát và nâng cấp toàn bộ hệ thống Popup trên cả 3 trang (`index.html`, `play.html`, `admin.html`):

1. **Đóng popup khi bấm ra ngoài khoảng trống (Backdrop Dismissal):**
   - Thêm `cursor: pointer` trên lớp nền `.modal-overlay`.
   - Bổ sung sự kiện `click` và `touchend` cho toàn bộ các modal: Tài khoản, Nạp tiền, Giftcode, Siêu LaMu, Tra cứu cư dân, Tin tức vương quốc, Đổi mật khẩu.
2. **Nút "X" và nút "← Trở lại" luôn hiển thị:**
   - Nút `&times;` (X) lớn, dễ bấm ở góc phải tiêu đề modal, rê chuột có hiệu ứng sáng bóng.
   - Tiêu đề modal (`.modal-header`) được gắn thuộc tính `position: sticky; top: -20px; z-index: 20` để khi cuộn trang nút X không bao giờ bị trôi.
   - Thêm nút **`← Trở lại`** và nút **`✕ Đóng`** ở chân của tất cả các tab.
3. **Phím tắt ESC:**
   - Nhấn phím `Escape` trên bàn phím sẽ lập tức đóng popup đang mở.
4. **Thoát trang Quản trị Admin:**
   - Màn hình đăng nhập Admin bổ sung nút `&times;` góc trên và nút `← Trở Lại Trang Chủ` bên dưới form để không bao giờ bị kẹt lại.

---

## 🚀 IV. BẢNG KIỂM KÊ TIẾN ĐỘ TỔNG THỂ DỰ ÁN

| Hạng mục | Công việc chi tiết | Trạng thái hiện tại | Ghi chú |
| :--- | :--- | :---: | :--- |
| **1. Đồ họa Đăng nhập** | 10 thành phần nút/banner (Bắt Đầu, Đăng Nhập, Đăng Ký, Quên MK, Đổi MK, Bảo Mật, Xóa Lưu, Tài Khoản Lưu, Banner randomMC, Logo 148) | **ĐÃ HOÀN TẤT & ĐÃ BIÊN DỊCH 100%** | Đã tích hợp vào `LoginHome.swf`, `Login.swf`, `randomMC.swf` |
| **2. Icon Thanh Công Cụ** | 12 icon chính (Bản đồ cập nhật mới, Ba lô Option 2, Quà Tặng biển gỗ, Động tác, Bạn bè, Gia viên, Shop, v.v.) | **ĐÃ HOÀN TẤT & ĐÃ BIÊN DỊCH 100%** | Đã tích h�## 🛠️ V. KẾT QUẢ BIÊN DỊCH VÀ CẬP NHẬT LÕI MỚI NHẤT (14/10/2026)

1. **Khắc phục 5 điểm phản hồi trực quan từ bạn**:
   - **Nút Admin vô hình 100%**: Ẩn triệt để trong modal tài khoản (`web/play.html` & `web/index.html`), con trỏ chuột bình thường, không hiện bất kỳ ký tự nào, chỉ Admin bấm đúng tâm đáy modal là mở `/admin.html`.
   - **`LoginHome.swf` (Màn hình mở đầu)**:
     - Nút Bắt Đầu: Thay thế Shape 128 bằng đồ họa 3D **BẮT ĐẦU** vàng kim viền đỏ, tách bỏ hoàn toàn bóng chữ Hán đỏ Shape 129.
     - Quy ước cư dân & Giấy phép: Chuyển DefineText sang `DefineEditTextTag` tiếng Việt, không phụ thuộc font nhúng, hiển thị chuẩn từng dấu câu.
     - Tooltip CADPA 8+: Hover vào huy hiệu 8+ hiện bong bóng hướng dẫn tiếng Việt chuẩn mực.
   - **`Login.swf` (Khung đăng nhập & Popup thông báo)**:
     - Popup cảnh báo `RES_Login_Alert`: Đổi tiêu đề thành **"THÔNG BÁO"**, nút bấm thành **"ĐÃ HIỂU"** / **"XÁC NHẬN"**. Biên dịch 48 chuỗi thông báo lỗi AS3 sang tiếng Việt.
     - 4 nút nhỏ chân trang (**ĐĂNG KÝ**, **QUÊN MK**, **ĐỔI MK**, **BẢO MẬT**): Vẽ lại theo đúng tỷ lệ 16px, chữ to rõ ràng, viền đỏ nền vàng hổ phách, không còn bị bẹp hay vỡ nét.
     - Logo & Bản quyền: Xóa bỏ thẻ `PlaceObject` chữ `© Taomee. All Rights Reserved.` dưới chân logo.
     - Nút Đăng Nhập: Xóa bỏ khung oval gỗ thừa đè sau nút cam 3D.
   - **Bộ đệm Proxy**: Cập nhật `tools/capture_proxy.py` trả về header `no-cache, no-store, must-revalidate` cho toàn bộ tài nguyên override, giúp game luôn tải bản mới nhất tức thì.

2. **Báo cáo rà soát toàn diện hệ thống game**:
   - Đã biên soạn tệp báo cáo master: [BAO_CAO_RA_SOAT_NOI_DUNG_CHUA_DICH.md](file:///e:/Codex/Projects/Moly-The-Gioi-Chuot-Chui/BAO_CAO_RA_SOAT_NOI_DUNG_CHUA_DICH.md) phân tích toàn bộ 6 phân vùng trong game (259 map SWF, 12 module panel, 272 XML cấu hình) và lộ trình giải pháp chi tiết cho bạn xem xét.
| **3. XML Bản đồ Game** | 257 file XML bản đồ, NPC, hội thoại | **ĐÃ VIỆT HÓA 100%** | Đã kiểm tra không lỗi cú pháp XML |
| **4. Trắc nghiệm & Câu hỏi** | 252 câu hỏi cư dân, thi thăng cấp kỵ sĩ | **ĐÃ VIỆT HÓA 100%** | Thay thế toàn bộ câu hỏi văn hóa Trung Quốc sang kiến thức chung & VN |
| **5. Cổng Game Web** | Nạp thẻ cào, QR động Vietcombank, quản lý tài khoản, đổi mã quà, Siêu LaMu | **ĐÃ HOÀN TẤT & ĐÃ TEST (11/11)** | Đã test tự động duyệt Đậu Vàng & VIP |
| **6. Giao diện Modal Web** | Thoát popup khi click ngoài, nút X, nút Trở lại | **ĐÃ HOÀN TẤT 100%** | Đã xác minh hoạt động trơn tru |
| **7. Dọn dẹp tệp tin rác** | Xóa bỏ ảnh thử nghiệm font, file compile demo | **ĐÃ DỌN SẠCH** | Giữ thư mục dự án gọn gàng nhất |
| **8. Đẩy lên mạng (Cloud)** | Render.com Web Server + Neon PostgreSQL | **KỊCH BẢN ĐÃ SẴN SÀNG** | Sẵn sàng triển khai theo yêu cầu |

---

## 🛠️ V. KẾT QUẢ ĐÓNG GÓI VÀ BÀN GIAO MỚI NHẤT

- **ui.swf**: Đã tích hợp thành công icon **Bản Đồ** do bạn thiết kế (`ui_3279.png`), icon **Ba Lô** bản Option 2 chữ to rõ (`ui_6844.png`, `ui_6846.png`), cùng 15 icon thanh điều khiển tiếng Việt sắc nét (`Động tác`, `Ném`, `Bạn bè`, `Thiên sứ`, `Gia viên`, `Shop`, `Nhà ở`).
- **topUI.swf**: Đã tích hợp thành công icon **Quà Tặng** biển gỗ do bạn thiết kế (`topui_82.png`), icon **Hoạt Hình** chú hề (`topui_361.png`), và icon **Gia Viên Mới** bé mèo (`topui_366.png`).
- Toàn bộ file đã được xuất ngược để kiểm chứng độ nguyên vẹn và đưa vào thư mục phục vụ game trực tiếp: `archive/clients/local-overrides/mole.61.com/`.
