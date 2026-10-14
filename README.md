# Moly - Thế Giới Chuột Chũi VN

Toàn bộ mã nguồn, client đã lưu, dữ liệu và kiến trúc máy chủ Tri-Play đám mây của dự án nằm trong thư mục này. Client game phiên bản Tiếng Việt 100% kết nối với máy chủ đám mây Neon PostgreSQL và Render, hỗ trợ chơi mượt mà trên cả Web (Ruffle WASM), Windows Desktop và Android.

- `archive/source/taomee-server-leak-full`: toàn bộ lịch sử Git của mã server cũ, có remote `upstream` trỏ tới `chenbk85/taomee`.
- `archive/source/MoleRuffle`: mã nguồn vỏ chạy client Flash Trung Quốc qua Ruffle; mặc định kết nối máy chủ chính thức, không phải máy chủ cục bộ.
- `archive/clients`: bản `Client.swf` công khai từ máy chủ chính thức Trung Quốc và Đài Loan, lưu riêng theo ngày và kiểm tra SHA-256. Đây chỉ là bộ nạp, không phải toàn bộ game.
- `archive/clients/captured-live`: kho nội dung bất biến lấy qua proxy cục bộ. Mỗi phản hồi công khai được lưu theo SHA-256.
- `archive/clients/offline-mirror`: cây host/đường dẫn được dựng từ kho SHA-256 để client ưu tiên đọc trực tiếp trên ổ E; lớp Việt hóa trong `local-overrides` luôn có độ ưu tiên cao hơn mirror.
- `archive/community/moleworld.net/mole2016/current`: bản chụp đủ `765/765` tài nguyên SWF/XML/NPC trong sơ đồ 255 map công khai của bản 2016 (132.115.986 byte), kèm URL và SHA-256 trong `data/server/current-map-graph-archive.json`.
- `updates`: các snapshot bất biến lấy về sau. `tools/Update-Archive.ps1` đã được kiểm thử: fetch lịch sử nguồn và lưu bộ khởi động công khai của hai vùng vào thư mục có dấu thời gian, không ghi đè bản đã lưu.
- `runtime`: dành cho phần chạy thử trên máy này khi có client/server tương thích.
- `data`: dành cho dữ liệu và bản sao lưu của server cục bộ khi dựng được.
- `docs`: kiểm kê, nguồn và kết quả kiểm tra.
- `localization`: bản dịch và bảng thuật ngữ, tách khỏi tài nguyên gốc.
- `tools`: công cụ và script của dự án.

Không chạy các script khởi động cũ trong kho server mà chưa kiểm tra: chúng có lệnh dừng tiến trình/xóa file. Không dùng tài khoản/mật khẩu chính thức với server bên thứ ba. Không phát hành tài nguyên game có bản quyền khi chưa có quyền sử dụng.

`runtime/client` là nhánh làm việc riêng của MoleRuffle, đã chỉnh để cache và Flash SharedObjects có thể nằm ở `E:\Codex\Projects\Moly-Viet\data\client` qua biến `MOLY_DATA_ROOT`. `tools/Build-Client.ps1` và `tools/Start-Client.ps1` được chuẩn bị nhưng chưa build vì máy chưa có Rust/Cargo. Việc kiểm thử hiện tại dùng Ruffle desktop dựng sẵn, không phụ thuộc nhánh Rust này.

Bản Ruffle desktop chính thức `v0.7.1` đã được tải và xác minh SHA-256 vào `archive/downloads`, giải nén ở `tools/ruffle-0.7.1`. Trình khởi chạy `runtime/launcher/Moly-Official-Test.exe` tự mở máy chủ cục bộ, proxy tài nguyên và Ruffle nếu chúng chưa chạy; config/cache/save nằm trong `data/ruffle-official`. Proxy ưu tiên lớp Việt hóa, rồi mirror trên E, sau đó mới dùng nguồn công khai còn hoạt động; `Server.xml` gửi cho client luôn được đổi sang `127.0.0.1`. Bài khởi động nguội và đăng nhập giao thức đã đạt. Xem `docs/Ruffle-desktop-test-2026-10-09.md` và `docs/protocol-notes.md`.

Các bản vá tương thích không ghi đè tài nguyên đã lưu theo SHA-256. Chúng nằm riêng ở `archive/clients/local-overrides`; hiện có danh sách nghề NPC rỗng cho các map không còn file trên máy chủ, cổng thoát tương thích Ruffle của map 62, SWF map 17 có nguồn từ bản Đài Loan 2016 và XML rỗng chuẩn cho map 19. SWF map 17 đã được kiểm tra mã: cửa `door_1` quay về map 1.

`tools/audit_offline_map_assets.py` đã kiểm tra qua đúng proxy đang chạy: toàn bộ `765/765` tài nguyên trong sơ đồ map được phục vụ cục bộ (`20` từ lớp ghi đè, `745` từ mirror), không tài nguyên nào phải rơi xuống upstream trong bài kiểm tra này.

Tài khoản kiểm thử `10000001` hiện là `Moly Admin`: VIP cấp 8, 999.999 Đậu Vàng và hồ sơ Kỵ sĩ nguyên tố phục vụ kiểm thử. Hệ thống tài khoản độc lập mới (`tools/account_system.py`) lưu trữ tại `data/server/accounts.json`, tự sinh ID từ `10000002`, mã hóa hai lớp `MD5(MD5(password))`, hỗ trợ đăng ký tài khoản trực tiếp trong game qua proxy (`cmd=1101` captcha, `cmd=1102` đăng ký), công cụ quản trị CLI `tools/manage_accounts.py` và tích hợp đăng nhập Google bằng OpenID Connect (`/auth/google/login`, `/auth/google/callback`).

Bộ kiểm thử tự động toàn diện `tools/test_full_system.py` kiểm tra trọn vẹn chu trình đăng ký, xác thực thư mục, đồng bộ thế giới, chặn 25 tên miền quảng cáo/theo dõi, duyệt 36 tuyến map hai chiều và phục vụ 100% tài nguyên ngoại tuyến từ ổ E mà không rò rỉ ra ngoài.

Việt hóa đang được nạp bằng lớp ghi đè, không sửa tài nguyên gốc: 22 bản đồ trọng yếu (`1`, `2`, `3`, `4`, `5`, `15`, `17`, `18`, `19`, `20`, `21`, `28`, `32`, `38`, `61`, `62`, `63`, `64`, `75`, `76`, `120`, `142`, `143`), tên NPC liên quan (Chị Cầu Vồng, Kulo, Tommy, Frank, Thầy Claus, Hoàng tử Jack, Đầu bếp Nick, Cô Hoa...), `MoleShop.swf` và một phần `BubbleMainB2.swf`. Các nội dung quảng bá lỗi thời, miền quảng cáo, thanh toán và liên kết ngoài đã biết bị loại hoặc chặn hoàn toàn. Xem `localization/README.md` và `docs/TEST-MATRIX.md`.
