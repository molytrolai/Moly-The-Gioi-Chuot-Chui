# Kiểm kê Moly Việt — 09/10/2026

## Bản đã lưu trên ổ E

| Thành phần | Nguồn | Bản lưu | Tình trạng |
|---|---|---|---|
| Server Flash cũ | [moleworld-dev/taomee-server-leak](https://github.com/moleworld-dev/taomee-server-leak) | `archive/source/taomee-server-leak-full` | Git đầy đủ, 10.215 file theo dõi, commit `3778de747a8a100c1ed4b1adfe22b5c3315f1d83`; đã fetch cả `chenbk85/taomee` vào remote `upstream`. Chỉ là server tham khảo, không chạy game trọn vẹn. |
| Vỏ client Ruffle | [moleworld-dev/MoleRuffle](https://github.com/moleworld-dev/MoleRuffle) | `archive/source/MoleRuffle` | Git đầy đủ, commit `4049280c878528731020e0c10ff0ca0e1e05c040`; mã vỏ chạy client chính thức Trung Quốc, **không chứa tài nguyên game**. |
| Client Trung Quốc | [Taomee](http://mole.61.com/Client.swf) | `archive/clients/2026-10-09/china/Client.swf` | 20.695 byte; SHA-256 `d371936cd83ac721441fb5e0c3073bfc634a20523a56c80af65144c092c0ae44`. |
| Client Đài Loan | [Taiwan Taomee](https://mole.61.com.tw/Client.swf) | `archive/clients/2026-10-09/taiwan/Client.swf` | 20.673 byte; SHA-256 `180b5e1988465d78fb692f5f8d580012df0d4dca1a1a98d1718d27e5cc0b3698`. |

Hai `Client.swf` trên là **bộ nạp nhỏ**, không phải toàn bộ hình ảnh/âm thanh/nhiệm vụ. Chưa có client Moly/Zing Việt Nam 2011–2012 được xác thực. Không lấy tài nguyên sau đăng nhập hay chạy file không rõ nguồn.

`updates/2026-10-09T06-48-32.4809859Z` là lần kiểm thử đầu tiên (hai SWF đầu vào). `updates/2026-10-09T06-53-09.1080649Z` lưu **28 tệp khởi động công khai** của hai vùng (20 SWF, khoảng 17 MB), gồm cấu hình phiên bản/server, màn đăng nhập, tài nguyên UI và 5 thư viện SWF mỗi vùng. Cả 28 SHA-256 trong manifest đã được xác minh. Đây vẫn **chưa phải bộ asset hoàn chỉnh**.

Chạy `tools/Update-Archive.ps1` thủ công khi muốn lấy snapshot mới. Nó chỉ `git fetch` và tải bộ khởi động vào thư mục mới, **không** cập nhật bản đang dùng hay khởi chạy server.

`archive/source/_incomplete-move-do-not-use` là bản chuyển dở từ ổ C, **không sử dụng**. Bản đầy đủ được xác minh là `taomee-server-leak-full`.

## Tình trạng dịch vụ theo nguồn chính thức

- [Taomee Đài Loan đăng thông báo cập nhật 09/10/2026](https://www.61.com.tw/molemain/news/more/MA__) và [trang game](https://molemain.61.com.tw/) vẫn có đường đăng nhập: **không phải chỉ còn bản lậu**.
- [Danh mục game chính thức của Taomee Trung Quốc](https://game.61.com/) vẫn liệt kê bản web 摩尔庄园; trang `http://mole.61.com/` và `Client.swf` trả HTTP 200 khi kiểm tra. Chưa đăng nhập để xác minh toàn bộ gameplay.
- Bản Moly/Zing Việt Nam cũ [được báo ngừng hoạt động ngày 26/12/2012](https://gamelandvn.com/vuong-quoc-chuot-chui-chia-tay-game-thu-viet/). Các bản mobile về sau là sản phẩm khác, không thay thế client Flash cũ.
- [moleworld.net](https://www.moleworld.net/) là server cộng đồng (ghi “2016 classic”), **không phải** server Taomee chính thức hay bản Moly/Zing 2011.

## Máy chủ cục bộ

`runtime/` và `data/` đã dành cho máy chủ cục bộ trên **máy tính này, ổ E**, nhưng chưa khởi chạy game. Build thử trước đó cho thấy thiếu `libtaomee/dirtyword/dirtyword.h`; kho cũng thiếu toàn bộ client SWF và dữ liệu thế giới đầy đủ. Không mở cổng Internet hay cài dịch vụ tự khởi động. Bước kỹ thuật tiếp theo là chứng minh một client cụ thể có thể nói chuyện với server phục dựng, rồi mới triển khai Việt hóa nội dung.

`runtime/client` là worktree riêng của MoleRuffle. Đã thêm `MOLY_DATA_ROOT` để cache và Flash SharedObjects trỏ về `data/client` trên E; `tools/Build-Client.ps1` đặt Cargo/Rustup/target trên E. Chưa biên dịch do máy chưa có Rust/Cargo, nên chưa xác minh bản client tùy chỉnh bằng chạy thực tế. Không chạy bản upstream nguyên gốc vì mặc định nó lưu cache vào AppData trên C.

Mã nguồn server là bản rò rỉ, không thấy giấy phép sử dụng công khai cho tài nguyên game. Cần làm rõ quyền với chủ sở hữu trước khi phát hành một bản Việt hóa cho cộng đồng.
