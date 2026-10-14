# TỆP TỔNG HỢP RÀ SOÁT & ĐỀ XUẤT CẢI TẠO CÂU HỎI MINIGAME MOLY-VIET

> **Dự án:** Moly-Viet (Thế Giới Chuột Chũi - Moly / Mole Manor)
> **Mục đích:** Rà soát toàn diện kho câu hỏi minigame, trắc nghiệm và lớp học SMC lấy từ phiên bản Trung Quốc; phát hiện các nội dung sai lệch về chủ quyền, địa lý, số điện thoại khẩn cấp, lịch sử và đố chữ Hán; lập danh sách đối chiếu chi tiết [Câu hỏi cũ - Đáp án cũ - Lý do - Câu hỏi đề xuất mới - Đáp án mới] để người dùng duyệt trước khi cập nhật chính thức vào hệ thống.

## 1. THỐNG KÊ TỔNG QUAN THEO NHÓM NỘI DUNG

- **Tổng số câu hỏi được rà soát:** 1.098 câu hỏi trên 3 kho dữ liệu gốc (`gamesvr/conf/questions.xml`, `online/conf/class_questions.xml`, `XMLInfo_kfcQuestion.bin`).
- **Tổng số câu hỏi phát hiện cần thay thế/sửa đổi:** **252 câu hỏi**.

| Nhóm Phân Loại | Số Lượng | Mức Độ Rủi Ro | Hướng Xử Lý & Giá Trị Đề Xuất |
| :--- | :---: | :---: | :--- |
| **Chủ quyền & Địa chính trị** | **2** câu | Cực kỳ cao | Loại bỏ hoàn toàn; thay bằng khẳng định chủ quyền Hoàng Sa, Trường Sa, Biển Đông. |
| **Số điện thoại khẩn cấp** | **7** câu | Cao (Nguy hiểm) | Sửa 110, 119 thành 113 (Cảnh sát), 114 (Cứu hỏa PCCC), 115 (Cấp cứu) chuẩn Việt Nam. |
| **Tuyên truyền quốc gia 'Nước ta'** | **129** câu | Cần chuẩn hóa | Thay các biểu tượng/ngày lễ Trung Quốc bằng Địa lý 63 tỉnh thành, Danh lam UNESCO, Lịch sử và Văn hóa Việt Nam. |
| **Đố chữ Hán & Chiết tự** | **104** câu | Không phù hợp | Thay toàn bộ đố nét chữ tượng hình bằng Câu đố dân gian, đố mẹo thông minh, toán tư duy logic học đường. |
| **Lịch sử phong kiến Trung Quốc** | **10** câu | Cần thay thế | Thay các triều đại TQ bằng trang sử vàng dựng nước và giữ nước oai hùng của dân tộc Việt Nam. |

---

## 2. BẢNG CHI TIẾT ĐỐI CHIẾU 252 CÂU HỎI [CŨ - MỚI - LÝ DO]

### Câu 1: [gamesvr_questions.xml - ID 3]
- **Phân loại vi phạm:** `Số điện thoại khẩn cấp` (Mức độ: **Cao (Nguy hiểm an toàn)** - Từ khóa phát hiện: *'急救'*)
- **Lý do cần sửa:** Sử dụng các số điện thoại khẩn cấp của Trung Quốc (110 công an, 119 cứu hỏa) gây hiểu lầm nguy hiểm trong đời sống tại Việt Nam.
- **Câu hỏi cũ (Tiếng Trung):** `地震发生后不应该做的是哪件事情呢？`
- **Lựa chọn cũ:** A: `保持镇定，从容进行分析你的具体情况` | B: `帮助受伤的人，必要时给予急救` | C: `检查火源,如可能就立即把火扑灭` | D: `触摸电力线或与其连接的物体` (Đáp án cũ: `4`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Khi phát hiện có hỏa hoạn hoặc đám cháy nguy hiểm, số điện thoại khẩn cấp gọi lực lượng Cứu hỏa tại Việt Nam là gì?**
- **👉 Lựa chọn mới:**
  - **A.** 113
  - **B.** 114
  - **C.** 115
  - **D.** 111
- **👉 Đáp án đúng mới:** **Lựa chọn 2** (114)
- **Giá trị giáo dục / Định hướng tư duy:** *Kỹ năng an toàn PCCC - Ghi nhớ tổng đài cứu hỏa 114 tại Việt Nam*

### Câu 2: [gamesvr_questions.xml - ID 14]
- **Phân loại vi phạm:** `Tuyên truyền quốc gia 'Nước ta'` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'中国'*)
- **Lý do cần sửa:** Dùng cụm từ 'nước ta' ('我国') để nhồi nhét biểu tượng, ngày lễ, thủ đô, chính sách của Trung Quốc cho người chơi Việt Nam.
- **Câu hỏi cũ (Tiếng Trung):** `下列哪个国家不是联合国常任理事国之一？`
- **Lựa chọn cũ:** A: `英国` | B: `法国` | C: `中国` | D: `德国` (Đáp án cũ: `4`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Thủ đô của nước Cộng hòa Xã hội Chủ nghĩa Việt Nam là thành phố nào?**
- **👉 Lựa chọn mới:**
  - **A.** Hà Nội
  - **B.** Hải Phòng
  - **C.** Đà Nẵng
  - **D.** TP. Hồ Chí Minh
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Hà Nội)
- **Giá trị giáo dục / Định hướng tư duy:** *Địa lý hành chính - Nhận biết Thủ đô trái tim của cả nước*

### Câu 3: [gamesvr_questions.xml - ID 16]
- **Phân loại vi phạm:** `Tuyên truyền quốc gia 'Nước ta'` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'我国'*)
- **Lý do cần sửa:** Dùng cụm từ 'nước ta' ('我国') để nhồi nhét biểu tượng, ngày lễ, thủ đô, chính sách của Trung Quốc cho người chơi Việt Nam.
- **Câu hỏi cũ (Tiếng Trung):** `我国最早发现的纸币是哪个时期的？`
- **Lựa chọn cũ:** A: `唐朝` | B: `宋朝` | C: `元朝` | D: `明朝` (Đáp án cũ: `2`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Đỉnh núi nào được mệnh danh là 'Nóc nhà của Đông Dương' nằm tại Việt Nam?**
- **👉 Lựa chọn mới:**
  - **A.** Đỉnh Fansipan
  - **B.** Đỉnh Bạch Mộc Lương Tử
  - **C.** Đỉnh Tây Côn Lĩnh
  - **D.** Đỉnh Ngọc Linh
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Đỉnh Fansipan)
- **Giá trị giáo dục / Định hướng tư duy:** *Địa lý tự nhiên - Đỉnh Fansipan cao 3.143m tại dãy Hoàng Liên Sơn*

### Câu 4: [gamesvr_questions.xml - ID 19]
- **Phân loại vi phạm:** `Tuyên truyền quốc gia 'Nước ta'` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'中国'*)
- **Lý do cần sửa:** Dùng cụm từ 'nước ta' ('我国') để nhồi nhét biểu tượng, ngày lễ, thủ đô, chính sách của Trung Quốc cho người chơi Việt Nam.
- **Câu hỏi cũ (Tiếng Trung):** `上海的南京路上，过往最多的是什么人？`
- **Lựa chọn cũ:** A: `上海人` | B: `行人` | C: `外国人` | D: `中国人` (Đáp án cũ: `2`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Con sông nào chảy qua Thủ đô Hà Nội mang phù sa màu mỡ bồi đắp đồng bằng Bắc Bộ?**
- **👉 Lựa chọn mới:**
  - **A.** Sông Hồng
  - **B.** Sông Cầu
  - **C.** Sông Đáy
  - **D.** Sông Đuống
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Sông Hồng)
- **Giá trị giáo dục / Định hướng tư duy:** *Sông ngòi Việt Nam - Dòng sông Hồng lịch sử*

### Câu 5: [gamesvr_questions.xml - ID 21]
- **Phân loại vi phạm:** `Chủ quyền & Địa chính trị` (Mức độ: **Cực kỳ cao (Chủ quyền)** - Từ khóa phát hiện: *'台湾'*)
- **Lý do cần sửa:** Gài cắm danh xưng đảo, biển (Nam Hải, Nam Sa, Đài Loan) vi phạm chủ quyền Việt Nam hoặc tuyên truyền lãnh thổ nước ngoài.
- **Câu hỏi cũ (Tiếng Trung):** `著名风景区九寨沟位于我国哪个省？`
- **Lựa chọn cũ:** A: `台湾` | B: `云南` | C: `广西` | D: `四川` (Đáp án cũ: `4`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Quần đảo Hoàng Sa và Quần đảo Trường Sa thuộc chủ quyền thiêng liêng của quốc gia nào?**
- **👉 Lựa chọn mới:**
  - **A.** Việt Nam
  - **B.** Philippines
  - **C.** Malaysia
  - **D.** Brunei
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Việt Nam)
- **Giá trị giáo dục / Định hướng tư duy:** *Chủ quyền biển đảo Việt Nam - Khẳng định chủ quyền thiêng liêng và toàn vẹn lãnh thổ*

### Câu 6: [gamesvr_questions.xml - ID 29]
- **Phân loại vi phạm:** `Tuyên truyền quốc gia 'Nước ta'` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'我国'*)
- **Lý do cần sửa:** Dùng cụm từ 'nước ta' ('我国') để nhồi nhét biểu tượng, ngày lễ, thủ đô, chính sách của Trung Quốc cho người chơi Việt Nam.
- **Câu hỏi cũ (Tiếng Trung):** `下列哪项不属于我国地震预报的政策？`
- **Lựa chọn cũ:** A: `预测、预防与政府行政决策相结合` | B: `鼓励预报研究与严格管理预报发布相结合` | C: `专家的科学判断与政府行政决策相结合` | D: `预测、预防与预报相结合` (Đáp án cũ: `1`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Hang động tự nhiên lớn nhất thế giới được phát hiện tại Vườn quốc gia Phong Nha - Kẻ Bàng tên là gì?**
- **👉 Lựa chọn mới:**
  - **A.** Hang Sơn Đoòng
  - **B.** Hang Én
  - **C.** Động Phong Nha
  - **D.** Động Thiên Đường
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Hang Sơn Đoòng)
- **Giá trị giáo dục / Định hướng tư duy:** *Di sản thiên nhiên - Kỳ quan Hang Sơn Đoòng Quảng Bình*

### Câu 7: [gamesvr_questions.xml - ID 30]
- **Phân loại vi phạm:** `Tuyên truyền quốc gia 'Nước ta'` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'我国'*)
- **Lý do cần sửa:** Dùng cụm từ 'nước ta' ('我国') để nhồi nhét biểu tượng, ngày lễ, thủ đô, chính sách của Trung Quốc cho người chơi Việt Nam.
- **Câu hỏi cũ (Tiếng Trung):** `我国上世纪第五个地震活跃期开始于何年？`
- **Lựa chọn cũ:** A: `1987年` | B: `1988年` | C: `1989年` | D: `1998年` (Đáp án cũ: `2`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Tỉnh nào nằm ở địa đầu cực Nam của Tổ quốc Việt Nam?**
- **👉 Lựa chọn mới:**
  - **A.** Cà Mau
  - **B.** Kiên Giang
  - **C.** Bạc Liêu
  - **D.** Sóc Trăng
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Cà Mau)
- **Giá trị giáo dục / Định hướng tư duy:** *Địa lý Việt Nam - Mũi Cà Mau cực Nam đất nước*

### Câu 8: [gamesvr_questions.xml - ID 47]
- **Phân loại vi phạm:** `Tuyên truyền quốc gia 'Nước ta'` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'我国'*)
- **Lý do cần sửa:** Dùng cụm từ 'nước ta' ('我国') để nhồi nhét biểu tượng, ngày lễ, thủ đô, chính sách của Trung Quốc cho người chơi Việt Nam.
- **Câu hỏi cũ (Tiếng Trung):** `打糕是我国哪一民族的风味食品？`
- **Lựa chọn cũ:** A: `彝族` | B: `傣族` | C: `朝鲜族` | D: `壮族` (Đáp án cũ: `3`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Cột cờ Lũng Cú - điểm cực Bắc địa đầu Tổ quốc thuộc tỉnh nào của Việt Nam?**
- **👉 Lựa chọn mới:**
  - **A.** Hà Giang
  - **B.** Cao Bằng
  - **C.** Lào Cai
  - **D.** Lạng Sơn
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Hà Giang)
- **Giá trị giáo dục / Định hướng tư duy:** *Địa lý Việt Nam - Cột cờ Lũng Cú Hà Giang*

### Câu 9: [gamesvr_questions.xml - ID 50]
- **Phân loại vi phạm:** `Chủ quyền & Địa chính trị` (Mức độ: **Cực kỳ cao (Chủ quyền)** - Từ khóa phát hiện: *'南海'*)
- **Lý do cần sửa:** Gài cắm danh xưng đảo, biển (Nam Hải, Nam Sa, Đài Loan) vi phạm chủ quyền Việt Nam hoặc tuyên truyền lãnh thổ nước ngoài.
- **Câu hỏi cũ (Tiếng Trung):** `黄河注入什么海？`
- **Lựa chọn cũ:** A: `渤海` | B: `黄海` | C: `东海` | D: `南海` (Đáp án cũ: `1`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Vùng biển nằm ở phía Đông Việt Nam, gắn liền với chủ quyền và không gian sinh tồn của dân tộc ta có tên là gì?**
- **👉 Lựa chọn mới:**
  - **A.** Biển Đỏ
  - **B.** Biển Đông
  - **C.** Biển Đen
  - **D.** Biển San Hô
- **👉 Đáp án đúng mới:** **Lựa chọn 2** (Biển Đông)
- **Giá trị giáo dục / Định hướng tư duy:** *Địa lý biển đảo Việt Nam - Nâng cao nhận thức về Biển Đông của Tổ quốc*

### Câu 10: [gamesvr_questions.xml - ID 53]
- **Phân loại vi phạm:** `Tuyên truyền quốc gia 'Nước ta'` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'我国'*)
- **Lý do cần sửa:** Dùng cụm từ 'nước ta' ('我国') để nhồi nhét biểu tượng, ngày lễ, thủ đô, chính sách của Trung Quốc cho người chơi Việt Nam.
- **Câu hỏi cũ (Tiếng Trung):** `我国卫星火箭发射基地“西昌”位于哪里？`
- **Lựa chọn cũ:** A: `西藏` | B: `新疆` | C: `四川` | D: `青海` (Đáp án cũ: `3`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Thành phố nào là trung tâm kinh tế, tài chính lớn nhất miền Nam Việt Nam?**
- **👉 Lựa chọn mới:**
  - **A.** TP. Hồ Chí Minh
  - **B.** Cần Thơ
  - **C.** Biên Hòa
  - **D.** Vũng Tàu
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (TP. Hồ Chí Minh)
- **Giá trị giáo dục / Định hướng tư duy:** *Kinh tế - Đô thị - Thành phố mang tên Bác năng động*

### Câu 11: [gamesvr_questions.xml - ID 77]
- **Phân loại vi phạm:** `Tuyên truyền quốc gia 'Nước ta'` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'我国'*)
- **Lý do cần sửa:** Dùng cụm từ 'nước ta' ('我国') để nhồi nhét biểu tượng, ngày lễ, thủ đô, chính sách của Trung Quốc cho người chơi Việt Nam.
- **Câu hỏi cũ (Tiếng Trung):** `体操比赛中有些动作以我国运动员的名字命名,其中鞍马是谁？`
- **Lựa chọn cũ:** A: `李月久` | B: `童非` | C: `李宁` | D: `李小双` (Đáp án cũ: `2`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Hồ nước ngọt tự nhiên trên núi lớn nhất của Việt Nam nằm tại tỉnh Bắc Kạn là hồ nào?**
- **👉 Lựa chọn mới:**
  - **A.** Hồ Ba Bể
  - **B.** Hồ Tây
  - **C.** Hồ Núi Cốc
  - **D.** Hồ Thác Bà
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Hồ Ba Bể)
- **Giá trị giáo dục / Định hướng tư duy:** *Danh lam thắng cảnh - Hồ Ba Bể viên ngọc xanh*

### Câu 12: [gamesvr_questions.xml - ID 80]
- **Phân loại vi phạm:** `Tuyên truyền quốc gia 'Nước ta'` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'我国'*)
- **Lý do cần sửa:** Dùng cụm từ 'nước ta' ('我国') để nhồi nhét biểu tượng, ngày lễ, thủ đô, chính sách của Trung Quốc cho người chơi Việt Nam.
- **Câu hỏi cũ (Tiếng Trung):** `“山城”是我国哪座城市的雅号？`
- **Lựa chọn cũ:** A: `洛阳` | B: `西安` | C: `重庆` | D: `福州` (Đáp án cũ: `3`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Hòn đảo có diện tích tự nhiên lớn nhất của Việt Nam được mệnh danh là 'Đảo Ngọc' là đảo nào?**
- **👉 Lựa chọn mới:**
  - **A.** Đảo Phú Quốc
  - **B.** Đảo Cát Bà
  - **C.** Đảo Côn Sơn
  - **D.** Đảo Lý Sơn
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Đảo Phú Quốc)
- **Giá trị giáo dục / Định hướng tư duy:** *Biển đảo quê hương - Thành phố đảo Phú Quốc*

### Câu 13: [gamesvr_questions.xml - ID 81]
- **Phân loại vi phạm:** `Tuyên truyền quốc gia 'Nước ta'` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'我国'*)
- **Lý do cần sửa:** Dùng cụm từ 'nước ta' ('我国') để nhồi nhét biểu tượng, ngày lễ, thủ đô, chính sách của Trung Quốc cho người chơi Việt Nam.
- **Câu hỏi cũ (Tiếng Trung):** `下列哪项不属于我国抗震救灾的基本策略？`
- **Lựa chọn cũ:** A: `实行以预防为主的救灾体制` | B: `实行以行政区域为主的组织指挥` | C: `发挥军队、民兵和各专业救灾队伍的作用` | D: `实行以军队、民兵为主的组织指挥` (Đáp án cũ: `4`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Quần thể di tích Cố đô Huế nằm ở miền nào của đất nước Việt Nam?**
- **👉 Lựa chọn mới:**
  - **A.** Miền Trung
  - **B.** Miền Bắc
  - **C.** Miền Nam
  - **D.** Tây Nguyên
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Miền Trung)
- **Giá trị giáo dục / Định hướng tư duy:** *Di sản văn hóa - Cố đô Huế trầm mặc cổ kính*

### Câu 14: [gamesvr_questions.xml - ID 83]
- **Phân loại vi phạm:** `Lịch sử & Phong kiến Trung Quốc` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'皇帝'*)
- **Lý do cần sửa:** Câu hỏi thuần về các triều đại, hoàng đế phong kiến Trung Quốc, không mang lại giá trị tư duy và không phù hợp môi trường học đường Việt Nam.
- **Câu hỏi cũ (Tiếng Trung):** `“贞观之治”是由唐朝的哪个皇帝开创的？`
- **Lựa chọn cũ:** A: `唐太宗` | B: `唐玄宗` | C: `唐高宗` | D: `唐高祖` (Đáp án cũ: `1`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Ai là vị anh hùng lãnh đạo chiến thắng Bạch Đằng năm 938, chấm dứt hơn một nghìn năm Bắc thuộc?**
- **👉 Lựa chọn mới:**
  - **A.** Ngô Quyền
  - **B.** Đinh Bộ Lĩnh
  - **C.** Lê Hoàn
  - **D.** Lý Bí
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Ngô Quyền)
- **Giá trị giáo dục / Định hướng tư duy:** *Lịch sử Việt Nam - Tôn vinh vị anh hùng mở đầu kỷ nguyên độc lập tự chủ*

### Câu 15: [gamesvr_questions.xml - ID 88]
- **Phân loại vi phạm:** `Tuyên truyền quốc gia 'Nước ta'` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'我国'*)
- **Lý do cần sửa:** Dùng cụm từ 'nước ta' ('我国') để nhồi nhét biểu tượng, ngày lễ, thủ đô, chính sách của Trung Quốc cho người chơi Việt Nam.
- **Câu hỏi cũ (Tiếng Trung):** `我国被称为“泉城”的是哪个城市？`
- **Lựa chọn cũ:** A: `济南` | B: `苏州` | C: `合肥` | D: `柳州` (Đáp án cũ: `1`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Đại công trình thủy điện lớn nhất Đông Nam Á được xây dựng trên sông Đà tại tỉnh nào của Việt Nam?**
- **👉 Lựa chọn mới:**
  - **A.** Sơn La
  - **B.** Hòa Bình
  - **C.** Lai Châu
  - **D.** Điện Biên
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Sơn La)
- **Giá trị giáo dục / Định hướng tư duy:** *Năng lượng quốc gia - Thủy điện Sơn La hùng vĩ*

### Câu 16: [gamesvr_questions.xml - ID 89]
- **Phân loại vi phạm:** `Tuyên truyền quốc gia 'Nước ta'` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'我国'*)
- **Lý do cần sửa:** Dùng cụm từ 'nước ta' ('我国') để nhồi nhét biểu tượng, ngày lễ, thủ đô, chính sách của Trung Quốc cho người chơi Việt Nam.
- **Câu hỏi cũ (Tiếng Trung):** `我国有一个专门进行核试验的“原子城”，它位于哪里？`
- **Lựa chọn cũ:** A: `新疆` | B: `内蒙古` | C: `青海` | D: `四川` (Đáp án cũ: `1`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Vùng đất nào ở Tây Nguyên nổi tiếng là thủ phủ cà phê của Việt Nam?**
- **👉 Lựa chọn mới:**
  - **A.** Buôn Ma Thuột (Đắk Lắk)
  - **B.** Pleiku (Gia Lai)
  - **C.** Kon Tum
  - **D.** Đà Lạt (Lâm Đồng)
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Buôn Ma Thuột (Đắk Lắk))
- **Giá trị giáo dục / Định hướng tư duy:** *Nông sản Việt Nam - Thương hiệu cà phê Buôn Ma Thuột*

### Câu 17: [gamesvr_questions.xml - ID 90]
- **Phân loại vi phạm:** `Tuyên truyền quốc gia 'Nước ta'` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'我国'*)
- **Lý do cần sửa:** Dùng cụm từ 'nước ta' ('我国') để nhồi nhét biểu tượng, ngày lễ, thủ đô, chính sách của Trung Quốc cho người chơi Việt Nam.
- **Câu hỏi cũ (Tiếng Trung):** `我国最早的神话小说是？`
- **Lựa chọn cũ:** A: `《山海经》` | B: `《古镜记》` | C: `《搜神记》` | D: `《世说新语》` (Đáp án cũ: `3`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Vịnh biển nào của Việt Nam hai lần được UNESCO vinh danh là Di sản Thiên nhiên Thế giới?**
- **👉 Lựa chọn mới:**
  - **A.** Vịnh Hạ Long
  - **B.** Vịnh Cam Ranh
  - **C.** Vịnh Xuân Đài
  - **D.** Vịnh Lăng Cô
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Vịnh Hạ Long)
- **Giá trị giáo dục / Định hướng tư duy:** *Kỳ quan thế giới - Vịnh Hạ Long ngàn đảo đá*

### Câu 18: [gamesvr_questions.xml - ID 94]
- **Phân loại vi phạm:** `Đố chữ Hán & Chiết tự` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'笔画'*)
- **Lý do cần sửa:** Đố chiết tự chữ tượng hình hoặc thành ngữ Hán ngữ cổ mà người chơi Việt Nam không thể suy luận logic.
- **Câu hỏi cũ (Tiếng Trung):** `“笑”和“哭”有什么相同之处吗？`
- **Lựa chọn cũ:** A: `没有相同之处` | B: `笔画都是10画` | C: `都会流眼泪` | D: `` (Đáp án cũ: `2`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Con gì nhỏ bé mà tha được mồi to, khi gặp nước lũ thì kết thành bè nổi?**
- **👉 Lựa chọn mới:**
  - **A.** Con kiến
  - **B.** Con voi
  - **C.** Con trâu
  - **D.** Con gấu
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Con kiến)
- **Giá trị giáo dục / Định hướng tư duy:** *Câu đố dân gian - Đố về loài kiến chăm chỉ đoàn kết*

### Câu 19: [gamesvr_questions.xml - ID 95]
- **Phân loại vi phạm:** `Đố chữ Hán & Chiết tự` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'汉字'*)
- **Lý do cần sửa:** Đố chiết tự chữ tượng hình hoặc thành ngữ Hán ngữ cổ mà người chơi Việt Nam không thể suy luận logic.
- **Câu hỏi cũ (Tiếng Trung):** `汉字“廿”表示什么？`
- **Lựa chọn cũ:** A: `这样` | B: `那样` | C: `二十` | D: `三十` (Đáp án cũ: `3`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Con gì ăn lá dâu tằm, nhả tơ óng ả dệt nên lụa là?**
- **👉 Lựa chọn mới:**
  - **A.** Con tằm
  - **B.** Con sâu róm
  - **C.** Con nhện
  - **D.** Con cuốn chiếu
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Con tằm)
- **Giá trị giáo dục / Định hướng tư duy:** *Câu đố dân gian - Đố về con tằm nhả tơ dệt lụa*

### Câu 20: [gamesvr_questions.xml - ID 101]
- **Phân loại vi phạm:** `Tuyên truyền quốc gia 'Nước ta'` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'中国'*)
- **Lý do cần sửa:** Dùng cụm từ 'nước ta' ('我国') để nhồi nhét biểu tượng, ngày lễ, thủ đô, chính sách của Trung Quốc cho người chơi Việt Nam.
- **Câu hỏi cũ (Tiếng Trung):** `亚洲第一个举办奥运会的国家是？`
- **Lựa chọn cũ:** A: `韩国` | B: `日本` | C: `新加坡` | D: `中国` (Đáp án cũ: `2`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Sông Mê Kông khi chảy vào lãnh thổ Việt Nam được chia thành 9 nhánh đổ ra biển nên gọi là dòng sông gì?**
- **👉 Lựa chọn mới:**
  - **A.** Sông Cửu Long
  - **B.** Sông Tiền
  - **C.** Sông Hậu
  - **D.** Sông Vàm Cỏ
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Sông Cửu Long)
- **Giá trị giáo dục / Định hướng tư duy:** *Địa lý miền Tây - Dòng Cửu Long chín rồng chở nặng phù sa*

### Câu 21: [gamesvr_questions.xml - ID 107]
- **Phân loại vi phạm:** `Tuyên truyền quốc gia 'Nước ta'` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'中国'*)
- **Lý do cần sửa:** Dùng cụm từ 'nước ta' ('我国') để nhồi nhét biểu tượng, ngày lễ, thủ đô, chính sách của Trung Quốc cho người chơi Việt Nam.
- **Câu hỏi cũ (Tiếng Trung):** `奥林匹克运动会的发源地是？`
- **Lựa chọn cũ:** A: `古罗马` | B: `古希腊` | C: `古代中国` | D: `古巴比伦` (Đáp án cũ: `2`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Cao nguyên nào ở tỉnh Lâm Đồng nổi tiếng với khí hậu mát mẻ quanh năm và ngàn hoa khoe sắc?**
- **👉 Lựa chọn mới:**
  - **A.** Cao nguyên Lâm Viên (Đà Lạt)
  - **B.** Cao nguyên Mộc Châu
  - **C.** Cao nguyên Đồng Văn
  - **D.** Cao nguyên Pleiku
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Cao nguyên Lâm Viên (Đà Lạt))
- **Giá trị giáo dục / Định hướng tư duy:** *Du lịch & Sinh thái - Thành phố ngàn hoa Đà Lạt*

### Câu 22: [gamesvr_questions.xml - ID 108]
- **Phân loại vi phạm:** `Tuyên truyền quốc gia 'Nước ta'` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'我国'*)
- **Lý do cần sửa:** Dùng cụm từ 'nước ta' ('我国') để nhồi nhét biểu tượng, ngày lễ, thủ đô, chính sách của Trung Quốc cho người chơi Việt Nam.
- **Câu hỏi cũ (Tiếng Trung):** `我国少数民族分布最多的省份是？`
- **Lựa chọn cũ:** A: `广西` | B: `西藏` | C: `云南` | D: `四川` (Đáp án cũ: `3`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Bãi biển nào ở miền Trung Việt Nam từng được tạp chí Forbes bình chọn là một trong những bãi biển quyến rũ nhất hành tinh?**
- **👉 Lựa chọn mới:**
  - **A.** Bãi biển Mỹ Khê (Đà Nẵng)
  - **B.** Bãi biển Sầm Sơn
  - **C.** Bãi biển Cửa Lò
  - **D.** Bãi biển Đồ Sơn
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Bãi biển Mỹ Khê (Đà Nẵng))
- **Giá trị giáo dục / Định hướng tư duy:** *Du lịch biển đảo - Bãi biển Mỹ Khê Đà Nẵng*

### Câu 23: [gamesvr_questions.xml - ID 121]
- **Phân loại vi phạm:** `Đố chữ Hán & Chiết tự` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'成语'*)
- **Lý do cần sửa:** Đố chiết tự chữ tượng hình hoặc thành ngữ Hán ngữ cổ mà người chơi Việt Nam không thể suy luận logic.
- **Câu hỏi cũ (Tiếng Trung):** `“破釜沉舟”这个成语出于哪次战争？`
- **Lựa chọn cũ:** A: `赤壁之战` | B: `长平之战` | C: `巨鹿之战` | D: `官渡之战` (Đáp án cũ: `3`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Con gì sớm sớm gáy vang 'Ò ó o' báo hiệu trời sáng gọi mọi người thức giấc?**
- **👉 Lựa chọn mới:**
  - **A.** Con gà trống
  - **B.** Con gà mái
  - **C.** Con vịt
  - **D.** Con ngỗng
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Con gà trống)
- **Giá trị giáo dục / Định hướng tư duy:** *Câu đố dân gian - Tiếng gáy quen thuộc của chú gà trống*

### Câu 24: [gamesvr_questions.xml - ID 126]
- **Phân loại vi phạm:** `Tuyên truyền quốc gia 'Nước ta'` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'我国'*)
- **Lý do cần sửa:** Dùng cụm từ 'nước ta' ('我国') để nhồi nhét biểu tượng, ngày lễ, thủ đô, chính sách của Trung Quốc cho người chơi Việt Nam.
- **Câu hỏi cũ (Tiếng Trung):** `泼水节是我国哪个少数民族的传统节日？`
- **Lựa chọn cũ:** A: `彝族` | B: `回族` | C: `壮族` | D: `傣族` (Đáp án cũ: `4`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Cây cầu quay đầu tiên tại Việt Nam bắc qua sông Hàn nằm ở thành phố nào?**
- **👉 Lựa chọn mới:**
  - **A.** Đà Nẵng
  - **B.** Hà Nội
  - **C.** Hải Phòng
  - **D.** Huế
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Đà Nẵng)
- **Giá trị giáo dục / Định hướng tư duy:** *Kiến trúc cầu đường - Cầu quay sông Hàn Đà Nẵng*

### Câu 25: [gamesvr_questions.xml - ID 129]
- **Phân loại vi phạm:** `Tuyên truyền quốc gia 'Nước ta'` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'我国'*)
- **Lý do cần sửa:** Dùng cụm từ 'nước ta' ('我国') để nhồi nhét biểu tượng, ngày lễ, thủ đô, chính sách của Trung Quốc cho người chơi Việt Nam.
- **Câu hỏi cũ (Tiếng Trung):** `我国是在哪个时期进入奴隶社会的？`
- **Lựa chọn cũ:** A: `夏` | B: `商` | C: `战国` | D: `秦` (Đáp án cũ: `1`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Cánh đồng lúa nào lớn nhất vùng Tây Bắc gắn liền với câu nói 'nhất Thanh, nhì Lò, tam Than, tứ Tấc'?**
- **👉 Lựa chọn mới:**
  - **A.** Cánh đồng Mường Thanh (Điện Biên)
  - **B.** Cánh đồng Mường Lò
  - **C.** Cánh đồng Than Uyên
  - **D.** Cánh đồng Quang Huy
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Cánh đồng Mường Thanh (Điện Biên))
- **Giá trị giáo dục / Định hướng tư duy:** *Văn hóa Tây Bắc - Cánh đồng Mường Thanh lịch sử*

### Câu 26: [gamesvr_questions.xml - ID 132]
- **Phân loại vi phạm:** `Tuyên truyền quốc gia 'Nước ta'` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'我国'*)
- **Lý do cần sửa:** Dùng cụm từ 'nước ta' ('我国') để nhồi nhét biểu tượng, ngày lễ, thủ đô, chính sách của Trung Quốc cho người chơi Việt Nam.
- **Câu hỏi cũ (Tiếng Trung):** `我国第一个南极考察基地“长城站”是什么时候落成的？`
- **Lựa chọn cũ:** A: `1980` | B: `1981` | C: `1985` | D: `1986` (Đáp án cũ: `3`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Hồ nước ngọt tự nhiên lớn nhất nằm ngay giữa lòng Thủ đô Hà Nội là hồ nào?**
- **👉 Lựa chọn mới:**
  - **A.** Hồ Tây
  - **B.** Hồ Hoàn Kiếm
  - **C.** Hồ Trúc Bạch
  - **D.** Hồ Bảy Mẫu
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Hồ Tây)
- **Giá trị giáo dục / Định hướng tư duy:** *Thắng cảnh Hà Nội - Hồ Tây ngát hương sen*

### Câu 27: [gamesvr_questions.xml - ID 133]
- **Phân loại vi phạm:** `Tuyên truyền quốc gia 'Nước ta'` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'中国'*)
- **Lý do cần sửa:** Dùng cụm từ 'nước ta' ('我国') để nhồi nhét biểu tượng, ngày lễ, thủ đô, chính sách của Trung Quốc cho người chơi Việt Nam.
- **Câu hỏi cũ (Tiếng Trung):** `飞利浦电器是哪一个国家的产品？`
- **Lựa chọn cũ:** A: `日本` | B: `荷兰` | C: `美国` | D: `中国` (Đáp án cũ: `2`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Hồ Hoàn Kiếm tại Hà Nội gắn liền với truyền thuyết lịch sử vua Lê Lợi trả gươm báu cho ai?**
- **👉 Lựa chọn mới:**
  - **A.** Rùa Vàng
  - **B.** Long Vương
  - **C.** Lạc Long Quân
  - **D.** Tiên Ông
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Rùa Vàng)
- **Giá trị giáo dục / Định hướng tư duy:** *Truyền thuyết ngàn năm - Sự tích Hồ Gươm trả gươm*

### Câu 28: [gamesvr_questions.xml - ID 150]
- **Phân loại vi phạm:** `Tuyên truyền quốc gia 'Nước ta'` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'中国'*)
- **Lý do cần sửa:** Dùng cụm từ 'nước ta' ('我国') để nhồi nhét biểu tượng, ngày lễ, thủ đô, chính sách của Trung Quốc cho người chơi Việt Nam.
- **Câu hỏi cũ (Tiếng Trung):** `下列中国象棋手哪位获全国冠军次数最多？`
- **Lựa chọn cũ:** A: `杨官璘` | B: `谢思明` | C: `胡荣华` | D: `谢侠逊` (Đáp án cũ: `3`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Hệ thống sông nào dài nhất bắt nguồn và chảy hoàn toàn trên lãnh thổ Việt Nam?**
- **👉 Lựa chọn mới:**
  - **A.** Sông Đồng Nai
  - **B.** Sông Thái Bình
  - **C.** Sông Mã
  - **D.** Sông Cả
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Sông Đồng Nai)
- **Giá trị giáo dục / Định hướng tư duy:** *Thủy văn Việt Nam - Hệ thống sông Đồng Nai*

