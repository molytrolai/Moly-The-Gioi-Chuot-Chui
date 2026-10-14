# Hướng Dẫn Triển Khai Moly Việt (Cloudflare + Render + Neon PostgreSQL + GitHub)

Tài liệu hướng dẫn chi tiết quy trình đưa hệ sinh thái game **Moly - Thế Giới Chuột Chũi** lên môi trường Internet công cộng với kiến trúc **Tri-Play (3 nền tảng song hành)**, tối ưu đường truyền tại Việt Nam với chi phí 0đ (hoặc chi phí tối thiểu).

---

## 1. Mô Hình Kiến Trúc Đám Mây (Tri-Play Cloud Architecture)

```
       ┌───────────────────────────────┐
       │     NGƯỜI CHƠI / CỘNG ĐỒNG    │
       └──────────────┬────────────────┘
                      │
       ┌──────────────┴────────────────────────┐
       │                                       │
       ▼                                       ▼
[ 1. Web Browser (PC/Laptop) ]        [ 2. Tải Bản Chơi ]
Chơi trực tiếp trên Chrome/Edge/Cốc Cốc ├── Android APK (13 MB - Điện thoại/Tablet)
Ruffle WebAssembly (Không cần Flash)   └── Desktop PC ZIP (150 MB - 257 Maps Offline)
       │                                       │
       └──────────────┬────────────────────────┘
                      │
                      ▼
       [ Cloudflare CDN & DNS ]
       - Quản lý tên miền chính thức (ví dụ: `molyviet.vn` hoặc `moly.games`)
       - Chứng chỉ SSL/TLS Full (Strict) miễn phí
       - Chống tấn công từ chối dịch vụ (DDoS) và chống Flood bot rác
       - Edge Caching tại các PoP Việt Nam (Hà Nội & TP.HCM):
         Cache 257 file SWF bản đồ, Ruffle WASM, âm thanh, icon (Tải map < 0.1s)
       - WebSocket WSS Bridge (`wss://molyviet.vn/ws/1863`, `wss://molyviet.vn/ws/3200`)
                      │
                      ▼
             [ Render.com (Cloud) ]
       - Chạy container Docker từ repository GitHub (Region Singapore, Ping ~20-30ms)
       - `capture_proxy.py`: Cổng Web Portal, WebSocket-to-TCP Gateway, HTTP Proxy
       - `moly_probe_server.py`: Máy chủ Thế giới (World), Đăng nhập, Mặc đồ, Mua sắm, Minigame
                      │
                      ▼
         [ Neon PostgreSQL Serverless ]
       - Cơ sở dữ liệu trên mây (Singapore Region - `neondb`)
       - Bảng `moly_users`: Lưu tài khoản người chơi, Đậu Vàng, Quần áo, Túi đồ, Lamu, Nhiệm vụ
       - Tự động co giãn theo lượng cư dân trực tuyến, sao lưu an toàn 100%
```

---

## 2. Quy Trình Triển Khai Từng Bước

### Bước 1: Khởi Tạo Cơ Sở Dữ Liệu Neon PostgreSQL (Miễn Phí)
1. Truy cập [neon.tech](https://neon.tech) và đăng ký tài khoản miễn phí.
2. Tạo 1 dự án mới: `moly-viet-db`.
   - **Region**: Chọn `ap-southeast-1 (Singapore)` để có độ trễ cực thấp về Việt Nam.
   - **Postgres version**: Khuyến nghị version 16 hoặc 17.
3. Chạy Schema SQL:
   - Trong bảng điều khiển Neon, vào mục **SQL Editor**.
   - Mở tệp [`deploy/neon_schema.sql`](file:///E:/Codex/Projects/Moly-Viet/deploy/neon_schema.sql) trong dự án, sao chép toàn bộ nội dung và dán vào SQL Editor rồi bấm **Run**.
   - Lệnh này sẽ tự động tạo bảng `moly_users`, các index và tạo sẵn tài khoản `Moly Admin` (`10000001`, VIP 8, 999.999 Đậu Vàng).
4. Lấy chuỗi kết nối **Connection String**:
   - Chọn tab **Dashboard** -> Mục **Connection Details** -> Chọn chuỗi dạng `Connection String`:
     ```
     postgres://moly_owner:mat_khau_cua_ban@ep-xyz-pooler.ap-southeast-1.neon.tech/neondb?sslmode=require
     ```

---

### Bước 2: Đẩy Mã Nguồn Lên GitHub & Phát Hành Tải Về
1. Tạo một repository mới trên GitHub ở chế độ **Private**: `Moly-Viet`.
2. Khởi tạo Git và đẩy mã nguồn từ thư mục dự án lên GitHub:
   ```bash
   git init
   git add .
   git commit -m "feat: complete Moly Viet Tri-Play cloud architecture"
   git branch -M main
   git remote add origin https://github.com/<tai-khoan-cua-ban>/Moly-Viet.git
   git push -u origin main
   ```
3. **Phát hành file tải về qua GitHub Releases (Khuyên dùng)**:
   - Vào repository trên GitHub -> Mục **Releases** -> **Draft a new release**.
   - Đặt tag: `v1.0.0`, tiêu đề: `Moly - Thế Giới Chuột Chũi (Bản Chính Thức)`.
   - Tải lên 2 tệp cài đặt:
     - `Moly Thế Giới Chuột chũi.apk` (13 MB) nằm trong thư mục `web/download/`.
     - `Moly Thế Giới Chuột chũi.zip` (149 MB) nằm trong thư mục `web/download/`.
   - Nhấn **Publish release**. Người chơi có thể tải game với tốc độ băng thông cao không giới hạn từ CDN của GitHub!

---

### Bước 3: Triển Khai Máy Chủ Game Trên Render.com
1. Truy cập [render.com](https://render.com) và đăng nhập bằng tài khoản GitHub.
2. Chọn **New +** -> **Web Service**.
3. Kết nối với repository GitHub `Moly-Viet`.
4. Render sẽ tự động đọc tệp cấu hình `render.yaml` và `Dockerfile` có sẵn trong dự án:
   - **Name**: `moly-viet-game`
   - **Region**: `Singapore (Southeast Asia)`
   - **Runtime**: `Docker`
   - **Plan**: `Starter` (hoặc `Free`)
5. Vào mục **Environment Variables** trên Render, thêm biến:
   - `DATABASE_URL`: dán chuỗi kết nối Neon Postgres đã lấy ở Bước 1.
   - `PYTHONUNBUFFERED`: `1`
6. Nhấn **Create Web Service**.
   - Render sẽ tự động build image Docker và khởi động cả hai máy chủ: `moly_probe_server.py` và `capture_proxy.py`.
   - Khi hoàn tất, Render cung cấp cho bạn một domain HTTPS miễn phí:  
     `https://moly-viet-game.onrender.com`

