# Kiểm tra mã nguồn Moly / 摩尔庄园 (2026-10-09)

> Bản lưu chính hiện nay: `E:\Codex\Projects\Moly-Viet\archive\source\taomee-server-leak-full`. Các đường dẫn ổ C ở phần ghi chép gốc là môi trường thử tạm trước khi chuyển dự án sang E, không phải vị trí vận hành.

## Kết luận

Kho [moleworld-dev/taomee-server-leak](https://github.com/moleworld-dev/taomee-server-leak) chứa mã server của game Flash **摩尔庄园**, cùng dòng game với **Moly – Thế Giới Chuột Chũi**. Các chức năng trong `mole/online` và nhật ký thay đổi 2009–2010 phù hợp giai đoạn game cũ. Tuy nhiên **không thể chạy game từ kho này như một dự án hoàn chỉnh**: thiếu client Flash, dữ liệu game/cơ sở dữ liệu đầy đủ và một số phụ thuộc mã nguồn.

Kho đã được clone tại `C:\Users\Admin\Documents\Codex\2026-10-09\to\work\taomee-server-leak`, commit `3778de7`. Không chỉnh sửa mã gốc.

## Những gì đã kiểm tra thực tế

- Quét toàn kho: **0** file `.swf`, `.fla`, `.as`; **151** file XML cấu hình trong `mole/online/conf`; **0** file tên `dirtyword.h`.
- Do cài WSL cần quyền quản trị và hộp thoại UAC đã bị hủy, phép thử build được thực hiện trong máy ảo Linux tạm bằng QEMU, Debian Bookworm/glibc 2.36 và GCC 12. Không cài WSL hay thay đổi cấu hình Windows.
- `make -C mole/flashpolicy` dừng ở `benchapi.h: No such file or directory`. File này có trong cây `c/library/serverbench/...`; khi cấp đúng đường dẫn include, `service.c` biên dịch được. Liên kết `.so` còn cần `-fPIC`; sau khi thêm cờ này, `libflashpolicy.so` tạo thành công thủ công. Đây chỉ là dịch vụ Flash socket policy, **không phải game**.
- `make -C mole/online` dừng ở `libtaomee/log.h: No such file or directory`. Gói `Libtaomee-0.7.5.tar.gz` có header đó nhưng Makefile chưa dựng/cài thư viện. Sau khi giải nén thư viện và cấp include path để biên dịch riêng `main.c`, lỗi kế tiếp là `libtaomee/dirtyword/dirtyword.h: No such file or directory`; file này không có trong toàn bộ kho. Bởi vậy phần online chính chưa build được.
- README của kho cũng xác nhận không có client Flash và không có dữ liệu thế giới/người chơi đầy đủ. Không có màn chơi nào được chạy từ mã nguồn này.

## Hướng đi hợp lý nếu muốn Việt hóa

1. Dùng kho server này làm tài liệu tham chiếu về giao thức, nhiệm vụ, vật phẩm và 151 XML cấu hình; **không coi là bộ game chơi ngay**.
2. Xác định phiên bản client Flash phù hợp thời Moly Việt Nam, hoặc một client Trung Quốc có quyền sử dụng; đối chiếu hình ảnh/giao thức trước khi đầu tư dịch thuật. [MoleRuffle](https://github.com/moleworld-dev/MoleRuffle) là vỏ chạy client Trung Quốc từ máy chủ chính thức, không kèm tài nguyên game. [Bản demo online của cộng đồng](https://www.moleworld.net/) là một hệ khác (ghi là “2016 classic”), không chứng minh bản 2011 đã phục dựng.
3. Nếu hướng tới server riêng, cần dựng lại phụ thuộc còn thiếu, xác thực/đăng nhập, dữ liệu MySQL khởi tạo và kiểm thử tương thích client. Đây là dự án phục dựng đáng kể, không phải chỉ chạy `make`.
4. Kiểm tra quyền sử dụng mã nguồn rò rỉ và tài nguyên game trước khi phát hành một bản dịch công khai.

**Trạng thái:** xác nhận đúng dòng game; chưa chạy được game từ kho này; chưa tiến hành Việt hóa.