### Câu 29: [gamesvr_questions.xml - ID 151]
- **Phân loại vi phạm:** `Tuyên truyền quốc gia 'Nước ta'` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'我国'*)
- **Lý do cần sửa:** Dùng cụm từ 'nước ta' ('我国') để nhồi nhét biểu tượng, ngày lễ, thủ đô, chính sách của Trung Quốc cho người chơi Việt Nam.
- **Câu hỏi cũ (Tiếng Trung):** `我国境内最早的人类是？`
- **Lựa chọn cũ:** A: `北京人` | B: `元谋人` | C: `山顶洞人` | D: `丁村人` (Đáp án cũ: `2`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Đèo Hải Vân nổi tiếng với danh xưng 'Thiên hạ đệ nhất hùng quan' nằm giữa ranh giới hai địa phương nào?**
- **👉 Lựa chọn mới:**
  - **A.** Thừa Thiên Huế và Đà Nẵng
  - **B.** Quảng Bình và Hà Tĩnh
  - **C.** Quảng Nam và Quảng Ngãi
  - **D.** Bình Định và Phú Yên
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Thừa Thiên Huế và Đà Nẵng)
- **Giá trị giáo dục / Định hướng tư duy:** *Danh lam đèo núi - Đèo Hải Vân kỳ vĩ*

### Câu 30: [gamesvr_questions.xml - ID 152]
- **Phân loại vi phạm:** `Lịch sử & Phong kiến Trung Quốc` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'清朝'*)
- **Lý do cần sửa:** Câu hỏi thuần về các triều đại, hoàng đế phong kiến Trung Quốc, không mang lại giá trị tư duy và không phù hợp môi trường học đường Việt Nam.
- **Câu hỏi cũ (Tiếng Trung):** `清朝晚期,被今人誉为“开眼看世界第一人”的是谁？`
- **Lựa chọn cũ:** A: `魏源` | B: `龚自珍` | C: `林则徐` | D: `严复` (Đáp án cũ: `3`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Vị vua nào đã ban hành 'Chiếu dời đô' chuyển kinh đô từ Hoa Lư về Thăng Long vào mùa thu năm 1010?**
- **👉 Lựa chọn mới:**
  - **A.** Lý Thái Tổ (Lý Công Uẩn)
  - **B.** Lý Thánh Tông
  - **C.** Lý Nhân Tông
  - **D.** Trần Thái Tông
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Lý Thái Tổ (Lý Công Uẩn))
- **Giá trị giáo dục / Định hướng tư duy:** *Lịch sử ngàn năm Thăng Long - Khởi đầu kinh đô Thăng Long Hà Nội*

### Câu 31: [gamesvr_questions.xml - ID 154]
- **Phân loại vi phạm:** `Tuyên truyền quốc gia 'Nước ta'` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'我国'*)
- **Lý do cần sửa:** Dùng cụm từ 'nước ta' ('我国') để nhồi nhét biểu tượng, ngày lễ, thủ đô, chính sách của Trung Quốc cho người chơi Việt Nam.
- **Câu hỏi cũ (Tiếng Trung):** `我国鸟类中，消灭森林害虫最多的是谁？`
- **Lựa chọn cũ:** A: `喜鹊` | B: `啄木鸟` | C: `燕子` | D: `杜鹃` (Đáp án cũ: `4`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Vườn quốc gia nào được thành lập đầu tiên tại Việt Nam vào năm 1962?**
- **👉 Lựa chọn mới:**
  - **A.** Vườn quốc gia Cúc Phương
  - **B.** Vườn quốc gia Ba Vì
  - **C.** Vườn quốc gia Cát Tiên
  - **D.** Vườn quốc gia Bạch Mã
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Vườn quốc gia Cúc Phương)
- **Giá trị giáo dục / Định hướng tư duy:** *Bảo tồn thiên nhiên - Vườn quốc gia Cúc Phương*

### Câu 32: [gamesvr_questions.xml - ID 162]
- **Phân loại vi phạm:** `Tuyên truyền quốc gia 'Nước ta'` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'中国'*)
- **Lý do cần sửa:** Dùng cụm từ 'nước ta' ('我国') để nhồi nhét biểu tượng, ngày lễ, thủ đô, chính sách của Trung Quốc cho người chơi Việt Nam.
- **Câu hỏi cũ (Tiếng Trung):** `新中国成立后,第一次参加奥运会是在哪一年？ `
- **Lựa chọn cũ:** A: `1952` | B: `1956` | C: `1980` | D: `1984` (Đáp án cũ: `1`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Thác nước tự nhiên lớn và đẹp nhất Việt Nam nằm trên biên giới Việt - Trung tại Cao Bằng tên là gì?**
- **👉 Lựa chọn mới:**
  - **A.** Thác Bản Giốc
  - **B.** Thác Cam Ly
  - **C.** Thác Pongour
  - **D.** Thác Datanla
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Thác Bản Giốc)
- **Giá trị giáo dục / Định hướng tư duy:** *Kỳ quan thác nước - Thác Bản Giốc Cao Bằng*

### Câu 33: [gamesvr_questions.xml - ID 164]
- **Phân loại vi phạm:** `Tuyên truyền quốc gia 'Nước ta'` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'中国'*)
- **Lý do cần sửa:** Dùng cụm từ 'nước ta' ('我国') để nhồi nhét biểu tượng, ngày lễ, thủ đô, chính sách của Trung Quốc cho người chơi Việt Nam.
- **Câu hỏi cũ (Tiếng Trung):** `中国面积最大的省份是哪一个？`
- **Lựa chọn cũ:** A: `四川` | B: `新疆` | C: `内蒙古` | D: `西藏` (Đáp án cũ: `2`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Rừng ngập mặn Cần Giờ - Khu dự trữ sinh quyển thế giới nằm tại địa phương nào của Việt Nam?**
- **👉 Lựa chọn mới:**
  - **A.** TP. Hồ Chí Minh
  - **B.** Đồng Nai
  - **C.** Tiền Giang
  - **D.** Bà Rịa - Vũng Tàu
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (TP. Hồ Chí Minh)
- **Giá trị giáo dục / Định hướng tư duy:** *Sinh thái học - Lá phổi xanh Cần Giờ*

### Câu 34: [gamesvr_questions.xml - ID 166]
- **Phân loại vi phạm:** `Tuyên truyền quốc gia 'Nước ta'` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'中国'*)
- **Lý do cần sửa:** Dùng cụm từ 'nước ta' ('我国') để nhồi nhét biểu tượng, ngày lễ, thủ đô, chính sách của Trung Quốc cho người chơi Việt Nam.
- **Câu hỏi cũ (Tiếng Trung):** `世界上最长的运河是哪一条？`
- **Lựa chọn cũ:** A: `中国京杭大运河` | B: `苏伊士运河` | C: `巴拿马运河` | D: `` (Đáp án cũ: `1`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Mũi Đại Lãnh (Mũi Điện) - nơi đón ánh bình minh đầu tiên trên đất liền của Việt Nam thuộc tỉnh nào?**
- **👉 Lựa chọn mới:**
  - **A.** Phú Yên
  - **B.** Khánh Hòa
  - **C.** Bình Thuận
  - **D.** Ninh Thuận
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Phú Yên)
- **Giá trị giáo dục / Định hướng tư duy:** *Địa lý cực Đông đất liền - Mũi Điện Phú Yên*

### Câu 35: [gamesvr_questions.xml - ID 167]
- **Phân loại vi phạm:** `Tuyên truyền quốc gia 'Nước ta'` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'我国'*)
- **Lý do cần sửa:** Dùng cụm từ 'nước ta' ('我国') để nhồi nhét biểu tượng, ngày lễ, thủ đô, chính sách của Trung Quốc cho người chơi Việt Nam.
- **Câu hỏi cũ (Tiếng Trung):** `我国被称为哪一类体育运动的体育王国？`
- **Lựa chọn cũ:** A: `羽毛球王国` | B: `乒乓球王国` | C: `排球王国` | D: `举重王国` (Đáp án cũ: `2`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Cột mốc ngã ba biên giới 'một tiếng gà gáy ba nước cùng nghe' (Việt Nam - Lào - Campuchia) nằm tại đâu?**
- **👉 Lựa chọn mới:**
  - **A.** Ngã ba Đông Dương (Kon Tum)
  - **B.** Tây Trang (Điện Biên)
  - **C.** Lao Bảo (Quảng Trị)
  - **D.** Bờ Y (Gia Lai)
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Ngã ba Đông Dương (Kon Tum))
- **Giá trị giáo dục / Định hướng tư duy:** *Biên cương Tổ quốc - Cửa khẩu quốc tế Bờ Y Kon Tum*

### Câu 36: [gamesvr_questions.xml - ID 168]
- **Phân loại vi phạm:** `Tuyên truyền quốc gia 'Nước ta'` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'我国'*)
- **Lý do cần sửa:** Dùng cụm từ 'nước ta' ('我国') để nhồi nhét biểu tượng, ngày lễ, thủ đô, chính sách của Trung Quốc cho người chơi Việt Nam.
- **Câu hỏi cũ (Tiếng Trung):** `“发展体育运动,增强人民体质”是我国哪位领导人的题词？`
- **Lựa chọn cũ:** A: `毛泽东` | B: `周恩来` | C: `邓小平` | D: `贺龙` (Đáp án cũ: `1`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Quần thể danh thắng Tràng An được UNESCO công nhận là di sản hỗn hợp (văn hóa và thiên nhiên) thuộc tỉnh nào?**
- **👉 Lựa chọn mới:**
  - **A.** Ninh Bình
  - **B.** Nam Định
  - **C.** Hà Nam
  - **D.** Thanh Hóa
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Ninh Bình)
- **Giá trị giáo dục / Định hướng tư duy:** *Di sản thế giới - Non nước Tràng An Ninh Bình*

### Câu 37: [gamesvr_questions.xml - ID 176]
- **Phân loại vi phạm:** `Lịch sử & Phong kiến Trung Quốc` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'皇帝'*)
- **Lý do cần sửa:** Câu hỏi thuần về các triều đại, hoàng đế phong kiến Trung Quốc, không mang lại giá trị tư duy và không phù hợp môi trường học đường Việt Nam.
- **Câu hỏi cũ (Tiếng Trung):** `下列哪位皇帝是汉朝的？`
- **Lựa chọn cũ:** A: `汉武帝` | B: `唐太宗` | C: `唐明皇` | D: `元世祖` (Đáp án cũ: `1`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Bài thơ thần 'Nam quốc sơn hà' được xem là bản Tuyên ngôn Độc lập đầu tiên của nước ta vang lên trong cuộc kháng chiến chống quân Tống của ai?**
- **👉 Lựa chọn mới:**
  - **A.** Trần Hưng Đạo
  - **B.** Lý Thường Kiệt
  - **C.** Nguyễn Trãi
  - **D.** Quang Trung
- **👉 Đáp án đúng mới:** **Lựa chọn 2** (Lý Thường Kiệt)
- **Giá trị giáo dục / Định hướng tư duy:** *Văn học & Lịch sử nước nhà - Tinh thần bất khuất bảo vệ giang sơn sông núi*

### Câu 38: [gamesvr_questions.xml - ID 179]
- **Phân loại vi phạm:** `Tuyên truyền quốc gia 'Nước ta'` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'我国'*)
- **Lý do cần sửa:** Dùng cụm từ 'nước ta' ('我国') để nhồi nhét biểu tượng, ngày lễ, thủ đô, chính sách của Trung Quốc cho người chơi Việt Nam.
- **Câu hỏi cũ (Tiếng Trung):** `跳竹杆是我国哪个少数民族的传统体育运动？`
- **Lựa chọn cũ:** A: `壮族` | B: `苗族` | C: `白族` | D: `黎族` (Đáp án cũ: `4`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Phố cổ Hội An với những mái ngói rêu phong và đèn lồng rực rỡ thuộc tỉnh nào của miền Trung?**
- **👉 Lựa chọn mới:**
  - **A.** Quảng Nam
  - **B.** Quảng Ngãi
  - **C.** Bình Định
  - **D.** Huế
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Quảng Nam)
- **Giá trị giáo dục / Định hướng tư duy:** *Di sản văn hóa - Đô thị cổ Hội An*

### Câu 39: [gamesvr_questions.xml - ID 182]
- **Phân loại vi phạm:** `Tuyên truyền quốc gia 'Nước ta'` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'我国'*)
- **Lý do cần sửa:** Dùng cụm từ 'nước ta' ('我国') để nhồi nhét biểu tượng, ngày lễ, thủ đô, chính sách của Trung Quốc cho người chơi Việt Nam.
- **Câu hỏi cũ (Tiếng Trung):** `著名古迹“秦始皇兵马俑”位于我国哪个省份？`
- **Lựa chọn cũ:** A: `湖北` | B: `湖南` | C: `河南` | D: `陕西` (Đáp án cũ: `4`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Thánh địa Mỹ Sơn - quần thể kiến trúc đền tháp Chăm Pa cổ xưa nằm tại tỉnh nào?**
- **👉 Lựa chọn mới:**
  - **A.** Quảng Nam
  - **B.** Khánh Hòa
  - **C.** Ninh Thuận
  - **D.** Bình Thuận
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Quảng Nam)
- **Giá trị giáo dục / Định hướng tư duy:** *Di sản kiến trúc - Thánh địa Mỹ Sơn*

### Câu 40: [gamesvr_questions.xml - ID 183]
- **Phân loại vi phạm:** `Tuyên truyền quốc gia 'Nước ta'` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'我国'*)
- **Lý do cần sửa:** Dùng cụm từ 'nước ta' ('我国') để nhồi nhét biểu tượng, ngày lễ, thủ đô, chính sách của Trung Quốc cho người chơi Việt Nam.
- **Câu hỏi cũ (Tiếng Trung):** `我国最早的一部医学理论著作是？`
- **Lựa chọn cũ:** A: `《本草纲目》` | B: `《黄帝内经》` | C: `《千金方》` | D: `《伤寒杂病论》` (Đáp án cũ: `2`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Hoàng thành Thăng Long - trung tâm quyền lực chính trị qua nhiều triều đại phong kiến nằm ở đâu?**
- **👉 Lựa chọn mới:**
  - **A.** Hà Nội
  - **B.** Huế
  - **C.** Ninh Bình
  - **D.** Thanh Hóa
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Hà Nội)
- **Giá trị giáo dục / Định hướng tư duy:** *Di sản ngàn năm - Hoàng thành Thăng Long*

### Câu 41: [gamesvr_questions.xml - ID 188]
- **Phân loại vi phạm:** `Tuyên truyền quốc gia 'Nước ta'` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'中国'*)
- **Lý do cần sửa:** Dùng cụm từ 'nước ta' ('我国') để nhồi nhét biểu tượng, ngày lễ, thủ đô, chính sách của Trung Quốc cho người chơi Việt Nam.
- **Câu hỏi cũ (Tiếng Trung):** `世界上是被称为“教育王国”的哪一个国家？`
- **Lựa chọn cũ:** A: `中国` | B: `美国` | C: `以色列` | D: `日本` (Đáp án cũ: `3`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Không gian văn hóa Cồng chiêng Tây Nguyên của Việt Nam được UNESCO công nhận là gì?**
- **👉 Lựa chọn mới:**
  - **A.** Kiệt tác di sản truyền khẩu và phi vật thể của nhân loại
  - **B.** Di sản thiên nhiên thế giới
  - **C.** Kỳ quan kiến trúc cổ
  - **D.** Di sản tư liệu thế giới
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Kiệt tác di sản truyền khẩu và phi vật thể của nhân loại)
- **Giá trị giáo dục / Định hướng tư duy:** *Bản sắc văn hóa - Tiếng cồng chiêng đại ngàn*

### Câu 42: [gamesvr_questions.xml - ID 194]
- **Phân loại vi phạm:** `Tuyên truyền quốc gia 'Nước ta'` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'中国'*)
- **Lý do cần sửa:** Dùng cụm từ 'nước ta' ('我国') để nhồi nhét biểu tượng, ngày lễ, thủ đô, chính sách của Trung Quốc cho người chơi Việt Nam.
- **Câu hỏi cũ (Tiếng Trung):** `最早的纸币源于哪国？`
- **Lựa chọn cũ:** A: `中国` | B: `美国` | C: `日本` | D: `法国` (Đáp án cũ: `1`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Nghệ thuật Đờn ca tài tử là nét văn hóa truyền thống đặc sắc của vùng miền nào tại Việt Nam?**
- **👉 Lựa chọn mới:**
  - **A.** Nam Bộ
  - **B.** Bắc Bộ
  - **C.** Tây Bắc
  - **D.** Duyên hải miền Trung
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Nam Bộ)
- **Giá trị giáo dục / Định hướng tư duy:** *Âm nhạc dân tộc - Đờn ca tài tử Nam Bộ*

### Câu 43: [gamesvr_questions.xml - ID 198]
- **Phân loại vi phạm:** `Tuyên truyền quốc gia 'Nước ta'` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'中国'*)
- **Lý do cần sửa:** Dùng cụm từ 'nước ta' ('我国') để nhồi nhét biểu tượng, ngày lễ, thủ đô, chính sách của Trung Quốc cho người chơi Việt Nam.
- **Câu hỏi cũ (Tiếng Trung):** `中国民间为什么要吃腊八粥？`
- **Lựa chọn cũ:** A: `迎接春节` | B: `纪念释迦牟尼` | C: `纪念小寒来临` | D: `` (Đáp án cũ: `2`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Dân ca Quan họ - làn điệu dân ca mượt mà, sâu lắng gắn liền với vùng đất nào?**
- **👉 Lựa chọn mới:**
  - **A.** Bắc Ninh - Bắc Giang (Kinh Bắc)
  - **B.** Phú Thọ
  - **C.** Hà Tây
  - **D.** Nghệ An
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Bắc Ninh - Bắc Giang (Kinh Bắc))
- **Giá trị giáo dục / Định hướng tư duy:** *Dân ca dân tộc - Quan họ Kinh Bắc mượt mà*

### Câu 44: [gamesvr_questions.xml - ID 199]
- **Phân loại vi phạm:** `Lịch sử & Phong kiến Trung Quốc` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'刘邦'*)
- **Lý do cần sửa:** Câu hỏi thuần về các triều đại, hoàng đế phong kiến Trung Quốc, không mang lại giá trị tư duy và không phù hợp môi trường học đường Việt Nam.
- **Câu hỏi cũ (Tiếng Trung):** `“成也萧何，败也萧何”说的是谁的经历？`
- **Lựa chọn cũ:** A: `刘邦` | B: `张良` | C: `韩信` | D: `项羽` (Đáp án cũ: `3`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Vị danh tướng ba lần lãnh đạo quân dân Đại Việt đánh tan quân xâm lược Nguyên Mông hung hãn là ai?**
- **👉 Lựa chọn mới:**
  - **A.** Trần Quốc Toản
  - **B.** Hưng Đạo Đại Vương Trần Quốc Tuấn
  - **C.** Trần Khánh Dư
  - **D.** Phạm Ngũ Lão
- **👉 Đáp án đúng mới:** **Lựa chọn 2** (Hưng Đạo Đại Vương Trần Quốc Tuấn)
- **Giá trị giáo dục / Định hướng tư duy:** *Hào khí Đông A - Tấm gương ái quốc vĩ đại Trần Quốc Tuấn*

### Câu 45: [gamesvr_questions.xml - ID 200]
- **Phân loại vi phạm:** `Tuyên truyền quốc gia 'Nước ta'` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'中国'*)
- **Lý do cần sửa:** Dùng cụm từ 'nước ta' ('我国') để nhồi nhét biểu tượng, ngày lễ, thủ đô, chính sách của Trung Quốc cho người chơi Việt Nam.
- **Câu hỏi cũ (Tiếng Trung):** `世界上最早种植棉花的国家是哪个？`
- **Lựa chọn cũ:** A: `中国` | B: `印度` | C: `日本` | D: `美国` (Đáp án cũ: `2`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Hát Xoan - nét sinh hoạt văn hóa tín ngưỡng độc đáo của người Việt gắn liền với vùng đất cội nguồn nào?**
- **👉 Lựa chọn mới:**
  - **A.** Phú Thọ (Đất Tổ Hùng Vương)
  - **B.** Tuyên Quang
  - **C.** Yên Bái
  - **D.** Vĩnh Phúc
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Phú Thọ (Đất Tổ Hùng Vương))
- **Giá trị giáo dục / Định hướng tư duy:** *Cội nguồn dân tộc - Hát Xoan Phú Thọ*

### Câu 46: [gamesvr_questions.xml - ID 209]
- **Phân loại vi phạm:** `Tuyên truyền quốc gia 'Nước ta'` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'我国'*)
- **Lý do cần sửa:** Dùng cụm từ 'nước ta' ('我国') để nhồi nhét biểu tượng, ngày lễ, thủ đô, chính sách của Trung Quốc cho người chơi Việt Nam.
- **Câu hỏi cũ (Tiếng Trung):** `阿诗玛是我国云南哪个民族塑造的艺术形象？`
- **Lựa chọn cũ:** A: `彝族` | B: `瑶族` | C: `白族` | D: `苗族` (Đáp án cũ: `1`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Nhã nhạc cung đình Huế là thể loại âm nhạc cung đình dưới triều đại phong kiến nào ở Việt Nam?**
- **👉 Lựa chọn mới:**
  - **A.** Triều Nguyễn
  - **B.** Triều Lê
  - **C.** Triều Lý
  - **D.** Triều Trần
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Triều Nguyễn)
- **Giá trị giáo dục / Định hướng tư duy:** *Âm nhạc bác học - Nhã nhạc cung đình triều Nguyễn*

### Câu 47: [gamesvr_questions.xml - ID 211]
- **Phân loại vi phạm:** `Tuyên truyền quốc gia 'Nước ta'` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'我国'*)
- **Lý do cần sửa:** Dùng cụm từ 'nước ta' ('我国') để nhồi nhét biểu tượng, ngày lễ, thủ đô, chính sách của Trung Quốc cho người chơi Việt Nam.
- **Câu hỏi cũ (Tiếng Trung):** `我国最著名的热水湖是哪一个？`
- **Lựa chọn cũ:** A: `西藏羊八井` | B: `新疆罗布泊` | C: `内蒙古呼伦湖` | D: `` (Đáp án cũ: `1`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Huyện đảo Lý Sơn nổi tiếng với đặc sản tỏi thơm ngon thuộc tỉnh nào của Việt Nam?**
- **👉 Lựa chọn mới:**
  - **A.** Quảng Ngãi
  - **B.** Quảng Nam
  - **C.** Bình Định
  - **D.** Phú Yên
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Quảng Ngãi)
- **Giá trị giáo dục / Định hướng tư duy:** *Nông sản biển đảo - Huyện đảo Lý Sơn quê hương hải đội*

### Câu 48: [gamesvr_questions.xml - ID 216]
- **Phân loại vi phạm:** `Tuyên truyền quốc gia 'Nước ta'` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'我国'*)
- **Lý do cần sửa:** Dùng cụm từ 'nước ta' ('我国') để nhồi nhét biểu tượng, ngày lễ, thủ đô, chính sách của Trung Quốc cho người chơi Việt Nam.
- **Câu hỏi cũ (Tiếng Trung):** `我国的“冰城”是指哪个城市？`
- **Lựa chọn cũ:** A: `吉林市` | B: `哈尔滨` | C: `辽阳市` | D: `牡丹江` (Đáp án cũ: `2`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Quần đảo Cát Bà với hàng trăm đảo đá vôi kỳ vĩ nằm trong vịnh Lan Hạ thuộc thành phố nào?**
- **👉 Lựa chọn mới:**
  - **A.** Hải Phòng
  - **B.** Quảng Ninh
  - **C.** Hải Dương
  - **D.** Thái Bình
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Hải Phòng)
- **Giá trị giáo dục / Định hướng tư duy:** *Du lịch biển đảo - Quần đảo Cát Bà Hải Phòng*

### Câu 49: [gamesvr_questions.xml - ID 219]
- **Phân loại vi phạm:** `Tuyên truyền quốc gia 'Nước ta'` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'中国'*)
- **Lý do cần sửa:** Dùng cụm từ 'nước ta' ('我国') để nhồi nhét biểu tượng, ngày lễ, thủ đô, chính sách của Trung Quốc cho người chơi Việt Nam.
- **Câu hỏi cũ (Tiếng Trung):** `世界上生产玉米最多的国家是哪个？`
- **Lựa chọn cũ:** A: `中国` | B: `日本` | C: `美国` | D: `英国` (Đáp án cũ: `3`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Đảo Côn Đảo - nơi ghi dấu lịch sử đấu tranh kiên cường của các chiến sĩ cách mạng thuộc tỉnh nào?**
- **👉 Lựa chọn mới:**
  - **A.** Bà Rịa - Vũng Tàu
  - **B.** Bình Thuận
  - **C.** Bến Tre
  - **D.** Trà Vinh
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Bà Rịa - Vũng Tàu)
- **Giá trị giáo dục / Định hướng tư duy:** *Lịch sử cách mạng - Côn Đảo anh hùng*

### Câu 50: [gamesvr_questions.xml - ID 226]
- **Phân loại vi phạm:** `Tuyên truyền quốc gia 'Nước ta'` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'我国'*)
- **Lý do cần sửa:** Dùng cụm từ 'nước ta' ('我国') để nhồi nhét biểu tượng, ngày lễ, thủ đô, chính sách của Trung Quốc cho người chơi Việt Nam.
- **Câu hỏi cũ (Tiếng Trung):** `我国最大的诗歌集是哪部？`
- **Lựa chọn cũ:** A: `诗经` | B: `楚词` | C: `全唐诗` | D: `千家诗` (Đáp án cũ: `3`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Cây cầu dây văng đầu tiên được xây dựng tại Việt Nam bắc qua sông Tiền là cầu nào?**
- **👉 Lựa chọn mới:**
  - **A.** Cầu Mỹ Thuận
  - **B.** Cầu Cần Thơ
  - **C.** Cầu Rạch Miễu
  - **D.** Cầu Bãi Cháy
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Cầu Mỹ Thuận)
- **Giá trị giáo dục / Định hướng tư duy:** *Công trình thế kỷ - Cầu Mỹ Thuận nối đôi bờ sông Tiền*

### Câu 51: [gamesvr_questions.xml - ID 229]
- **Phân loại vi phạm:** `Tuyên truyền quốc gia 'Nước ta'` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'中国'*)
- **Lý do cần sửa:** Dùng cụm từ 'nước ta' ('我国') để nhồi nhét biểu tượng, ngày lễ, thủ đô, chính sách của Trung Quốc cho người chơi Việt Nam.
- **Câu hỏi cũ (Tiếng Trung):** `中国签定的第一个不平等条约是哪个？`
- **Lựa chọn cũ:** A: `望厦条约` | B: `南京条约` | C: `辛丑条约` | D: `` (Đáp án cũ: `2`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Đầm phá Tam Giang - hệ thống đầm phá nước lợ lớn nhất Đông Nam Á thuộc tỉnh nào?**
- **👉 Lựa chọn mới:**
  - **A.** Thừa Thiên Huế
  - **B.** Quảng Trị
  - **C.** Quảng Bình
  - **D.** Đà Nẵng
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Thừa Thiên Huế)
- **Giá trị giáo dục / Định hướng tư duy:** *Địa lý miền Trung - Phá Tam Giang mênh mông sông nước*

### Câu 52: [gamesvr_questions.xml - ID 231]
- **Phân loại vi phạm:** `Tuyên truyền quốc gia 'Nước ta'` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'我国'*)
- **Lý do cần sửa:** Dùng cụm từ 'nước ta' ('我国') để nhồi nhét biểu tượng, ngày lễ, thủ đô, chính sách của Trung Quốc cho người chơi Việt Nam.
- **Câu hỏi cũ (Tiếng Trung):** `我国珍稀野生动物特种纪念币系列的首枚纪念币图案是什么？`
- **Lựa chọn cũ:** A: `大熊猫` | B: `金丝猴` | C: `扬子鳄` | D: `白鳍豚` (Đáp án cũ: `1`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Mùa lúa chín vàng trên những thửa ruộng bậc thang kỳ vĩ ở Mù Cang Chải thuộc tỉnh nào?**
- **👉 Lựa chọn mới:**
  - **A.** Yên Bái
  - **B.** Lào Cai
  - **C.** Sơn La
  - **D.** Hà Giang
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Yên Bái)
- **Giá trị giáo dục / Định hướng tư duy:** *Cảnh sắc quê hương - Ruộng bậc thang Mù Cang Chải*

### Câu 53: [gamesvr_questions.xml - ID 233]
- **Phân loại vi phạm:** `Tuyên truyền quốc gia 'Nước ta'` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'中国'*)
- **Lý do cần sửa:** Dùng cụm từ 'nước ta' ('我国') để nhồi nhét biểu tượng, ngày lễ, thủ đô, chính sách của Trung Quốc cho người chơi Việt Nam.
- **Câu hỏi cũ (Tiếng Trung):** `中国四大名砚中哪一种不是石砚？`
- **Lựa chọn cũ:** A: `端砚` | B: `洮河砚` | C: `澄泥砚` | D: `歙砚` (Đáp án cũ: `3`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Chợ nổi Cái Răng - nét văn hóa mua bán trên sông nước độc đáo thuộc thành phố nào?**
- **👉 Lựa chọn mới:**
  - **A.** Cần Thơ
  - **B.** An Giang
  - **C.** Tiền Giang
  - **D.** Vĩnh Long
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Cần Thơ)
- **Giá trị giáo dục / Định hướng tư duy:** *Văn hóa sông nước - Chợ nổi Cái Răng miền Tây*

### Câu 54: [gamesvr_questions.xml - ID 236]
- **Phân loại vi phạm:** `Tuyên truyền quốc gia 'Nước ta'` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'我国'*)
- **Lý do cần sửa:** Dùng cụm từ 'nước ta' ('我国') để nhồi nhét biểu tượng, ngày lễ, thủ đô, chính sách của Trung Quốc cho người chơi Việt Nam.
- **Câu hỏi cũ (Tiếng Trung):** `我国运动员打破的第一个世界田径纪录是什么？`
- **Lựa chọn cũ:** A: `女子跳高` | B: `女子跳远` | C: `女子铅球` | D: `男子百米` (Đáp án cũ: `1`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Cánh đồng muối Sa Huỳnh nổi tiếng với hạt muối trắng trong nằm ở tỉnh nào?**
- **👉 Lựa chọn mới:**
  - **A.** Quảng Ngãi
  - **B.** Khánh Hòa
  - **C.** Bình Thuận
  - **D.** Ninh Thuận
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Quảng Ngãi)
- **Giá trị giáo dục / Định hướng tư duy:** *Nghề truyền thống - Đồng muối Sa Huỳnh Quảng Ngãi*

### Câu 55: [gamesvr_questions.xml - ID 269]
- **Phân loại vi phạm:** `Tuyên truyền quốc gia 'Nước ta'` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'我国'*)
- **Lý do cần sửa:** Dùng cụm từ 'nước ta' ('我国') để nhồi nhét biểu tượng, ngày lễ, thủ đô, chính sách của Trung Quốc cho người chơi Việt Nam.
- **Câu hỏi cũ (Tiếng Trung):** `仰韶文化是我国历史上哪个时代中期的文化`
- **Lựa chọn cũ:** A: `旧石器` | B: `新石器` | C: `青铜器` | D: `铁器` (Đáp án cũ: `2`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Hồ Ba Hầm, Động Thiên Cung, Hang Đầu Gỗ là những điểm tham quan nổi tiếng tại thắng cảnh nào?**
- **👉 Lựa chọn mới:**
  - **A.** Vịnh Hạ Long
  - **B.** Tràng An
  - **C.** Phong Nha - Kẻ Bàng
  - **D.** Ba Bể
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Vịnh Hạ Long)
- **Giá trị giáo dục / Định hướng tư duy:** *Kỳ quan thiên nhiên - Cảnh sắc Vịnh Hạ Long*

### Câu 56: [gamesvr_questions.xml - ID 279]
- **Phân loại vi phạm:** `Lịch sử & Phong kiến Trung Quốc` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'皇帝'*)
- **Lý do cần sửa:** Câu hỏi thuần về các triều đại, hoàng đế phong kiến Trung Quốc, không mang lại giá trị tư duy và không phù hợp môi trường học đường Việt Nam.
- **Câu hỏi cũ (Tiếng Trung):** `后周大将赵匡胤发动了“陈桥兵变”，成为哪个国家的开国皇帝？`
- **Lựa chọn cũ:** A: `唐朝` | B: `宋朝` | C: `元朝` | D: `清朝` (Đáp án cũ: `2`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Vua Đinh Tiên Hoàng (Đinh Bộ Lĩnh) thời niên thiếu gắn liền với trò chơi dân gian nổi tiếng nào cùng lũ trẻ chăn trâu?**
- **👉 Lựa chọn mới:**
  - **A.** Cờ tướng
  - **B.** Tập trận cờ lau
  - **C.** Kéo co
  - **D.** Đá cầu
- **👉 Đáp án đúng mới:** **Lựa chọn 2** (Tập trận cờ lau)
- **Giá trị giáo dục / Định hướng tư duy:** *Giai thoại lịch sử Việt Nam - Ý chí tự lập và tài năng lãnh đạo của Vạn Thắng Vương*

### Câu 57: [gamesvr_questions.xml - ID 293]
- **Phân loại vi phạm:** `Tuyên truyền quốc gia 'Nước ta'` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'中国'*)
- **Lý do cần sửa:** Dùng cụm từ 'nước ta' ('我国') để nhồi nhét biểu tượng, ngày lễ, thủ đô, chính sách của Trung Quốc cho người chơi Việt Nam.
- **Câu hỏi cũ (Tiếng Trung):** `你知道人类首次登陆月球的宇航员是哪个国家的吗？`
- **Lựa chọn cũ:** A: `前苏联` | B: `美国` | C: `英国` | D: `中国` (Đáp án cũ: `2`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Quốc kỳ của nước Cộng hòa Xã hội Chủ nghĩa Việt Nam có hình dáng và màu sắc như thế nào?**
- **👉 Lựa chọn mới:**
  - **A.** Nền đỏ, ở giữa có ngôi sao vàng năm cánh
  - **B.** Nền xanh, ở giữa có ngôi sao trắng
  - **C.** Nền đỏ, ba ngôi sao vàng
  - **D.** Nền vàng, sọc đỏ
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Nền đỏ, ở giữa có ngôi sao vàng năm cánh)
- **Giá trị giáo dục / Định hướng tư duy:** *Biểu tượng quốc gia - Lá cờ đỏ sao vàng thiêng liêng*

### Câu 58: [gamesvr_questions.xml - ID 294]
- **Phân loại vi phạm:** `Tuyên truyền quốc gia 'Nước ta'` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'中国'*)
- **Lý do cần sửa:** Dùng cụm từ 'nước ta' ('我国') để nhồi nhét biểu tượng, ngày lễ, thủ đô, chính sách của Trung Quốc cho người chơi Việt Nam.
- **Câu hỏi cũ (Tiếng Trung):** `你知道著名的天文学家伽利略是哪个国家的吗？`
- **Lựa chọn cũ:** A: `英国` | B: `法国` | C: `意大利` | D: `中国` (Đáp án cũ: `3`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Quốc ca của nước Việt Nam là bài hát nào do nhạc sĩ Văn Cao sáng tác?**
- **👉 Lựa chọn mới:**
  - **A.** Tiến quân ca
  - **B.** Giai điệu Tổ quốc
  - **C.** Lên đàng
  - **D.** Hát vang lý tưởng thanh niên
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Tiến quân ca)
- **Giá trị giáo dục / Định hướng tư duy:** *Âm nhạc Tổ quốc - Bài Tiến quân ca hào hùng*

### Câu 59: [gamesvr_questions.xml - ID 295]
- **Phân loại vi phạm:** `Tuyên truyền quốc gia 'Nước ta'` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'中国'*)
- **Lý do cần sửa:** Dùng cụm từ 'nước ta' ('我国') để nhồi nhét biểu tượng, ngày lễ, thủ đô, chính sách của Trung Quốc cho người chơi Việt Nam.
- **Câu hỏi cũ (Tiếng Trung):** `宇航员费俊龙和聂海胜是下面哪个国家的？`
- **Lựa chọn cũ:** A: `美国` | B: `英国` | C: `中国` | D: `日本` (Đáp án cũ: `3`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Bác Hồ đọc bản Tuyên ngôn Độc lập khai sinh nước Việt Nam Dân chủ Cộng hòa vào ngày tháng năm nào?**
- **👉 Lựa chọn mới:**
  - **A.** Ngày 2 tháng 9 năm 1945
  - **B.** Ngày 19 tháng 8 năm 1945
  - **C.** Ngày 30 tháng 4 năm 1975
  - **D.** Ngày 1 tháng 1 năm 1945
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Ngày 2 tháng 9 năm 1945)
- **Giá trị giáo dục / Định hướng tư duy:** *Ngày Quốc khánh - Ngày 2 tháng 9 bất diệt*

