# Ma trận kiểm thử Moly Việt

Cập nhật: 13/10/2026. Trạng thái phục dựng thực tế và kiểm thử tự động toàn diện trên ổ E.

| Khu vực | Trạng thái | Bằng chứng / Chi tiết kỹ thuật |
|---|---|---|
| Hệ thống tài khoản độc lập | Đạt (100%) | `tools/account_system.py` thread-safe (`threading.RLock`), lưu trữ cục bộ tại `data/server/accounts.json`, tự sinh ID từ `10000002`, bảo lưu vĩnh viễn tài khoản `Moly Admin` (`10000001`). Hỗ trợ công cụ quản trị CLI `tools/manage_accounts.py`. |
| Đăng nhập Google (OAuth / OIDC) | Đạt (100%) | Tích hợp OpenID Connect (`/auth/google/login`, `/auth/google/callback`) cấu hình tại `data/server/oauth_config.json`, tự động liên kết hoặc tạo tài khoản Moly tương ứng. Đã kiểm thử luồng xác thực và sinh trang xác nhận HTML tiếng Việt. |
| Đăng ký trong game (Flash Client) | Đạt (100%) | Proxy `tools/capture_proxy.py` mô phỏng `account-httpd.61.com`: sinh mã xác nhận ảnh PNG qua Pillow (`cmd=1101`), xử lý đăng ký tài khoản mới (`cmd=1102`), tạo tài khoản thật vào `accounts.json` và trả về JSON chuẩn cho client Flash hiển thị thông báo thành công. |
| Xác thực đăng nhập Probe Server | Đạt (100%) | Máy chủ thư mục (cổng 1863) xử lý lệnh `cmd 103`: xác thực băm mật khẩu `MD5(MD5(password))`, cho phép đăng nhập tài khoản vừa tạo và đăng nhập bypass đối với `Moly Admin` (`10000001`), từ chối mật khẩu sai với cờ `flag=1`. |
| Hồ sơ Admin & VIP | Đạt (100%) | Tài khoản `10000001` duy trì VIP cấp 8, cờ VIP 33, hạn VIP năm 2100, 999.999 Đậu Vàng, Kỵ sĩ nguyên tố cấp 40 (tài năng 40, chỉ số 9999). Lệnh `10303` trả về 27.000 ngày VIP; lệnh `8990` trả hồ sơ Kỵ sĩ nguyên tố chuẩn xác. |
| Chặn quảng cáo & liên kết ngoài | Đạt (100%) | Chặn triệt để 25 tên miền quảng cáo, theo dõi, diễn đàn và thanh toán Trung Quốc (`newmisc.taomee.com`, `g.cn.miaozhen.com`, `ad.61.com`, `stat.61.com`, `pay.61.com`, `bbs.61.com`, `kf.61.com`, v.v.). Trả về 200 rỗng với tiêu đề `X-Moly-Blocked: external-content` và `X-Moly-Source: blocked`, không rò rỉ dữ liệu ngoài. |
| Kiểm kê 257 Bản đồ & Tài nguyên | Đạt (100%) | Kiểm tra qua `tools/audit_map_portals.py`: đủ 257/257 bản đồ có cả SWF và XML (0 tài nguyên thiếu). Toàn bộ được phục vụ cục bộ từ `local-overrides` và `offline-mirror` trên ổ E. |
| Cổng dịch chuyển & Lộ trình map | Đạt (100%) | Đã bổ sung các cổng thoát tương thích Ruffle và đường về cho tất cả các bản đồ nội thất / phụ: Map 18 (Nhà thờ), Map 32 (Thư viện), Map 17 (Nhà hàng), Map 20 (Thời trang), Map 21 (Tiệm Cầu Vồng), Map 75 (Sở Cứu hỏa), Map 142 (Đầm Trứng), Map 143 (Sở Xây dựng), Map 19 (Đạo cụ), Map 76 (Quà tặng), Map 63 (Trại Kỵ sĩ), Map 64 (Đấu trường). Xác minh 36 chu trình dịch chuyển hai chiều thành công. |
| Việt hóa giao diện, map & NPC | Đạt (Giai đoạn 1) | 22 bản đồ trọng yếu có lớp XML tiếng Việt, dịch tên các NPC (Chị Cầu Vồng, Kulo, Tommy, Frank, Thầy Claus, Hoàng tử Jack, Đầu bếp Nick, Cô Hoa, v.v.), hội thoại và gợi ý cửa thoát. Các module SWF trọng điểm (`MoleShop.swf`, `BubbleMainB2.swf`) đã được Việt hóa và xác minh. |
| Bộ kiểm thử tự động toàn diện | Đạt (100%) | `tools/test_full_system.py` thực hiện chuỗi 8 bước kiểm thử tự động từ khởi động dịch vụ, đăng ký, đăng nhập thư mục, đồng bộ thế giới (cmd 201, 10301, 406, 10303, 8990), duyệt đồ thị map đến xác minh tài nguyên ngoại tuyến, đạt 100% OK. |

## Các tuyến di chuyển đã kiểm chứng hai chiều

- **Trục trung tâm lâu đài**: `Map 1 (Lâu đài) ⇄ Map 4 (Núi Moly)`
- **Tuyến tiền đồn kỵ sĩ**: `Map 4 ⇄ Map 61 (Tiền đồn) ⇄ Map 62 (Tháp canh Frank)`
- **Doanh trại kỵ sĩ mở rộng**: `Map 61 ⇄ Map 63 (Trại Kỵ sĩ)`, `Map 61 ⇄ Map 64 (Đấu trường)`
- **Tuyến phố mua sắm**: `Map 1 ⇄ Map 3 (Đường Phố Taomee) ⇄ Map 20 (Cửa hàng thời trang Xiso)`
- **Tuyến dịch vụ thương mại**: `Map 3 ⇄ Map 21 (Tiệm thú cưng Chị Cầu Vồng)`, `Map 3 ⇄ Map 19 (Cửa hàng đạo cụ) ⇄ Map 76 (Cửa hàng quà tặng)`
- **Tuyến công trình & khám phá**: `Map 3 ⇄ Map 142 (Đại lộ Miller / Đầm Trứng)`, `Map 4 ⇄ Map 143 (Sở Xây dựng Tommy)`, `Map 4 ⇄ Map 75 (Sở Cứu hỏa Kulo)`
- **Tuyến hoàng gia & tín ngưỡng**: `Map 1 ⇄ Map 2 (Quảng trường Tình Yêu) ⇄ Map 18 (Nhà thờ Claus)`, `Map 1 ⇄ Map 32 (Thư viện Hoàng gia Jack)`, `Map 1 ⇄ Map 17 (Nhà hàng Nick)`, `Map 1 ⇄ Map 15 (Quảng trường Lâu đài)`
