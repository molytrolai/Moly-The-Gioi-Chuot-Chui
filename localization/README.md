# Bản địa hóa tiếng Việt

Không dịch trực tiếp trong các bản gốc bất biến tại `archive/clients/captured-live/objects`. Nguồn dịch SWF nằm trong `localization/vi/swf`; bản đã biên dịch và XML Việt hóa được proxy phục vụ từ `archive/clients/local-overrides`.

Thuật ngữ có bằng chứng ban đầu:

| Trung Quốc / Đài Loan | Tiếng Việt dùng tạm | Nguồn / ghi chú |
|---|---|---|
| 摩尔庄园 / 摩爾莊園 | Vương Quốc Chuột Chũi | Tên game VNG thời 2011–2012; không phải tên của bản mobile mới. |
| 摩尔 / 摩爾 | Moly | [Bài giới thiệu thời phát hành](https://vtcnews.vn/vuong-quoc-chuot-chui-chinh-thuc-mo-cua-don-gamer-ar55882.html) gọi nhân vật là Moly. |
| 拉姆 / 拉姆 | Đậu Đậu | Cùng bài giới thiệu gọi pet là Đậu Đậu; cần đối chiếu trong màn chơi trước khi dùng hàng loạt. |

Chưa có cache/client bản Việt gốc, nên các tên nhiệm vụ, bản đồ, vật phẩm và thoại NPC cần được xác minh qua tư liệu thời đó. Không ghi đè SWF gốc một cách hàng loạt.

## Trạng thái hiện tại

- XML bản đồ `1`, `2`, `3`, `4`, `5`, `15`, `17`, `19`, `20`, `21`, `28`, `38`, `61`, `62`, `75`, `120`, `142`, `143`: đã Việt hóa các NPC, hội thoại và chỉ dẫn chính đang hoạt động. Map 62 giữ bản vá cổng thoát tương thích Ruffle; map 17 dùng SWF Đài Loan 2016 có cửa về map 1; map 19 dùng XML rỗng chuẩn từ kho cộng đồng.
- Danh sách NPC chung đã dịch các tên thường gặp trên những tuyến này. Các giá trị `Face="正常"` còn chữ Trung Quốc là mã trạng thái khuôn mặt của client, không phải nội dung hiển thị và không được đổi tùy tiện.
- Map 2 đã bỏ các điểm bấm quảng bá/phim/sự kiện cũ không còn liên quan khỏi lớp đang chạy, nhưng bản gốc vẫn được giữ nguyên trong kho SHA-256.
- `MoleShop.swf`: đã dịch các danh mục, trợ giúp, số lượng, điểm và Đậu Vàng. Nội dung nạp tiền được thay bằng thông báo bản thử nghiệm miễn phí. Bản biên dịch đã được xuất ngược để xác minh và proxy đã phục vụ đúng SHA-256.
- `BubbleMainB2.swf`: đã dịch tiêu đề Nữ hoàng Alina và thông báo bong bóng nổ; một số chữ hoạt họa dùng font nhúng chỉ có ký tự Trung Quốc nên tạm giữ nguyên để không làm mất hình.
- Hội thoại NPC chạy qua XML; vì vậy không cần sửa mã `NPCDialogPanel.swf` cho phần thoại chính.

Mọi thay đổi Việt hóa mới phải qua ba bước: kiểm tra XML/SWF hợp lệ, xuất ngược nội dung để xác minh, rồi thử đường dẫn qua proxy cục bộ.