### Câu 60: [gamesvr_questions.xml - ID 299]
- **Phân loại vi phạm:** `Tuyên truyền quốc gia 'Nước ta'` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'我国'*)
- **Lý do cần sửa:** Dùng cụm từ 'nước ta' ('我国') để nhồi nhét biểu tượng, ngày lễ, thủ đô, chính sách của Trung Quốc cho người chơi Việt Nam.
- **Câu hỏi cũ (Tiếng Trung):** `你知道我国进行第一次防震减灾演习的城市和时间吗？`
- **Lựa chọn cũ:** A: `乌鲁木齐市、1991年7月28日` | B: `乌鲁木齐市、1992年7月28日` | C: `齐齐哈尔市、1991年7月28日` | D: `齐齐哈尔市、1992年7月28日` (Đáp án cũ: `1`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Ngày Giải phóng hoàn toàn miền Nam, thống nhất non sông đất nước là ngày nào?**
- **👉 Lựa chọn mới:**
  - **A.** Ngày 30 tháng 4 năm 1975
  - **B.** Ngày 1 tháng 5 năm 1975
  - **C.** Ngày 2 tháng 9 năm 1975
  - **D.** Ngày 19 tháng 5 năm 1975
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Ngày 30 tháng 4 năm 1975)
- **Giá trị giáo dục / Định hướng tư duy:** *Ngày Chiến thắng - 30 tháng 4 non sông liền một dải*

### Câu 61: [gamesvr_questions.xml - ID 300]
- **Phân loại vi phạm:** `Lịch sử & Phong kiến Trung Quốc` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'刘邦'*)
- **Lý do cần sửa:** Câu hỏi thuần về các triều đại, hoàng đế phong kiến Trung Quốc, không mang lại giá trị tư duy và không phù hợp môi trường học đường Việt Nam.
- **Câu hỏi cũ (Tiếng Trung):** `号称“西楚霸王”的是谁？`
- **Lựa chọn cũ:** A: `刘备` | B: `刘邦` | C: `项羽` | D: `关羽` (Đáp án cũ: `3`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Cuộc khởi nghĩa Lam Sơn kéo dài 10 năm gian khổ đánh đuổi quân Minh xâm lược do vị anh hùng nào lãnh đạo?**
- **👉 Lựa chọn mới:**
  - **A.** Lê Lợi
  - **B.** Nguyễn Trãi
  - **C.** Lê Lai
  - **D.** Trần Nguyên Hãn
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Lê Lợi)
- **Giá trị giáo dục / Định hướng tư duy:** *Khởi nghĩa Lam Sơn - Khát vọng hòa bình và tinh thần kiên cường của dân tộc*

### Câu 62: [gamesvr_questions.xml - ID 303]
- **Phân loại vi phạm:** `Tuyên truyền quốc gia 'Nước ta'` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'中国'*)
- **Lý do cần sửa:** Dùng cụm từ 'nước ta' ('我国') để nhồi nhét biểu tượng, ngày lễ, thủ đô, chính sách của Trung Quốc cho người chơi Việt Nam.
- **Câu hỏi cũ (Tiếng Trung):** `中国古代建筑是世界古建筑中的一个独特体系，大多采用什么结构`
- **Lựa chọn cũ:** A: `木构架` | B: `钢筋` | C: `水` | D: `砖石` (Đáp án cũ: `1`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Ngày Nhà giáo Việt Nam nhằm tôn vinh các thầy cô giáo được tổ chức vào ngày nào hàng năm?**
- **👉 Lựa chọn mới:**
  - **A.** Ngày 20 tháng 11
  - **B.** Ngày 20 tháng 10
  - **C.** Ngày 8 tháng 3
  - **D.** Ngày 15 tháng 10
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Ngày 20 tháng 11)
- **Giá trị giáo dục / Định hướng tư duy:** *Tôn sư trọng đạo - Ngày Nhà giáo Việt Nam 20/11*

### Câu 63: [gamesvr_questions.xml - ID 305]
- **Phân loại vi phạm:** `Tuyên truyền quốc gia 'Nước ta'` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'中国'*)
- **Lý do cần sửa:** Dùng cụm từ 'nước ta' ('我国') để nhồi nhét biểu tượng, ngày lễ, thủ đô, chính sách của Trung Quốc cho người chơi Việt Nam.
- **Câu hỏi cũ (Tiếng Trung):** `在中国神话中，谁发明了农业？`
- **Lựa chọn cũ:** A: `后稷` | B: `燧人` | C: `` | D: `` (Đáp án cũ: `1`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Ngày thành lập Quân đội Nhân dân Việt Nam và Ngày hội Quốc phòng toàn dân là ngày nào?**
- **👉 Lựa chọn mới:**
  - **A.** Ngày 22 tháng 12
  - **B.** Ngày 19 tháng 8
  - **C.** Ngày 27 tháng 7
  - **D.** Ngày 3 tháng 2
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Ngày 22 tháng 12)
- **Giá trị giáo dục / Định hướng tư duy:** *Lực lượng vũ trang - Ngày Quân đội Nhân dân 22/12*

### Câu 64: [gamesvr_questions.xml - ID 309]
- **Phân loại vi phạm:** `Tuyên truyền quốc gia 'Nước ta'` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'我国'*)
- **Lý do cần sửa:** Dùng cụm từ 'nước ta' ('我国') để nhồi nhét biểu tượng, ngày lễ, thủ đô, chính sách của Trung Quốc cho người chơi Việt Nam.
- **Câu hỏi cũ (Tiếng Trung):** `当我国正处于冬季的时候，澳大利亚是什么季节？`
- **Lựa chọn cũ:** A: `春天` | B: `夏天` | C: `秋天` | D: `冬天` (Đáp án cũ: `2`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Ngày Giỗ Tổ Hùng Vương được tổ chức trang trọng vào ngày nào theo âm lịch hàng năm?**
- **👉 Lựa chọn mới:**
  - **A.** Mùng 10 tháng 3 âm lịch
  - **B.** Mùng 1 tháng Giêng
  - **C.** Rằm tháng Giêng
  - **D.** Mùng 5 tháng 5 âm lịch
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Mùng 10 tháng 3 âm lịch)
- **Giá trị giáo dục / Định hướng tư duy:** *Cội nguồn thiêng liêng - Mùng 10 tháng 3 âm lịch*

### Câu 65: [gamesvr_questions.xml - ID 313]
- **Phân loại vi phạm:** `Tuyên truyền quốc gia 'Nước ta'` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'我国'*)
- **Lý do cần sửa:** Dùng cụm từ 'nước ta' ('我国') để nhồi nhét biểu tượng, ngày lễ, thủ đô, chính sách của Trung Quốc cho người chơi Việt Nam.
- **Câu hỏi cũ (Tiếng Trung):** `我国曲艺中的相声是？`
- **Lựa chọn cũ:** A: `北方曲种` | B: `南方曲种` | C: `` | D: `` (Đáp án cũ: `1`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Trường đại học đầu tiên của Việt Nam được xây dựng dưới thời vua Lý Thánh Tông là trường nào?**
- **👉 Lựa chọn mới:**
  - **A.** Quốc Tử Giám (Hà Nội)
  - **B.** Trường Thi Hương
  - **C.** Quốc Học Huế
  - **D.** Trường Bưởi
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Quốc Tử Giám (Hà Nội))
- **Giá trị giáo dục / Định hướng tư duy:** *Lịch sử giáo dục - Văn Miếu Quốc Tử Giám ngàn năm văn hiến*

### Câu 66: [gamesvr_questions.xml - ID 320]
- **Phân loại vi phạm:** `Lịch sử & Phong kiến Trung Quốc` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'李世民'*)
- **Lý do cần sửa:** Câu hỏi thuần về các triều đại, hoàng đế phong kiến Trung Quốc, không mang lại giá trị tư duy và không phù hợp môi trường học đường Việt Nam.
- **Câu hỏi cũ (Tiếng Trung):** `下列历史上的事变哪个是李世民发动的？`
- **Lựa chọn cũ:** A: `玄武门之变` | B: `陈桥兵变` | C: `靖康之变` | D: `土木之变` (Đáp án cũ: `1`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Vị anh hùng áo vải cờ đào đánh tan 29 vạn quân Thanh xâm lược trong trận đại thắng Ngọc Hồi - Đống Đa mùa xuân 1789 là ai?**
- **👉 Lựa chọn mới:**
  - **A.** Quang Trung (Nguyễn Huệ)
  - **B.** Nguyễn Nhạc
  - **C.** Nguyễn Lữ
  - **D.** Lê Chiêu Thống
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Quang Trung (Nguyễn Huệ))
- **Giá trị giáo dục / Định hướng tư duy:** *Chiến công hiển hách - Thiên tài quân sự Hoàng đế Quang Trung*

### Câu 67: [gamesvr_questions.xml - ID 323]
- **Phân loại vi phạm:** `Đố chữ Hán & Chiết tự` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'成语'*)
- **Lý do cần sửa:** Đố chiết tự chữ tượng hình hoặc thành ngữ Hán ngữ cổ mà người chơi Việt Nam không thể suy luận logic.
- **Câu hỏi cũ (Tiếng Trung):** `成语“闻鸡起舞”“中流击楫”是出自哪们古代将领的故事？`
- **Lựa chọn cũ:** A: `岳飞` | B: `戚继光` | C: `祖逖` | D: `郑成功` (Đáp án cũ: `3`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Con gì hai mắt tròn xoe, thích bắt chuột nhắt và leo trèo rất giỏi?**
- **👉 Lựa chọn mới:**
  - **A.** Con mèo
  - **B.** Con cún
  - **C.** Con lợn
  - **D.** Con thỏ
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Con mèo)
- **Giá trị giáo dục / Định hướng tư duy:** *Câu đố dân gian - Đố về bạn mèo đáng yêu*

### Câu 68: [gamesvr_questions.xml - ID 324]
- **Phân loại vi phạm:** `Tuyên truyền quốc gia 'Nước ta'` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'我国'*)
- **Lý do cần sửa:** Dùng cụm từ 'nước ta' ('我国') để nhồi nhét biểu tượng, ngày lễ, thủ đô, chính sách của Trung Quốc cho người chơi Việt Nam.
- **Câu hỏi cũ (Tiếng Trung):** `我国古代“三十六计”中第36计是什么？`
- **Lựa chọn cũ:** A: `美人计` | B: `空城计` | C: `走为上计` | D: `反间计` (Đáp án cũ: `3`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Bác Hồ kính yêu sinh ngày tháng năm nào tại làng Sen, Nam Đàn, Nghệ An?**
- **👉 Lựa chọn mới:**
  - **A.** 19 tháng 5 năm 1890
  - **B.** 2 tháng 9 năm 1890
  - **C.** 1 tháng 1 năm 1890
  - **D.** 3 tháng 2 năm 1890
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (19 tháng 5 năm 1890)
- **Giá trị giáo dục / Định hướng tư duy:** *Lãnh tụ kính yêu - Ngày sinh Chủ tịch Hồ Chí Minh 19/5*

### Câu 69: [gamesvr_questions.xml - ID 326]
- **Phân loại vi phạm:** `Tuyên truyền quốc gia 'Nước ta'` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'我国'*)
- **Lý do cần sửa:** Dùng cụm từ 'nước ta' ('我国') để nhồi nhét biểu tượng, ngày lễ, thủ đô, chính sách của Trung Quốc cho người chơi Việt Nam.
- **Câu hỏi cũ (Tiếng Trung):** `我国现存最早的兵书是？`
- **Lựa chọn cũ:** A: `《孙膑兵法》` | B: `《吴子》` | C: `《孙子兵法》` | D: `《六韬》` (Đáp án cũ: `3`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Việt Nam hiện có bao nhiêu dân tộc anh em cùng chung sống đoàn kết trên dải đất hình chữ S?**
- **👉 Lựa chọn mới:**
  - **A.** 54 dân tộc
  - **B.** 50 dân tộc
  - **C.** 56 dân tộc
  - **D.** 60 dân tộc
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (54 dân tộc)
- **Giá trị giáo dục / Định hướng tư duy:** *Khối đại đoàn kết - 54 dân tộc anh em một nhà*

### Câu 70: [gamesvr_questions.xml - ID 327]
- **Phân loại vi phạm:** `Tuyên truyền quốc gia 'Nước ta'` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'我国'*)
- **Lý do cần sửa:** Dùng cụm từ 'nước ta' ('我国') để nhồi nhét biểu tượng, ngày lễ, thủ đô, chính sách của Trung Quốc cho người chơi Việt Nam.
- **Câu hỏi cũ (Tiếng Trung):** `我国人民解放军第一位女将军是谁？`
- **Lựa chọn cũ:** A: `李贞` | B: `贺子珍` | C: `邓颖超` | D: `蔡畅` (Đáp án cũ: `1`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Bộ luật đầu tiên bằng văn bản thành văn của nhà nước phong kiến Đại Việt thời Lý có tên là gì?**
- **👉 Lựa chọn mới:**
  - **A.** Hình thư
  - **B.** Quốc triều hình luật
  - **C.** Hoàng Việt luật lệ
  - **D.** Luật Hồng Đức
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Hình thư)
- **Giá trị giáo dục / Định hướng tư duy:** *Pháp luật lịch sử - Bộ luật Hình thư thời Lý*

### Câu 71: [gamesvr_questions.xml - ID 328]
- **Phân loại vi phạm:** `Tuyên truyền quốc gia 'Nước ta'` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'我国'*)
- **Lý do cần sửa:** Dùng cụm từ 'nước ta' ('我国') để nhồi nhét biểu tượng, ngày lễ, thủ đô, chính sách của Trung Quốc cho người chơi Việt Nam.
- **Câu hỏi cũ (Tiếng Trung):** `我国进行抗美援朝是在哪一年？`
- **Lựa chọn cũ:** A: `1949` | B: `1950` | C: `1951` | D: `1952` (Đáp án cũ: `2`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Ai là người thầy thuốc lỗi lạc được tôn vinh là 'Đại danh y' với bộ sách 'Nam dược trị Nam nhân'?**
- **👉 Lựa chọn mới:**
  - **A.** Tuệ Tĩnh
  - **B.** Hải Thượng Lãn Ông
  - **C.** Lê Hữu Trác
  - **D.** Hoa Đà
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Tuệ Tĩnh)
- **Giá trị giáo dục / Định hướng tư duy:** *Y học cổ truyền - Danh y Tuệ Tĩnh*

### Câu 72: [gamesvr_questions.xml - ID 329]
- **Phân loại vi phạm:** `Tuyên truyền quốc gia 'Nước ta'` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'我国'*)
- **Lý do cần sửa:** Dùng cụm từ 'nước ta' ('我国') để nhồi nhét biểu tượng, ngày lễ, thủ đô, chính sách của Trung Quốc cho người chơi Việt Nam.
- **Câu hỏi cũ (Tiếng Trung):** `我国古代项羽“破釜沉舟”战胜秦军是在哪次战役？`
- **Lựa chọn cũ:** A: `牧野之战` | B: `巨鹿之战` | C: `官渡之战` | D: `昆阳之战` (Đáp án cũ: `2`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Tác giả cuốn bách khoa toàn thư y học cổ truyền 'Hải Thượng y tông tâm lĩnh' là danh y nào?**
- **👉 Lựa chọn mới:**
  - **A.** Lê Hữu Trác (Hải Thượng Lãn Ông)
  - **B.** Tuệ Tĩnh
  - **C.** Chu Văn An
  - **D.** Nguyễn Du
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Lê Hữu Trác (Hải Thượng Lãn Ông))
- **Giá trị giáo dục / Định hướng tư duy:** *Y đức ngời sáng - Hải Thượng Lãn Ông Lê Hữu Trác*

### Câu 73: [gamesvr_questions.xml - ID 333]
- **Phân loại vi phạm:** `Tuyên truyền quốc gia 'Nước ta'` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'我国'*)
- **Lý do cần sửa:** Dùng cụm từ 'nước ta' ('我国') để nhồi nhét biểu tượng, ngày lễ, thủ đô, chính sách của Trung Quốc cho người chơi Việt Nam.
- **Câu hỏi cũ (Tiếng Trung):** `下列我国名泉中哪一眼位于杭州？`
- **Lựa chọn cũ:** A: `观音泉` | B: `虎跑泉` | C: `趵突泉` | D: `招隐泉` (Đáp án cũ: `2`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Tác phẩm văn học kiệt tác 'Truyện Kiều' (Đoạn trường tân thanh) là sáng tác của đại thi hào nào?**
- **👉 Lựa chọn mới:**
  - **A.** Nguyễn Du
  - **B.** Nguyễn Trãi
  - **C.** Hồ Xuân Hương
  - **D.** Bà Huyện Thanh Quan
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Nguyễn Du)
- **Giá trị giáo dục / Định hướng tư duy:** *Đại thi hào dân tộc - Tác phẩm Truyện Kiều của Nguyễn Du*

### Câu 74: [gamesvr_questions.xml - ID 334]
- **Phân loại vi phạm:** `Tuyên truyền quốc gia 'Nước ta'` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'我国'*)
- **Lý do cần sửa:** Dùng cụm từ 'nước ta' ('我国') để nhồi nhét biểu tượng, ngày lễ, thủ đô, chính sách của Trung Quốc cho người chơi Việt Nam.
- **Câu hỏi cũ (Tiếng Trung):** `我国四大名亭中哪一座亭名是毛泽东题的？`
- **Lựa chọn cũ:** A: `爱晚亭` | B: `醉翁亭` | C: `陶然亭` | D: `湖心亭` (Đáp án cũ: `1`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Áng văn 'Bình Ngô đại cáo' được coi là bản Tuyên ngôn Độc lập thứ hai của nước ta do ai chấp bút?**
- **👉 Lựa chọn mới:**
  - **A.** Nguyễn Trãi
  - **B.** Lê Lợi
  - **C.** Trần Hưng Đạo
  - **D.** Lý Thường Kiệt
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Nguyễn Trãi)
- **Giá trị giáo dục / Định hướng tư duy:** *Văn học kiệt xuất - Danh nhân văn hóa thế giới Nguyễn Trãi*

### Câu 75: [gamesvr_questions.xml - ID 335]
- **Phân loại vi phạm:** `Tuyên truyền quốc gia 'Nước ta'` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'我国'*)
- **Lý do cần sửa:** Dùng cụm từ 'nước ta' ('我国') để nhồi nhét biểu tượng, ngày lễ, thủ đô, chính sách của Trung Quốc cho người chơi Việt Nam.
- **Câu hỏi cũ (Tiếng Trung):** `下列我国哪个古迹被誉为“世界八大奇迹”之一？`
- **Lựa chọn cũ:** A: `万里长城` | B: `乐山大佛` | C: `秦始皇兵马俑` | D: `敦煌` (Đáp án cũ: `3`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Người đội viên thiếu niên dũng cảm lấy thân mình lấp lỗ châu mai trong chiến dịch Điện Biên Phủ là ai?**
- **👉 Lựa chọn mới:**
  - **A.** Phan Đình Giót
  - **B.** Bế Văn Đàn
  - **C.** Tô Vĩnh Diện
  - **D.** La Văn Cầu
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Phan Đình Giót)
- **Giá trị giáo dục / Định hướng tư duy:** *Gương anh hùng liệt sĩ - Liệt sĩ Phan Đình Giót*

### Câu 76: [gamesvr_questions.xml - ID 338]
- **Phân loại vi phạm:** `Tuyên truyền quốc gia 'Nước ta'` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'我国'*)
- **Lý do cần sửa:** Dùng cụm từ 'nước ta' ('我国') để nhồi nhét biểu tượng, ngày lễ, thủ đô, chính sách của Trung Quốc cho người chơi Việt Nam.
- **Câu hỏi cũ (Tiếng Trung):** `我国最大的佛像是哪一座？`
- **Lựa chọn cũ:** A: `潼南金佛` | B: `屏山大佛` | C: `荣成大佛` | D: `乐山大佛` (Đáp án cũ: `4`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Người chiến sĩ anh dũng lấy thân mình làm giá súng trong chiến dịch Điện Biên Phủ là ai?**
- **👉 Lựa chọn mới:**
  - **A.** Bế Văn Đàn
  - **B.** Phan Đình Giót
  - **C.** Tô Vĩnh Diện
  - **D.** Võ Thị Sáu
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Bế Văn Đàn)
- **Giá trị giáo dục / Định hướng tư duy:** *Gương anh hùng liệt sĩ - Liệt sĩ Bế Văn Đàn*

### Câu 77: [gamesvr_questions.xml - ID 339]
- **Phân loại vi phạm:** `Tuyên truyền quốc gia 'Nước ta'` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'我国'*)
- **Lý do cần sửa:** Dùng cụm từ 'nước ta' ('我国') để nhồi nhét biểu tượng, ngày lễ, thủ đô, chính sách của Trung Quốc cho người chơi Việt Nam.
- **Câu hỏi cũ (Tiếng Trung):** `下列哪座山不属于我国四大佛山之一？`
- **Lựa chọn cũ:** A: `雁荡山` | B: `五台山` | C: `九华山` | D: `峨眉山` (Đáp án cũ: `1`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Anh hùng thiếu niên dũng cảm lấy thân mình chèn bánh pháo trong chiến dịch Điện Biên Phủ là ai?**
- **👉 Lựa chọn mới:**
  - **A.** Tô Vĩnh Diện
  - **B.** Bế Văn Đàn
  - **C.** Phan Đình Giót
  - **D.** Kim Đồng
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Tô Vĩnh Diện)
- **Giá trị giáo dục / Định hướng tư duy:** *Gương anh hùng liệt sĩ - Liệt sĩ Tô Vĩnh Diện*

### Câu 78: [gamesvr_questions.xml - ID 342]
- **Phân loại vi phạm:** `Tuyên truyền quốc gia 'Nước ta'` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'我国'*)
- **Lý do cần sửa:** Dùng cụm từ 'nước ta' ('我国') để nhồi nhét biểu tượng, ngày lễ, thủ đô, chính sách của Trung Quốc cho người chơi Việt Nam.
- **Câu hỏi cũ (Tiếng Trung):** `下列哪一个城市不是我国的“三大火炉”(高温)之一？`
- **Lựa chọn cũ:** A: `重庆` | B: `成都` | C: `武汉` | D: `南京` (Đáp án cũ: `2`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Người đội trưởng đầu tiên của Đội Thiếu niên Tiền phong Hồ Chí Minh là ai?**
- **👉 Lựa chọn mới:**
  - **A.** Kim Đồng (Nông Văn Dền)
  - **B.** Lê Văn Tám
  - **C.** Vừ A Dính
  - **D.** Kpa Klơng
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Kim Đồng (Nông Văn Dền))
- **Giá trị giáo dục / Định hướng tư duy:** *Lịch sử Đội TNTP - Anh Kim Đồng anh dũng*

### Câu 79: [gamesvr_questions.xml - ID 348]
- **Phân loại vi phạm:** `Tuyên truyền quốc gia 'Nước ta'` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'我国'*)
- **Lý do cần sửa:** Dùng cụm từ 'nước ta' ('我国') để nhồi nhét biểu tượng, ngày lễ, thủ đô, chính sách của Trung Quốc cho người chơi Việt Nam.
- **Câu hỏi cũ (Tiếng Trung):** `“鲁”是我国哪个省份的简称？`
- **Lựa chọn cũ:** A: `河北` | B: `吉林` | C: `山东` | D: `山西` (Đáp án cũ: `3`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Nữ anh hùng trẻ tuổi quê ở Đất Đỏ kiên cường trước mũi súng quân thù là ai?**
- **👉 Lựa chọn mới:**
  - **A.** Chị Võ Thị Sáu
  - **B.** Chị Nguyễn Thị Minh Khai
  - **C.** Chị Út Tịch
  - **D.** Chị Đặng Thùy Trâm
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Chị Võ Thị Sáu)
- **Giá trị giáo dục / Định hướng tư duy:** *Gương sáng thiếu niên - Chị Võ Thị Sáu*

### Câu 80: [gamesvr_questions.xml - ID 349]
- **Phân loại vi phạm:** `Tuyên truyền quốc gia 'Nước ta'` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'我国'*)
- **Lý do cần sửa:** Dùng cụm từ 'nước ta' ('我国') để nhồi nhét biểu tượng, ngày lễ, thủ đô, chính sách của Trung Quốc cho người chơi Việt Nam.
- **Câu hỏi cũ (Tiếng Trung):** `峨眉山位于我国哪个省份？`
- **Lựa chọn cũ:** A: `四川` | B: `云南` | C: `贵州` | D: `西藏` (Đáp án cũ: `1`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Anh hùng liệt sĩ thiếu niên dân tộc H'Mông dũng cảm hy sinh khi làm nhiệm vụ liên lạc là ai?**
- **👉 Lựa chọn mới:**
  - **A.** Vừ A Dính
  - **B.** Kim Đồng
  - **C.** Kpa Klơng
  - **D.** Bế Văn Đàn
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Vừ A Dính)
- **Giá trị giáo dục / Định hướng tư duy:** *Gương anh hùng thiếu niên - Anh Vừ A Dính*

### Câu 81: [gamesvr_questions.xml - ID 351]
- **Phân loại vi phạm:** `Tuyên truyền quốc gia 'Nước ta'` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'我国'*)
- **Lý do cần sửa:** Dùng cụm từ 'nước ta' ('我国') để nhồi nhét biểu tượng, ngày lễ, thủ đô, chính sách của Trung Quốc cho người chơi Việt Nam.
- **Câu hỏi cũ (Tiếng Trung):** `下列我国名茶中哪一种是产于福建安溪？`
- **Lựa chọn cũ:** A: `龙井` | B: `碧螺春` | C: `武夷岩茶` | D: `铁观音` (Đáp án cũ: `4`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Phong trào 'Kế hoạch nhỏ' của thiếu nhi Việt Nam nhằm gom phế liệu gây quỹ được khởi xướng từ năm nào?**
- **👉 Lựa chọn mới:**
  - **A.** Năm 1958
  - **B.** Năm 1968
  - **C.** Năm 1975
  - **D.** Năm 1985
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Năm 1958)
- **Giá trị giáo dục / Định hướng tư duy:** *Hoạt động Đội - Phong trào Kế hoạch nhỏ ý nghĩa*

### Câu 82: [gamesvr_questions.xml - ID 352]
- **Phân loại vi phạm:** `Tuyên truyền quốc gia 'Nước ta'` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'我国'*)
- **Lý do cần sửa:** Dùng cụm từ 'nước ta' ('我国') để nhồi nhét biểu tượng, ngày lễ, thủ đô, chính sách của Trung Quốc cho người chơi Việt Nam.
- **Câu hỏi cũ (Tiếng Trung):** `下列哪一个湖泊是在我国江西省的境内？`
- **Lựa chọn cũ:** A: `洞庭湖` | B: `鄱阳湖` | C: `太湖` | D: `洪泽湖` (Đáp án cũ: `2`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Năm điều Bác Hồ dạy thiếu niên, nhi đồng mở đầu bằng điều gì?**
- **👉 Lựa chọn mới:**
  - **A.** Yêu Tổ quốc, yêu đồng bào
  - **B.** Học tập tốt, lao động tốt
  - **C.** Đoàn kết tốt, kỷ luật tốt
  - **D.** Giữ gìn vệ sinh thật tốt
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Yêu Tổ quốc, yêu đồng bào)
- **Giá trị giáo dục / Định hướng tư duy:** *Lời dạy của Bác - 5 điều Bác Hồ dạy thiếu niên nhi đồng*

### Câu 83: [gamesvr_questions.xml - ID 355]
- **Phân loại vi phạm:** `Tuyên truyền quốc gia 'Nước ta'` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'中国'*)
- **Lý do cần sửa:** Dùng cụm từ 'nước ta' ('我国') để nhồi nhét biểu tượng, ngày lễ, thủ đô, chính sách của Trung Quốc cho người chơi Việt Nam.
- **Câu hỏi cũ (Tiếng Trung):** `中国旧时流行的《百家姓》始写于什么时期？`
- **Lựa chọn cũ:** A: `北宋` | B: `唐朝` | C: `春秋` | D: `隋朝` (Đáp án cũ: `1`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Chiếc khăn quàng đỏ của Đội viên Đội Thiếu niên Tiền phong Hồ Chí Minh có ý nghĩa tượng trưng cho điều gì?**
- **👉 Lựa chọn mới:**
  - **A.** Một phần của lá cờ Tổ quốc và màu máu của các anh hùng liệt sĩ
  - **B.** Màu của hoa phượng vĩ
  - **C.** Màu của ánh mặt trời buổi sớm
  - **D.** Màu sắc thời trang
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Một phần của lá cờ Tổ quốc và màu máu của các anh hùng liệt sĩ)
- **Giá trị giáo dục / Định hướng tư duy:** *Ý nghĩa huy hiệu Đội - Màu khăn quàng đỏ thắm*

### Câu 84: [gamesvr_questions.xml - ID 356]
- **Phân loại vi phạm:** `Tuyên truyền quốc gia 'Nước ta'` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'我国'*)
- **Lý do cần sửa:** Dùng cụm từ 'nước ta' ('我国') để nhồi nhét biểu tượng, ngày lễ, thủ đô, chính sách của Trung Quốc cho người chơi Việt Nam.
- **Câu hỏi cũ (Tiếng Trung):** `大汶口文化遗址在我国的什么地方？ `
- **Lựa chọn cũ:** A: `湖南` | B: `广西` | C: `山东` | D: `陕西` (Đáp án cũ: `3`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Món bánh cổ truyền tượng trưng cho Đất tròn Trời vuông trong ngày Tết Nguyên Đán của người Việt là bánh gì?**
- **👉 Lựa chọn mới:**
  - **A.** Bánh chưng và bánh giầy
  - **B.** Bánh gai và bánh cốm
  - **C.** Bánh phu thê và bánh dẻo
  - **D.** Bánh tét và bánh ú
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Bánh chưng và bánh giầy)
- **Giá trị giáo dục / Định hướng tư duy:** *Phong tục cổ truyền - Sự tích Bánh chưng bánh giầy*

### Câu 85: [gamesvr_questions.xml - ID 359]
- **Phân loại vi phạm:** `Tuyên truyền quốc gia 'Nước ta'` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'中国'*)
- **Lý do cần sửa:** Dùng cụm từ 'nước ta' ('我国') để nhồi nhét biểu tượng, ngày lễ, thủ đô, chính sách của Trung Quốc cho người chơi Việt Nam.
- **Câu hỏi cũ (Tiếng Trung):** `《孙子兵法》是中国对世界的一大贡献，请问这本兵书有多少篇？`
- **Lựa chọn cũ:** A: `10` | B: `13` | C: `16` | D: `18` (Đáp án cũ: `2`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Loài hoa đặc trưng cho mùa xuân và ngày Tết Nguyên đán ở miền Bắc Việt Nam là hoa gì?**
- **👉 Lựa chọn mới:**
  - **A.** Hoa đào
  - **B.** Hoa mai
  - **C.** Hoa cúc
  - **D.** Hoa lan
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Hoa đào)
- **Giá trị giáo dục / Định hướng tư duy:** *Văn hóa Tết Việt - Hoa đào đỏ thắm đón xuân sang*

### Câu 86: [gamesvr_questions.xml - ID 361]
- **Phân loại vi phạm:** `Tuyên truyền quốc gia 'Nước ta'` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'我国'*)
- **Lý do cần sửa:** Dùng cụm từ 'nước ta' ('我国') để nhồi nhét biểu tượng, ngày lễ, thủ đô, chính sách của Trung Quốc cho người chơi Việt Nam.
- **Câu hỏi cũ (Tiếng Trung):** `我国有“留学生”一词来源于何时？`
- **Lựa chọn cũ:** A: `汉朝` | B: `唐朝` | C: `宋朝` | D: `明朝` (Đáp án cũ: `2`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Loài hoa vàng rực rỡ đặc trưng cho không khí Tết Nguyên đán ở miền Nam Việt Nam là hoa gì?**
- **👉 Lựa chọn mới:**
  - **A.** Hoa mai vàng
  - **B.** Hoa đào
  - **C.** Hoa hướng dương
  - **D.** Hoa cúc vạn thọ
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Hoa mai vàng)
- **Giá trị giáo dục / Định hướng tư duy:** *Văn hóa Tết Việt - Sắc mai vàng đón Tết phương Nam*

### Câu 87: [gamesvr_questions.xml - ID 365]
- **Phân loại vi phạm:** `Tuyên truyền quốc gia 'Nước ta'` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'中国'*)
- **Lý do cần sửa:** Dùng cụm từ 'nước ta' ('我国') để nhồi nhét biểu tượng, ngày lễ, thủ đô, chính sách của Trung Quốc cho người chơi Việt Nam.
- **Câu hỏi cũ (Tiếng Trung):** `中国古代中最早提到小孔成像的原理的著作是？`
- **Lựa chọn cũ:** A: `《九章算术》` | B: `《墨经》` | C: `《天工开物》` | D: `《四库全书》` (Đáp án cũ: `2`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Ngày Tết Trung thu dành cho thiếu nhi diễn ra vào ngày nào âm lịch hàng năm?**
- **👉 Lựa chọn mới:**
  - **A.** Rằm tháng 8 (15/8 âm lịch)
  - **B.** Rằm tháng 7
  - **C.** Mùng 5 tháng 5
  - **D.** Mùng 1 tháng Giêng
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Rằm tháng 8 (15/8 âm lịch))
- **Giá trị giáo dục / Định hướng tư duy:** *Lễ hội thiếu nhi - Đêm hội trăng rằm Tết Trung thu*

### Câu 88: [gamesvr_questions.xml - ID 366]
- **Phân loại vi phạm:** `Tuyên truyền quốc gia 'Nước ta'` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'我国'*)
- **Lý do cần sửa:** Dùng cụm từ 'nước ta' ('我国') để nhồi nhét biểu tượng, ngày lễ, thủ đô, chính sách của Trung Quốc cho người chơi Việt Nam.
- **Câu hỏi cũ (Tiếng Trung):** `我国传统工艺有“三绝”，下列不是的是？`
- **Lựa chọn cũ:** A: `北京景泰蓝` | B: `江西景德镇瓷器` | C: `福州脱胎瓷器` | D: `江苏宜兴紫砂` (Đáp án cũ: `4`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Nhân vật quen thuộc trong cổ tích Việt Nam thường gắn liền với cung trăng và cây đa là ai?**
- **👉 Lựa chọn mới:**
  - **A.** Chú Cuội và Chị Hằng
  - **B.** Thạch Sanh
  - **C.** Sọ Dừa
  - **D.** Mai An Tiêm
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Chú Cuội và Chị Hằng)
- **Giá trị giáo dục / Định hướng tư duy:** *Cổ tích dân gian - Chuyện chú Cuội ngồi gốc cây đa*

### Câu 89: [gamesvr_questions.xml - ID 382]
- **Phân loại vi phạm:** `Tuyên truyền quốc gia 'Nước ta'` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'中国'*)
- **Lý do cần sửa:** Dùng cụm từ 'nước ta' ('我国') để nhồi nhét biểu tượng, ngày lễ, thủ đô, chính sách của Trung Quốc cho người chơi Việt Nam.
- **Câu hỏi cũ (Tiếng Trung):** `世界上最大的古代士石建筑工程是哪一个？`
- **Lựa chọn cũ:** A: `中国的万里长城` | B: `埃及的金字塔` | C: `古罗马的斗兽场` | D: `中国的故宫` (Đáp án cũ: `1`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Truyền thuyết nào giải thích nguồn gốc của quả dưa hấu ruột đỏ ngọt lịm ngoài đảo xa?**
- **👉 Lựa chọn mới:**
  - **A.** Sự tích Mai An Tiêm
  - **B.** Sự tích Quả bầu mẹ
  - **C.** Sự tích Trầu cau
  - **D.** Sự tích Cây khế
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Sự tích Mai An Tiêm)
- **Giá trị giáo dục / Định hướng tư duy:** *Truyền thuyết dân gian - Mai An Tiêm và quả dưa đỏ*

