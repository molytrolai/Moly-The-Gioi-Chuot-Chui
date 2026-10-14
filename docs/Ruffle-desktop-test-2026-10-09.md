# Kiểm thử Ruffle desktop (09-10-2026)

- Tải bản Ruffle chính thức `v0.7.1` cho Windows x64 từ GitHub Releases của `ruffle-rs/ruffle` vào `archive/downloads/ruffle-0.7.1-windows-x86_64.zip`; giải nén vào `tools/ruffle-0.7.1`.
- SHA-256 của ZIP: `a5f6df9881771226e330e08a1fa7666f4caff50ddf9f2f993cdd95293edca627`, trùng trường `digest` do GitHub API công bố cho asset này.
- `ruffle.exe --help` xác nhận bản dựng sẵn có `--spoof-url`, `--base`, `--tcp-connections allow`, `--config`, `--cache-directory`, `--save-directory`. Về lý thuyết các tham số này đáp ứng 3 điểm cốt lõi trong README MoleRuffle mà không cần biên dịch Rust.
- Đã tạo trình khởi chạy cố định `runtime/launcher/Moly-Official-Test.exe`. Nó mở `Client.swf` với URL giả `http://mole.61.com/Client.swf`, base URL chính thức, quyền TCP, đồ họa DX12 và toàn bộ config/cache/save dưới `data/ruffle-official`.
- Người dùng đã trực tiếp xác nhận cửa sổ client hiển thị và đang tải. Công cụ chụp Windows Graphics Capture không đọc được bề mặt Ruffle (timeout), nên xác nhận hình ảnh dựa trên màn hình người dùng; trạng thái kỹ thuật được kiểm chứng độc lập bằng tiến trình, kết nối, SharedObject và log proxy.
- Proxy `tools/capture_proxy.py` chạy ở `127.0.0.1:18080`, chỉ cho GET/HEAD công khai, loại Cookie/Authorization/Set-Cookie và lưu nội dung theo SHA-256. Nó đã lưu chuỗi bộ nạp tới `Login.swf`, `TaomeeCoreDLL.swf`, `ClientConfigDLL.swf`, `ClientCommonDLL.swf`, `ClientSocketDLL.swf` và `ClientAppDLL.swf`.
- Bản `Server.xml` gốc vẫn được lưu nguyên. Chỉ phản hồi gửi cho client được đổi các địa chỉ đăng nhập/game sang `127.0.0.1`, nhờ đó tài khoản thử không bị gửi tới máy chủ chính thức.
- `tools/moly_probe_server.py` nghe cục bộ ở các cổng 843, 1863 và 3200. Nó đã có phản hồi tối thiểu cho đăng nhập thư mục, danh sách máy chủ và gói vào thế giới 201; mọi gói thử được ghi ở `data/server/probe-events.jsonl`.
- `tools/Run-Official-Ruffle.ps1` và trình khởi chạy đều dùng dữ liệu trên E. File `data/ruffle-official/capture-proxy.txt` bật proxy lưu trữ khi có URL hợp lệ.

Mốc cập nhật 10-10-2026: tài khoản giả cục bộ đã đăng nhập, nhân vật và UI bản đồ hiển thị, di chuyển hoạt động, và chuỗi chuyển map `1 → 4 → 61 → 62` đã được xác nhận bằng gói mạng cùng tài nguyên tải thành công. Map 62 đã có cổng thoát tương thích Ruffle riêng trong `local-overrides`. Bước tiếp theo là kiểm thử lại đường `62 → 61` và tiếp tục phủ các map/chức năng còn thiếu.
