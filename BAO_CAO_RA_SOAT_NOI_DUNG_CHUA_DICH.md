# BÁO CÁO RÀ SOÁT TOÀN DIỆN NỘI DUNG CHƯA BIÊN DỊCH & KẾ HOẠCH BẢN ĐỊA HÓA
## Dự án: Moly - Thế Giới Chuột Chũi VN (Phiên Bản Độc Lập 2026)
*Thời gian lập báo cáo: 14/10/2026*  
*Người thực hiện: Antigravity AI Pair Programmer*

---

## MỤC LỤC
1. [Nghiệm Thu 5 Hạng Mục Đã Sửa Chữa Khẩn Cấp Theo Phản Hồi](#1-nghiệm-thu-5-hạng-mục-đã-sửa-chữa-khẩn-cấp-theo-phản-hồi)
2. [Tổng Quan Hiện Trạng Hệ Thống Game](#2-tổng-quan-hiện-trạng-hệ-thống-game)
3. [Rà Soát Chi Tiết 6 Phân Vùng Chưa Biên Dịch](#3-rà-soát-chi-tiết-6-phân-vùng-chưa-biên-dịch)
   - [Phân Vùng 1: Cổng Web & Modal Hệ Thống](#phân-vùng-1-cổng-web--modal-hệ-thống)
   - [Phân Vùng 2: Khung Đăng Nhập & Mở Đầu Flash](#phân-vùng-2-khung-đăng-nhập--mở-đầu-flash)
   - [Phân Vùng 3: Thanh Công Cụ & Menu Điều Khiển](#phân-vùng-3-thanh-công-cụ--menu-điều-khiển)
   - [Phân Vùng 4: Các Bảng Tính Năng Mở Rộng & Hội Thoại NPC](#phân-vùng-4-các-bảng-tính-năng-mở-rộng--hội-thoại-npc)
   - [Phân Vùng 5: Bản Đồ Thế Giới & Chi Tiết Biển Hiệu Công Trình](#phân-vùng-5-bản-đồ-thế-giới--chi-tiết-biển-hiệu-công-trình)
   - [Phân Vùng 6: Cơ Sở Dữ Liệu Cấu Hình XML](#phân-vùng-6-cơ-sở-dữ-liệu-cấu-hình-xml)
4. [Đề Xuất Hướng Giải Quyết & Kế Hoạch Triển Khai](#4-đề-xuất-hướng-giải-quyết--kế-hoạch-triển-khai)

---

## 1. NGHIỆM THU 5 HẠNG MỤC ĐÃ SỬA CHỮA KHẨN CẤP THEO PHẢN HỒI

Trước khi rà soát toàn bộ hệ thống, 5 vấn đề trực quan bạn báo đã được xử lý triệt để:

| STT | Vấn đề bạn phản ánh | Nguyên nhân kỹ thuật | Giải pháp đã thực hiện & Kết quả |
| :--- | :--- | :--- | :--- |
| **1** | **Nút đăng nhập Admin bị lộ** (Hình 1) | Thẻ `<a>` trong Modal có màu `#55627a` và `opacity: 0.6` | Đã đổi thành `color: transparent; opacity: 0; cursor: default; user-select: none; tabindex="-1"`. Người chơi hoàn toàn không thấy chữ, con trỏ không biến thành bàn tay, chỉ admin bấm đúng tâm đáy modal là mở `/admin.html`. |
| **2** | **Màn hình mở đầu còn tiếng Trung** (Hình 2) | Nút tròn "开始" (Shape 128 + 129), khối chữ quy ước (Text 234), bản quyền (Text 197), tooltip CADPA 8+ (Text 232) chưa dịch hoặc font thiếu glyph | Đã thay Shape 128 bằng chữ 3D **"BẮT ĐẦU"** vàng óng viền đỏ; xóa bóng chữ Hán Shape 129; chuyển Text 197, 234, 232 sang `DefineEditTextTag` tiếng Việt sắc nét. Tooltip hover hiện tiếng Việt hướng dẫn phụ huynh. |
| **3** | **Popup lỗi tiếng Trung & 4 nút dưới bị bẹp** (Hình 3) | Hộp thoại `RES_Login_Alert` (Sprite 396) có tiêu đề Shape 361 và nút bấm 367 tiếng Hán; 4 nút dưới bị ép vào khung 16px | Đã thay Shape 361 thành **"THÔNG BÁO"**, nút 367 thành **"ĐÃ HIỂU"**; biên dịch 48 chuỗi thông báo lỗi AS3 sang tiếng Việt; vẽ lại 4 nút **ĐĂNG KÝ, QUÊN MK, ĐỔI MK, BẢO MẬT** đúng tỷ lệ pixel, chữ to rõ ràng không méo. |
| **4** | **Còn chữ Taomee All Rights** (Hình 4) | Thẻ `DefineTextTag 151` nằm ở Sprite 197 (dưới logo) | Đã xóa lệnh đặt đối tượng `characterId="151"` khỏi Sprite 197. Không còn chữ Taomee dưới chân logo. |
| **5** | **Nút Đăng Nhập bị lồng 2 viền kép** (Hình 5) | Nút cam 3D đặt đè lên khung gỗ oval cũ (Shape 170 và Shape 103) trong Sprite 172 | Đã xóa `Shape 170` (đế oval gỗ) và `Shape 103` (viền bóng đổ) khỏi Sprite 172. Hiện chỉ hiển thị duy nhất 1 nút Đăng Nhập 3D cam bóng bẩy, chuẩn chỉnh. |

> *Hình ảnh kiểm tra trực quan tổng hợp của 5 mục trên đã được xuất tại file: `bang_kiem_tra_5_muc_da_sua.png`.*

---

## 2. TỔNG QUAN HIỆN TRẠNG HỆ THỐNG GAME

Qua quá trình rà soát toàn bộ thư mục mã nguồn và tài nguyên game (`mole.61.com`):
* **Tổng số tệp cấu hình XML**: 528 tệp. Trong đó có **272 tệp chứa chuỗi tiếng Trung Quốc**.
* **Tổng số tệp đồ họa & mã Flash (SWF)**: 312 tệp.
  * Bản đồ game (`resource/map/`): **259 tệp**.
  * Bảng tính năng giao diện mở rộng (`module/external/`): **12 tệp**.
  * Thư viện logic & giao diện cốt lõi (`resource/ui/`, `dll/`, `resource/login/`): **18 tệp**.
* **Trạng thái bộ đệm Proxy**: Đã khắc phục triệt để lỗi ép lưu cache (`max-age=604800`), máy chủ proxy `capture_proxy.py` hiện trả về `no-cache, must-revalidate` đối với toàn bộ tệp bản địa hóa trong `local-overrides`.

---

## 3. RÀ SOÁT CHI TIẾT 6 PHÂN VÙNG CHƯA BIÊN DỊCH

### PHÂN VÙNG 1: CỔNG WEB & MODAL HỆ THỐNG
* **Phạm vi**: `web/index.html`, `web/play.html`, `web/admin.html`, `web/assets/`.
* **Hiện trạng**:
  * Các trang HTML, popup đăng nhập, đăng ký, quên mật khẩu, quản lý tài khoản và Bảng điều khiển Quản trị Tối cao đã được Việt hóa **99%**.
  * **Còn tồn đọng nhỏ**:
    1. Một số thông báo console log và comment trong mã script còn chứa từ gốc tiếng Trung (không ảnh hưởng người dùng, nhưng cần dọn dẹp sạch).
    2. Nút "Chơi ngay" trên một số banner quảng cáo tĩnh (ảnh JPG/PNG) nếu có logo cũ cần đồng bộ logo MoLy VN.

---

### PHÂN VÙNG 2: KHUNG ĐĂNG NHẬP & MỞ ĐẦU FLASH
* **Phạm vi**: `resource/login/LoginHome.swf`, `resource/login/Login.swf`, `module/external/logo/*.swf`.
* **Hiện trạng**:
  * Đã dịch xong: Nút Bắt Đầu, Nút Đăng Nhập, 4 nút chân trang, Logo MoLy VN, Hộp thoại cảnh báo lỗi, Quy ước cư dân, Giấy phép bản quyền, Tooltip CADPA 8+.
  * **Còn tồn đọng**:
    1. **Bảng Chọn Cụm Máy Chủ** (`LoginServerPage`):
       - Chữ "电信区" (Khu Viễn Thông), "网通区" (Khu Netcom) trong danh sách server cần đổi thành "Cụm Vương Quốc 1 (Moly Bắc)", "Cụm Vương Quốc 2 (Moly Nam)", "Máy Chủ Thử Nghiệm".
       - Các tag trạng thái server: "爆满" (Đầy), "良好" (Tốt), "流畅" (Mượt) trong SWF cần thay bằng chữ Việt.
    2. **Bảng Nhập Mã Bảo Vệ Nâng Cao** (`LoginOneAuthCode`):
       - Chữ "请输入验证码" (Vui lòng nhập mã xác nhận) trong khung popup phụ.

---

### PHÂN VÙNG 3: THANH CÔNG CỤ & MENU ĐIỀU KHIỂN
* **Phạm vi**: `resource/ui/ui.swf` (Thanh công cụ đáy), `resource/ui/topUI.swf` (Thanh điều hướng đỉnh), `resource/ui/loading.swf`.
* **Hiện trạng**:
  * Đã dịch: 17 icon chức năng, 35 chuỗi hội thoại bạn bè, thông tin La Mỗ (Độ đói, khát, vệ sinh, tâm trạng).
  * **Còn tồn đọng**:
    1. **Bảng Động Tác Cư Dân (Actions Panel)** trong `ui.swf`:
       - Các chữ: "坐下" (Ngồi xuống), "招手" (Vẫy tay), "跳舞" (Nhảy múa), "投掷" (Ném tuyết/ném cà chua), "大笑" (Cười lớn), "哭泣" (Khóc lóc).
    2. **Bảng Biểu Cảm (Emote Panel)** trong `ui.swf`:
       - Tên và tooltip các icon mặt cười, ngạc nhiên, giận dữ, tim bay.
    3. **Bảng Bạn Bè (Friend Panel)** trong `ui.swf`:
       - Tab "好友" (Bạn bè), "黑名单" (Chặn), "最近" (Gần đây), nút "添加好友" (Kết bạn).
    4. **Bảng Bản Đồ Thế Giới (World Map Navigator)** mở từ `topUI.swf`:
       - Khi nhấn vào la bàn/bản đồ ở góc trên bên trái, một tấm bản đồ lớn toàn vương quốc hiện ra. Trên đó có các địa danh viết bằng tiếng Trung: "摩尔城堡" (Lâu Đài Moly), "淘淘乐街" (Phố Mua Sắm Đào Đào), "爱心教堂" (Nhà Thờ Ái Tâm), "浆果丛林" (Rừng Quả Mọng), "摩尔拉雅雪山" (Núi Tuyết Moly Lạp Á).
    5. **Màn hình Tải Bản Đồ (`loading.swf`)**:
       - Câu nhắc mẹo khi tải: "小摩尔正在前往..." (Cư dân Moly đang di chuyển tới...).

---

### PHÂN VÙNG 4: CÁC BẢNG TÍNH NĂNG MỞ RỘNG & HỘI THOẠI NPC
* **Phạm vi**: `module/external/*.swf`.
* **Hiện trạng**:
  * `NPCDialogPanel.swf`: Đã dịch khung viền, nhưng các câu trả lời lựa chọn ("好的", "我想了解更多", "下次再说") cần chuẩn hóa toàn bộ.
  * **Các SWF còn nguyên tiếng Trung**:
    1. `MoleShop.swf` (Cửa hàng Moly): Tab "服装" (Thời trang), "家具" (Nội thất), nút "试穿" (Mặc thử), "购买" (Mua ngay).
    2. `AfuSmallShopPanel.swf` (Tiệm A Phúc): Bảng đổi đồ thủ công, quà tặng đặc sản.
    3. `OnlineAwardPanel.swf` (Nhận thưởng online): Chữ "领取奖励" (Nhận quà), "今日在线时长" (Thời gian online hôm nay).
    4. `SuperLahmIntroPanel.swf` (Đậu Đậu Siêu Cấp): Bảng giới thiệu đặc quyền VIP La Mỗ, các gói nạp thẻ và quyền lợi bay, biến hình.
    5. `ElementKnightTransferPanel.swf` (Hiệp sĩ Nguyên tố): Lời thề hiệp sĩ, bảng chọn hệ Lửa, Nước, Gió, Đất.
    6. `Speaker.swf` (Loa lớn toàn server): Nút "发送广播" (Gửi thông báo), "花费摩尔豆" (Tiêu tốn Đậu Moly).

---

### PHÂN VÙNG 5: BẢN ĐỒ THẾ GIỚI & CHI TIẾT BIỂN HIỆU CÔNG TRÌNH
* **Phạm vi**: 259 tệp trong `resource/map/Map_*.swf`.
* **Đặc điểm kỹ thuật**: Trong game Moly, các biển hiệu trên công trình không phải là văn bản thường mà là **hình vẽ vector nghệ thuật cách điệu** gắn chặt vào bối cảnh bản đồ.
* **Chi tiết rà soát các công trình trọng điểm cần dịch**:
  1. **Lâu Đài Moly (`Map_001.swf`)**:
     - Biển cổng thành: Chữ "摩尔城堡" -> Cần thành "LÂU ĐÀI MOLY".
     - Biển cửa hàng đạo cụ: "道具店" -> Cần thành "TIỆM ĐẠO CỤ".
  2. **Quảng Trường Trung Tâm (`Map_004.swf`)**:
     - Biển rạp xiếc: "摩尔大剧院" -> "RẠP XIẾC MOLY".
     - Biển văn phòng thị trưởng Bodhi: "摩尔庄园行政处" -> "TÒA THỊ CHÍNH".
  3. **Phố Mua Sắm Đào Đào (`Map_005.swf` / `Map_006.swf`)**:
     - Biển tiệm thời trang Romy: "服装店" -> "TIỆM THỜI TRANG".
     - Biển tiệm thú cưng Pet Shop: "宠物店" -> "TIỆM LA MỖ".
     - Biển ngân hàng Moly: "摩尔银行" -> "NGÂN HÀNG MOLY".
  4. **Nông Trại Vui Vẻ (`Map_002.swf`)**:
     - Biển tiệm nông sản Mai Mai: "开心农场" -> "NÔNG TRẠI VUI VẺ".
     - Cối xay gió, bảng thông báo mùa vụ.
  5. **Bến Xe & Đồn Cảnh Sát (`Map_007.swf`)**:
     - Biển trụ sở cảnh sát Huân Yến: "警局" -> "SỞ CẢNH SÁT".
     - Cứu hỏa trạm: "消防署" -> "TRẠM CỨU HỎA".
  6. **Núi Tuyết Moly Lạp Á (`Map_008.swf`)**:
     - Biển cáp treo: "滑雪场" -> "BÃI TRƯỢT TUYẾT".
     - Biển tiệm đồ săn bắn: "猎人小屋" -> "NHÀ THỢ SĂN".

---

### PHÂN VÙNG 6: CƠ SỞ DỮ LIỆU CẤU HÌNH XML
* **Phạm vi**: 272 tệp XML trong `archive/clients/offline-mirror/mole.61.com/config/` và `data/`.
* **Hiện trạng**: Toàn bộ tên vật phẩm, lời thoại nhiệm vụ, câu đố học tập, kỹ năng nghề nghiệp và tên món ăn trong game đều lưu trữ tại các tệp XML này.
* **Các tệp quan trọng nhất**:
  1. `item.xml` / `cloth.xml`: Hơn 8.000 tên trang phục, mũ nón, cánh thiên thần, giày dép, công cụ đào khoáng.
  2. `furniture.xml`: Hơn 3.000 đồ đạc nội thất trang trí nhà cửa (giường, bàn học, tivi, bể cá, thảm trải sàn).
  3. `task.xml` / `quest.xml`: Hơn 400 chuỗi nhiệm vụ cốt truyện chính tuyến và nhiệm vụ hàng tuần.
  4. `pet.xml` / `lamu.xml`: Các giai đoạn tiến hóa của La Mỗ (Mầm cây, cây nhỏ, kết hoa, La Mỗ siêu cấp).
  5. `map.xml`: Tên hiển thị của 150 khu vực bản đồ.
  6. `npc.xml`: Danh sách tên các nhân vật: Bồ Đề Thị Trưởng (Bodhi), Công Chúa Meme, Cảnh Sát Trưởng Lạc Khắc (Locker), Bác Sĩ Romy, Đầu Bếp A Phúc, v.v.

---

## 4. ĐỀ XUẤT HƯỚNG GIẢI QUYẾT & KẾ HOẠCH TRIỂN KHAI

Để hoàn thiện bản địa hóa 100% không còn sót bất kỳ ngóc ngách nào, tôi đề xuất chia lộ trình thành 3 giai đoạn rõ ràng:

### Giai Đoạn 1: Hoàn Tất Toàn Bộ Giao Diện Người Dùng Lõi (Core UI & Navigation)
* **Mục tiêu**: Khi người chơi di chuyển, mở túi đồ, mở bản đồ, chat, kết bạn không còn gặp bất kỳ chữ Hán nào.
* **Công việc cụ thể**:
  1. Việt hóa `topUI.swf`: Bản đồ thế giới phóng to (World Map Navigator) -> Vẽ lại các địa danh bằng tiếng Việt.
  2. Hoàn thiện `ui.swf`: Các tab Bạn bè, Bảng Động tác, Bảng Biểu cảm, Bảng Báo cáo vi phạm.
  3. Hoàn thiện `loading.swf`: Màn hình chuyển map tiếng Việt.
* **Công nghệ**: Dùng bộ công cụ tự động `compile_master_game_swfs.py` + ElementTree XML patching + Pillow rendering.

### Giai Đoạn 2: Dịch Thuật Tự Động Hóa 272 Tệp Cấu Hình XML (Data & Quests)
* **Mục tiêu**: Đưa toàn bộ tên vật phẩm, nhiệm vụ, lời thoại và thú cưng sang tiếng Việt mượt mà.
* **Công việc cụ thể**:
  1. Viết script trích xuất (extract) toàn bộ văn bản tiếng Trung từ 272 tệp XML thành tệp từ điển JSON song ngữ.
  2. Sử dụng công nghệ dịch thuật thuật ngữ Moly chuẩn (giữ nguyên phong cách dí dỏm, thiếu nhi, trong sáng).
  3. Tự động tiêm (inject) dữ liệu tiếng Việt ngược lại vào `local-overrides/mole.61.com/config/`.

### Giai Đoạn 3: Mỹ Thuật Biển Hiệu Công Trình Các Bản Đồ Trọng Điểm (Maps & Buildings)
* **Mục tiêu**: Các bảng hiệu trên công trình (Lâu đài, Cửa hàng, Nông trại) mang phong cách hoạt hình thuần Việt.
* **Công việc cụ thể**:
  1. Ưu tiên 15 bản đồ cốt lõi người chơi lui tới thường xuyên nhất (Lâu Đài, Nông Trại, Phố Đào Đào, Nhà Thờ, Cảnh Sát, Núi Tuyết, Bãi Biển).
  2. Trích xuất các shape biển hiệu vector -> Thay thế bằng texture tiếng Việt vẽ 3D viền gỗ / viền đá tương ứng.

---

*Báo cáo này đã được lưu vào hệ thống để bạn theo dõi và phê duyệt hướng xử lý tiếp theo.*