### Câu 90: [gamesvr_questions.xml - ID 390]
- **Phân loại vi phạm:** `Tuyên truyền quốc gia 'Nước ta'` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'我国'*)
- **Lý do cần sửa:** Dùng cụm từ 'nước ta' ('我国') để nhồi nhét biểu tượng, ngày lễ, thủ đô, chính sách của Trung Quốc cho người chơi Việt Nam.
- **Câu hỏi cũ (Tiếng Trung):** `我国国防系统最高学府是下列哪所大学？`
- **Lựa chọn cũ:** A: `清华大学` | B: `北京航空航天大学` | C: `北京大学` | D: `国防大学` (Đáp án cũ: `4`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Chiếc áo dài truyền thống duyên dáng được coi là quốc phục của quốc gia nào?**
- **👉 Lựa chọn mới:**
  - **A.** Việt Nam
  - **B.** Hàn Quốc
  - **C.** Nhật Bản
  - **D.** Thái Lan
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Việt Nam)
- **Giá trị giáo dục / Định hướng tư duy:** *Trang phục truyền thống - Tà áo dài Việt Nam*

### Câu 91: [gamesvr_questions.xml - ID 395]
- **Phân loại vi phạm:** `Lịch sử & Phong kiến Trung Quốc` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'朝代'*)
- **Lý do cần sửa:** Câu hỏi thuần về các triều đại, hoàng đế phong kiến Trung Quốc, không mang lại giá trị tư duy và không phù hợp môi trường học đường Việt Nam.
- **Câu hỏi cũ (Tiếng Trung):** `杜甫的诗《江南逢李龟年》中的李龟年是哪个朝代的人？`
- **Lựa chọn cũ:** A: `唐朝` | B: `宋朝` | C: `明朝` | D: `` (Đáp án cũ: `1`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Hai vị nữ anh hùng đầu tiên trong lịch sử dân tộc cưỡi voi phất cờ khởi nghĩa đánh đuổi Thái thú Tô Định năm 40 là ai?**
- **👉 Lựa chọn mới:**
  - **A.** Hai Bà Trưng (Trưng Trắc, Trưng Nhị)
  - **B.** Bà Triệu
  - **C.** Bùi Thị Xuân
  - **D.** Lê Chân
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Hai Bà Trưng (Trưng Trắc, Trưng Nhị))
- **Giá trị giáo dục / Định hướng tư duy:** *Nữ kiệt anh hùng - Tôn vinh truyền thống anh dũng của phụ nữ Việt Nam*

### Câu 92: [gamesvr_questions.xml - ID 396]
- **Phân loại vi phạm:** `Tuyên truyền quốc gia 'Nước ta'` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'我国'*)
- **Lý do cần sửa:** Dùng cụm từ 'nước ta' ('我国') để nhồi nhét biểu tượng, ngày lễ, thủ đô, chính sách của Trung Quốc cho người chơi Việt Nam.
- **Câu hỏi cũ (Tiếng Trung):** `我国最早的字典是什么？`
- **Lựa chọn cũ:** A: `《说文解字》` | B: `《康熙字典》` | C: `《辞海》` | D: `` (Đáp án cũ: `1`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Món phở truyền thống thơm ngon đậm đà là tinh hoa ẩm thực nổi tiếng thế giới của đất nước nào?**
- **👉 Lựa chọn mới:**
  - **A.** Việt Nam
  - **B.** Thái Lan
  - **C.** Lào
  - **D.** Campuchia
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Việt Nam)
- **Giá trị giáo dục / Định hướng tư duy:** *Văn hóa ẩm thực - Món phở truyền thống Việt Nam*

### Câu 93: [gamesvr_questions.xml - ID 402]
- **Phân loại vi phạm:** `Tuyên truyền quốc gia 'Nước ta'` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'我国'*)
- **Lý do cần sửa:** Dùng cụm từ 'nước ta' ('我国') để nhồi nhét biểu tượng, ngày lễ, thủ đô, chính sách của Trung Quốc cho người chơi Việt Nam.
- **Câu hỏi cũ (Tiếng Trung):** `我国宋朝已建立了望火楼，担负防火任务的机构名称是什么？`
- **Lựa chọn cũ:** A: `潜火队` | B: `防隅军` | C: `军巡铺` | D: `` (Đáp án cũ: `3`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Chiếc nón lá truyền thống che mưa che nắng được làm chủ yếu từ lá cây gì?**
- **👉 Lựa chọn mới:**
  - **A.** Lá nón (lá cọ, lá thốt nốt)
  - **B.** Lá chuối
  - **C.** Lá dừa nước
  - **D.** Lá sen
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Lá nón (lá cọ, lá thốt nốt))
- **Giá trị giáo dục / Định hướng tư duy:** *Vật dụng dân gian - Chiếc nón lá bài thơ*

### Câu 94: [gamesvr_questions.xml - ID 404]
- **Phân loại vi phạm:** `Tuyên truyền quốc gia 'Nước ta'` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'我国'*)
- **Lý do cần sửa:** Dùng cụm từ 'nước ta' ('我国') để nhồi nhét biểu tượng, ngày lễ, thủ đô, chính sách của Trung Quốc cho người chơi Việt Nam.
- **Câu hỏi cũ (Tiếng Trung):** `你知道最早使用火的是我国的西候度人和什么人吗？`
- **Lựa chọn cũ:** A: `元谋人` | B: `北京人` | C: `蓝田人` | D: `` (Đáp án cũ: `2`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Lễ hội đền Hùng diễn ra hàng năm trên đỉnh núi Nghĩa Lĩnh thuộc tỉnh nào?**
- **👉 Lựa chọn mới:**
  - **A.** Phú Thọ
  - **B.** Vĩnh Phúc
  - **C.** Bắc Ninh
  - **D.** Thái Nguyên
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Phú Thọ)
- **Giá trị giáo dục / Định hướng tư duy:** *Tín ngưỡng dân tộc - Đền Hùng Phú Thọ*

### Câu 95: [gamesvr_questions.xml - ID 405]
- **Phân loại vi phạm:** `Tuyên truyền quốc gia 'Nước ta'` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'我国'*)
- **Lý do cần sửa:** Dùng cụm từ 'nước ta' ('我国') để nhồi nhét biểu tượng, ngày lễ, thủ đô, chính sách của Trung Quốc cho người chơi Việt Nam.
- **Câu hỏi cũ (Tiếng Trung):** `你知道我国从什么朝代开始用刑罚手段管理火政吗？`
- **Lựa chọn cũ:** A: `夏朝` | B: `商朝` | C: `周朝` | D: `` (Đáp án cũ: `2`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Hình ảnh chim Lạc bay liệng được chạm khắc tinh xảo trên bảo vật lịch sử nào của nền văn minh Đông Sơn?**
- **👉 Lựa chọn mới:**
  - **A.** Trống đồng Đông Sơn
  - **B.** Thạp đồng Đào Thịnh
  - **C.** Kiếm đồng
  - **D.** Chuông đồng
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Trống đồng Đông Sơn)
- **Giá trị giáo dục / Định hướng tư duy:** *Văn minh Đông Sơn - Trống đồng Đông Sơn cổ đại*

### Câu 96: [gamesvr_questions.xml - ID 406]
- **Phân loại vi phạm:** `Tuyên truyền quốc gia 'Nước ta'` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'我国'*)
- **Lý do cần sửa:** Dùng cụm từ 'nước ta' ('我国') để nhồi nhét biểu tượng, ngày lễ, thủ đô, chính sách của Trung Quốc cho người chơi Việt Nam.
- **Câu hỏi cũ (Tiếng Trung):** `我国最早的救火工具水囊、水袋，出现在哪个朝代？`
- **Lựa chọn cũ:** A: `唐代` | B: `宋朝` | C: `明朝` | D: `清朝` (Đáp án cũ: `1`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Cây đàn bầu của Việt Nam là nhạc cụ độc đáo chỉ có mấy dây nhưng phát ra âm thanh du dương?**
- **👉 Lựa chọn mới:**
  - **A.** 1 dây duy nhất
  - **B.** 2 dây
  - **C.** 3 dây
  - **D.** 4 dây
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (1 dây duy nhất)
- **Giá trị giáo dục / Định hướng tư duy:** *Nhạc cụ dân tộc - Tiếng đàn bầu nắn nót cung thanh*

### Câu 97: [gamesvr_questions.xml - ID 407]
- **Phân loại vi phạm:** `Tuyên truyền quốc gia 'Nước ta'` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'我国'*)
- **Lý do cần sửa:** Dùng cụm từ 'nước ta' ('我国') để nhồi nhét biểu tượng, ngày lễ, thủ đô, chính sách của Trung Quốc cho người chơi Việt Nam.
- **Câu hỏi cũ (Tiếng Trung):** `我国近代第一支消防队在哪个城市建立？`
- **Lựa chọn cũ:** A: `上海` | B: `北京` | C: `天津` | D: `广州` (Đáp án cũ: `1`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Rối nước là môn nghệ thuật biểu diễn dân gian độc đáo ra đời từ nền văn minh lúa nước của vùng nào?**
- **👉 Lựa chọn mới:**
  - **A.** Đồng bằng Bắc Bộ
  - **B.** Đồng bằng Nam Bộ
  - **C.** Duyên hải miền Trung
  - **D.** Tây Nguyên
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Đồng bằng Bắc Bộ)
- **Giá trị giáo dục / Định hướng tư duy:** *Nghệ thuật truyền thống - Múa rối nước Việt Nam*

### Câu 98: [gamesvr_questions.xml - ID 408]
- **Phân loại vi phạm:** `Tuyên truyền quốc gia 'Nước ta'` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'我国'*)
- **Lý do cần sửa:** Dùng cụm từ 'nước ta' ('我国') để nhồi nhét biểu tượng, ngày lễ, thủ đô, chính sách của Trung Quốc cho người chơi Việt Nam.
- **Câu hỏi cũ (Tiếng Trung):** `你知道我国近代第一批消火栓出现在哪一年吗？`
- **Lựa chọn cũ:** A: `1883` | B: `1905` | C: `1921` | D: `` (Đáp án cũ: `1`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Vị Trạng nguyên nhỏ tuổi nhất trong lịch sử khoa cử Việt Nam (đỗ Trạng nguyên năm 13 tuổi) là ai?**
- **👉 Lựa chọn mới:**
  - **A.** Nguyễn Hiền
  - **B.** Lương Thế Vinh
  - **C.** Lê Văn Hưu
  - **D.** Nguyễn Bỉnh Khiêm
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Nguyễn Hiền)
- **Giá trị giáo dục / Định hướng tư duy:** *Gương hiếu học - Trạng nguyên Nguyễn Hiền*

### Câu 99: [gamesvr_questions.xml - ID 413]
- **Phân loại vi phạm:** `Số điện thoại khẩn cấp` (Mức độ: **Cao (Nguy hiểm an toàn)** - Từ khóa phát hiện: *'火警'*)
- **Lý do cần sửa:** Sử dụng các số điện thoại khẩn cấp của Trung Quốc (110 công an, 119 cứu hỏa) gây hiểu lầm nguy hiểm trong đời sống tại Việt Nam.
- **Câu hỏi cũ (Tiếng Trung):** `成年人谎报火警的，将会被处以什么惩罚？`
- **Lựa chọn cũ:** A: `警告、罚款或拘留` | B: `拘留或劳动教养` | C: `行政处分或者刑罚` | D: `` (Đáp án cũ: `1`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Tại Việt Nam, hành vi cố ý gọi điện báo cháy giả tới tổng đài 114 sẽ bị xử lý như thế nào?**
- **👉 Lựa chọn mới:**
  - **A.** Không bị xử lý
  - **B.** Bị xử phạt vi phạm hành chính nặng và xử lý nghiêm theo pháp luật
  - **C.** Chỉ bị nhắc nhở
  - **D.** Được hoan nghênh
- **👉 Đáp án đúng mới:** **Lựa chọn 2** (Bị xử phạt vi phạm hành chính nặng và xử lý nghiêm theo pháp luật)
- **Giá trị giáo dục / Định hướng tư duy:** *Pháp luật đời sống - Giáo dục ý thức tôn trọng các đầu số cứu nạn khẩn cấp*

### Câu 100: [gamesvr_questions.xml - ID 423]
- **Phân loại vi phạm:** `Số điện thoại khẩn cấp` (Mức độ: **Cao (Nguy hiểm an toàn)** - Từ khóa phát hiện: *'报警'*)
- **Lý do cần sửa:** Sử dụng các số điện thoại khẩn cấp của Trung Quốc (110 công an, 119 cứu hỏa) gây hiểu lầm nguy hiểm trong đời sống tại Việt Nam.
- **Câu hỏi cũ (Tiếng Trung):** `向公安消防部门报警的内容有哪些？`
- **Lựa chọn cũ:** A: `单位名称、详细地址` | B: `起火物、火势情况` | C: `报警人的姓名、电话号码` | D: `上述都对` (Đáp án cũ: `4`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Khi gọi điện khẩn cấp báo cháy tới 114, thông tin quan trọng hàng đầu cần cung cấp chính xác là gì?**
- **👉 Lựa chọn mới:**
  - **A.** Sở thích cá nhân
  - **B.** Địa chỉ cụ thể nơi xảy ra cháy, chất cháy và có người mắc kẹt hay không
  - **C.** Thời tiết hôm nay
  - **D.** Tên bạn bè
- **👉 Đáp án đúng mới:** **Lựa chọn 2** (Địa chỉ cụ thể nơi xảy ra cháy, chất cháy và có người mắc kẹt hay không)
- **Giá trị giáo dục / Định hướng tư duy:** *Kỹ năng sống an toàn - Hướng dẫn kỹ năng báo tin cứu hộ khẩn cấp chuẩn xác*

### Câu 101: [gamesvr_questions.xml - ID 438]
- **Phân loại vi phạm:** `Số điện thoại khẩn cấp` (Mức độ: **Cao (Nguy hiểm an toàn)** - Từ khóa phát hiện: *'火警'*)
- **Lý do cần sửa:** Sử dụng các số điện thoại khẩn cấp của Trung Quốc (110 công an, 119 cứu hỏa) gây hiểu lầm nguy hiểm trong đời sống tại Việt Nam.
- **Câu hỏi cũ (Tiếng Trung):** `身边没有IC卡，是否可以拨打IC卡电话报火警呢？`
- **Lựa chọn cũ:** A: `可以` | B: `不可以` | C: `不一定可以` | D: `` (Đáp án cũ: `1`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Các đầu số gọi khẩn cấp quốc gia tại Việt Nam (113, 114, 115) từ điện thoại di động có mất cước phí không?**
- **👉 Lựa chọn mới:**
  - **A.** Rất đắt tiền
  - **B.** Hoàn toàn miễn phí cước và gọi được ngay cả khi tài khoản 0 đồng
  - **C.** Phải nạp thẻ trước
  - **D.** Phải đăng ký 4G
- **👉 Đáp án đúng mới:** **Lựa chọn 2** (Hoàn toàn miễn phí cước và gọi được ngay cả khi tài khoản 0 đồng)
- **Giá trị giáo dục / Định hướng tư duy:** *Kiến thức xã hội - Hiểu rõ quyền lợi và cách sử dụng tổng đài khẩn cấp*

### Câu 102: [gamesvr_questions.xml - ID 447]
- **Phân loại vi phạm:** `Tuyên truyền quốc gia 'Nước ta'` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'我国'*)
- **Lý do cần sửa:** Dùng cụm từ 'nước ta' ('我国') để nhồi nhét biểu tượng, ngày lễ, thủ đô, chính sách của Trung Quốc cho người chơi Việt Nam.
- **Câu hỏi cũ (Tiếng Trung):** `我国的位置在哪里？`
- **Lựa chọn cũ:** A: `亚洲东部，太平洋南岸` | B: `亚洲东部，太平洋西岸` | C: `亚洲西部，太平洋南岸` | D: `亚洲西部，太平洋东岸` (Đáp án cũ: `2`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Vị Trạng nguyên tài ba được mệnh danh là 'Trạng Lường' nhờ tài đo lường và tính toán toán học xuất chúng là ai?**
- **👉 Lựa chọn mới:**
  - **A.** Lương Thế Vinh
  - **B.** Nguyễn Hiền
  - **C.** Phùng Khắc Khoan
  - **D.** Lê Quý Đôn
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Lương Thế Vinh)
- **Giá trị giáo dục / Định hướng tư duy:** *Toán học cổ truyền - Trạng Lường Lương Thế Vinh*

### Câu 103: [gamesvr_questions.xml - ID 451]
- **Phân loại vi phạm:** `Tuyên truyền quốc gia 'Nước ta'` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'我国'*)
- **Lý do cần sửa:** Dùng cụm từ 'nước ta' ('我国') để nhồi nhét biểu tượng, ngày lễ, thủ đô, chính sách của Trung Quốc cho người chơi Việt Nam.
- **Câu hỏi cũ (Tiếng Trung):** `我国的陆地面积是多少？`
- **Lựa chọn cũ:** A: `900万平方千米` | B: `960万平方千米` | C: `980万平方千米` | D: `920万平方千米` (Đáp án cũ: `2`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Tập thơ 'Nhật ký trong tù' (Ngục trung nhật ký) bằng chữ Hán là sáng tác của ai?**
- **👉 Lựa chọn mới:**
  - **A.** Chủ tịch Hồ Chí Minh
  - **B.** Phan Bội Châu
  - **C.** Phan Châu Trinh
  - **D.** Tố Hữu
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Chủ tịch Hồ Chí Minh)
- **Giá trị giáo dục / Định hướng tư duy:** *Văn học cách mạng - Tập thơ Nhật ký trong tù*

### Câu 104: [gamesvr_questions.xml - ID 452]
- **Phân loại vi phạm:** `Tuyên truyền quốc gia 'Nước ta'` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'我国'*)
- **Lý do cần sửa:** Dùng cụm từ 'nước ta' ('我国') để nhồi nhét biểu tượng, ngày lễ, thủ đô, chính sách của Trung Quốc cho người chơi Việt Nam.
- **Câu hỏi cũ (Tiếng Trung):** `我国的四大海域位于哪个方向？`
- **Lựa chọn cũ:** A: `东面和南面` | B: `东面和北面` | C: `西面和南面` | D: `西面和北面` (Đáp án cũ: `1`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Hành tinh nào trong Hệ Mặt Trời nằm gần Mặt Trời nhất?**
- **👉 Lựa chọn mới:**
  - **A.** Sao Thủy (Mercury)
  - **B.** Sao Kim
  - **C.** Trái Đất
  - **D.** Sao Hỏa
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Sao Thủy (Mercury))
- **Giá trị giáo dục / Định hướng tư duy:** *Thiên văn học - Vị trí của Sao Thủy trong Hệ Mặt Trời*

### Câu 105: [gamesvr_questions.xml - ID 454]
- **Phân loại vi phạm:** `Tuyên truyền quốc gia 'Nước ta'` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'我国'*)
- **Lý do cần sửa:** Dùng cụm từ 'nước ta' ('我国') để nhồi nhét biểu tượng, ngày lễ, thủ đô, chính sách của Trung Quốc cho người chơi Việt Nam.
- **Câu hỏi cũ (Tiếng Trung):** `我国陆地面积居世界第几位？`
- **Lựa chọn cũ:** A: `第一位` | B: `第二位` | C: `第三位` | D: `第四位` (Đáp án cũ: `3`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Hành tinh nào lớn nhất trong toàn bộ Hệ Mặt Trời của chúng ta?**
- **👉 Lựa chọn mới:**
  - **A.** Sao Mộc (Jupiter)
  - **B.** Sao Thổ
  - **C.** Sao Hải Vương
  - **D.** Sao Thiên Vương
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Sao Mộc (Jupiter))
- **Giá trị giáo dục / Định hướng tư duy:** *Thiên văn học - Kích thước khổng lồ của Sao Mộc*

### Câu 106: [gamesvr_questions.xml - ID 457]
- **Phân loại vi phạm:** `Tuyên truyền quốc gia 'Nước ta'` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'我国'*)
- **Lý do cần sửa:** Dùng cụm từ 'nước ta' ('我国') để nhồi nhét biểu tượng, ngày lễ, thủ đô, chính sách của Trung Quốc cho người chơi Việt Nam.
- **Câu hỏi cũ (Tiếng Trung):** `我国的海域面积有多少？`
- **Lựa chọn cũ:** A: `100万平方千米` | B: `200万平方千米` | C: `300万平方千米` | D: `400万平方千米` (Đáp án cũ: `3`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Khí nào chiếm tỉ lệ thể tích lớn nhất trong bầu khí quyển của Trái Đất (khoảng 78%)?**
- **👉 Lựa chọn mới:**
  - **A.** Khí Nitơ
  - **B.** Khí Oxy
  - **C.** Khí Cacbonic
  - **D.** Khí Hiđrô
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Khí Nitơ)
- **Giá trị giáo dục / Định hướng tư duy:** *Khoa học khí quyển - Thành phần không khí Trái Đất*

### Câu 107: [gamesvr_questions.xml - ID 460]
- **Phân loại vi phạm:** `Tuyên truyền quốc gia 'Nước ta'` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'中国'*)
- **Lý do cần sửa:** Dùng cụm từ 'nước ta' ('我国') để nhồi nhét biểu tượng, ngày lễ, thủ đô, chính sách của Trung Quốc cho người chơi Việt Nam.
- **Câu hỏi cũ (Tiếng Trung):** `哪个国家的陆地面积位于世界第二？`
- **Lựa chọn cũ:** A: `美国` | B: `中国` | C: `俄罗斯` | D: `加拿大` (Đáp án cũ: `4`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Chất diệp lục trong lá cây giúp cây thực hiện quá trình quang hợp có màu gì?**
- **👉 Lựa chọn mới:**
  - **A.** Màu xanh lục
  - **B.** Màu vàng
  - **C.** Màu đỏ
  - **D.** Màu tím
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Màu xanh lục)
- **Giá trị giáo dục / Định hướng tư duy:** *Sinh học thực vật - Tác dụng của chất diệp lục*

### Câu 108: [gamesvr_questions.xml - ID 464]
- **Phân loại vi phạm:** `Tuyên truyền quốc gia 'Nước ta'` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'我国'*)
- **Lý do cần sửa:** Dùng cụm từ 'nước ta' ('我国') để nhồi nhét biểu tượng, ngày lễ, thủ đô, chính sách của Trung Quốc cho người chơi Việt Nam.
- **Câu hỏi cũ (Tiếng Trung):** `我国的四大海域是哪个大洋的一部分？`
- **Lựa chọn cũ:** A: `北冰洋` | B: `太平洋` | C: `大西洋` | D: `印度洋` (Đáp án cũ: `2`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Trong cơ thể người, cơ quan nào hoạt động như một chiếc máy bơm liên tục bơm máu đi khắp cơ thể?**
- **👉 Lựa chọn mới:**
  - **A.** Trái tim
  - **B.** Lá phổi
  - **C.** Bộ não
  - **D.** Dạ dày
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Trái tim)
- **Giá trị giáo dục / Định hướng tư duy:** *Cơ thể người - Chức năng của hệ tuần hoàn và quả tim*

### Câu 109: [gamesvr_questions.xml - ID 465]
- **Phân loại vi phạm:** `Tuyên truyền quốc gia 'Nước ta'` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'中国'*)
- **Lý do cần sửa:** Dùng cụm từ 'nước ta' ('我国') để nhồi nhét biểu tượng, ngày lễ, thủ đô, chính sách của Trung Quốc cho người chơi Việt Nam.
- **Câu hỏi cũ (Tiếng Trung):** `哪个国家的陆地面积居世界第一？`
- **Lựa chọn cũ:** A: `中国` | B: `俄罗斯` | C: `美国` | D: `加拿大` (Đáp án cũ: `2`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Loài động vật có vú nào to lớn nhất từng tồn tại trên Trái Đất đang sinh sống dưới đại dương?**
- **👉 Lựa chọn mới:**
  - **A.** Cá voi xanh
  - **B.** Cá voi sát thủ
  - **C.** Cá mập voi
  - **D.** Voi châu Phi
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Cá voi xanh)
- **Giá trị giáo dục / Định hướng tư duy:** *Động vật học - Cá voi xanh khổng lồ*

### Câu 110: [gamesvr_questions.xml - ID 471]
- **Phân loại vi phạm:** `Số điện thoại khẩn cấp` (Mức độ: **Cao (Nguy hiểm an toàn)** - Từ khóa phát hiện: *'119'*)
- **Lý do cần sửa:** Sử dụng các số điện thoại khẩn cấp của Trung Quốc (110 công an, 119 cứu hỏa) gây hiểu lầm nguy hiểm trong đời sống tại Việt Nam.
- **Câu hỏi cũ (Tiếng Trung):** `着火后应自己先扑救，救不灭时再打“119”。这种做法正确吗？`
- **Lựa chọn cũ:** A: `正确` | B: `不正确` | C: `` | D: `` (Đáp án cũ: `2`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Tại Việt Nam, số điện thoại khẩn cấp 113 phục vụ cho lực lượng chức năng nào?**
- **👉 Lựa chọn mới:**
  - **A.** Cứu hỏa PCCC
  - **B.** Cảnh sát phản ứng nhanh giữ gìn an ninh trật tự
  - **C.** Cấp cứu y tế
  - **D.** Điện lực
- **👉 Đáp án đúng mới:** **Lựa chọn 2** (Cảnh sát phản ứng nhanh giữ gìn an ninh trật tự)
- **Giá trị giáo dục / Định hướng tư duy:** *Kỹ năng sống - Nhận biết đúng chức năng tổng đài Cảnh sát 113*

### Câu 111: [gamesvr_questions.xml - ID 473]
- **Phân loại vi phạm:** `Lịch sử & Phong kiến Trung Quốc` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'朝代'*)
- **Lý do cần sửa:** Câu hỏi thuần về các triều đại, hoàng đế phong kiến Trung Quốc, không mang lại giá trị tư duy và không phù hợp môi trường học đường Việt Nam.
- **Câu hỏi cũ (Tiếng Trung):** `故宫始建于哪个朝代？`
- **Lựa chọn cũ:** A: `唐朝` | B: `宋朝` | C: `元朝` | D: `明朝` (Đáp án cũ: `4`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Người thầy mẫu mực được người đời suy tôn là 'Vạn thế sư biểu' thời nhà Trần của nền giáo dục Việt Nam là ai?**
- **👉 Lựa chọn mới:**
  - **A.** Thầy Chu Văn An
  - **B.** Nguyễn Bỉnh Khiêm
  - **C.** Lê Quý Đôn
  - **D.** Lương Thế Vinh
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Thầy Chu Văn An)
- **Giá trị giáo dục / Định hướng tư duy:** *Truyền thống tôn sư trọng đạo - Tấm gương đạo đức trong sáng của nhà giáo Chu Văn An*

### Câu 112: [gamesvr_questions.xml - ID 474]
- **Phân loại vi phạm:** `Số điện thoại khẩn cấp` (Mức độ: **Cao (Nguy hiểm an toàn)** - Từ khóa phát hiện: *'报警'*)
- **Lý do cần sửa:** Sử dụng các số điện thoại khẩn cấp của Trung Quốc (110 công an, 119 cứu hỏa) gây hiểu lầm nguy hiểm trong đời sống tại Việt Nam.
- **Câu hỏi cũ (Tiếng Trung):** `报警人拨打火灾报警电话后，应该怎样做？`
- **Lựa chọn cũ:** A: `在家等候` | B: `不再理会此事` | C: `到门口或街上等候消防车到来` | D: `` (Đáp án cũ: `3`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Khi phát hiện người bị tai nạn nguy kịch hoặc đột quỵ cần cấp cứu y tế khẩn cấp, cần gọi tới số nào?**
- **👉 Lựa chọn mới:**
  - **A.** 114
  - **B.** 113
  - **C.** 115
  - **D.** 119
- **👉 Đáp án đúng mới:** **Lựa chọn 3** (115)
- **Giá trị giáo dục / Định hướng tư duy:** *Sơ cấp cứu y tế - Ghi nhớ tổng đài cấp cứu y tế 115*

### Câu 113: [gamesvr_questions.xml - ID 475]
- **Phân loại vi phạm:** `Tuyên truyền quốc gia 'Nước ta'` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'中国'*)
- **Lý do cần sửa:** Dùng cụm từ 'nước ta' ('我国') để nhồi nhét biểu tượng, ngày lễ, thủ đô, chính sách của Trung Quốc cho người chơi Việt Nam.
- **Câu hỏi cũ (Tiếng Trung):** `中国野生动物保护协会的会徽上画的是什么动物？`
- **Lựa chọn cũ:** A: `丹顶鹤` | B: `大熊猫` | C: `骆驼` | D: `` (Đáp án cũ: `2`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Loại vitamin nào được cơ thể người tự tổng hợp dưới da khi tiếp xúc với ánh nắng mặt trời sáng sớm?**
- **👉 Lựa chọn mới:**
  - **A.** Vitamin D
  - **B.** Vitamin A
  - **C.** Vitamin C
  - **D.** Vitamin B
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Vitamin D)
- **Giá trị giáo dục / Định hướng tư duy:** *Sức khỏe - Tác dụng tắm nắng tạo Vitamin D*

### Câu 114: [gamesvr_questions.xml - ID 481]
- **Phân loại vi phạm:** `Tuyên truyền quốc gia 'Nước ta'` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'我国'*)
- **Lý do cần sửa:** Dùng cụm từ 'nước ta' ('我国') để nhồi nhét biểu tượng, ngày lễ, thủ đô, chính sách của Trung Quốc cho người chơi Việt Nam.
- **Câu hỏi cũ (Tiếng Trung):** `我国绝大部分地区位于哪里？`
- **Lựa chọn cũ:** A: `温带` | B: `热带` | C: `亚热带` | D: `寒带` (Đáp án cũ: `1`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Nước tinh khiết bắt đầu đóng băng thành thể rắn ở nhiệt độ bao nhiêu độ C?**
- **👉 Lựa chọn mới:**
  - **A.** 0 độ C
  - **B.** -10 độ C
  - **C.** 4 độ C
  - **D.** 100 độ C
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (0 độ C)
- **Giá trị giáo dục / Định hướng tư duy:** *Vật lý thường thức - Điểm đóng băng của nước*

### Câu 115: [gamesvr_questions.xml - ID 503]
- **Phân loại vi phạm:** `Số điện thoại khẩn cấp` (Mức độ: **Cao (Nguy hiểm an toàn)** - Từ khóa phát hiện: *'报警'*)
- **Lý do cần sửa:** Sử dụng các số điện thoại khẩn cấp của Trung Quốc (110 công an, 119 cứu hỏa) gây hiểu lầm nguy hiểm trong đời sống tại Việt Nam.
- **Câu hỏi cũ (Tiếng Trung):** `任何人发现火灾时，都应当怎样？`
- **Lựa chọn cũ:** A: `视而不见` | B: `立即报警` | C: `马上灭火` | D: `` (Đáp án cũ: `2`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Khi phát hiện đám cháy trong nhà, việc đầu tiên cần làm là gì?**
- **👉 Lựa chọn mới:**
  - **A.** Quay video đăng mạng xã hội
  - **B.** Hô hoán báo động, nhanh chóng thoát hiểm và gọi ngay 114
  - **C.** Vào gầm giường trốn
  - **D.** Tìm đồ chơi mang theo
- **👉 Đáp án đúng mới:** **Lựa chọn 2** (Hô hoán báo động, nhanh chóng thoát hiểm và gọi ngay 114)
- **Giá trị giáo dục / Định hướng tư duy:** *Kỹ năng thoát hiểm - Ưu tiên bảo toàn tính mạng và báo động cứu nạn kịp thời*

### Câu 116: [gamesvr_questions.xml - ID 522]
- **Phân loại vi phạm:** `Tuyên truyền quốc gia 'Nước ta'` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'中国'*)
- **Lý do cần sửa:** Dùng cụm từ 'nước ta' ('我国') để nhồi nhét biểu tượng, ngày lễ, thủ đô, chính sách của Trung Quốc cho người chơi Việt Nam.
- **Câu hỏi cũ (Tiếng Trung):** `第一包方便面诞生在哪个国家？`
- **Lựa chọn cũ:** A: `美国` | B: `日本` | C: `英国` | D: `中国` (Đáp án cũ: `2`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Nước nguyên chất bắt đầu sôi và chuyển thành thể khí ở điều kiện tiêu chuẩn tại bao nhiêu độ C?**
- **👉 Lựa chọn mới:**
  - **A.** 100 độ C
  - **B.** 80 độ C
  - **C.** 90 độ C
  - **D.** 120 độ C
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (100 độ C)
- **Giá trị giáo dục / Định hướng tư duy:** *Vật lý thường thức - Điểm sôi của nước*

### Câu 117: [gamesvr_questions.xml - ID 525]
- **Phân loại vi phạm:** `Tuyên truyền quốc gia 'Nước ta'` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'中国'*)
- **Lý do cần sửa:** Dùng cụm từ 'nước ta' ('我国') để nhồi nhét biểu tượng, ngày lễ, thủ đô, chính sách của Trung Quốc cho người chơi Việt Nam.
- **Câu hỏi cũ (Tiếng Trung):** `中国的国花是什么花？`
- **Lựa chọn cũ:** A: `玫瑰` | B: `桃花` | C: `牡丹` | D: `` (Đáp án cũ: `3`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Vận tốc ánh sáng truyền trong môi trường chân không xấp xỉ đạt bao nhiêu km mỗi giây?**
- **👉 Lựa chọn mới:**
  - **A.** Khoảng 300.000 km/s
  - **B.** Khoảng 3.000 km/s
  - **C.** Khoảng 30.000 km/s
  - **D.** Khoảng 1.000.000 km/s
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Khoảng 300.000 km/s)
- **Giá trị giáo dục / Định hướng tư duy:** *Vật lý hiện đại - Tốc độ ánh sáng cực đại trong vũ trụ*

### Câu 118: [gamesvr_questions.xml - ID 530]
- **Phân loại vi phạm:** `Tuyên truyền quốc gia 'Nước ta'` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'我国'*)
- **Lý do cần sửa:** Dùng cụm từ 'nước ta' ('我国') để nhồi nhét biểu tượng, ngày lễ, thủ đô, chính sách của Trung Quốc cho người chơi Việt Nam.
- **Câu hỏi cũ (Tiếng Trung):** `我国有多少个民族？`
- **Lựa chọn cũ:** A: `55个` | B: `56个` | C: `57个` | D: `58个` (Đáp án cũ: `2`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Loài cây nào có khả năng sinh sống tốt trong môi trường sa mạc khô hạn nhờ thân mọng nước và lá biến thành gai?**
- **👉 Lựa chọn mới:**
  - **A.** Cây xương rồng
  - **B.** Cây dương xỉ
  - **C.** Cây thông
  - **D.** Cây bèo tây
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Cây xương rồng)
- **Giá trị giáo dục / Định hướng tư duy:** *Thích nghi sinh học - Cây xương rồng trên sa mạc*

