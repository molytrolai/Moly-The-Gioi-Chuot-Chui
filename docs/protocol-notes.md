# Ghi chú giao thức client Moly 2013

## Hai giai đoạn đăng nhập

Client dùng đầu gói big-endian 17 byte ở cả máy chủ thư mục (cổng 1863) và máy chủ thế giới (cổng 3200):

1. `length` — `uint32`
2. `version` — `uint8`
3. `command` — `uint32`
4. `user_id` — `uint32`
5. `result` — `uint32`

Các lệnh thư mục đã xác định từ `Login.swf`:

- `103`: đăng nhập tài khoản, phản hồi thành công chứa cờ `uint32 = 0` và session 16 byte.
- `105`: danh sách máy chủ đề xuất.
- `106`: toàn bộ danh sách máy chủ.

Sau khi chọn máy chủ, client kết nối cổng 3200 và gửi lệnh `201`. Cấu trúc này khớp mã `PROTO_LOGIN = 201` trong kho server cũ.

## Mã hóa thân gói thế giới

`TaomeeCoreDLL.swf` chứa `com.fcc.MEncrypt/MDecrypt`. Thuật toán đã được phục hồi trong `tools/moly_probe_server.py`:

- XOR dữ liệu với chu kỳ khóa gốc `^FStx,wl6NquAVRF@f%6`, có byte kết thúc chuỗi và byte đầu được lặp theo đúng mã native.
- Dịch luồng bit trái 5 bit; dữ liệu mã hóa dài hơn dữ liệu rõ đúng 1 byte.
- Đầu gói 17 byte không mã hóa.

Kiểm thử vòng `decrypt(encrypt(data)) == data` đã đạt với dữ liệu rỗng, một byte và đủ 256 giá trị byte.

## Phản hồi lệnh 201

`ClientSocketDLL.swf` chứa `LoginOnlineSreRes`, đọc thân phản hồi theo thứ tự: ID, tên 16 byte, thông tin mời, màu/VIP/kiểu nhân vật, thuộc tính, bản đồ, trạng thái/hành động/vị trí, số lần đăng nhập, nhiệm vụ, VIP, rồng, thời gian còn lại, 32 byte hoạt động và danh sách vật phẩm khởi đầu.

Bộ server thử hiện tạo hồ sơ tối thiểu 215 byte trước mã hóa, nhân vật `Moly Viet`, bản đồ `1`, không VIP, không rồng và không vật phẩm. Đây là hồ sơ thử tạm thời để khám phá các gói kế tiếp, chưa phải mô hình dữ liệu server hoàn chỉnh.

## Chuyển bản đồ và phản hồi tối thiểu

Chuỗi đổi map đã được xác nhận từ client và log thật:

1. `402`: rời map cũ; phản hồi gồm số người rời và ID người chơi cục bộ.
2. `401`: vào map mới; yêu cầu chứa map mới/loại map, map cũ/loại map và hai trường grid. Phản hồi là bản ghi người chơi 219 byte.
3. `406`: lấy thông tin map; phản hồi phải lặp lại đúng map ID và map type đang yêu cầu.
4. `405`: lấy danh sách người chơi trong cảnh; bản thử trả một người chơi cục bộ.

Sau khi bổ sung chuỗi này, client đã đi qua các map `1`, `4`, `61` và `62`. Map 62 dùng một vùng chạm AS3 trong suốt cho cửa về map 61; Ruffle không phát hiện ổn định vùng này. Bản XML override đăng ký `buttonLevel.door_1` qua hệ trigger chuẩn tại vị trí `(102,357)` để bảo đảm có đường ra mà không sửa tài nguyên gốc đã lưu.

Các phản hồi rỗng an toàn hiện còn bao gồm truy vấn số vật phẩm (`511`), vật phẩm ngẫu nhiên (`317`), trứng kỹ năng trong map (`1408`), khởi tạo sổ bài hiệp sĩ (`3000`), đổi vật phẩm cũ (`1243`) và giá trị giới hạn hoạt động (`11120`).