---

### Bước 4: Cấu Hình Tên Miền & Tối Ưu Bằng Cloudflare
1. Đăng ký một tên miền bạn mong muốn (ví dụ: `molyviet.vn` tại iNET/P.A Việt Nam, hoặc `moly.games` tại Namecheap/Cloudflare Registrar).
2. Thêm tên miền vào tài khoản Cloudflare và trỏ NameServers về Cloudflare.
3. **Cấu hình Bản Ghi DNS**:
   - **Type**: `CNAME`
   - **Name**: `@` (hoặc tên miền phụ `play`)
   - **Target**: `moly-viet-game.onrender.com`
   - **Proxy status**: Bật **Proxied** (Đám mây màu cam).
4. **Cấu hình SSL/TLS**:
   - Vào **SSL/TLS** -> Chọn chế độ **Full** hoặc **Full (strict)**.
5. **Cấu hình Tăng Tốc Cache (Edge Caching)**:
   - Vào **Caching** -> **Cache Rules** -> Chọn **Create rule**:
     - Tên rule: `Cache Game Assets`
     - Biểu thức: `URI Path ends with ".swf" or URI Path ends with ".wasm" or URI Path ends with ".png" or URI Path ends with ".xml" or URI Path ends with ".mp3"`
     - Cài đặt bộ nhớ cache:
       - **Cache Eligibility**: `Eligible for cache`
       - **Edge TTL**: `Respect origin` hoặc chọn `7 days`
   - *Lợi ích*: Toàn bộ 257 map SWF và engine Ruffle WebAssembly sẽ được lưu sẵn tại cụm máy chủ Cloudflare tại Hà Nội và TP.HCM, người chơi tại Việt Nam tải map ngay lập tức mà không tiêu tốn băng thông của máy chủ Render!
6. **Bật tính năng WebSockets**:
   - Vào **Network** -> Kiểm tra và bật công tắc **WebSockets** (đang bật mặc định).

---

## 3. Trải Nghiệm & Quản Trị Hệ Thống

Sau khi hoàn tất, hệ thống hoạt động đồng bộ trên 3 kênh:
1. **Chơi trên Web Browser**: Truy cập `https://molyviet.vn/play.html`
   - Chạy Flash mượt mà qua Ruffle WebAssembly kết nối WebSocket WSS an toàn.
2. **Chơi trên Android (Điện thoại/Máy tính bảng)**: Tải tệp `.apk`
   - Tự động full màn hình ngang, đồ họa rõ nét, vuốt chạm điều khiển chu đáo.
3. **Chơi trên Máy tính Desktop PC**: Tải tệp `.zip`
   - Chạy `Chơi Game.bat`, nạp 257 map ngay từ ổ đĩa máy tính, 60 FPS không giật lag.
4. **Bảng Điều Khiển Quản Trị Trực Tuyến (Admin Web Dashboard)**:
   - Truy cập `https://molyviet.vn/admin`
   - Đăng nhập bảo mật bằng ID Quản trị viên `10000001`.
   - Xem thống kê số người chơi trực tuyến (CCU) theo thời gian thực, tổng số tài khoản đăng ký.
   - Thao tác nhanh 1-chạm: Cộng 100.000 Đậu Vàng, kích hoạt VIP 8 trọn đời, mở full nghề nghiệp SMC (Hiệp sĩ, Cảnh sát, HDV, Nhà báo), kích hoạt Siêu Lamu Cấp 5.
   - Phát sóng thông báo khẩn cấp chạy chữ toàn server cho tất cả người chơi.
5. **Tài khoản Quản Trị Cấp Cao**:
   - Tên tài khoản / ID: `10000001` (VIP cấp 8, 999.999 Đậu Vàng, Siêu Lamu Thần Thoại).
   - Dữ liệu tài khoản của người chơi tự động lưu trữ an toàn trên Neon PostgreSQL (hoặc file accounts.json độc lập).