### Câu 119: [gamesvr_questions.xml - ID 535]
- **Phân loại vi phạm:** `Tuyên truyền quốc gia 'Nước ta'` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'我国'*)
- **Lý do cần sửa:** Dùng cụm từ 'nước ta' ('我国') để nhồi nhét biểu tượng, ngày lễ, thủ đô, chính sách của Trung Quốc cho người chơi Việt Nam.
- **Câu hỏi cũ (Tiếng Trung):** `我国第一大高原是哪个？`
- **Lựa chọn cũ:** A: `内蒙古高原` | B: `青藏高原` | C: `云贵高原` | D: `黄土高原` (Đáp án cũ: `2`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Côn trùng nào được coi là 'kiến trúc sư tự nhiên' chăm chỉ hút mật hoa và thụ phấn cho cây trồng?**
- **👉 Lựa chọn mới:**
  - **A.** Con ong mật
  - **B.** Con bướm
  - **C.** Con ruồi
  - **D.** Con chuồn chuồn
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Con ong mật)
- **Giá trị giáo dục / Định hướng tư duy:** *Thế giới côn trùng - Lợi ích của loài ong mật*

### Câu 120: [gamesvr_questions.xml - ID 542]
- **Phân loại vi phạm:** `Tuyên truyền quốc gia 'Nước ta'` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'中国'*)
- **Lý do cần sửa:** Dùng cụm từ 'nước ta' ('我国') để nhồi nhét biểu tượng, ngày lễ, thủ đô, chính sách của Trung Quốc cho người chơi Việt Nam.
- **Câu hỏi cũ (Tiếng Trung):** `中国历史上杰出的天文学家是谁？`
- **Lựa chọn cũ:** A: `吴道子` | B: `李时珍` | C: `李白` | D: `张衡` (Đáp án cũ: `4`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Đơn vị nhỏ nhất cấu tạo nên mọi vật chất sống trong tự nhiên là gì?**
- **👉 Lựa chọn mới:**
  - **A.** Tế bào
  - **B.** Nguyên tử
  - **C.** Phân tử
  - **D.** Mô
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Tế bào)
- **Giá trị giáo dục / Định hướng tư duy:** *Sinh học đại cương - Tế bào đơn vị của sự sống*

### Câu 121: [gamesvr_questions.xml - ID 570]
- **Phân loại vi phạm:** `Tuyên truyền quốc gia 'Nước ta'` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'中国'*)
- **Lý do cần sửa:** Dùng cụm từ 'nước ta' ('我国') để nhồi nhét biểu tượng, ngày lễ, thủ đô, chính sách của Trung Quốc cho người chơi Việt Nam.
- **Câu hỏi cũ (Tiếng Trung):** `中国是何时参加奥运会的？`
- **Lựa chọn cũ:** A: `1921年` | B: `1922年` | C: `1923年` | D: `1924年` (Đáp án cũ: `4`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Loại khí nào cần thiết cho quá trình hô hấp của con người và hầu hết các sinh vật hiếu khí trên Trái Đất?**
- **👉 Lựa chọn mới:**
  - **A.** Khí Oxy
  - **B.** Khí Cacbonic
  - **C.** Khí Mêtan
  - **D.** Khí Nitơ
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Khí Oxy)
- **Giá trị giáo dục / Định hướng tư duy:** *Hô hấp sinh học - Tầm quan trọng của khí Oxy*

### Câu 122: [gamesvr_questions.xml - ID 573]
- **Phân loại vi phạm:** `Tuyên truyền quốc gia 'Nước ta'` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'中国'*)
- **Lý do cần sửa:** Dùng cụm từ 'nước ta' ('我国') để nhồi nhét biểu tượng, ngày lễ, thủ đô, chính sách của Trung Quốc cho người chơi Việt Nam.
- **Câu hỏi cũ (Tiếng Trung):** `中国最早的名医是谁？`
- **Lựa chọn cũ:** A: `扁鹊` | B: `华佗` | C: `李时珍` | D: `孙思邈` (Đáp án cũ: `1`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Nguồn năng lượng tự nhiên vô tận chiếu sáng và sưởi ấm toàn bộ Trái Đất đến từ đâu?**
- **👉 Lựa chọn mới:**
  - **A.** Mặt Trời
  - **B.** Mặt Trăng
  - **C.** Sao Kim
  - **D.** Các vì sao xa
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Mặt Trời)
- **Giá trị giáo dục / Định hướng tư duy:** *Vũ trụ học - Mặt Trời nguồn cội sự sống*

### Câu 123: [gamesvr_questions.xml - ID 590]
- **Phân loại vi phạm:** `Đố chữ Hán & Chiết tự` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'笔画'*)
- **Lý do cần sửa:** Đố chiết tự chữ tượng hình hoặc thành ngữ Hán ngữ cổ mà người chơi Việt Nam không thể suy luận logic.
- **Câu hỏi cũ (Tiếng Trung):** `“凸”字的笔画数是多少？`
- **Lựa chọn cũ:** A: `3` | B: `4` | C: `5` | D: `6` (Đáp án cũ: `3`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Con gì đầu đội hai sừng, bốn chân guốc sắt kéo cày đồng sâu?**
- **👉 Lựa chọn mới:**
  - **A.** Con trâu
  - **B.** Con ngựa
  - **C.** Con hươu
  - **D.** Con dê
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Con trâu)
- **Giá trị giáo dục / Định hướng tư duy:** *Câu đố dân gian - Con trâu là đầu cơ nghiệp người nông dân*

### Câu 124: [gamesvr_questions.xml - ID 591]
- **Phân loại vi phạm:** `Đố chữ Hán & Chiết tự` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'汉字'*)
- **Lý do cần sửa:** Đố chiết tự chữ tượng hình hoặc thành ngữ Hán ngữ cổ mà người chơi Việt Nam không thể suy luận logic.
- **Câu hỏi cũ (Tiếng Trung):** `汉字的五种基本笔画是横、竖、撇、点和什么？`
- **Lựa chọn cũ:** A: `捺` | B: `折` | C: `提` | D: `勾` (Đáp án cũ: `2`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Con gì cõng ngôi nhà trên lưng, đi đâu cũng bò chậm chạp từng bước?**
- **👉 Lựa chọn mới:**
  - **A.** Con ốc sên (hoặc con rùa)
  - **B.** Con cua
  - **C.** Con tôm
  - **D.** Con cá chép
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Con ốc sên (hoặc con rùa))
- **Giá trị giáo dục / Định hướng tư duy:** *Câu đố dân gian - Chiếc mai bảo vệ của chú ốc sên*

### Câu 125: [gamesvr_questions.xml - ID 594]
- **Phân loại vi phạm:** `Tuyên truyền quốc gia 'Nước ta'` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'中国'*)
- **Lý do cần sửa:** Dùng cụm từ 'nước ta' ('我国') để nhồi nhét biểu tượng, ngày lễ, thủ đô, chính sách của Trung Quốc cho người chơi Việt Nam.
- **Câu hỏi cũ (Tiếng Trung):** `中国学生营养日是每年的哪一天？`
- **Lựa chọn cũ:** A: `5月20日` | B: `4月20日` | C: `5月10日` | D: `3月20日` (Đáp án cũ: `1`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Vệ tinh tự nhiên duy nhất quay quanh hành tinh Trái Đất của chúng ta là gì?**
- **👉 Lựa chọn mới:**
  - **A.** Mặt Trăng
  - **B.** Sao Hỏa
  - **C.** Sao Kim
  - **D.** Trạm vũ trụ
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Mặt Trăng)
- **Giá trị giáo dục / Định hướng tư duy:** *Thiên văn học - Mặt Trăng người bạn đồng hành của Trái Đất*

### Câu 126: [class_questions.xml - ID 15]
- **Phân loại vi phạm:** `Đố chữ Hán & Chiết tự` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'成语'*)
- **Lý do cần sửa:** Đố chiết tự chữ tượng hình hoặc thành ngữ Hán ngữ cổ mà người chơi Việt Nam không thể suy luận logic.
- **Câu hỏi cũ (Tiếng Trung):** `你能根据这些数字“12345609”猜一句成语吗？`
- **Lựa chọn cũ:** A: `七零八落` | B: `七上八下` | C: `` | D: `` (Đáp án cũ: `1`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Con gì tám cẳng hai càng, chẳng đi thẳng lối mà bò ngang ngang?**
- **👉 Lựa chọn mới:**
  - **A.** Con cua
  - **B.** Con ốc
  - **C.** Con sò
  - **D.** Con nghêu
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Con cua)
- **Giá trị giáo dục / Định hướng tư duy:** *Câu đố dân gian - Điệu bò ngang đặc trưng của chú cua đồng*

### Câu 127: [class_questions.xml - ID 27]
- **Phân loại vi phạm:** `Đố chữ Hán & Chiết tự` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'字谜'*)
- **Lý do cần sửa:** Đố chiết tự chữ tượng hình hoặc thành ngữ Hán ngữ cổ mà người chơi Việt Nam không thể suy luận logic.
- **Câu hỏi cũ (Tiếng Trung):** `两点水（字谜）？`
- **Lựa chọn cũ:** A: `冷` | B: `冰` | C: `淼` | D: `` (Đáp án cũ: `2`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Con gì chỉ bay lượn ban đêm, ngủ treo ngược cành cây và định vị bằng sóng âm?**
- **👉 Lựa chọn mới:**
  - **A.** Con dơi
  - **B.** Con cú mèo
  - **C.** Con đại bàng
  - **D.** Con bồ câu
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Con dơi)
- **Giá trị giáo dục / Định hướng tư duy:** *Câu đố sinh học - Loài dơi thú biết bay duy nhất*

### Câu 128: [class_questions.xml - ID 28]
- **Phân loại vi phạm:** `Đố chữ Hán & Chiết tự` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'成语'*)
- **Lý do cần sửa:** Đố chiết tự chữ tượng hình hoặc thành ngữ Hán ngữ cổ mà người chơi Việt Nam không thể suy luận logic.
- **Câu hỏi cũ (Tiếng Trung):** `小白真像他哥哥？(猜成语)`
- **Lựa chọn cũ:** A: `惟妙惟肖` | B: `一模一样` | C: `真相大白` | D: `` (Đáp án cũ: `3`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Cây gì thân thẳng vươn cao, ruột rỗng thành gióng kết thành lũy làng xanh ngắt?**
- **👉 Lựa chọn mới:**
  - **A.** Cây tre
  - **B.** Cây cau
  - **C.** Cây đa
  - **D.** Cây dừa
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Cây tre)
- **Giá trị giáo dục / Định hướng tư duy:** *Câu đố quê hương - Hình tượng cây tre Việt Nam bất khuất*

### Câu 129: [class_questions.xml - ID 29]
- **Phân loại vi phạm:** `Đố chữ Hán & Chiết tự` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'字谜'*)
- **Lý do cần sửa:** Đố chiết tự chữ tượng hình hoặc thành ngữ Hán ngữ cổ mà người chơi Việt Nam không thể suy luận logic.
- **Câu hỏi cũ (Tiếng Trung):** `挥手告别。（字谜）`
- **Lựa chọn cũ:** A: `军` | B: `车` | C: `捌` | D: `` (Đáp án cũ: `1`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Cây gì trổ bông màu vàng, kết hạt ngọc trắng nuôi sống bao đời người Việt Nam?**
- **👉 Lựa chọn mới:**
  - **A.** Cây lúa
  - **B.** Cây ngô
  - **C.** Cây khoai
  - **D.** Cây sắn
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Cây lúa)
- **Giá trị giáo dục / Định hướng tư duy:** *Câu đố đồng quê - Cây lúa nuôi sống triệu triệu người*

### Câu 130: [class_questions.xml - ID 32]
- **Phân loại vi phạm:** `Đố chữ Hán & Chiết tự` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'字谜'*)
- **Lý do cần sửa:** Đố chiết tự chữ tượng hình hoặc thành ngữ Hán ngữ cổ mà người chơi Việt Nam không thể suy luận logic.
- **Câu hỏi cũ (Tiếng Trung):** `林字多一半。（字谜）`
- **Lựa chọn cũ:** A: `森` | B: `梦` | C: `` | D: `` (Đáp án cũ: `2`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Cây gì nghiêng bóng bờ ao, quả treo lủng lẳng đầy dòng nước mát ngọt lành?**
- **👉 Lựa chọn mới:**
  - **A.** Cây dừa
  - **B.** Cây bưởi
  - **C.** Cây chuối
  - **D.** Cây ổi
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Cây dừa)
- **Giá trị giáo dục / Định hướng tư duy:** *Câu đố thiên nhiên - Cây dừa rợp mát bóng bờ kênh*

### Câu 131: [class_questions.xml - ID 34]
- **Phân loại vi phạm:** `Đố chữ Hán & Chiết tự` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'成语'*)
- **Lý do cần sửa:** Đố chiết tự chữ tượng hình hoặc thành ngữ Hán ngữ cổ mà người chơi Việt Nam không thể suy luận logic.
- **Câu hỏi cũ (Tiếng Trung):** `你能根据下面的数字“333555”猜一句成语吗？`
- **Lựa chọn cũ:** A: `三心二意` | B: `三五成群` | C: `` | D: `` (Đáp án cũ: `2`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Cây gì lá to như cái quạt mo, buồng quả trĩu trịt chín vàng thơm lừng?**
- **👉 Lựa chọn mới:**
  - **A.** Cây chuối
  - **B.** Cây đu đủ
  - **C.** Cây xoài
  - **D.** Cây nhãn
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Cây chuối)
- **Giá trị giáo dục / Định hướng tư duy:** *Câu đố vườn cây - Cây chuối quen thuộc ở làng quê*

### Câu 132: [class_questions.xml - ID 36]
- **Phân loại vi phạm:** `Đố chữ Hán & Chiết tự` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'字谜'*)
- **Lý do cần sửa:** Đố chiết tự chữ tượng hình hoặc thành ngữ Hán ngữ cổ mà người chơi Việt Nam không thể suy luận logic.
- **Câu hỏi cũ (Tiếng Trung):** `百无一失。（字谜）`
- **Lựa chọn cũ:** A: `兀` | B: `天` | C: `白` | D: `` (Đáp án cũ: `3`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Quả gì vỏ xanh ruột đỏ, hạt đen nhánh, sinh ra từ truyền thuyết Mai An Tiêm ngoài đảo hoang?**
- **👉 Lựa chọn mới:**
  - **A.** Quả dưa hấu
  - **B.** Quả thanh long
  - **C.** Quả lựu
  - **D.** Quả gấc
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Quả dưa hấu)
- **Giá trị giáo dục / Định hướng tư duy:** *Sự tích dân gian - Quả dưa hấu ngọt lành*

### Câu 133: [class_questions.xml - ID 37]
- **Phân loại vi phạm:** `Đố chữ Hán & Chiết tự` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'成语'*)
- **Lý do cần sửa:** Đố chiết tự chữ tượng hình hoặc thành ngữ Hán ngữ cổ mà người chơi Việt Nam không thể suy luận logic.
- **Câu hỏi cũ (Tiếng Trung):** `笑死人。（猜成语）`
- **Lựa chọn cũ:** A: `欢欢喜喜` | B: `否极泰来` | C: `乐极生悲` | D: `` (Đáp án cũ: `3`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Quả gì gai góc xù xì, mùi thơm ngào ngạt chia thành từng múi béo ngậy được coi là vua các loại trái cây miền Tây?**
- **👉 Lựa chọn mới:**
  - **A.** Quả sầu riêng
  - **B.** Quả mít
  - **C.** Quả chôm chôm
  - **D.** Quả mãng cầu
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Quả sầu riêng)
- **Giá trị giáo dục / Định hướng tư duy:** *Đặc sản phương Nam - Quả sầu riêng nức tiếng*

### Câu 134: [class_questions.xml - ID 49]
- **Phân loại vi phạm:** `Đố chữ Hán & Chiết tự` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'字谜'*)
- **Lý do cần sửa:** Đố chiết tự chữ tượng hình hoặc thành ngữ Hán ngữ cổ mà người chơi Việt Nam không thể suy luận logic.
- **Câu hỏi cũ (Tiếng Trung):** `唇齿相依。（字谜）`
- **Lựa chọn cũ:** A: `叩` | B: `呀` | C: `啃` | D: `` (Đáp án cũ: `2`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Cái gì đen khi bạn mua về, đỏ rực khi đang nấu nướng và xám tro khi vứt đi?**
- **👉 Lựa chọn mới:**
  - **A.** Hòn than củi / than tổ ong
  - **B.** Cục sắt
  - **C.** Thanh gỗ
  - **D.** Nồi cơm điện
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Hòn than củi / than tổ ong)
- **Giá trị giáo dục / Định hướng tư duy:** *Câu đố vật dụng - Sự biến đổi màu sắc của than đốt*

### Câu 135: [class_questions.xml - ID 53]
- **Phân loại vi phạm:** `Đố chữ Hán & Chiết tự` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'字谜'*)
- **Lý do cần sửa:** Đố chiết tự chữ tượng hình hoặc thành ngữ Hán ngữ cổ mà người chơi Việt Nam không thể suy luận logic.
- **Câu hỏi cũ (Tiếng Trung):** `一箭穿心。（字谜）`
- **Lựa chọn cũ:** A: `必` | B: `心` | C: `几` | D: `` (Đáp án cũ: `1`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Cái gì có hai cánh mỏng tanh, kẹp vào cắt đứt giấy mềm vải êm nhưng không cắt được nước?**
- **👉 Lựa chọn mới:**
  - **A.** Cái kéo
  - **B.** Cái dao
  - **C.** Cái kìm
  - **D.** Cái cưa
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Cái kéo)
- **Giá trị giáo dục / Định hướng tư duy:** *Đồ dùng học tập - Chiếc kéo thủ công khéo léo*

### Câu 136: [class_questions.xml - ID 58]
- **Phân loại vi phạm:** `Đố chữ Hán & Chiết tự` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'字谜'*)
- **Lý do cần sửa:** Đố chiết tự chữ tượng hình hoặc thành ngữ Hán ngữ cổ mà người chơi Việt Nam không thể suy luận logic.
- **Câu hỏi cũ (Tiếng Trung):** `纵横交错。（字谜）`
- **Lựa chọn cũ:** A: `井` | B: `十` | C: `土` | D: `` (Đáp án cũ: `2`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Cái gì đứng suốt đêm ngày, kim quay tí tách nhắc ta đúng giờ học tập?**
- **👉 Lựa chọn mới:**
  - **A.** Chiếc đồng hồ
  - **B.** Chiếc quạt
  - **C.** Bức tranh
  - **D.** Chiếc bàn
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Chiếc đồng hồ)
- **Giá trị giáo dục / Định hướng tư duy:** *Vật dụng quen thuộc - Chiếc đồng hồ báo thức*

### Câu 137: [class_questions.xml - ID 60]
- **Phân loại vi phạm:** `Đố chữ Hán & Chiết tự` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'字谜'*)
- **Lý do cần sửa:** Đố chiết tự chữ tượng hình hoặc thành ngữ Hán ngữ cổ mà người chơi Việt Nam không thể suy luận logic.
- **Câu hỏi cũ (Tiếng Trung):** `三人去看日出。（字谜）`
- **Lựa chọn cũ:** A: `春` | B: `晶` | C: `` | D: `` (Đáp án cũ: `1`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Cái gì bạn nhìn vào thấy mình ở trong đó, bạn cười nó cười bạn khóc nó khóc?**
- **👉 Lựa chọn mới:**
  - **A.** Tấm gương soi
  - **B.** Cửa sổ
  - **C.** Bức tường
  - **D.** Quyển sách
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Tấm gương soi)
- **Giá trị giáo dục / Định hướng tư duy:** *Câu đố đồ vật - Tấm gương phản chiếu chân thật*

### Câu 138: [class_questions.xml - ID 62]
- **Phân loại vi phạm:** `Đố chữ Hán & Chiết tự` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'字谜'*)
- **Lý do cần sửa:** Đố chiết tự chữ tượng hình hoặc thành ngữ Hán ngữ cổ mà người chơi Việt Nam không thể suy luận logic.
- **Câu hỏi cũ (Tiếng Trung):** `四个人搬木头。（字谜）`
- **Lựa chọn cũ:** A: `森` | B: `李` | C: `杰` | D: `` (Đáp án cũ: `3`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Cái gì đi theo bạn dưới ánh nắng mặt trời, bạn chạy nó chạy bạn dừng nó dừng nhưng bóng tối thì biến mất?**
- **👉 Lựa chọn mới:**
  - **A.** Cái bóng của bạn
  - **B.** Đôi giày
  - **C.** Cái mũ
  - **D.** Chiếc áo
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Cái bóng của bạn)
- **Giá trị giáo dục / Định hướng tư duy:** *Hiện tượng quang học - Chiếc bóng trung thành*

### Câu 139: [class_questions.xml - ID 64]
- **Phân loại vi phạm:** `Đố chữ Hán & Chiết tự` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'字谜'*)
- **Lý do cần sửa:** Đố chiết tự chữ tượng hình hoặc thành ngữ Hán ngữ cổ mà người chơi Việt Nam không thể suy luận logic.
- **Câu hỏi cũ (Tiếng Trung):** `上下难分。（字谜）`
- **Lựa chọn cũ:** A: `卡` | B: `肯` | C: `吓` | D: `` (Đáp án cũ: `1`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Cái gì thân tròn nhỏ bé, thắp sáng trong đêm rồi tự rơi lệ tan chảy hết mình?**
- **👉 Lựa chọn mới:**
  - **A.** Cây nến (cây đèn cầy)
  - **B.** Bóng đèn
  - **C.** Bếp ga
  - **D.** Que diêm
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Cây nến (cây đèn cầy))
- **Giá trị giáo dục / Định hướng tư duy:** *Câu đố tượng hình - Cây nến thắp sáng giọt lệ lung linh*

### Câu 140: [class_questions.xml - ID 66]
- **Phân loại vi phạm:** `Đố chữ Hán & Chiết tự` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'字谜'*)
- **Lý do cần sửa:** Đố chiết tự chữ tượng hình hoặc thành ngữ Hán ngữ cổ mà người chơi Việt Nam không thể suy luận logic.
- **Câu hỏi cũ (Tiếng Trung):** `直冲云霄。（字谜）`
- **Lựa chọn cũ:** A: `去` | B: `肖` | C: `` | D: `` (Đáp án cũ: `1`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Cái gì bơi lội trên sông mang người qua lại, không có chân tay mà lướt sóng băng băng?**
- **👉 Lựa chọn mới:**
  - **A.** Chiếc thuyền / Chiếc ghe
  - **B.** Cái cầu
  - **C.** Cái phao
  - **D.** Cái bè
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Chiếc thuyền / Chiếc ghe)
- **Giá trị giáo dục / Định hướng tư duy:** *Phương tiện giao thông - Chiếc thuyền nan chở khách*

### Câu 141: [class_questions.xml - ID 68]
- **Phân loại vi phạm:** `Đố chữ Hán & Chiết tự` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'成语'*)
- **Lý do cần sửa:** Đố chiết tự chữ tượng hình hoặc thành ngữ Hán ngữ cổ mà người chơi Việt Nam không thể suy luận logic.
- **Câu hỏi cũ (Tiếng Trung):** `逆水划船。（猜一成语）`
- **Lựa chọn cũ:** A: `不进则退` | B: `白费力气` | C: `顺流而下` | D: `` (Đáp án cũ: `1`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Cái gì ru bé ngủ êm đềm, đung đưa kẽo kẹt nối liền hai bờ cột nhà?**
- **👉 Lựa chọn mới:**
  - **A.** Chiếc võng
  - **B.** Chiếc giường
  - **C.** Cái chiếu
  - **D.** Cái nôi
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Chiếc võng)
- **Giá trị giáo dục / Định hướng tư duy:** *Vật dụng tuổi thơ - Chiếc võng kẽo kẹt lời ru của mẹ*

### Câu 142: [class_questions.xml - ID 69]
- **Phân loại vi phạm:** `Đố chữ Hán & Chiết tự` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'字谜'*)
- **Lý do cần sửa:** Đố chiết tự chữ tượng hình hoặc thành ngữ Hán ngữ cổ mà người chơi Việt Nam không thể suy luận logic.
- **Câu hỏi cũ (Tiếng Trung):** `拆了围墙。（字谜）`
- **Lựa chọn cũ:** A: `韦` | B: `啬` | C: `` | D: `` (Đáp án cũ: `1`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Cái gì có mặt mà không có mắt, có chân mà chẳng biết đi, chuyên để sách vở bát đĩa?**
- **👉 Lựa chọn mới:**
  - **A.** Cái bàn
  - **B.** Cái ghế
  - **C.** Cái tủ
  - **D.** Cái phản
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Cái bàn)
- **Giá trị giáo dục / Định hướng tư duy:** *Đồ gia dụng - Cái bàn học thân quen*

### Câu 143: [class_questions.xml - ID 70]
- **Phân loại vi phạm:** `Đố chữ Hán & Chiết tự` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'成语'*)
- **Lý do cần sửa:** Đố chiết tự chữ tượng hình hoặc thành ngữ Hán ngữ cổ mà người chơi Việt Nam không thể suy luận logic.
- **Câu hỏi cũ (Tiếng Trung):** `水淹邮筒。（猜一成语）`
- **Lựa chọn cũ:** A: `不予理睬` | B: `难以置信` | C: `` | D: `` (Đáp án cũ: `2`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Cái gì có chân mà không biết đi, có lưng dựa vào nhưng không có bụng?**
- **👉 Lựa chọn mới:**
  - **A.** Cái ghế tựa
  - **B.** Cái bàn
  - **C.** Cái giường
  - **D.** Cái chõng
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Cái ghế tựa)
- **Giá trị giáo dục / Định hướng tư duy:** *Đồ dùng học đường - Chiếc ghế tựa thoải mái*

### Câu 144: [class_questions.xml - ID 72]
- **Phân loại vi phạm:** `Đố chữ Hán & Chiết tự` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'成语'*)
- **Lý do cần sửa:** Đố chiết tự chữ tượng hình hoặc thành ngữ Hán ngữ cổ mà người chơi Việt Nam không thể suy luận logic.
- **Câu hỏi cũ (Tiếng Trung):** `根据下面的数字“1256789”猜一句成语吧。`
- **Lựa chọn cũ:** A: `十全十美` | B: `丢三落四` | C: `五湖四海` | D: `` (Đáp án cũ: `2`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Cái gì mỏng manh từng trang, mở ra thế giới kiến thức bao la cho học trò đọc?**
- **👉 Lựa chọn mới:**
  - **A.** Quyển sách
  - **B.** Cái bảng
  - **C.** Chiếc cặp
  - **D.** Tờ giấy kiểm tra
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Quyển sách)
- **Giá trị giáo dục / Định hướng tư duy:** *Văn hóa đọc - Quyển sách người thầy vô giá*

### Câu 145: [class_questions.xml - ID 73]
- **Phân loại vi phạm:** `Tuyên truyền quốc gia 'Nước ta'` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'中国'*)
- **Lý do cần sửa:** Dùng cụm từ 'nước ta' ('我国') để nhồi nhét biểu tượng, ngày lễ, thủ đô, chính sách của Trung Quốc cho người chơi Việt Nam.
- **Câu hỏi cũ (Tiếng Trung):** `拿枪的男子。（猜中国城市名）？`
- **Lựa chọn cũ:** A: `北京` | B: `广西` | C: `武汉` | D: `` (Đáp án cũ: `3`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Loài chim nào có khả năng bay lượn lùi về phía sau và đập cánh hàng chục lần mỗi giây?**
- **👉 Lựa chọn mới:**
  - **A.** Chim ruồi
  - **B.** Chim bồ câu
  - **C.** Chim sẻ
  - **D.** Chim én
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Chim ruồi)
- **Giá trị giáo dục / Định hướng tư duy:** *Động vật học - Kỳ quan loài chim ruồi bé nhỏ*

### Câu 146: [class_questions.xml - ID 74]
- **Phân loại vi phạm:** `Tuyên truyền quốc gia 'Nước ta'` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'中国'*)
- **Lý do cần sửa:** Dùng cụm từ 'nước ta' ('我国') để nhồi nhét biểu tượng, ngày lễ, thủ đô, chính sách của Trung Quốc cho người chơi Việt Nam.
- **Câu hỏi cũ (Tiếng Trung):** `船出长江口。（猜中国城市名）`
- **Lựa chọn cũ:** A: `大连` | B: `上海` | C: `深圳` | D: `` (Đáp án cũ: `2`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Loài linh trưởng nào thông minh nhất và có bộ gen gần gũi với con người nhất trong giới động vật?**
- **👉 Lựa chọn mới:**
  - **A.** Tinh tinh (Chimpanzee)
  - **B.** Vượn
  - **C.** Khỉ đột
  - **D.** Đười ươi
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Tinh tinh (Chimpanzee))
- **Giá trị giáo dục / Định hướng tư duy:** *Tiến hóa sinh học - Loài tinh tinh thông minh*

### Câu 147: [class_questions.xml - ID 76]
- **Phân loại vi phạm:** `Đố chữ Hán & Chiết tự` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'成语'*)
- **Lý do cần sửa:** Đố chiết tự chữ tượng hình hoặc thành ngữ Hán ngữ cổ mà người chơi Việt Nam không thể suy luận logic.
- **Câu hỏi cũ (Tiếng Trung):** `根据下面的数字“23456789”猜一句成语吧。`
- **Lựa chọn cũ:** A: `无头无尾` | B: `缺衣少食` | C: `` | D: `` (Đáp án cũ: `2`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Cái gì nuốt mực đen mực xanh, nhả chữ đều đều trên trang vở trắng tinh?**
- **👉 Lựa chọn mới:**
  - **A.** Cây bút mực / Bút bi
  - **B.** Cục tẩy
  - **C.** Thước kẻ
  - **D.** Hộp bút
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Cây bút mực / Bút bi)
- **Giá trị giáo dục / Định hướng tư duy:** *Đồ dùng học sinh - Cây bút nắn nót từng con chữ*

### Câu 148: [class_questions.xml - ID 78]
- **Phân loại vi phạm:** `Tuyên truyền quốc gia 'Nước ta'` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'中国'*)
- **Lý do cần sửa:** Dùng cụm từ 'nước ta' ('我国') để nhồi nhét biểu tượng, ngày lễ, thủ đô, chính sách của Trung Quốc cho người chơi Việt Nam.
- **Câu hỏi cũ (Tiếng Trung):** `东、西、北全部堵塞。（猜中国城市名）`
- **Lựa chọn cũ:** A: `三亚` | B: `南通` | C: `` | D: `` (Đáp án cũ: `2`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Trong máy tính, thiết bị nào dùng để nhập văn bản và các ký tự vào máy tính?**
- **👉 Lựa chọn mới:**
  - **A.** Bàn phím (Keyboard)
  - **B.** Màn hình
  - **C.** Chuột máy tính
  - **D.** Tai nghe
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Bàn phím (Keyboard))
- **Giá trị giáo dục / Định hướng tư duy:** *Tin học phổ thông - Thiết bị nhập liệu bàn phím*

### Câu 149: [class_questions.xml - ID 79]
- **Phân loại vi phạm:** `Đố chữ Hán & Chiết tự` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'字谜'*)
- **Lý do cần sửa:** Đố chiết tự chữ tượng hình hoặc thành ngữ Hán ngữ cổ mà người chơi Việt Nam không thể suy luận logic.
- **Câu hỏi cũ (Tiếng Trung):** `水落石出。（字谜）`
- **Lựa chọn cũ:** A: `各` | B: `泵` | C: `路` | D: `` (Đáp án cũ: `2`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Cái gì thẳng tắp một hàng, có vạch xăng-ti-mét giúp em kẻ đường thẳng ngay ngắn?**
- **👉 Lựa chọn mới:**
  - **A.** Cây thước kẻ
  - **B.** Cây bút chì
  - **C.** Cục tẩy
  - **D.** Com-pa
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Cây thước kẻ)
- **Giá trị giáo dục / Định hướng tư duy:** *Dụng cụ học tập - Chiếc thước kẻ đo độ dài*

### Câu 150: [class_questions.xml - ID 82]
- **Phân loại vi phạm:** `Đố chữ Hán & Chiết tự` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'字谜'*)
- **Lý do cần sửa:** Đố chiết tự chữ tượng hình hoặc thành ngữ Hán ngữ cổ mà người chơi Việt Nam không thể suy luận logic.
- **Câu hỏi cũ (Tiếng Trung):** `天人何处去（字谜）`
- **Lựa chọn cũ:** A: `土` | B: `二` | C: `` | D: `` (Đáp án cũ: `2`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Cái gì chuyên xóa lỗi sai, cọ xát một lúc thân mình mòn đi?**
- **👉 Lựa chọn mới:**
  - **A.** Cục tẩy (cục gôm)
  - **B.** Bút chì
  - **C.** Giấy nháp
  - **D.** Mực xóa
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Cục tẩy (cục gôm))
- **Giá trị giáo dục / Định hướng tư duy:** *Dụng cụ học sinh - Cục gôm xóa nét vẽ chì*

### Câu 151: [class_questions.xml - ID 89]
- **Phân loại vi phạm:** `Đố chữ Hán & Chiết tự` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'字谜'*)
- **Lý do cần sửa:** Đố chiết tự chữ tượng hình hoặc thành ngữ Hán ngữ cổ mà người chơi Việt Nam không thể suy luận logic.
- **Câu hỏi cũ (Tiếng Trung):** `一边是水，一边是山。（字谜）`
- **Lựa chọn cũ:** A: `冰` | B: `汕` | C: `衫` | D: `` (Đáp án cũ: `2`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Vừa bằng hạt đỗ, ăn giỗ cả làng là con gì?**
- **👉 Lựa chọn mới:**
  - **A.** Con ruồi
  - **B.** Con kiến
  - **C.** Con muỗi
  - **D.** Con bọ
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Con ruồi)
- **Giá trị giáo dục / Định hướng tư duy:** *Câu đố dân gian cổ truyền - Con ruồi đậu cỗ cưới*

### Câu 152: [class_questions.xml - ID 93]
- **Phân loại vi phạm:** `Tuyên truyền quốc gia 'Nước ta'` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'中国'*)
- **Lý do cần sửa:** Dùng cụm từ 'nước ta' ('我国') để nhồi nhét biểu tượng, ngày lễ, thủ đô, chính sách của Trung Quốc cho người chơi Việt Nam.
- **Câu hỏi cũ (Tiếng Trung):** `风平浪静。（猜中国城市名）`
- **Lựa chọn cũ:** A: `大连` | B: `海南` | C: `宁波` | D: `` (Đáp án cũ: `3`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Mạng lưới kết nối toàn cầu hàng tỷ máy tính và thiết bị thông minh với nhau gọi là gì?**
- **👉 Lựa chọn mới:**
  - **A.** Mạng Internet
  - **B.** Mạng Bluetooth
  - **C.** Mạng LAN
  - **D.** Mạng vệ tinh
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Mạng Internet)
- **Giá trị giáo dục / Định hướng tư duy:** *Công nghệ số - Mạng toàn cầu Internet*

### Câu 153: [class_questions.xml - ID 94]
- **Phân loại vi phạm:** `Đố chữ Hán & Chiết tự` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'字谜'*)
- **Lý do cần sửa:** Đố chiết tự chữ tượng hình hoặc thành ngữ Hán ngữ cổ mà người chơi Việt Nam không thể suy luận logic.
- **Câu hỏi cũ (Tiếng Trung):** `一月七日。(字谜)`
- **Lựa chọn cũ:** A: `指` | B: `旨` | C: `脂` | D: `` (Đáp án cũ: `3`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Đầu rồng đuôi phụng cánh tiên, ngày thì ẩn nấp đêm thì sáng lung linh là con gì?**
- **👉 Lựa chọn mới:**
  - **A.** Con đom đóm
  - **B.** Con ve sầu
  - **C.** Con bướm
  - **D.** Con bọ rùa
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Con đom đóm)
- **Giá trị giáo dục / Định hướng tư duy:** *Thế giới côn trùng - Chú đom đóm thắp sáng màn đêm*

### Câu 154: [class_questions.xml - ID 95]
- **Phân loại vi phạm:** `Đố chữ Hán & Chiết tự` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'成语'*)
- **Lý do cần sửa:** Đố chiết tự chữ tượng hình hoặc thành ngữ Hán ngữ cổ mà người chơi Việt Nam không thể suy luận logic.
- **Câu hỏi cũ (Tiếng Trung):** `根据算式“15分钟=1000元”猜一句成语吧。`
- **Lựa chọn cũ:** A: `分秒必争` | B: `一刻千金` | C: `` | D: `` (Đáp án cũ: `2`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Lưng còng khúc khuỷu, búng nước nhảy tanh tách, râu dài ngực đỏ là con gì?**
- **👉 Lựa chọn mới:**
  - **A.** Con tôm
  - **B.** Con cá trê
  - **C.** Con cua
  - **D.** Con lươn
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Con tôm)
- **Giá trị giáo dục / Định hướng tư duy:** *Sinh vật sông nước - Con tôm cong mình nhảy lùi*

### Câu 155: [class_questions.xml - ID 101]
- **Phân loại vi phạm:** `Đố chữ Hán & Chiết tự` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'字谜'*)
- **Lý do cần sửa:** Đố chiết tự chữ tượng hình hoặc thành ngữ Hán ngữ cổ mà người chơi Việt Nam không thể suy luận logic.
- **Câu hỏi cũ (Tiếng Trung):** `他有你没有，地有天没有。（字谜）`
- **Lựa chọn cũ:** A: `人` | B: `也` | C: `土` | D: `` (Đáp án cũ: `2`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Thân dài ngoằn ngoèo, da trơn lùi lủi, thích chui dưới bùn lầy sâu là con gì?**
- **👉 Lựa chọn mới:**
  - **A.** Con lươn (hoặc con trạch)
  - **B.** Con rắn
  - **C.** Con cá quả
  - **D.** Con giun
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Con lươn (hoặc con trạch))
- **Giá trị giáo dục / Định hướng tư duy:** *Câu đố loài vật - Con lươn da trơn tuột*

### Câu 156: [class_questions.xml - ID 102]
- **Phân loại vi phạm:** `Đố chữ Hán & Chiết tự` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'成语'*)
- **Lý do cần sửa:** Đố chiết tự chữ tượng hình hoặc thành ngữ Hán ngữ cổ mà người chơi Việt Nam không thể suy luận logic.
- **Câu hỏi cũ (Tiếng Trung):** `根据数字“5 10”猜一句成语吧。`
- **Lựa chọn cũ:** A: `积少成多` | B: `一五一十` | C: `` | D: `` (Đáp án cũ: `2`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Chân vịt thịt gà, bơi giỏi dưới nước, kêu cạc cạc quanh năm là con gì?**
- **👉 Lựa chọn mới:**
  - **A.** Con vịt
  - **B.** Con ngỗng
  - **C.** Con ngan
  - **D.** Con bồ nông
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Con vịt)
- **Giá trị giáo dục / Định hướng tư duy:** *Gia cầm làng quê - Chú vịt bầu bơi lội dưới ao*

### Câu 157: [class_questions.xml - ID 113]
- **Phân loại vi phạm:** `Đố chữ Hán & Chiết tự` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'成语'*)
- **Lý do cần sửa:** Đố chiết tự chữ tượng hình hoặc thành ngữ Hán ngữ cổ mà người chơi Việt Nam không thể suy luận logic.
- **Câu hỏi cũ (Tiếng Trung):** `闭门能知天下事。（猜成语）`
- **Lựa chọn cũ:** A: `不出所料` | B: `鸡犬不宁` | C: `` | D: `` (Đáp án cũ: `1`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Bốn cột đung đưa, hai tai quạt mát, cái vòi uống nước dạo bước trong rừng là con gì?**
- **👉 Lựa chọn mới:**
  - **A.** Con voi
  - **B.** Con hươu cao cổ
  - **C.** Con hà mã
  - **D.** Con tê giác
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Con voi)
- **Giá trị giáo dục / Định hướng tư duy:** *Động vật rừng già - Chú voi Tây Nguyên to lớn*

### Câu 158: [class_questions.xml - ID 119]
- **Phân loại vi phạm:** `Đố chữ Hán & Chiết tự` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'成语'*)
- **Lý do cần sửa:** Đố chiết tự chữ tượng hình hoặc thành ngữ Hán ngữ cổ mà người chơi Việt Nam không thể suy luận logic.
- **Câu hỏi cũ (Tiếng Trung):** `螃蟹上路。（猜一成语）`
- **Lựa chọn cũ:** A: `横行霸道` | B: `上行下效` | C: `` | D: `` (Đáp án cũ: `1`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Cổ cao nghều nghệu vươn tới ngọn cây ăn lá xanh tươi là con gì?**
- **👉 Lựa chọn mới:**
  - **A.** Con hươu cao cổ
  - **B.** Con đà điểu
  - **C.** Con ngựa vằn
  - **D.** Con lạc đà
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Con hươu cao cổ)
- **Giá trị giáo dục / Định hướng tư duy:** *Động vật hoang dã - Hươu cao cổ đáng yêu*

### Câu 159: [class_questions.xml - ID 124]
- **Phân loại vi phạm:** `Đố chữ Hán & Chiết tự` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'成语'*)
- **Lý do cần sửa:** Đố chiết tự chữ tượng hình hoặc thành ngữ Hán ngữ cổ mà người chơi Việt Nam không thể suy luận logic.
- **Câu hỏi cũ (Tiếng Trung):** `根据算式“9寸+1寸=1尺”猜一个成语吧。`
- **Lựa chọn cũ:** A: `循序渐进` | B: `得寸进尺` | C: `` | D: `` (Đáp án cũ: `2`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Con gì có túi trước bụng mang con nhỏ đi khắp nơi nhảy tưng tưng?**
- **👉 Lựa chọn mới:**
  - **A.** Chuột túi (Kangaroo)
  - **B.** Gấu Koala
  - **C.** Chó sói
  - **D.** Thỏ rừng
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Chuột túi (Kangaroo))
- **Giá trị giáo dục / Định hướng tư duy:** *Thế giới muôn loài - Chuột túi xứ Australia*

### Câu 160: [class_questions.xml - ID 129]
- **Phân loại vi phạm:** `Đố chữ Hán & Chiết tự` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'字谜'*)
- **Lý do cần sửa:** Đố chiết tự chữ tượng hình hoặc thành ngữ Hán ngữ cổ mà người chơi Việt Nam không thể suy luận logic.
- **Câu hỏi cũ (Tiếng Trung):** `一人一张口，口下长只手。（字谜）`
- **Lựa chọn cũ:** A: `好` | B: `盒` | C: `拿` | D: `` (Đáp án cũ: `3`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Mùa hè cất tiếng ve ve râm ran trên cành phượng vĩ là con gì?**
- **👉 Lựa chọn mới:**
  - **A.** Con ve sầu
  - **B.** Con dế mèn
  - **C.** Con bọ hung
  - **D.** Con chuồn chuồn
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Con ve sầu)
- **Giá trị giáo dục / Định hướng tư duy:** *Âm thanh mùa hè - Tiếng ve sầu gọi hè về*

### Câu 161: [class_questions.xml - ID 137]
- **Phân loại vi phạm:** `Đố chữ Hán & Chiết tự` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'字谜'*)
- **Lý do cần sửa:** Đố chiết tự chữ tượng hình hoặc thành ngữ Hán ngữ cổ mà người chơi Việt Nam không thể suy luận logic.
- **Câu hỏi cũ (Tiếng Trung):** `查看结果，杳无踪迹。（字谜）`
- **Lựa chọn cũ:** A: `木` | B: `旦` | C: `一` | D: `` (Đáp án cũ: `3`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Đêm hè cất tiếng gáy vang dưới hang đất, bạn thân của Dế Trũi trong truyện Tô Hoài là ai?**
- **👉 Lựa chọn mới:**
  - **A.** Dế Mèn
  - **B.** Bọ ngựa
  - **C.** Châu chấu
  - **D.** Cào cào
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Dế Mèn)
- **Giá trị giáo dục / Định hướng tư duy:** *Văn học thiếu nhi - Chú Dế Mèn phiêu lưu ký*

### Câu 162: [class_questions.xml - ID 139]
- **Phân loại vi phạm:** `Tuyên truyền quốc gia 'Nước ta'` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'中国'*)
- **Lý do cần sửa:** Dùng cụm từ 'nước ta' ('我国') để nhồi nhét biểu tượng, ngày lễ, thủ đô, chính sách của Trung Quốc cho người chơi Việt Nam.
- **Câu hỏi cũ (Tiếng Trung):** `夸夸其谈。（打中国城市名）`
- **Lựa chọn cũ:** A: `吉林` | B: `海口` | C: `` | D: `` (Đáp án cũ: `2`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Để bảo vệ mắt khi sử dụng máy tính và điện thoại, khoảng cách an toàn tối thiểu từ mắt đến màn hình nên là bao nhiêu?**
- **👉 Lựa chọn mới:**
  - **A.** Khoảng 40 - 50 cm
  - **B.** Khoảng 10 cm
  - **C.** Khoảng 20 cm
  - **D.** Khoảng 1 mét
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Khoảng 40 - 50 cm)
- **Giá trị giáo dục / Định hướng tư duy:** *Sức khỏe học đường - Thói quen bảo vệ thị lực*

### Câu 163: [class_questions.xml - ID 141]
- **Phân loại vi phạm:** `Đố chữ Hán & Chiết tự` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'成语'*)
- **Lý do cần sửa:** Đố chiết tự chữ tượng hình hoặc thành ngữ Hán ngữ cổ mà người chơi Việt Nam không thể suy luận logic.
- **Câu hỏi cũ (Tiếng Trung):** `小猫走路。（猜一成语）`
- **Lựa chọn cũ:** A: `不声不响` | B: `名扬四方` | C: `` | D: `` (Đáp án cũ: `1`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Quả gì nhiều mắt mọc quanh mình, thơm nức khi chín vàng gai góc?**
- **👉 Lựa chọn mới:**
  - **A.** Quả dứa (quả thơm)
  - **B.** Quả mãng cầu
  - **C.** Quả chôm chôm
  - **D.** Quả lựu
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Quả dứa (quả thơm))
- **Giá trị giáo dục / Định hướng tư duy:** *Trái cây nhiệt đới - Quả dứa thơm ngọt*

### Câu 164: [class_questions.xml - ID 147]
- **Phân loại vi phạm:** `Đố chữ Hán & Chiết tự` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'字谜'*)
- **Lý do cần sửa:** Đố chiết tự chữ tượng hình hoặc thành ngữ Hán ngữ cổ mà người chơi Việt Nam không thể suy luận logic.
- **Câu hỏi cũ (Tiếng Trung):** `一口咬去多半截。（字谜）`
- **Lựa chọn cũ:** A: `夕` | B: `交` | C: `名` | D: `` (Đáp án cũ: `3`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Quả gì vỏ đỏ đầy gai mềm, bóc ra cùi trắng mọng nước ngọt lịm ở miền Tây?**
- **👉 Lựa chọn mới:**
  - **A.** Quả chôm chôm
  - **B.** Quả vải
  - **C.** Quả nhãn
  - **D.** Quả mận
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Quả chôm chôm)
- **Giá trị giáo dục / Định hướng tư duy:** *Đặc sản trái cây - Quả chôm chôm chín đỏ*

### Câu 165: [class_questions.xml - ID 150]
- **Phân loại vi phạm:** `Đố chữ Hán & Chiết tự` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'成语'*)
- **Lý do cần sửa:** Đố chiết tự chữ tượng hình hoặc thành ngữ Hán ngữ cổ mà người chơi Việt Nam không thể suy luận logic.
- **Câu hỏi cũ (Tiếng Trung):** `150分钟。（猜一成语）`
- **Lựa chọn cũ:** A: `天旋地转` | B: `时时刻刻` | C: `` | D: `` (Đáp án cũ: `2`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Hoa gì nở rộ trên mặt bùn lầy lội mà chẳng hôi tanh mùi bùn, tỏa ngát hương thơm thanh khiết?**
- **👉 Lựa chọn mới:**
  - **A.** Hoa sen
  - **B.** Hoa súng
  - **C.** Hoa bèo
  - **D.** Hoa quỳnh
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Hoa sen)
- **Giá trị giáo dục / Định hướng tư duy:** *Quốc hoa Việt Nam - Bông sen ngát hương gần bùn mà chẳng hôi tanh*

### Câu 166: [class_questions.xml - ID 152]
- **Phân loại vi phạm:** `Đố chữ Hán & Chiết tự` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'字谜'*)
- **Lý do cần sửa:** Đố chiết tự chữ tượng hình hoặc thành ngữ Hán ngữ cổ mà người chơi Việt Nam không thể suy luận logic.
- **Câu hỏi cũ (Tiếng Trung):** `三加三等于几？（字谜）`
- **Lựa chọn cũ:** A: `田` | B: `弄` | C: `` | D: `` (Đáp án cũ: `1`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Hoa gì đỏ rực báo hiệu mùa hè đến và gắn liền với tuổi học trò chia tay mái trường?**
- **👉 Lựa chọn mới:**
  - **A.** Hoa phượng vĩ
  - **B.** Hoa bằng lăng
  - **C.** Hoa điệp vàng
  - **D.** Hoa bằng lăng tím
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Hoa phượng vĩ)
- **Giá trị giáo dục / Định hướng tư duy:** *Kỷ niệm học trò - Hoa phượng đỏ rực sân trường*

### Câu 167: [class_questions.xml - ID 162]
- **Phân loại vi phạm:** `Đố chữ Hán & Chiết tự` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'字谜'*)
- **Lý do cần sửa:** Đố chiết tự chữ tượng hình hoặc thành ngữ Hán ngữ cổ mà người chơi Việt Nam không thể suy luận logic.
- **Câu hỏi cũ (Tiếng Trung):** `连环洞。（字谜）`
- **Lựa chọn cũ:** A: `吕` | B: `窜` | C: `` | D: `` (Đáp án cũ: `2`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Hoa gì sắc tím dịu dàng nở cùng lúc với hoa phượng mỗi mùa chia tay lớp học?**
- **👉 Lựa chọn mới:**
  - **A.** Hoa bằng lăng tím
  - **B.** Hoa cúc
  - **C.** Hoa thược dược
  - **D.** Hoa cẩm chướng
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Hoa bằng lăng tím)
- **Giá trị giáo dục / Định hướng tư duy:** *Hoa học trò - Sắc tím hoa bằng lăng*

### Câu 168: [class_questions.xml - ID 163]
- **Phân loại vi phạm:** `Đố chữ Hán & Chiết tự` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'成语'*)
- **Lý do cần sửa:** Đố chiết tự chữ tượng hình hoặc thành ngữ Hán ngữ cổ mà người chơi Việt Nam không thể suy luận logic.
- **Câu hỏi cũ (Tiếng Trung):** `掉了毛的刷子。（猜一成语）`
- **Lựa chọn cũ:** A: `一干二净` | B: `有板有眼` | C: `` | D: `` (Đáp án cũ: `2`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Hoa gì luôn luôn hướng về phía Mặt Trời đón ánh nắng rực rỡ buổi bình minh?**
- **👉 Lựa chọn mới:**
  - **A.** Hoa hướng dương
  - **B.** Hoa hồng
  - **C.** Hoa đồng tiền
  - **D.** Hoa mười giờ
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Hoa hướng dương)
- **Giá trị giáo dục / Định hướng tư duy:** *Hiện tượng sinh học - Loài hoa hướng dương kiên định*

### Câu 169: [class_questions.xml - ID 164]
- **Phân loại vi phạm:** `Đố chữ Hán & Chiết tự` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'字谜'*)
- **Lý do cần sửa:** Đố chiết tự chữ tượng hình hoặc thành ngữ Hán ngữ cổ mà người chơi Việt Nam không thể suy luận logic.
- **Câu hỏi cũ (Tiếng Trung):** `一大二小。（字谜）`
- **Lựa chọn cũ:** A: `好` | B: `奈` | C: `茶` | D: `` (Đáp án cũ: `2`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Hoa gì chỉ nở rộ vào lúc giữa trưa tròn bóng râm rồi chiều tà khép lại?**
- **👉 Lựa chọn mới:**
  - **A.** Hoa mười giờ
  - **B.** Hoa lài
  - **C.** Hoa cúc
  - **D.** Hoa dạ lý hương
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Hoa mười giờ)
- **Giá trị giáo dục / Định hướng tư duy:** *Tên loài hoa đẹp - Hoa mười giờ khoe sắc nắng trưa*

### Câu 170: [class_questions.xml - ID 166]
- **Phân loại vi phạm:** `Đố chữ Hán & Chiết tự` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'字谜'*)
- **Lý do cần sửa:** Đố chiết tự chữ tượng hình hoặc thành ngữ Hán ngữ cổ mà người chơi Việt Nam không thể suy luận logic.
- **Câu hỏi cũ (Tiếng Trung):** `八十八。（字谜）`
- **Lựa chọn cũ:** A: `众` | B: `米` | C: `茶` | D: `` (Đáp án cũ: `2`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Bánh gì ăn được mà không làm từ bột gạo bột mì (dùng để lái xe)?**
- **👉 Lựa chọn mới:**
  - **A.** Bánh lái xe / Bánh xe
  - **B.** Bánh mì
  - **C.** Bánh quy
  - **D.** Bánh kem
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Bánh lái xe / Bánh xe)
- **Giá trị giáo dục / Định hướng tư duy:** *Đố mẹo tiếng Việt - Hiện tượng đồng âm chữ 'bánh'*

### Câu 171: [class_questions.xml - ID 167]
- **Phân loại vi phạm:** `Đố chữ Hán & Chiết tự` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'字谜'*)
- **Lý do cần sửa:** Đố chiết tự chữ tượng hình hoặc thành ngữ Hán ngữ cổ mà người chơi Việt Nam không thể suy luận logic.
- **Câu hỏi cũ (Tiếng Trung):** `大雨落在横山上。（字谜）`
- **Lựa chọn cũ:** A: `雪` | B: `雷` | C: `霜` | D: `` (Đáp án cũ: `1`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Bút gì cầm trên tay mà không dùng để viết chữ mà dùng để kiểm tra an toàn điện?**
- **👉 Lựa chọn mới:**
  - **A.** Bút thử điện
  - **B.** Bút chì
  - **C.** Bút lông
  - **D.** Bút dạ
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Bút thử điện)
- **Giá trị giáo dục / Định hướng tư duy:** *An toàn điện - Chiếc bút thử điện hữu ích*

### Câu 172: [class_questions.xml - ID 169]
- **Phân loại vi phạm:** `Tuyên truyền quốc gia 'Nước ta'` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'中国'*)
- **Lý do cần sửa:** Dùng cụm từ 'nước ta' ('我国') để nhồi nhét biểu tượng, ngày lễ, thủ đô, chính sách của Trung Quốc cho người chơi Việt Nam.
- **Câu hỏi cũ (Tiếng Trung):** `中国的四大发明不包括哪个？`
- **Lựa chọn cũ:** A: `造纸术` | B: `活字印刷术` | C: `指南针` | D: `地动仪` (Đáp án cũ: `4`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Quy tắc '20 - 20 - 20' khi sử dụng máy tính nhằm bảo vệ mắt khuyên chúng ta làm gì sau mỗi 20 phút nhìn màn hình?**
- **👉 Lựa chọn mới:**
  - **A.** Nhìn ra xa 20 feet (khoảng 6m) trong 20 giây
  - **B.** Chớp mắt 20 lần
  - **C.** Nhắm mắt ngủ 20 phút
  - **D.** Uống 20 ngụm nước
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Nhìn ra xa 20 feet (khoảng 6m) trong 20 giây)
- **Giá trị giáo dục / Định hướng tư duy:** *Y tế dự phòng - Quy tắc thư giãn mắt khi học tập*

### Câu 173: [class_questions.xml - ID 174]
- **Phân loại vi phạm:** `Đố chữ Hán & Chiết tự` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'字谜'*)
- **Lý do cần sửa:** Đố chiết tự chữ tượng hình hoặc thành ngữ Hán ngữ cổ mà người chơi Việt Nam không thể suy luận logic.
- **Câu hỏi cũ (Tiếng Trung):** `久雷不雨。（字谜）`
- **Lựa chọn cũ:** A: `霉` | B: `田` | C: `` | D: `` (Đáp án cũ: `2`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Bàn gì không có bốn chân, không để đồ vật mà là môn thể thao trí tuệ 64 ô?**
- **👉 Lựa chọn mới:**
  - **A.** Bàn cờ vua / Bàn cờ tướng
  - **B.** Bàn ăn
  - **C.** Bàn là
  - **D.** Bàn chải
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Bàn cờ vua / Bàn cờ tướng)
- **Giá trị giáo dục / Định hướng tư duy:** *Đố mẹo chữ Việt - Chữ 'bàn' đa nghĩa*

### Câu 174: [class_questions.xml - ID 177]
- **Phân loại vi phạm:** `Tuyên truyền quốc gia 'Nước ta'` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'我国'*)
- **Lý do cần sửa:** Dùng cụm từ 'nước ta' ('我国') để nhồi nhét biểu tượng, ngày lễ, thủ đô, chính sách của Trung Quốc cho người chơi Việt Nam.
- **Câu hỏi cũ (Tiếng Trung):** `下列哪种动物是我国一级保护动物？`
- **Lựa chọn cũ:** A: `猕猴` | B: `孟加拉虎` | C: `白鳍豚` | D: `` (Đáp án cũ: `3`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Khi đi bộ sang đường trên phố, người đi bộ an toàn nhất là đi ở vị trí nào?**
- **👉 Lựa chọn mới:**
  - **A.** Vạch kẻ đường dành cho người đi bộ khi có tín hiệu đèn xanh
  - **B.** Băng qua giữa dòng xe
  - **C.** Vừa đi vừa nhìn điện thoại
  - **D.** Chạy thật nhanh cắt mặt xe bus
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Vạch kẻ đường dành cho người đi bộ khi có tín hiệu đèn xanh)
- **Giá trị giáo dục / Định hướng tư duy:** *An toàn giao thông - Văn hóa đi bộ an toàn*

### Câu 175: [class_questions.xml - ID 179]
- **Phân loại vi phạm:** `Đố chữ Hán & Chiết tự` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'字谜'*)
- **Lý do cần sửa:** Đố chiết tự chữ tượng hình hoặc thành ngữ Hán ngữ cổ mà người chơi Việt Nam không thể suy luận logic.
- **Câu hỏi cũ (Tiếng Trung):** `一个人搬两个土。（字谜）`
- **Lựa chọn cũ:** A: `佳` | B: `住` | C: `往` | D: `` (Đáp án cũ: `1`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Cây gì không có lá, không có rễ cành, chỉ có thân thẳng đứng cắm ngoài đường truyền tải điện năng?**
- **👉 Lựa chọn mới:**
  - **A.** Cột điện
  - **B.** Cây cau
  - **C.** Cây đa
  - **D.** Cây thông
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Cột điện)
- **Giá trị giáo dục / Định hướng tư duy:** *Đố vui từ ngữ - Cột điện truyền tải dòng điện*

### Câu 176: [class_questions.xml - ID 180]
- **Phân loại vi phạm:** `Tuyên truyền quốc gia 'Nước ta'` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'中国'*)
- **Lý do cần sửa:** Dùng cụm từ 'nước ta' ('我国') để nhồi nhét biểu tượng, ngày lễ, thủ đô, chính sách của Trung Quốc cho người chơi Việt Nam.
- **Câu hỏi cũ (Tiếng Trung):** `你知道富士山是哪个国家的吗？`
- **Lựa chọn cũ:** A: `中国` | B: `美国` | C: `日本` | D: `德国` (Đáp án cũ: `3`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Khi tham gia giao thông bằng xe máy hoặc xe đạp điện, trang bị bắt buộc phải đội đúng quy cách là gì?**
- **👉 Lựa chọn mới:**
  - **A.** Mũ bảo hiểm đạt chuẩn
  - **B.** Mũ lưỡi trai
  - **C.** Tai nghe nhạc
  - **D.** Kính râm
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Mũ bảo hiểm đạt chuẩn)
- **Giá trị giáo dục / Định hướng tư duy:** *An toàn giao thông - Đội mũ bảo hiểm bảo vệ tính mạng*

### Câu 177: [class_questions.xml - ID 183]
- **Phân loại vi phạm:** `Tuyên truyền quốc gia 'Nước ta'` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'中国'*)
- **Lý do cần sửa:** Dùng cụm từ 'nước ta' ('我国') để nhồi nhét biểu tượng, ngày lễ, thủ đô, chính sách của Trung Quốc cho người chơi Việt Nam.
- **Câu hỏi cũ (Tiếng Trung):** `你知道中国有多少个民族吗？`
- **Lựa chọn cũ:** A: `57个` | B: `56个` | C: `55个` | D: `` (Đáp án cũ: `2`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Việc phân loại rác thải tại nguồn (rác hữu cơ, rác tái chế, rác vô cơ) mang lại lợi ích lớn nhất là gì?**
- **👉 Lựa chọn mới:**
  - **A.** Bảo vệ môi trường và giảm thiểu lượng rác chôn lấp
  - **B.** Làm mất thời gian
  - **C.** Không có tác dụng gì
  - **D.** Để nhà chật thêm
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Bảo vệ môi trường và giảm thiểu lượng rác chôn lấp)
- **Giá trị giáo dục / Định hướng tư duy:** *Bảo vệ môi trường - Phân loại rác vì một Trái Đất xanh*

### Câu 178: [class_questions.xml - ID 187]
- **Phân loại vi phạm:** `Đố chữ Hán & Chiết tự` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'成语'*)
- **Lý do cần sửa:** Đố chiết tự chữ tượng hình hoặc thành ngữ Hán ngữ cổ mà người chơi Việt Nam không thể suy luận logic.
- **Câu hỏi cũ (Tiếng Trung):** `纺织专家。（猜一成语）`
- **Lựa chọn cũ:** A: `满腹经纶` | B: `直来直去` | C: `` | D: `` (Đáp án cũ: `1`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Cái gì bạn có thể giữ gìn cẩn thận nhất sau khi đã trao cho người bạn thân?**
- **👉 Lựa chọn mới:**
  - **A.** Lời hứa chân thành
  - **B.** Bức ảnh
  - **C.** Cây bút
  - **D.** Cục tẩy
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Lời hứa chân thành)
- **Giá trị giáo dục / Định hướng tư duy:** *Giáo dục nhân cách - Giữ trọn lời hứa và chữ tín*

### Câu 179: [class_questions.xml - ID 190]
- **Phân loại vi phạm:** `Đố chữ Hán & Chiết tự` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'字谜'*)
- **Lý do cần sửa:** Đố chiết tự chữ tượng hình hoặc thành ngữ Hán ngữ cổ mà người chơi Việt Nam không thể suy luận logic.
- **Câu hỏi cũ (Tiếng Trung):** `人不在其位。（字谜）`
- **Lựa chọn cũ:** A: `粒` | B: `立` | C: `笠` | D: `` (Đáp án cũ: `2`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Con gì đập liên tục thì sống khỏe mạnh, ngừng đập là nguy hiểm đến tính mạng?**
- **👉 Lựa chọn mới:**
  - **A.** Trái tim
  - **B.** Con mắt
  - **C.** Bàn tay
  - **D.** Đôi chân
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Trái tim)
- **Giá trị giáo dục / Định hướng tư duy:** *Giải phẫu cơ thể - Nhịp đập liên hồi của trái tim*

### Câu 180: [class_questions.xml - ID 192]
- **Phân loại vi phạm:** `Tuyên truyền quốc gia 'Nước ta'` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'我国'*)
- **Lý do cần sửa:** Dùng cụm từ 'nước ta' ('我国') để nhồi nhét biểu tượng, ngày lễ, thủ đô, chính sách của Trung Quốc cho người chơi Việt Nam.
- **Câu hỏi cũ (Tiếng Trung):** `我国古代“三十六计”中第36计是什么？`
- **Lựa chọn cũ:** A: `美人计` | B: `空城计` | C: `走为上计` | D: `反间计` (Đáp án cũ: `3`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Hành động nào sau đây giúp tiết kiệm nguồn tài nguyên nước sạch sinh hoạt hàng ngày?**
- **👉 Lựa chọn mới:**
  - **A.** Tắt vòi nước khi đang chải răng hoặc xoa xà phòng
  - **B.** Mở vòi nước chảy tự do
  - **C.** Xả tràn bể chứa
  - **D.** Dùng vòi nước áp lực rửa đồ vô cớ
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Tắt vòi nước khi đang chải răng hoặc xoa xà phòng)
- **Giá trị giáo dục / Định hướng tư duy:** *Lối sống xanh - Ý thức tiết kiệm nước sinh hoạt*

### Câu 181: [class_questions.xml - ID 194]
- **Phân loại vi phạm:** `Đố chữ Hán & Chiết tự` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'字谜'*)
- **Lý do cần sửa:** Đố chiết tự chữ tượng hình hoặc thành ngữ Hán ngữ cổ mà người chơi Việt Nam không thể suy luận logic.
- **Câu hỏi cũ (Tiếng Trung):** `1和9。（字谜）`
- **Lựa chọn cũ:** A: `杂` | B: `丸` | C: `九` | D: `` (Đáp án cũ: `2`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Tháng nào trong năm theo dương lịch luôn có số ngày ít nhất (28 hoặc 29 ngày)?**
- **👉 Lựa chọn mới:**
  - **A.** Tháng 2
  - **B.** Tháng 1
  - **C.** Tháng 4
  - **D.** Tháng 12
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Tháng 2)
- **Giá trị giáo dục / Định hướng tư duy:** *Dương lịch học - Tháng hai năm nhuận*

### Câu 182: [class_questions.xml - ID 195]
- **Phân loại vi phạm:** `Tuyên truyền quốc gia 'Nước ta'` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'我国'*)
- **Lý do cần sửa:** Dùng cụm từ 'nước ta' ('我国') để nhồi nhét biểu tượng, ngày lễ, thủ đô, chính sách của Trung Quốc cho người chơi Việt Nam.
- **Câu hỏi cũ (Tiếng Trung):** `下列哪个城市不是我国的“三大火炉”城市？`
- **Lựa chọn cũ:** A: `重庆` | B: `成都` | C: `武汉` | D: `南京` (Đáp án cũ: `2`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Để giảm thiểu rác thải nhựa đại dương, thay vì dùng túi nilon một lần ta nên dùng túi gì khi đi chợ?**
- **👉 Lựa chọn mới:**
  - **A.** Túi vải dùng nhiều lần
  - **B.** Dùng nhiều túi nilon hơn
  - **C.** Vứt túi nhựa ra sông
  - **D.** Đốt túi nilon ngoài trời
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Túi vải dùng nhiều lần)
- **Giá trị giáo dục / Định hướng tư duy:** *Ý thức môi trường - Giảm rác thải nhựa dùng một lần*

### Câu 183: [class_questions.xml - ID 196]
- **Phân loại vi phạm:** `Tuyên truyền quốc gia 'Nước ta'` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'中国'*)
- **Lý do cần sửa:** Dùng cụm từ 'nước ta' ('我国') để nhồi nhét biểu tượng, ngày lễ, thủ đô, chính sách của Trung Quốc cho người chơi Việt Nam.
- **Câu hỏi cũ (Tiếng Trung):** `两个胖子拥抱。（中国城市名）`
- **Lựa chọn cũ:** A: `南宁` | B: `合肥` | C: `` | D: `` (Đáp án cũ: `2`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Màu sắc đèn tín hiệu giao thông lần lượt có ý nghĩa là gì?**
- **👉 Lựa chọn mới:**
  - **A.** Đỏ: dừng lại, Vàng: đi chậm/chuẩn bị dừng, Xanh: được phép đi
  - **B.** Đỏ: đi nhanh, Vàng: dừng, Xanh: lùi lại
  - **C.** Xanh: dừng, Đỏ: đi, Vàng: rẽ
  - **D.** Cả 3 màu đều có nghĩa giống nhau
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Đỏ: dừng lại, Vàng: đi chậm/chuẩn bị dừng, Xanh: được phép đi)
- **Giá trị giáo dục / Định hướng tư duy:** *Luật giao thông - Tuân thủ tín hiệu đèn giao thông*

### Câu 184: [class_questions.xml - ID 203]
- **Phân loại vi phạm:** `Đố chữ Hán & Chiết tự` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'成语'*)
- **Lý do cần sửa:** Đố chiết tự chữ tượng hình hoặc thành ngữ Hán ngữ cổ mà người chơi Việt Nam không thể suy luận logic.
- **Câu hỏi cũ (Tiếng Trung):** `七个躺着，八个站着。（猜一成语）`
- **Lựa chọn cũ:** A: `横七竖八` | B: `乱七八糟` | C: `七上八下` | D: `` (Đáp án cũ: `1`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Trong một cuộc thi chạy tiếp sức, nếu bạn chạy vượt qua người đang ở vị trí thứ hai, bạn sẽ ở vị trí thứ mấy?**
- **👉 Lựa chọn mới:**
  - **A.** Vị trí thứ hai
  - **B.** Vị trí thứ nhất
  - **C.** Vị trí thứ ba
  - **D.** Vị trí cuối cùng
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Vị trí thứ hai)
- **Giá trị giáo dục / Định hướng tư duy:** *Tư duy logic - Xác định đúng thứ hạng khi vượt người thứ 2*

### Câu 185: [class_questions.xml - ID 206]
- **Phân loại vi phạm:** `Đố chữ Hán & Chiết tự` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'汉字'*)
- **Lý do cần sửa:** Đố chiết tự chữ tượng hình hoặc thành ngữ Hán ngữ cổ mà người chơi Việt Nam không thể suy luận logic.
- **Câu hỏi cũ (Tiếng Trung):** `什么字全世界通用 ？`
- **Lựa chọn cũ:** A: `汉字` | B: `英文字母` | C: `阿拉伯数字` | D: `` (Đáp án cũ: `3`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Một người đi câu cá câu được 6 con cá mất đầu, 9 con cá mất đuôi, 8 con cá mất một nửa. Hỏi người đó câu được mấy con cá?**
- **👉 Lựa chọn mới:**
  - **A.** 0 con cá (số 6 mất đầu là 0, số 9 mất đuôi là 0, số 8 cắt đôi là 0)
  - **B.** 23 con
  - **C.** 8 con
  - **D.** 6 con
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (0 con cá (số 6 mất đầu là 0, số 9 mất đuôi là 0, số 8 cắt đôi là 0))
- **Giá trị giáo dục / Định hướng tư duy:** *Toán đố mẹo chữ số - Phép biến hình chữ số hình học*

### Câu 186: [class_questions.xml - ID 209]
- **Phân loại vi phạm:** `Đố chữ Hán & Chiết tự` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'成语'*)
- **Lý do cần sửa:** Đố chiết tự chữ tượng hình hoặc thành ngữ Hán ngữ cổ mà người chơi Việt Nam không thể suy luận logic.
- **Câu hỏi cũ (Tiếng Trung):** `最慢的时间。(猜一成语）`
- **Lựa chọn cũ:** A: `沧海桑田` | B: `度日如年` | C: `白驹过隙` | D: `` (Đáp án cũ: `2`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Cái gì tay trái của bạn có thể cầm nắm được nhưng tay phải không bao giờ cầm được?**
- **👉 Lựa chọn mới:**
  - **A.** Cổ tay phải / Cùi chỏ tay phải
  - **B.** Bàn chân
  - **C.** Cái tai
  - **D.** Cái mũi
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Cổ tay phải / Cùi chỏ tay phải)
- **Giá trị giáo dục / Định hướng tư duy:** *Đố mẹo cơ thể - Vị trí đối xứng trên cơ thể con người*

### Câu 187: [class_questions.xml - ID 213]
- **Phân loại vi phạm:** `Đố chữ Hán & Chiết tự` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'字谜'*)
- **Lý do cần sửa:** Đố chiết tự chữ tượng hình hoặc thành ngữ Hán ngữ cổ mà người chơi Việt Nam không thể suy luận logic.
- **Câu hỏi cũ (Tiếng Trung):** `一口吃掉牛尾巴。（字谜）`
- **Lựa chọn cũ:** A: `车` | B: `告` | C: `干` | D: `` (Đáp án cũ: `2`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Một gia đình có bố mẹ và 6 người con trai, mỗi người con trai đều có 1 người em gái. Hỏi gia đình có tất cả mấy người con?**
- **👉 Lựa chọn mới:**
  - **A.** 7 người con (6 con trai và 1 cô con gái út)
  - **B.** 12 người
  - **C.** 14 người
  - **D.** 8 người
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (7 người con (6 con trai và 1 cô con gái út))
- **Giá trị giáo dục / Định hướng tư duy:** *Toán tư duy gia đình - Mối quan hệ anh em chung một cô em gái*

### Câu 188: [class_questions.xml - ID 216]
- **Phân loại vi phạm:** `Đố chữ Hán & Chiết tự` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'成语'*)
- **Lý do cần sửa:** Đố chiết tự chữ tượng hình hoặc thành ngữ Hán ngữ cổ mà người chơi Việt Nam không thể suy luận logic.
- **Câu hỏi cũ (Tiếng Trung):** `少了一本书。（猜一成语）`
- **Lựa chọn cũ:** A: `缺一不可` | B: `丢三落四` | C: `焉知非福` | D: `` (Đáp án cũ: `1`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Cái gì bạn càng kéo dài thổi bùng lên thì tuổi thọ của nó lại càng ngắn lại?**
- **👉 Lựa chọn mới:**
  - **A.** Cây nến cháy
  - **B.** Sợi dây thừng
  - **C.** Dây chun
  - **D.** Bức tranh
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Cây nến cháy)
- **Giá trị giáo dục / Định hướng tư duy:** *Tư duy nghịch lý - Sự tiêu hao khi sử dụng*

### Câu 189: [class_questions.xml - ID 218]
- **Phân loại vi phạm:** `Đố chữ Hán & Chiết tự` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'字谜'*)
- **Lý do cần sửa:** Đố chiết tự chữ tượng hình hoặc thành ngữ Hán ngữ cổ mà người chơi Việt Nam không thể suy luận logic.
- **Câu hỏi cũ (Tiếng Trung):** `学子远去,又见归来。（字谜）`
- **Lựa chọn cũ:** A: `观` | B: `觉` | C: `好` | D: `` (Đáp án cũ: `2`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Cái gì bạn càng lấy đi nhiều thì nó lại càng trở nên to lớn hơn?**
- **👉 Lựa chọn mới:**
  - **A.** Một cái hố đất
  - **B.** Cục xà phòng
  - **C.** Bình nước
  - **D.** Cây nến
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Một cái hố đất)
- **Giá trị giáo dục / Định hướng tư duy:** *Tư duy không gian - Càng đào sâu cái hố càng to*

### Câu 190: [class_questions.xml - ID 224]
- **Phân loại vi phạm:** `Đố chữ Hán & Chiết tự` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'字谜'*)
- **Lý do cần sửa:** Đố chiết tự chữ tượng hình hoặc thành ngữ Hán ngữ cổ mà người chơi Việt Nam không thể suy luận logic.
- **Câu hỏi cũ (Tiếng Trung):** `草木之中有个人。(字谜）`
- **Lựa chọn cũ:** A: `茶` | B: `荼` | C: `杂` | D: `` (Đáp án cũ: `1`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Cái gì có cổ mà không có đầu, có hai cánh tay rỗng mà không có bàn tay?**
- **👉 Lựa chọn mới:**
  - **A.** Chiếc áo sơ mi
  - **B.** Cái chai
  - **C.** Cái ấm nước
  - **D.** Cái bàn
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Chiếc áo sơ mi)
- **Giá trị giáo dục / Định hướng tư duy:** *Đồ dùng thường ngày - Cấu tạo chiếc áo*

### Câu 191: [class_questions.xml - ID 227]
- **Phân loại vi phạm:** `Đố chữ Hán & Chiết tự` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'成语'*)
- **Lý do cần sửa:** Đố chiết tự chữ tượng hình hoặc thành ngữ Hán ngữ cổ mà người chơi Việt Nam không thể suy luận logic.
- **Câu hỏi cũ (Tiếng Trung):** `哑。（猜一成语）`
- **Lựa chọn cũ:** A: `惟妙惟肖` | B: `有口难言` | C: `默不作声` | D: `` (Đáp án cũ: `2`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Cái gì có một miệng mở rộng nhưng không có răng, nuốt chìa khóa vào thì mở khóa ra?**
- **👉 Lựa chọn mới:**
  - **A.** Ổ khóa cửa
  - **B.** Cái hộp
  - **C.** Cái túi
  - **D.** Cái hòm
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Ổ khóa cửa)
- **Giá trị giáo dục / Định hướng tư duy:** *Vật dụng thường ngày - Ổ khóa bảo vệ ngôi nhà*

### Câu 192: [class_questions.xml - ID 229]
- **Phân loại vi phạm:** `Đố chữ Hán & Chiết tự` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'字谜'*)
- **Lý do cần sửa:** Đố chiết tự chữ tượng hình hoặc thành ngữ Hán ngữ cổ mà người chơi Việt Nam không thể suy luận logic.
- **Câu hỏi cũ (Tiếng Trung):** `无头无尾一亩田。（字谜）`
- **Lựa chọn cũ:** A: `亩` | B: `鱼` | C: `田` | D: `` (Đáp án cũ: `2`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Cái gì có răng sắc nhọn xếp hàng đều đặn nhưng không bao giờ cắn ai, dùng để chải mượt mái tóc?**
- **👉 Lựa chọn mới:**
  - **A.** Chiếc lược chải đầu
  - **B.** Cái cưa
  - **C.** Cái cào
  - **D.** Cái bàn chải
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Chiếc lược chải đầu)
- **Giá trị giáo dục / Định hướng tư duy:** *Vật dụng vệ sinh - Chiếc lược chải tóc*

### Câu 193: [class_questions.xml - ID 232]
- **Phân loại vi phạm:** `Đố chữ Hán & Chiết tự` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'成语'*)
- **Lý do cần sửa:** Đố chiết tự chữ tượng hình hoặc thành ngữ Hán ngữ cổ mà người chơi Việt Nam không thể suy luận logic.
- **Câu hỏi cũ (Tiếng Trung):** `跷跷板。(猜一成语）`
- **Lựa chọn cũ:** A: `一触即发` | B: `乐极生悲` | C: `此起彼伏` | D: `` (Đáp án cũ: `3`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Cái gì luôn đi lên khi trời đổ mưa to gió lớn?**
- **👉 Lựa chọn mới:**
  - **A.** Chiếc ô dù che mưa
  - **B.** Mặt trời
  - **C.** Con diều
  - **D.** Khinh khí cầu
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Chiếc ô dù che mưa)
- **Giá trị giáo dục / Định hướng tư duy:** *Tư duy quan sát - Chiếc ô bật mở hướng lên trời*

### Câu 194: [class_questions.xml - ID 235]
- **Phân loại vi phạm:** `Đố chữ Hán & Chiết tự` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'字谜'*)
- **Lý do cần sửa:** Đố chiết tự chữ tượng hình hoặc thành ngữ Hán ngữ cổ mà người chơi Việt Nam không thể suy luận logic.
- **Câu hỏi cũ (Tiếng Trung):** `阎罗王。（字谜）`
- **Lựa chọn cũ:** A: `主` | B: `瑰` | C: `萝` | D: `` (Đáp án cũ: `2`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Cái gì có thể đi vòng quanh thế giới mà suốt đời chỉ đứng yên ở một góc phong bì thư?**
- **👉 Lựa chọn mới:**
  - **A.** Con tem bưu chính
  - **B.** Bức thư
  - **C.** Cái kéo
  - **D.** Hòm thư
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Con tem bưu chính)
- **Giá trị giáo dục / Định hướng tư duy:** *Bưu chính viễn thông - Con tem dán góc bì thư*

### Câu 195: [class_questions.xml - ID 237]
- **Phân loại vi phạm:** `Tuyên truyền quốc gia 'Nước ta'` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'我国'*)
- **Lý do cần sửa:** Dùng cụm từ 'nước ta' ('我国') để nhồi nhét biểu tượng, ngày lễ, thủ đô, chính sách của Trung Quốc cho người chơi Việt Nam.
- **Câu hỏi cũ (Tiếng Trung):** `泰山属于我国哪个省份？`
- **Lựa chọn cũ:** A: `河南` | B: `江苏` | C: `山东` | D: `` (Đáp án cũ: `3`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Chất cồn trong rượu bia ảnh hưởng nghiêm trọng đến cơ quan nào khiến người lái xe mất phản xạ an toàn?**
- **👉 Lựa chọn mới:**
  - **A.** Hệ thần kinh trung ương và não bộ
  - **B.** Xương khớp
  - **C.** Móng tay
  - **D.** Tóc
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Hệ thần kinh trung ương và não bộ)
- **Giá trị giáo dục / Định hướng tư duy:** *Tuyên truyền an toàn - Đã uống rượu bia thì không lái xe*

### Câu 196: [class_questions.xml - ID 241]
- **Phân loại vi phạm:** `Đố chữ Hán & Chiết tự` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'成语'*)
- **Lý do cần sửa:** Đố chiết tự chữ tượng hình hoặc thành ngữ Hán ngữ cổ mà người chơi Việt Nam không thể suy luận logic.
- **Câu hỏi cũ (Tiếng Trung):** `初一。(猜一成语）`
- **Lựa chọn cũ:** A: `有始有终` | B: `日新月异` | C: `` | D: `` (Đáp án cũ: `2`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Cái gì thuộc về riêng bạn, do bố mẹ đặt cho, nhưng người khác lại dùng nó nhiều hơn bạn?**
- **👉 Lựa chọn mới:**
  - **A.** Tên gọi của bạn
  - **B.** Đôi giày
  - **C.** Cái mũ
  - **D.** Chiếc cặp
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Tên gọi của bạn)
- **Giá trị giáo dục / Định hướng tư duy:** *Đố mẹo đời sống - Tên gọi để người khác xưng hô*

### Câu 197: [class_questions.xml - ID 243]
- **Phân loại vi phạm:** `Đố chữ Hán & Chiết tự` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'字谜'*)
- **Lý do cần sửa:** Đố chiết tự chữ tượng hình hoặc thành ngữ Hán ngữ cổ mà người chơi Việt Nam không thể suy luận logic.
- **Câu hỏi cũ (Tiếng Trung):** `与吾同行。(字谜）`
- **Lựa chọn cũ:** A: `行` | B: `衙` | C: `衔` | D: `` (Đáp án cũ: `2`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Con gì có mũi mà không có mắt, có lưỡi sắc bén mà không có miệng?**
- **👉 Lựa chọn mới:**
  - **A.** Con dao
  - **B.** Con kéo
  - **C.** Con kìm
  - **D.** Con ốc
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Con dao)
- **Giá trị giáo dục / Định hướng tư duy:** *Đồ dùng nhà bếp - Cấu tạo lưỡi dao và mũi dao*

### Câu 198: [class_questions.xml - ID 246]
- **Phân loại vi phạm:** `Đố chữ Hán & Chiết tự` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'成语'*)
- **Lý do cần sửa:** Đố chiết tự chữ tượng hình hoặc thành ngữ Hán ngữ cổ mà người chơi Việt Nam không thể suy luận logic.
- **Câu hỏi cũ (Tiếng Trung):** `无底洞。（猜一成语）`
- **Lựa chọn cũ:** A: `深不可测` | B: `漆黑一片` | C: `` | D: `` (Đáp án cũ: `1`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Có một chiếc thuyền chở tối đa được 2 người. Có 2 người cha và 2 người con muốn qua sông. Hỏi cần chở ít nhất mấy lượt?**
- **👉 Lựa chọn mới:**
  - **A.** Chỉ cần 1 lượt chở 3 người (ông, cha, con trai)
  - **B.** 4 lượt
  - **C.** 3 lượt
  - **D.** 2 lượt
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Chỉ cần 1 lượt chở 3 người (ông, cha, con trai))
- **Giá trị giáo dục / Định hướng tư duy:** *Toán đố gia đình - Ba thế hệ ông - cha - con*

### Câu 199: [class_questions.xml - ID 248]
- **Phân loại vi phạm:** `Đố chữ Hán & Chiết tự` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'字谜'*)
- **Lý do cần sửa:** Đố chiết tự chữ tượng hình hoặc thành ngữ Hán ngữ cổ mà người chơi Việt Nam không thể suy luận logic.
- **Câu hỏi cũ (Tiếng Trung):** `裹脚。（字谜）`
- **Lựa chọn cũ:** A: `跳` | B: `跑` | C: `踝` | D: `` (Đáp án cũ: `2`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Một đàn vịt: 1 con đi trước 2 con, 1 con đi sau 2 con, 1 con đi giữa 2 con. Hỏi đàn vịt có ít nhất mấy con?**
- **👉 Lựa chọn mới:**
  - **A.** 3 con vịt đi nối đuôi nhau hàng dọc
  - **B.** 6 con
  - **C.** 4 con
  - **D.** 5 con
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (3 con vịt đi nối đuôi nhau hàng dọc)
- **Giá trị giáo dục / Định hướng tư duy:** *Toán đố logic vị trí - 3 chú vịt xếp hàng dọc*

### Câu 200: [class_questions.xml - ID 253]
- **Phân loại vi phạm:** `Đố chữ Hán & Chiết tự` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'字谜'*)
- **Lý do cần sửa:** Đố chiết tự chữ tượng hình hoặc thành ngữ Hán ngữ cổ mà người chơi Việt Nam không thể suy luận logic.
- **Câu hỏi cũ (Tiếng Trung):** `昨日不可留。(字谜）`
- **Lựa chọn cũ:** A: `叩` | B: `乍` | C: `咋` | D: `` (Đáp án cũ: `2`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Vừa gà vừa chó, bó lại cho tròn, 36 con, 100 chân chẵn. Hỏi có bao nhiêu con gà và bao nhiêu con chó?**
- **👉 Lựa chọn mới:**
  - **A.** 22 con gà và 14 con chó
  - **B.** 20 con gà và 16 con chó
  - **C.** 24 con gà và 12 con chó
  - **D.** 18 con gà và 18 con chó
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (22 con gà và 14 con chó)
- **Giá trị giáo dục / Định hướng tư duy:** *Toán cổ dân gian - Bài toán gà chó kinh điển*

### Câu 201: [class_questions.xml - ID 257]
- **Phân loại vi phạm:** `Đố chữ Hán & Chiết tự` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'字谜'*)
- **Lý do cần sửa:** Đố chiết tự chữ tượng hình hoặc thành ngữ Hán ngữ cổ mà người chơi Việt Nam không thể suy luận logic.
- **Câu hỏi cũ (Tiếng Trung):** `脱口而出。（字谜）`
- **Lựa chọn cũ:** A: `嘘` | B: `咄` | C: `` | D: `` (Đáp án cũ: `2`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Một chú ốc sên leo lên cây cau cao 10m. Ban ngày leo được 3m, ban đêm tụt xuống 2m. Hỏi sau bao nhiêu ngày chú ốc sên leo lên tới đỉnh cây?**
- **👉 Lựa chọn mới:**
  - **A.** 8 ngày (ngày thứ 8 leo 3m chạm đỉnh cây không bị tụt)
  - **B.** 10 ngày
  - **C.** 7 ngày
  - **D.** 9 ngày
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (8 ngày (ngày thứ 8 leo 3m chạm đỉnh cây không bị tụt))
- **Giá trị giáo dục / Định hướng tư duy:** *Toán tư duy thực tế - Bài toán ốc sên leo cây*

### Câu 202: [class_questions.xml - ID 259]
- **Phân loại vi phạm:** `Đố chữ Hán & Chiết tự` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'字谜'*)
- **Lý do cần sửa:** Đố chiết tự chữ tượng hình hoặc thành ngữ Hán ngữ cổ mà người chơi Việt Nam không thể suy luận logic.
- **Câu hỏi cũ (Tiếng Trung):** `金字塔。（字谜）`
- **Lựa chọn cũ:** A: `晶` | B: `鑫` | C: `淼` | D: `` (Đáp án cũ: `2`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Một bể nước có 2 vòi chảy vào: Vòi thứ nhất chảy một mình 2 giờ đầy bể, Vòi thứ hai chảy một mình 3 giờ đầy bể. Mở cả 2 vòi cùng lúc thì sau bao lâu đầy bể?**
- **👉 Lựa chọn mới:**
  - **A.** 1.2 giờ (tức 1 giờ 12 phút)
  - **B.** 1.5 giờ
  - **C.** 2.5 giờ
  - **D.** 5 giờ
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (1.2 giờ (tức 1 giờ 12 phút))
- **Giá trị giáo dục / Định hướng tư duy:** *Toán tư duy công việc chung - Bài toán vòi nước chảy vào bể*

### Câu 203: [class_questions.xml - ID 261]
- **Phân loại vi phạm:** `Đố chữ Hán & Chiết tự` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'字谜'*)
- **Lý do cần sửa:** Đố chiết tự chữ tượng hình hoặc thành ngữ Hán ngữ cổ mà người chơi Việt Nam không thể suy luận logic.
- **Câu hỏi cũ (Tiếng Trung):** `苗头不对。（字谜）`
- **Lựa chọn cũ:** A: `田` | B: `笛` | C: `瞄` | D: `` (Đáp án cũ: `2`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Để nguyên là thứ thắp trong đêm rằm, thêm sắc thành thứ đội trên đầu khi trời nắng là chữ gì?**
- **👉 Lựa chọn mới:**
  - **A.** Nến - Nón
  - **B.** Đèn - Đón
  - **C.** Trăng - Trắng
  - **D.** Sao - Sáng
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Nến - Nón)
- **Giá trị giáo dục / Định hướng tư duy:** *Đố chữ tiếng Việt - Nến thắp sáng và chiếc nón lá*

### Câu 204: [class_questions.xml - ID 267]
- **Phân loại vi phạm:** `Đố chữ Hán & Chiết tự` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'成语'*)
- **Lý do cần sửa:** Đố chiết tự chữ tượng hình hoặc thành ngữ Hán ngữ cổ mà người chơi Việt Nam không thể suy luận logic.
- **Câu hỏi cũ (Tiếng Trung):** `千里通电话。（猜一成语）`
- **Lựa chọn cũ:** A: `遥相呼应` | B: `白费力气` | C: `屡见不鲜` | D: `` (Đáp án cũ: `1`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Để nguyên dùng bắc qua sông, thêm huyền thành màu của mây trời ngày giông bão là chữ gì?**
- **👉 Lựa chọn mới:**
  - **A.** Cầu - Cầu huyền Cầu (Cầu - Cầu)
  - **B.** Cầu - Cầu
  - **C.** Cầu - Cầu
  - **D.** Cầu - Cầu
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Cầu - Cầu huyền Cầu (Cầu - Cầu))
- **Giá trị giáo dục / Định hướng tư duy:** *Đố chữ tiếng Việt - Cây cầu bắc nhịp*

### Câu 205: [class_questions.xml - ID 268]
- **Phân loại vi phạm:** `Đố chữ Hán & Chiết tự` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'字谜'*)
- **Lý do cần sửa:** Đố chiết tự chữ tượng hình hoặc thành ngữ Hán ngữ cổ mà người chơi Việt Nam không thể suy luận logic.
- **Câu hỏi cũ (Tiếng Trung):** `有声有色。（字谜）`
- **Lựa chọn cũ:** A: `黯` | B: `扰` | C: `音` | D: `` (Đáp án cũ: `1`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Để nguyên bay lượn trên trời, thêm sắc thành con vật bắt chuột là chữ gì?**
- **👉 Lựa chọn mới:**
  - **A.** Mây - Mấy
  - **B.** Gió - Gió
  - **C.** Sao - Sáo
  - **D.** Bướm - Bướm
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Mây - Mấy)
- **Giá trị giáo dục / Định hướng tư duy:** *Đố chữ tiếng Việt - Chim sáo bay lượn*

### Câu 206: [class_questions.xml - ID 278]
- **Phân loại vi phạm:** `Đố chữ Hán & Chiết tự` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'字谜'*)
- **Lý do cần sửa:** Đố chiết tự chữ tượng hình hoặc thành ngữ Hán ngữ cổ mà người chơi Việt Nam không thể suy luận logic.
- **Câu hỏi cũ (Tiếng Trung):** `枫树无风，旁边有位公公。（字谜）`
- **Lựa chọn cũ:** A: `抚` | B: `松` | C: `飒` | D: `` (Đáp án cũ: `2`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Để nguyên là loài cá bơi dưới nước, bớt đầu thành loài chim báo hiệu mùa xuân là chữ gì?**
- **👉 Lựa chọn mới:**
  - **A.** Én (Cá bén - Én)
  - **B.** Cá chép
  - **C.** Cá quả
  - **D.** Cá thu
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Én (Cá bén - Én))
- **Giá trị giáo dục / Định hướng tư duy:** *Đố chữ tiếng Việt - Chim én liệng mùa xuân*

### Câu 207: [class_questions.xml - ID 281]
- **Phân loại vi phạm:** `Đố chữ Hán & Chiết tự` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'字谜'*)
- **Lý do cần sửa:** Đố chiết tự chữ tượng hình hoặc thành ngữ Hán ngữ cổ mà người chơi Việt Nam không thể suy luận logic.
- **Câu hỏi cũ (Tiếng Trung):** `挖空心思。（字谜）`
- **Lựa chọn cũ:** A: `田` | B: `供` | C: `究` | D: `` (Đáp án cũ: `1`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Từ nào trong tiếng Việt có 12 chữ cái nhưng ai đọc vào cũng chỉ thấy có một chữ?**
- **👉 Lựa chọn mới:**
  - **A.** Chữ 'Mười hai' (hoặc Chữ nhật)
  - **B.** Chữ cái
  - **C.** Bảng chữ cái
  - **D.** Bách khoa
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Chữ 'Mười hai' (hoặc Chữ nhật))
- **Giá trị giáo dục / Định hướng tư duy:** *Đố vui ngôn ngữ - Chơi chữ độc đáo tiếng Việt*

### Câu 208: [class_questions.xml - ID 288]
- **Phân loại vi phạm:** `Đố chữ Hán & Chiết tự` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'成语'*)
- **Lý do cần sửa:** Đố chiết tự chữ tượng hình hoặc thành ngữ Hán ngữ cổ mà người chơi Việt Nam không thể suy luận logic.
- **Câu hỏi cũ (Tiếng Trung):** `飞行员。（猜一成语）`
- **Lựa chọn cũ:** A: `有机可乘` | B: `高瞻远瞩` | C: `日上千里` | D: `` (Đáp án cũ: `1`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Từ nào trong tiếng Việt có tất cả các dấu thanh (ngang, huyền, sắc, hỏi, ngã, nặng)?**
- **👉 Lựa chọn mới:**
  - **A.** Tiếng Việt thân yêu
  - **B.** Bảng chữ cái
  - **C.** Ngôn ngữ
  - **D.** Từ điển
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Tiếng Việt thân yêu)
- **Giá trị giáo dục / Định hướng tư duy:** *Đặc trưng tiếng Việt - Hệ thống thanh điệu phong phú*

### Câu 209: [class_questions.xml - ID 293]
- **Phân loại vi phạm:** `Đố chữ Hán & Chiết tự` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'字谜'*)
- **Lý do cần sửa:** Đố chiết tự chữ tượng hình hoặc thành ngữ Hán ngữ cổ mà người chơi Việt Nam không thể suy luận logic.
- **Câu hỏi cũ (Tiếng Trung):** `真丢人。(字谜)`
- **Lựa chọn cũ:** A: `三` | B: `直` | C: `县` | D: `` (Đáp án cũ: `2`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Trong bảng chữ cái tiếng Việt hiện đại có tất cả bao nhiêu chữ cái chính thức?**
- **👉 Lựa chọn mới:**
  - **A.** 29 chữ cái
  - **B.** 26 chữ cái
  - **C.** 24 chữ cái
  - **D.** 32 chữ cái
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (29 chữ cái)
- **Giá trị giáo dục / Định hướng tư duy:** *Tiếng Việt chuẩn mực - 29 chữ cái quốc ngữ*

### Câu 210: [class_questions.xml - ID 294]
- **Phân loại vi phạm:** `Đố chữ Hán & Chiết tự` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'成语'*)
- **Lý do cần sửa:** Đố chiết tự chữ tượng hình hoặc thành ngữ Hán ngữ cổ mà người chơi Việt Nam không thể suy luận logic.
- **Câu hỏi cũ (Tiếng Trung):** `快刀斩乱麻。（猜一成语）`
- **Lựa chọn cũ:** A: `分秒必争` | B: `一刻千金` | C: `迎刃而解` | D: `` (Đáp án cũ: `3`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Dấu câu nào trong tiếng Việt dùng để kết thúc một câu trần thuật kể chuyện?**
- **👉 Lựa chọn mới:**
  - **A.** Dấu chấm (.)
  - **B.** Dấu chấm hỏi (?)
  - **C.** Dấu chấm than (!)
  - **D.** Dấu hai chấm (:)
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Dấu chấm (.))
- **Giá trị giáo dục / Định hướng tư duy:** *Ngữ pháp tiếng Việt - Chức năng của dấu chấm*

### Câu 211: [class_questions.xml - ID 299]
- **Phân loại vi phạm:** `Tuyên truyền quốc gia 'Nước ta'` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'我国'*)
- **Lý do cần sửa:** Dùng cụm từ 'nước ta' ('我国') để nhồi nhét biểu tượng, ngày lễ, thủ đô, chính sách của Trung Quốc cho người chơi Việt Nam.
- **Câu hỏi cũ (Tiếng Trung):** `什么球被誉为我国的“国球”？`
- **Lựa chọn cũ:** A: `足球` | B: `篮球` | C: `乒乓球` | D: `` (Đáp án cũ: `3`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Khi gặp biển báo giao thông hình tròn viền đỏ nền trắng, đó thường là loại biển báo gì?**
- **👉 Lựa chọn mới:**
  - **A.** Biển báo cấm
  - **B.** Biển chỉ dẫn
  - **C.** Biển cảnh báo nguy hiểm
  - **D.** Biển hiệu lệnh
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Biển báo cấm)
- **Giá trị giáo dục / Định hướng tư duy:** *Luật giao thông - Phân biệt các nhóm biển báo đường bộ*

### Câu 212: [class_questions.xml - ID 300]
- **Phân loại vi phạm:** `Đố chữ Hán & Chiết tự` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'成语'*)
- **Lý do cần sửa:** Đố chiết tự chữ tượng hình hoặc thành ngữ Hán ngữ cổ mà người chơi Việt Nam không thể suy luận logic.
- **Câu hỏi cũ (Tiếng Trung):** `遇事不求人。（猜一成语）`
- **Lựa chọn cũ:** A: `自力更生` | B: `不言而喻` | C: `难以沟通` | D: `` (Đáp án cũ: `1`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Dấu câu nào dùng ở cuối câu để bày tỏ cảm xúc ngạc nhiên, thán phục hoặc vui mừng?**
- **👉 Lựa chọn mới:**
  - **A.** Dấu chấm than (!)
  - **B.** Dấu chấm (.)
  - **C.** Dấu phẩy (,)
  - **D.** Dấu ngoặc kép
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Dấu chấm than (!))
- **Giá trị giáo dục / Định hướng tư duy:** *Ngữ pháp tiếng Việt - Biểu cảm cùng dấu chấm than*

### Câu 213: [class_questions.xml - ID 305]
- **Phân loại vi phạm:** `Đố chữ Hán & Chiết tự` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'成语'*)
- **Lý do cần sửa:** Đố chiết tự chữ tượng hình hoặc thành ngữ Hán ngữ cổ mà người chơi Việt Nam không thể suy luận logic.
- **Câu hỏi cũ (Tiếng Trung):** `导游。（猜一成语）`
- **Lựa chọn cũ:** A: `半途而废` | B: `有口难言` | C: `引人入胜` | D: `` (Đáp án cũ: `3`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Thành ngữ nào của người Việt khuyên chúng ta phải biết ơn người đã giúp đỡ mình?**
- **👉 Lựa chọn mới:**
  - **A.** Ăn quả nhớ kẻ trồng cây
  - **B.** Ăn cháo đá bát
  - **C.** Nước chảy đá mòn
  - **D.** Qua cầu rút ván
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Ăn quả nhớ kẻ trồng cây)
- **Giá trị giáo dục / Định hướng tư duy:** *Đạo lý truyền thống - Uống nước nhớ nguồn, ăn quả nhớ kẻ trồng cây*

### Câu 214: [class_questions.xml - ID 311]
- **Phân loại vi phạm:** `Đố chữ Hán & Chiết tự` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'成语'*)
- **Lý do cần sửa:** Đố chiết tự chữ tượng hình hoặc thành ngữ Hán ngữ cổ mà người chơi Việt Nam không thể suy luận logic.
- **Câu hỏi cũ (Tiếng Trung):** `伞兵。(猜一成语）`
- **Lựa chọn cũ:** A: `腾云驾雾` | B: `从天而降` | C: `不同凡响` | D: `` (Đáp án cũ: `2`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Thành ngữ nào khuyên chúng ta phải có tinh thần đoàn kết, giúp đỡ người hoạn nạn?**
- **👉 Lựa chọn mới:**
  - **A.** Lá lành đùm lá rách
  - **B.** Đèn nhà ai nấy rạng
  - **C.** Cháy nhà hàng xóm bình chân như vại
  - **D.** Mạnh ai nấy làm
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Lá lành đùm lá rách)
- **Giá trị giáo dục / Định hướng tư duy:** *Truyền thống tương thân tương ái - Lá lành đùm lá rách*

### Câu 215: [class_questions.xml - ID 315]
- **Phân loại vi phạm:** `Đố chữ Hán & Chiết tự` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'字谜'*)
- **Lý do cần sửa:** Đố chiết tự chữ tượng hình hoặc thành ngữ Hán ngữ cổ mà người chơi Việt Nam không thể suy luận logic.
- **Câu hỏi cũ (Tiếng Trung):** `充耳不闻。（字谜）`
- **Lựa chọn cũ:** A: `耳` | B: `儿` | C: `龙` | D: `` (Đáp án cũ: `3`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Câu tục ngữ 'Học thầy không tày học...' khuyên chúng ta nên học hỏi thêm từ ai?**
- **👉 Lựa chọn mới:**
  - **A.** Học bạn
  - **B.** Học sách
  - **C.** Học máy tính
  - **D.** Học người lạ
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Học bạn)
- **Giá trị giáo dục / Định hướng tư duy:** *Kinh nghiệm học tập - Học hỏi bạn bè cùng tiến bộ*

### Câu 216: [class_questions.xml - ID 318]
- **Phân loại vi phạm:** `Đố chữ Hán & Chiết tự` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'成语'*)
- **Lý do cần sửa:** Đố chiết tự chữ tượng hình hoặc thành ngữ Hán ngữ cổ mà người chơi Việt Nam không thể suy luận logic.
- **Câu hỏi cũ (Tiếng Trung):** `垃圾箱。（猜一成语）`
- **Lựa chọn cũ:** A: `藏污纳垢` | B: `谈何容易` | C: `好景不长` | D: `` (Đáp án cũ: `1`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Câu tục ngữ 'Gần mực thì đen, gần đèn thì...' dạy chúng ta điều gì?**
- **👉 Lựa chọn mới:**
  - **A.** Gần đèn thì rạng (sáng)
  - **B.** Gần đèn thì nóng
  - **C.** Gần đèn thì mờ
  - **D.** Gần đèn thì tối
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Gần đèn thì rạng (sáng))
- **Giá trị giáo dục / Định hướng tư duy:** *Bài học đạo đức - Chọn bạn tốt mà chơi*

### Câu 217: [class_questions.xml - ID 320]
- **Phân loại vi phạm:** `Đố chữ Hán & Chiết tự` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'成语'*)
- **Lý do cần sửa:** Đố chiết tự chữ tượng hình hoặc thành ngữ Hán ngữ cổ mà người chơi Việt Nam không thể suy luận logic.
- **Câu hỏi cũ (Tiếng Trung):** `显微镜。（成语谜）`
- **Lựa chọn cũ:** A: `放大效应` | B: `目不转睛` | C: `一孔之见` | D: `` (Đáp án cũ: `3`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Thành ngữ 'Vạn sự khởi đầu nan' có ý nghĩa khuyên nhủ con người điều gì?**
- **👉 Lựa chọn mới:**
  - **A.** Mọi việc lúc bắt đầu đều khó khăn, cần kiên trì không nản chí
  - **B.** Làm việc gì cũng thất bại
  - **C.** Không nên làm việc khó
  - **D.** Chờ may mắn đến
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Mọi việc lúc bắt đầu đều khó khăn, cần kiên trì không nản chí)
- **Giá trị giáo dục / Định hướng tư duy:** *Ý chí rèn luyện - Vượt qua khó khăn ban đầu để thành công*

### Câu 218: [class_questions.xml - ID 323]
- **Phân loại vi phạm:** `Đố chữ Hán & Chiết tự` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'成语'*)
- **Lý do cần sửa:** Đố chiết tự chữ tượng hình hoặc thành ngữ Hán ngữ cổ mà người chơi Việt Nam không thể suy luận logic.
- **Câu hỏi cũ (Tiếng Trung):** `鹊巢鸦占。（成语谜）`
- **Lựa chọn cũ:** A: `力争上游` | B: `悲喜交加` | C: `化为乌有` | D: `` (Đáp án cũ: `3`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Câu ca dao 'Công cha như núi Thái Sơn / Nghĩa mẹ như nước trong nguồn chảy ra' nhắc nhở bổn phận gì?**
- **👉 Lựa chọn mới:**
  - **A.** Bổn phận chữ hiếu biết ơn cha mẹ sinh thành nuôi dưỡng
  - **B.** Phải leo núi cao
  - **C.** Phải đi tìm nguồn nước
  - **D.** Đi xa quê hương
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Bổn phận chữ hiếu biết ơn cha mẹ sinh thành nuôi dưỡng)
- **Giá trị giáo dục / Định hướng tư duy:** *Công ơn sinh thành - Chữ hiếu thiêng liêng với cha mẹ*

### Câu 219: [class_questions.xml - ID 326]
- **Phân loại vi phạm:** `Đố chữ Hán & Chiết tự` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'字谜'*)
- **Lý do cần sửa:** Đố chiết tự chữ tượng hình hoặc thành ngữ Hán ngữ cổ mà người chơi Việt Nam không thể suy luận logic.
- **Câu hỏi cũ (Tiếng Trung):** `三面墙，一面空，小孩子，在当中。(字谜）`
- **Lựa chọn cũ:** A: `四` | B: `匹` | C: `兀` | D: `` (Đáp án cũ: `2`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Từ đồng nghĩa với từ 'Tổ quốc' trong tiếng Việt là từ nào?**
- **👉 Lựa chọn mới:**
  - **A.** Đất nước, Giang sơn, Quê hương
  - **B.** Ngôi nhà
  - **C.** Lớp học
  - **D.** Khu phố
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Đất nước, Giang sơn, Quê hương)
- **Giá trị giáo dục / Định hướng tư duy:** *Từ vựng tiếng Việt - Các từ đồng nghĩa chỉ Tổ quốc*

### Câu 220: [class_questions.xml - ID 331]
- **Phân loại vi phạm:** `Đố chữ Hán & Chiết tự` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'字谜'*)
- **Lý do cần sửa:** Đố chiết tự chữ tượng hình hoặc thành ngữ Hán ngữ cổ mà người chơi Việt Nam không thể suy luận logic.
- **Câu hỏi cũ (Tiếng Trung):** `鱼肚子。（字谜）`
- **Lựa chọn cũ:** A: `亩` | B: `鱼` | C: `田` | D: `` (Đáp án cũ: `3`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Từ trái nghĩa với từ 'Dũng cảm' trong tiếng Việt là từ nào?**
- **👉 Lựa chọn mới:**
  - **A.** Hèn nhát
  - **B.** Gan dạ
  - **C.** Anh dũng
  - **D.** Kiên cường
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Hèn nhát)
- **Giá trị giáo dục / Định hướng tư duy:** *Từ trái nghĩa - Rèn luyện lòng dũng cảm, bài trừ hèn nhát*

### Câu 221: [class_questions.xml - ID 334]
- **Phân loại vi phạm:** `Đố chữ Hán & Chiết tự` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'成语'*)
- **Lý do cần sửa:** Đố chiết tự chữ tượng hình hoặc thành ngữ Hán ngữ cổ mà người chơi Việt Nam không thể suy luận logic.
- **Câu hỏi cũ (Tiếng Trung):** `没关水龙头。(猜一成语）`
- **Lựa chọn cũ:** A: `自由自在` | B: `水到渠成` | C: `放任自流` | D: `` (Đáp án cũ: `3`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Từ trái nghĩa với từ 'Trung thực' trong học tập và thi cử là từ nào?**
- **👉 Lựa chọn mới:**
  - **A.** Gian dối
  - **B.** Thật thà
  - **C.** Ngay thẳng
  - **D.** Chân thành
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Gian dối)
- **Giá trị giáo dục / Định hướng tư duy:** *Đức tính học sinh - Trung thực trong học tập*

### Câu 222: [class_questions.xml - ID 339]
- **Phân loại vi phạm:** `Tuyên truyền quốc gia 'Nước ta'` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'我国'*)
- **Lý do cần sửa:** Dùng cụm từ 'nước ta' ('我国') để nhồi nhét biểu tượng, ngày lễ, thủ đô, chính sách của Trung Quốc cho người chơi Việt Nam.
- **Câu hỏi cũ (Tiếng Trung):** `九寨沟属于我国哪个省份？`
- **Lựa chọn cũ:** A: `黑龙江` | B: `四川省` | C: `辽宁省` | D: `` (Đáp án cũ: `2`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Biển báo giao thông hình tam giác đều viền đỏ nền vàng bên trong có hình vẽ màu đen là biển báo gì?**
- **👉 Lựa chọn mới:**
  - **A.** Biển báo nguy hiểm và cảnh báo
  - **B.** Biển cấm
  - **C.** Biển chỉ dẫn
  - **D.** Biển ưu tiên
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Biển báo nguy hiểm và cảnh báo)
- **Giá trị giáo dục / Định hướng tư duy:** *Luật giao thông - Biển báo nguy hiểm cảnh báo tai nạn*

### Câu 223: [class_questions.xml - ID 343]
- **Phân loại vi phạm:** `Đố chữ Hán & Chiết tự` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'成语'*)
- **Lý do cần sửa:** Đố chiết tự chữ tượng hình hoặc thành ngữ Hán ngữ cổ mà người chơi Việt Nam không thể suy luận logic.
- **Câu hỏi cũ (Tiếng Trung):** `零存整取。(猜一成语）`
- **Lựa chọn cũ:** A: `从无到有` | B: `积少成多` | C: `` | D: `` (Đáp án cũ: `2`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Trong câu thơ 'Tre xanh xanh tự bao giờ / Chuyện ngày xưa đã có bờ tre xanh', hình ảnh cây tre tượng trưng cho ai?**
- **👉 Lựa chọn mới:**
  - **A.** Con người và phẩm chất kiên cường của dân tộc Việt Nam
  - **B.** Loài cây dại
  - **C.** Vật liệu xây nhà
  - **D.** Món đồ trang trí
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Con người và phẩm chất kiên cường của dân tộc Việt Nam)
- **Giá trị giáo dục / Định hướng tư duy:** *Hình tượng văn học - Cây tre biểu tượng cốt cách Việt Nam*

### Câu 224: [class_questions.xml - ID 345]
- **Phân loại vi phạm:** `Đố chữ Hán & Chiết tự` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'字谜'*)
- **Lý do cần sửa:** Đố chiết tự chữ tượng hình hoặc thành ngữ Hán ngữ cổ mà người chơi Việt Nam không thể suy luận logic.
- **Câu hỏi cũ (Tiếng Trung):** `四方一条心。(字谜）`
- **Lựa chọn cũ:** A: `塄` | B: `愣` | C: `棱` | D: `` (Đáp án cũ: `2`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Hình ảnh con cò lặn lội bờ sông trong ca dao Việt Nam thường tượng trưng cho ai?**
- **👉 Lựa chọn mới:**
  - **A.** Người mẹ, người phụ nữ tần tảo sớm hôm
  - **B.** Người đi câu
  - **C.** Trẻ chăn trâu
  - **D.** Thương nhân
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Người mẹ, người phụ nữ tần tảo sớm hôm)
- **Giá trị giáo dục / Định hướng tư duy:** *Hình ảnh ca dao - Thân cò lặn lội tần tảo nuôi con*

### Câu 225: [class_questions.xml - ID 350]
- **Phân loại vi phạm:** `Đố chữ Hán & Chiết tự` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'字谜'*)
- **Lý do cần sửa:** Đố chiết tự chữ tượng hình hoặc thành ngữ Hán ngữ cổ mà người chơi Việt Nam không thể suy luận logic.
- **Câu hỏi cũ (Tiếng Trung):** `日月同行。（字谜）`
- **Lựa chọn cũ:** A: `明` | B: `胆` | C: `崩` | D: `` (Đáp án cũ: `1`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Tác phẩm thiếu nhi kinh điển kể về cuộc phiêu lưu của chú dế giàu nghĩa khí của nhà văn Tô Hoài tên là gì?**
- **👉 Lựa chọn mới:**
  - **A.** Dế Mèn phiêu lưu ký
  - **B.** Đất rừng phương Nam
  - **C.** Góc sân và khoảng trời
  - **D.** Búp sen xanh
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Dế Mèn phiêu lưu ký)
- **Giá trị giáo dục / Định hướng tư duy:** *Văn học thiếu nhi - Tác phẩm Dế Mèn phiêu lưu ký*

### Câu 226: [class_questions.xml - ID 351]
- **Phân loại vi phạm:** `Đố chữ Hán & Chiết tự` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'成语'*)
- **Lý do cần sửa:** Đố chiết tự chữ tượng hình hoặc thành ngữ Hán ngữ cổ mà người chơi Việt Nam không thể suy luận logic.
- **Câu hỏi cũ (Tiếng Trung):** `下面哪个成语没有错别字？`
- **Lựa chọn cũ:** A: `目不转睛` | B: `刻服困难` | C: `丢三拉四` | D: `` (Đáp án cũ: `1`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Tác phẩm 'Đất rừng phương Nam' kể về hành trình tìm cha của cậu bé An là của nhà văn nào?**
- **👉 Lựa chọn mới:**
  - **A.** Nhà văn Đoàn Giỏi
  - **B.** Nhà văn Kim Lân
  - **C.** Nhà văn Nam Cao
  - **D.** Nhà văn Vũ Tú Nam
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Nhà văn Đoàn Giỏi)
- **Giá trị giáo dục / Định hướng tư duy:** *Văn học Nam Bộ - Nhà văn Đoàn Giỏi và Đất rừng phương Nam*

### Câu 227: [class_questions.xml - ID 355]
- **Phân loại vi phạm:** `Đố chữ Hán & Chiết tự` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'字谜'*)
- **Lý do cần sửa:** Đố chiết tự chữ tượng hình hoặc thành ngữ Hán ngữ cổ mà người chơi Việt Nam không thể suy luận logic.
- **Câu hỏi cũ (Tiếng Trung):** `随风而舞。(字谜）`
- **Lựa chọn cũ:** A: `飘` | B: `足` | C: `口` | D: `` (Đáp án cũ: `1`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Tập thơ thiếu nhi trong trẻo 'Góc sân và khoảng trời' là sáng tác của nhà thơ thần đồng nào?**
- **👉 Lựa chọn mới:**
  - **A.** Trần Đăng Khoa
  - **B.** Định Hải
  - **C.** Xuân Quỳnh
  - **D.** Phạm Hổ
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Trần Đăng Khoa)
- **Giá trị giáo dục / Định hướng tư duy:** *Thơ ca tuổi thơ - Nhà thơ Trần Đăng Khoa*

### Câu 228: [class_questions.xml - ID 359]
- **Phân loại vi phạm:** `Đố chữ Hán & Chiết tự` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'成语'*)
- **Lý do cần sửa:** Đố chiết tự chữ tượng hình hoặc thành ngữ Hán ngữ cổ mà người chơi Việt Nam không thể suy luận logic.
- **Câu hỏi cũ (Tiếng Trung):** `愚公之家。（猜一成语）`
- **Lựa chọn cũ:** A: `开门见山` | B: `开天辟地` | C: `感同身受` | D: `` (Đáp án cũ: `1`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Bài thơ 'Hạt gạo làng ta' ca ngợi công sức lao động của ai làm ra hạt gạo trắng thơm?**
- **👉 Lựa chọn mới:**
  - **A.** Người nông dân, mẹ và các bạn nhỏ hậu phương
  - **B.** Máy móc nông nghiệp
  - **C.** Mưa gió tự nhiên
  - **D.** Thương lái
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Người nông dân, mẹ và các bạn nhỏ hậu phương)
- **Giá trị giáo dục / Định hướng tư duy:** *Thơ ca đồng quê - Hạt gạo làng ta nặng tình đất nước*

### Câu 229: [class_questions.xml - ID 361]
- **Phân loại vi phạm:** `Đố chữ Hán & Chiết tự` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'字谜'*)
- **Lý do cần sửa:** Đố chiết tự chữ tượng hình hoặc thành ngữ Hán ngữ cổ mà người chơi Việt Nam không thể suy luận logic.
- **Câu hỏi cũ (Tiếng Trung):** `一口咬破衣。（字谜）`
- **Lựa chọn cũ:** A: `哀` | B: `蓑` | C: `衰` | D: `` (Đáp án cũ: `1`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Trong môn Tiếng Việt, câu dùng để hỏi thông tin luôn kết thúc bằng dấu gì?**
- **👉 Lựa chọn mới:**
  - **A.** Dấu hỏi (?)
  - **B.** Dấu chấm (.)
  - **C.** Dấu ngã
  - **D.** Dấu gạch ngang
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Dấu hỏi (?))
- **Giá trị giáo dục / Định hướng tư duy:** *Ngữ pháp tiểu học - Nhận biết câu hỏi*

### Câu 230: [class_questions.xml - ID 363]
- **Phân loại vi phạm:** `Đố chữ Hán & Chiết tự` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'字谜'*)
- **Lý do cần sửa:** Đố chiết tự chữ tượng hình hoặc thành ngữ Hán ngữ cổ mà người chơi Việt Nam không thể suy luận logic.
- **Câu hỏi cũ (Tiếng Trung):** `说话的才能。（字谜）`
- **Lựa chọn cũ:** A: `团` | B: `叩` | C: `咯` | D: `` (Đáp án cũ: `1`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Trong phép nhân số học, bất kỳ số nào nhân với số 0 cũng có kết quả bằng bao nhiêu?**
- **👉 Lựa chọn mới:**
  - **A.** Bằng 0
  - **B.** Bằng chính số đó
  - **C.** Bằng 1
  - **D.** Bằng vô cực
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Bằng 0)
- **Giá trị giáo dục / Định hướng tư duy:** *Toán học cơ bản - Tính chất của số 0 trong phép nhân*

### Câu 231: [class_questions.xml - ID 369]
- **Phân loại vi phạm:** `Đố chữ Hán & Chiết tự` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'成语'*)
- **Lý do cần sửa:** Đố chiết tự chữ tượng hình hoặc thành ngữ Hán ngữ cổ mà người chơi Việt Nam không thể suy luận logic.
- **Câu hỏi cũ (Tiếng Trung):** `纸老虎。（猜一成语）`
- **Lựa chọn cũ:** A: `栩栩如生` | B: `凶猛无比` | C: `外强中干` | D: `` (Đáp án cũ: `3`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Trong phép cộng, bất kỳ số nào cộng với số 0 cũng có kết quả bằng bao nhiêu?**
- **👉 Lựa chọn mới:**
  - **A.** Bằng chính số đó
  - **B.** Bằng 0
  - **C.** Bằng 1
  - **D.** Tăng gấp đôi
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Bằng chính số đó)
- **Giá trị giáo dục / Định hướng tư duy:** *Toán học cơ bản - Tính chất số 0 trong phép cộng*

### Câu 232: [class_questions.xml - ID 373]
- **Phân loại vi phạm:** `Tuyên truyền quốc gia 'Nước ta'` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'中国'*)
- **Lý do cần sửa:** Dùng cụm từ 'nước ta' ('我国') để nhồi nhét biểu tượng, ngày lễ, thủ đô, chính sách của Trung Quốc cho người chơi Việt Nam.
- **Câu hỏi cũ (Tiếng Trung):** `歇后语“中国的功夫”的后半句是什么？`
- **Lựa chọn cũ:** A: `名不虚传` | B: `拳打脚踢` | C: `` | D: `` (Đáp án cũ: `1`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Thời gian ngủ hợp lý mỗi ngày đối với lứa tuổi học sinh thiếu nhi để cơ thể phát triển khỏe mạnh là bao nhiêu tiếng?**
- **👉 Lựa chọn mới:**
  - **A.** Khoảng 8 - 10 tiếng mỗi đêm
  - **B.** Khoảng 3 - 4 tiếng
  - **C.** Khoảng 15 tiếng
  - **D.** Càng ít càng tốt
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Khoảng 8 - 10 tiếng mỗi đêm)
- **Giá trị giáo dục / Định hướng tư duy:** *Sức khỏe thiếu nhi - Tầm quan trọng của giấc ngủ đối với sự phát triển*

### Câu 233: [class_questions.xml - ID 376]
- **Phân loại vi phạm:** `Tuyên truyền quốc gia 'Nước ta'` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'中国'*)
- **Lý do cần sửa:** Dùng cụm từ 'nước ta' ('我国') để nhồi nhét biểu tượng, ngày lễ, thủ đô, chính sách của Trung Quốc cho người chơi Việt Nam.
- **Câu hỏi cũ (Tiếng Trung):** `不冷不热的地方，猜一中国城市。`
- **Lựa chọn cũ:** A: `南京` | B: `武汉` | C: `温州` | D: `` (Đáp án cũ: `3`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Bữa ăn quan trọng nhất trong ngày cung cấp năng lượng dồi dào cho việc học tập và hoạt động buổi sáng là bữa nào?**
- **👉 Lựa chọn mới:**
  - **A.** Bữa ăn sáng
  - **B.** Bữa ăn khuya lúc nửa đêm
  - **C.** Bữa ăn vặt buổi chiều
  - **D.** Bỏ bữa sáng ăn bù buổi trưa
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Bữa ăn sáng)
- **Giá trị giáo dục / Định hướng tư duy:** *Dinh dưỡng học đường - Bữa sáng nạp năng lượng vàng*

### Câu 234: [class_questions.xml - ID 380]
- **Phân loại vi phạm:** `Đố chữ Hán & Chiết tự` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'成语'*)
- **Lý do cần sửa:** Đố chiết tự chữ tượng hình hoặc thành ngữ Hán ngữ cổ mà người chơi Việt Nam không thể suy luận logic.
- **Câu hỏi cũ (Tiếng Trung):** `和尚撑伞。（成语谜）`
- **Lựa chọn cũ:** A: `无法无天` | B: `滴水不漏` | C: `安然无恙` | D: `` (Đáp án cũ: `1`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Một tam giác có ba cạnh bằng nhau thì gọi là hình tam giác gì?**
- **👉 Lựa chọn mới:**
  - **A.** Tam giác đều
  - **B.** Tam giác vuông
  - **C.** Tam giác cân
  - **D.** Tam giác nhọn
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Tam giác đều)
- **Giá trị giáo dục / Định hướng tư duy:** *Hình học phẳng - Định nghĩa tam giác đều*

### Câu 235: [class_questions.xml - ID 381]
- **Phân loại vi phạm:** `Đố chữ Hán & Chiết tự` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'成语'*)
- **Lý do cần sửa:** Đố chiết tự chữ tượng hình hoặc thành ngữ Hán ngữ cổ mà người chơi Việt Nam không thể suy luận logic.
- **Câu hỏi cũ (Tiếng Trung):** `下面哪个成语有错别字？`
- **Lựa chọn cũ:** A: `狐假虎威` | B: `虎背熊腰` | C: `熊心勃勃` | D: `` (Đáp án cũ: `3`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Hình vuông là hình tứ giác đặc biệt có đặc điểm gì?**
- **👉 Lựa chọn mới:**
  - **A.** Bốn cạnh bằng nhau và bốn góc vuông
  - **B.** Bốn cạnh bằng nhau nhưng không có góc vuông
  - **C.** Chỉ có hai cạnh bằng nhau
  - **D.** Bốn góc nhọn
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Bốn cạnh bằng nhau và bốn góc vuông)
- **Giá trị giáo dục / Định hướng tư duy:** *Hình học trực quan - Tính chất cơ bản của hình vuông*

### Câu 236: [class_questions.xml - ID 383]
- **Phân loại vi phạm:** `Đố chữ Hán & Chiết tự` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'字谜'*)
- **Lý do cần sửa:** Đố chiết tự chữ tượng hình hoặc thành ngữ Hán ngữ cổ mà người chơi Việt Nam không thể suy luận logic.
- **Câu hỏi cũ (Tiếng Trung):** `二十四小时。（字谜）`
- **Lựa chọn cũ:** A: `日` | B: `旧` | C: `土` | D: `` (Đáp án cũ: `2`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Đơn vị đo độ dài chuẩn quốc tế viết tắt là 'km' đọc là gì?**
- **👉 Lựa chọn mới:**
  - **A.** Ki-lô-mét
  - **B.** Ki-lô-gam
  - **C.** Mi-li-mét
  - **D.** Xăng-ti-mét
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Ki-lô-mét)
- **Giá trị giáo dục / Định hướng tư duy:** *Toán đo lường - Đơn vị đo độ dài ki-lô-mét*

### Câu 237: [class_questions.xml - ID 385]
- **Phân loại vi phạm:** `Đố chữ Hán & Chiết tự` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'成语'*)
- **Lý do cần sửa:** Đố chiết tự chữ tượng hình hoặc thành ngữ Hán ngữ cổ mà người chơi Việt Nam không thể suy luận logic.
- **Câu hỏi cũ (Tiếng Trung):** `尽收眼底。（成语谜）`
- **Lựa chọn cũ:** A: `一览无余` | B: `目空一切` | C: `鼠目寸光` | D: `` (Đáp án cũ: `1`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Một ki-lô-gam (1 kg) bằng bao nhiêu gam?**
- **👉 Lựa chọn mới:**
  - **A.** 1.000 gam
  - **B.** 100 gam
  - **C.** 10 gam
  - **D.** 10.000 gam
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (1.000 gam)
- **Giá trị giáo dục / Định hướng tư duy:** *Toán đo lường - Đổi đơn vị khối lượng kg sang gam*

### Câu 238: [class_questions.xml - ID 390]
- **Phân loại vi phạm:** `Đố chữ Hán & Chiết tự` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'成语'*)
- **Lý do cần sửa:** Đố chiết tự chữ tượng hình hoặc thành ngữ Hán ngữ cổ mà người chơi Việt Nam không thể suy luận logic.
- **Câu hỏi cũ (Tiếng Trung):** `千里通电话。（猜一成语）`
- **Lựa chọn cũ:** A: `遥相呼应` | B: `不言而喻` | C: `心有灵犀` | D: `` (Đáp án cũ: `1`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Một ngày đêm trên Trái Đất có tổng cộng bao nhiêu giờ?**
- **👉 Lựa chọn mới:**
  - **A.** 24 giờ
  - **B.** 12 giờ
  - **C.** 36 giờ
  - **D.** 48 giờ
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (24 giờ)
- **Giá trị giáo dục / Định hướng tư duy:** *Toán thời gian - Chu kỳ 24 giờ của một ngày đêm*

### Câu 239: [class_questions.xml - ID 392]
- **Phân loại vi phạm:** `Tuyên truyền quốc gia 'Nước ta'` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'中国'*)
- **Lý do cần sửa:** Dùng cụm từ 'nước ta' ('我国') để nhồi nhét biểu tượng, ngày lễ, thủ đô, chính sách của Trung Quốc cho người chơi Việt Nam.
- **Câu hỏi cũ (Tiếng Trung):** `你知道牡丹是哪个国家的国花吗？`
- **Lựa chọn cũ:** A: `美国` | B: `英国` | C: `中国` | D: `` (Đáp án cũ: `3`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Để giữ răng chắc khỏe và ngăn ngừa sâu răng, nha sĩ khuyên chúng ta nên đánh răng ít nhất mấy lần mỗi ngày?**
- **👉 Lựa chọn mới:**
  - **A.** Ít nhất 2 lần mỗi ngày (sau bữa ăn và trước khi đi ngủ)
  - **B.** Mỗi tuần 1 lần
  - **C.** Mỗi tháng 1 lần
  - **D.** Chỉ khi nào đau răng mới đánh
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Ít nhất 2 lần mỗi ngày (sau bữa ăn và trước khi đi ngủ))
- **Giá trị giáo dục / Định hướng tư duy:** *Vệ sinh cá nhân - Thói quen chăm sóc răng miệng*

### Câu 240: [class_questions.xml - ID 402]
- **Phân loại vi phạm:** `Đố chữ Hán & Chiết tự` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'成语'*)
- **Lý do cần sửa:** Đố chiết tự chữ tượng hình hoặc thành ngữ Hán ngữ cổ mà người chơi Việt Nam không thể suy luận logic.
- **Câu hỏi cũ (Tiếng Trung):** `齐唱。（猜一成语）`
- **Lựa chọn cũ:** A: `异口同声` | B: `不言而喻` | C: `不约而同` | D: `` (Đáp án cũ: `1`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Một giờ đồng hồ có bao nhiêu phút và một phút có bao nhiêu giây?**
- **👉 Lựa chọn mới:**
  - **A.** 60 phút và 60 giây
  - **B.** 100 phút và 100 giây
  - **C.** 24 phút và 60 giây
  - **D.** 60 phút và 100 giây
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (60 phút và 60 giây)
- **Giá trị giáo dục / Định hướng tư duy:** *Toán thời gian - Quy đổi đơn vị giờ, phút, giây*

### Câu 241: [kfc_questions.bin - ID 37]
- **Phân loại vi phạm:** `Tuyên truyền quốc gia 'Nước ta'` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'我国'*)
- **Lý do cần sửa:** Dùng cụm từ 'nước ta' ('我国') để nhồi nhét biểu tượng, ngày lễ, thủ đô, chính sách của Trung Quốc cho người chơi Việt Nam.
- **Câu hỏi cũ (Tiếng Trung):** `我国杂交水稻之父是是谁？`
- **Lựa chọn cũ:** A: `钱学森` | B: `陈景润` | C: `袁隆平` | D: `` (Đáp án cũ: `3`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Rửa tay sạch bằng xà phòng dưới vòi nước chảy ít nhất bao nhiêu giây để loại bỏ vi khuẩn có hại?**
- **👉 Lựa chọn mới:**
  - **A.** Ít nhất 20 - 30 giây
  - **B.** Chỉ cần nhúng tay 2 giây
  - **C.** Không cần xà phòng
  - **D.** Chỉ rửa khi tay lấm bùn
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Ít nhất 20 - 30 giây)
- **Giá trị giáo dục / Định hướng tư duy:** *Phòng chống dịch bệnh - Quy trình rửa tay sạch 6 bước*

### Câu 242: [kfc_questions.bin - ID 41]
- **Phân loại vi phạm:** `Đố chữ Hán & Chiết tự` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'成语'*)
- **Lý do cần sửa:** Đố chiết tự chữ tượng hình hoặc thành ngữ Hán ngữ cổ mà người chơi Việt Nam không thể suy luận logic.
- **Câu hỏi cũ (Tiếng Trung):** `含义深刻的小故事是什么？`
- **Lựa chọn cũ:** A: `成语` | B: `寓言` | C: `小说` | D: `` (Đáp án cũ: `2`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Một thế kỷ trong lịch sử nhân loại tương đương với bao nhiêu năm?**
- **👉 Lựa chọn mới:**
  - **A.** 100 năm
  - **B.** 10 năm
  - **C.** 1.000 năm
  - **D.** 50 năm
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (100 năm)
- **Giá trị giáo dục / Định hướng tư duy:** *Toán lịch sử - Đơn vị thế kỷ bằng một trăm năm*

### Câu 243: [kfc_questions.bin - ID 45]
- **Phân loại vi phạm:** `Tuyên truyền quốc gia 'Nước ta'` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'我国'*)
- **Lý do cần sửa:** Dùng cụm từ 'nước ta' ('我国') để nhồi nhét biểu tượng, ngày lễ, thủ đô, chính sách của Trung Quốc cho người chơi Việt Nam.
- **Câu hỏi cũ (Tiếng Trung):** `我国古代四大发明中的造纸术是谁发明的？`
- **Lựa chọn cũ:** A: `蔡伦` | B: `李时珍` | C: `鲁班` | D: `` (Đáp án cũ: `1`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Uống đủ nước lọc mỗi ngày giúp cơ thể con người điều hòa thân nhiệt và bài tiết tốt. Lượng nước trung bình một ngày là bao nhiêu?**
- **👉 Lựa chọn mới:**
  - **A.** Khoảng 1.5 đến 2 lít nước
  - **B.** Chỉ cần 1 chén nhỏ
  - **C.** 10 lít nước
  - **D.** Không cần uống nước
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Khoảng 1.5 đến 2 lít nước)
- **Giá trị giáo dục / Định hướng tư duy:** *Sức khỏe - Bổ sung đủ nước lọc cho cơ thể*

### Câu 244: [kfc_questions.bin - ID 48]
- **Phân loại vi phạm:** `Tuyên truyền quốc gia 'Nước ta'` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'中国'*)
- **Lý do cần sửa:** Dùng cụm từ 'nước ta' ('我国') để nhồi nhét biểu tượng, ngày lễ, thủ đô, chính sách của Trung Quốc cho người chơi Việt Nam.
- **Câu hỏi cũ (Tiếng Trung):** `中国最早的名医是谁？`
- **Lựa chọn cũ:** A: `扁鹊` | B: `华佗` | C: `李时珍` | D: `` (Đáp án cũ: `1`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Loại trái cây nào giàu Vitamin C giúp tăng cường sức đề kháng cho cơ thể?**
- **👉 Lựa chọn mới:**
  - **A.** Cam, quýt, bưởi, ổi
  - **B.** Mỡ động vật
  - **C.** Đường tinh luyện
  - **D.** Thịt nướng cháy
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Cam, quýt, bưởi, ổi)
- **Giá trị giáo dục / Định hướng tư duy:** *Dinh dưỡng - Tăng đề kháng tự nhiên bằng trái cây tươi*

### Câu 245: [kfc_questions.bin - ID 49]
- **Phân loại vi phạm:** `Tuyên truyền quốc gia 'Nước ta'` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'我国'*)
- **Lý do cần sửa:** Dùng cụm từ 'nước ta' ('我国') để nhồi nhét biểu tượng, ngày lễ, thủ đô, chính sách của Trung Quốc cho người chơi Việt Nam.
- **Câu hỏi cũ (Tiếng Trung):** `我国最有名的长篇神话小说是什么书？`
- **Lựa chọn cũ:** A: `三国演义` | B: `聊斋志异` | C: `西游记` | D: `` (Đáp án cũ: `3`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Tập thể dục thể thao buổi sáng hoặc chơi các môn vận động đều đặn mang lại lợi ích gì?**
- **👉 Lựa chọn mới:**
  - **A.** Tăng cường sức khỏe, tinh thần sảng khoái và phát triển chiều cao
  - **B.** Làm cơ thể yếu đi
  - **C.** Gây mất ngủ
  - **D.** Lãng phí thời gian
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Tăng cường sức khỏe, tinh thần sảng khoái và phát triển chiều cao)
- **Giá trị giáo dục / Định hướng tư duy:** *Thể dục thể thao - Rèn luyện thân thể khỏe mạnh*

### Câu 246: [kfc_questions.bin - ID 52]
- **Phân loại vi phạm:** `Tuyên truyền quốc gia 'Nước ta'` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'我国'*)
- **Lý do cần sửa:** Dùng cụm từ 'nước ta' ('我国') để nhồi nhét biểu tượng, ngày lễ, thủ đô, chính sách của Trung Quốc cho người chơi Việt Nam.
- **Câu hỏi cũ (Tiếng Trung):** `我国的建军节是哪一天？`
- **Lựa chọn cũ:** A: `8月1日` | B: `5月1日` | C: `10月1日` | D: `` (Đáp án cũ: `1`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Khi bị sốt cao trên 38.5 độ C, việc cần làm trước khi đưa đi khám bác sĩ là gì?**
- **👉 Lựa chọn mới:**
  - **A.** Uống nhiều nước, chườm ấm và dùng thuốc hạ sốt theo hướng dẫn y tế
  - **B.** Đắp chăn thật dày kín mít
  - **C.** Tắm nước đá lạnh buốt
  - **D.** Nhịn ăn uống hoàn toàn
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Uống nhiều nước, chườm ấm và dùng thuốc hạ sốt theo hướng dẫn y tế)
- **Giá trị giáo dục / Định hướng tư duy:** *Kỹ năng sơ cứu - Xử trí đúng cách khi trẻ bị sốt*

### Câu 247: [kfc_questions.bin - ID 54]
- **Phân loại vi phạm:** `Tuyên truyền quốc gia 'Nước ta'` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'我国'*)
- **Lý do cần sửa:** Dùng cụm từ 'nước ta' ('我国') để nhồi nhét biểu tượng, ngày lễ, thủ đô, chính sách của Trung Quốc cho người chơi Việt Nam.
- **Câu hỏi cũ (Tiếng Trung):** `我国的国旗是什么？`
- **Lựa chọn cũ:** A: `五星旗` | B: `五星红旗` | C: `红旗` | D: `` (Đáp án cũ: `2`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Bộ phận nào trên cơ thể người có chức năng tiếp nhận âm thanh từ môi trường xung quanh?**
- **👉 Lựa chọn mới:**
  - **A.** Đôi tai
  - **B.** Đôi mắt
  - **C.** Chiếc mũi
  - **D.** Miệng
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Đôi tai)
- **Giá trị giáo dục / Định hướng tư duy:** *Giải phẫu cơ thể - Giác quan thính giác của con người*

### Câu 248: [kfc_questions.bin - ID 56]
- **Phân loại vi phạm:** `Tuyên truyền quốc gia 'Nước ta'` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'我国'*)
- **Lý do cần sửa:** Dùng cụm từ 'nước ta' ('我国') để nhồi nhét biểu tượng, ngày lễ, thủ đô, chính sách của Trung Quốc cho người chơi Việt Nam.
- **Câu hỏi cũ (Tiếng Trung):** `请问我国的教师节是哪一天？`
- **Lựa chọn cũ:** A: `5月4日` | B: `9月10日` | C: `10月1日` | D: `` (Đáp án cũ: `2`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Mắt người nhìn rõ vật là nhờ giác quan nào tiếp nhận thông tin hình ảnh và ánh sáng?**
- **👉 Lựa chọn mới:**
  - **A.** Thị giác
  - **B.** Khứu giác
  - **C.** Vị giác
  - **D.** Xúc giác
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Thị giác)
- **Giá trị giáo dục / Định hướng tư duy:** *Giải phẫu cơ thể - Giác quan thị giác*

### Câu 249: [kfc_questions.bin - ID 58]
- **Phân loại vi phạm:** `Tuyên truyền quốc gia 'Nước ta'` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'我国'*)
- **Lý do cần sửa:** Dùng cụm từ 'nước ta' ('我国') để nhồi nhét biểu tượng, ngày lễ, thủ đô, chính sách của Trung Quốc cho người chơi Việt Nam.
- **Câu hỏi cũ (Tiếng Trung):** `我国最长的河流是什么？`
- **Lựa chọn cũ:** A: `长江` | B: `黄河` | C: `黄浦江` | D: `` (Đáp án cũ: `1`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Khứu giác của con người giúp chúng ta cảm nhận được điều gì?**
- **👉 Lựa chọn mới:**
  - **A.** Mùi hương (thơm, thối, cay, nồng)
  - **B.** Màu sắc
  - **C.** Âm thanh
  - **D.** Nhiệt độ nóng lạnh
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Mùi hương (thơm, thối, cay, nồng))
- **Giá trị giáo dục / Định hướng tư duy:** *Giải phẫu cơ thể - Giác quan khứu giác*

### Câu 250: [kfc_questions.bin - ID 59]
- **Phân loại vi phạm:** `Tuyên truyền quốc gia 'Nước ta'` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'我国'*)
- **Lý do cần sửa:** Dùng cụm từ 'nước ta' ('我国') để nhồi nhét biểu tượng, ngày lễ, thủ đô, chính sách của Trung Quốc cho người chơi Việt Nam.
- **Câu hỏi cũ (Tiếng Trung):** `我国的国歌的名称是什么？`
- **Lựa chọn cũ:** A: `义勇军进行曲` | B: `七子之歌` | C: `龙的传人` | D: `` (Đáp án cũ: `1`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Vị giác ở lưỡi người có thể phân biệt được các vị cơ bản nào?**
- **👉 Lựa chọn mới:**
  - **A.** Ngọt, mặn, chua, đắng và vị umami
  - **B.** Nóng và lạnh
  - **C.** Xanh và đỏ
  - **D.** Cứng và mềm
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Ngọt, mặn, chua, đắng và vị umami)
- **Giá trị giáo dục / Định hướng tư duy:** *Sinh lý học - Khả năng cảm thụ vị giác của lưỡi*

### Câu 251: [kfc_questions.bin - ID 64]
- **Phân loại vi phạm:** `Lịch sử & Phong kiến Trung Quốc` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'朝代'*)
- **Lý do cần sửa:** Câu hỏi thuần về các triều đại, hoàng đế phong kiến Trung Quốc, không mang lại giá trị tư duy và không phù hợp môi trường học đường Việt Nam.
- **Câu hỏi cũ (Tiếng Trung):** `李白是什么朝代的诗人？`
- **Lựa chọn cũ:** A: `唐代` | B: `宋代` | C: `清代` | D: `` (Đáp án cũ: `1`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Chiến dịch lịch sử chấn động địa cầu năm 1954 chấm dứt ách thống trị của thực dân Pháp tại Việt Nam là chiến dịch nào?**
- **👉 Lựa chọn mới:**
  - **A.** Chiến dịch Điện Biên Phủ
  - **B.** Chiến dịch Biên giới
  - **C.** Chiến dịch Tây Nguyên
  - **D.** Chiến dịch Hồ Chí Minh
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Chiến dịch Điện Biên Phủ)
- **Giá trị giáo dục / Định hướng tư duy:** *Lịch sử hiện đại - Chiến thắng Điện Biên Phủ lẫy lừng*

### Câu 252: [kfc_questions.bin - ID 69]
- **Phân loại vi phạm:** `Tuyên truyền quốc gia 'Nước ta'` (Mức độ: **Cần thay thế chuẩn hóa** - Từ khóa phát hiện: *'中国'*)
- **Lý do cần sửa:** Dùng cụm từ 'nước ta' ('我国') để nhồi nhét biểu tượng, ngày lễ, thủ đô, chính sách của Trung Quốc cho người chơi Việt Nam.
- **Câu hỏi cũ (Tiếng Trung):** `中国历史上杰出的天文学家是谁？`
- **Lựa chọn cũ:** A: `祖冲之` | B: `司马光` | C: `张衡` | D: `` (Đáp án cũ: `3`)
- **👉 Đề xuất Câu hỏi mới (Tiếng Việt):** **Để bảo vệ cột sống lưng không bị gù vẹo khi ngồi học bài, tư thế ngồi đúng là gì?**
- **👉 Lựa chọn mới:**
  - **A.** Ngồi thẳng lưng, hai chân chạm sàn, mắt cách bàn khoảng 25-30cm
  - **B.** Nằm bò ra bàn
  - **C.** Cúi gập sát mắt vào vở
  - **D.** Ngồi bắt chéo vẹo người
- **👉 Đáp án đúng mới:** **Lựa chọn 1** (Ngồi thẳng lưng, hai chân chạm sàn, mắt cách bàn khoảng 25-30cm)
- **Giá trị giáo dục / Định hướng tư duy:** *Vệ sinh học đường - Tư thế ngồi học chuẩn chống cận thị và vẹo cột sống*
