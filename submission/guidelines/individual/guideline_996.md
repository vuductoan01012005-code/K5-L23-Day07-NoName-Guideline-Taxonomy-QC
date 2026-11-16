
# Guideline gán nhãn — v1.0-individual — Nguyễn Thanh Sơn

- **Phiên bản:** v1.0-individual
- **Ngày:** 2026-11-16
- **Người viết:** Nguyễn Thanh Sơn
- **Loại nhãn:** Bounding Box (hộp bao 2D)
- **Công cụ:** CVAT
- **Định dạng xuất:** COCO 1.0

---

## 1. Mục tiêu

Tài liệu này xây dựng bộ quy chuẩn gán nhãn Bounding Box cho 40 ảnh giao thông đường phố, phục vụ quá trình huấn luyện, kiểm thử và đánh giá mô hình thị giác máy tính phát hiện đối tượng (Object Detection 2D).

Mục tiêu là xác định chính xác vị trí, phân loại người và các phương tiện giao thông xuất hiện trong ảnh, đảm bảo dữ liệu có tính nhất quán và hạn chế sai sót trong quá trình annotation.

- **Nhiệm vụ của mô hình:** Phát hiện và phân loại chính xác các đối tượng giao thông như ô tô, xe tải, xe van, xe máy và người trong nhiều điều kiện khác nhau.
- **Yêu cầu đối với người gán nhãn:** Không bỏ sót đối tượng có thể nhận diện, không gán nhầm các vật thể không thuộc taxonomy và đảm bảo Bounding Box bao sát đối tượng.
- **Mức độ ảnh hưởng khi gán nhãn sai:**
  - **False Negative:** Bỏ sót người hoặc phương tiện khiến mô hình không học được đầy đủ các đối tượng trong môi trường giao thông.
  - **False Positive:** Nhầm tượng, hình ảnh quảng cáo, ma-nơ-canh hoặc vật thể mô phỏng thành người và phương tiện thật.
  - **Sai lệch Bounding Box:** Box quá rộng, quá hẹp hoặc bao gồm nhiều đối tượng sẽ làm giảm chất lượng dữ liệu huấn luyện.

## 2. Lớp và thuộc tính

### 2.1. Định nghĩa các lớp đối tượng (Classes)

Sử dụng 6 lớp theo taxonomy ban đầu. Mỗi đối tượng được gán một lớp phù hợp nhất với đặc điểm nhận dạng.

| Lớp (Class) | Định nghĩa | Ví dụ | Trường hợp không thuộc lớp |
|---|---|---|---|
| `car` | Ô tô con dùng chủ yếu để chở người. | Sedan, SUV, hatchback, MPV, xe bán tải cá nhân. | Xe tải lớn, xe van chuyên dụng. |
| `truck` | Phương tiện cơ giới chuyên chở hàng hóa, có kết cấu thùng hoặc bộ phận chuyên dụng. | Xe tải thùng, xe ben, xe đầu kéo, xe chở hàng. | Ô tô con, xe van nhỏ. |
| `van` | Phương tiện có khoang chở hàng hoặc chở khách liền với cabin, thường có kích thước nhỏ hơn xe tải. | Minivan, xe giao hàng kín thùng, xe van chở khách. | SUV, xe tải thùng rời. |
| `motorcycle` | Phương tiện giao thông có động cơ, chủ yếu sử dụng hai hoặc ba bánh. | Xe máy số, xe tay ga, mô tô, xe máy điện. | Xe đạp thông thường, xe kéo bằng sức người. |
| `person` | Người thật xuất hiện trong không gian giao thông, không phân biệt tư thế hoặc hoạt động. | Người đi bộ, người lái xe, người ngồi sau xe, người đứng bên đường. | Tượng người, ma-nơ-canh, hình người trên poster. |
| `ignore_region` | Vùng chứa đối tượng hoặc khu vực không đủ điều kiện gán nhãn chi tiết và cần được bỏ qua khi đánh giá theo quy định. | Đám đông quá xa, vùng hình ảnh không thể xác định, khu vực có vật thể gây nhiễu. | Không sử dụng để bỏ qua đối tượng lớn, rõ ràng và có thể nhận diện. |

**Quy tắc đối với phương tiện ngoài taxonomy:**

- Xe đạp, xích lô và xe kéo không được tự ý gán vào lớp `motorcycle`.
- Nếu có người điều khiển hoặc đẩy phương tiện, vẫn gán nhãn `person` cho người đó.
- Không tạo nhãn riêng cho phần xe đạp hoặc xích lô vì taxonomy hiện tại chưa có lớp tương ứng.
- Những trường hợp đặc biệt chưa xác định được cách xử lý cần đánh dấu `can_review` và đưa ra thảo luận.

### 2.2. Định nghĩa các thuộc tính (Attributes)

Mỗi đối tượng được gán nhãn cần thiết lập đầy đủ các thuộc tính theo quy định.

**1. `occluded_level` – Mức độ che khuất**

| Giá trị | Mô tả | Cách nhận biết |
|---|---|---|
| `0` | Không bị che khuất. | Có thể quan sát gần như toàn bộ đối tượng. |
| `1` | Che khuất nhẹ. | Một phần nhỏ đối tượng bị vật khác che. |
| `2` | Che khuất vừa hoặc nhiều. | Một phần đáng kể đối tượng không nhìn thấy nhưng vẫn nhận diện được. |
| `3` | Che khuất nghiêm trọng. | Chỉ còn một phần nhỏ đặc trưng nhưng vẫn đủ căn cứ xác định đối tượng. |

**2. `truncated` – Đối tượng bị cắt bởi mép ảnh**

- `no`: Đối tượng nằm hoàn toàn trong phạm vi ảnh.
- `yes`: Một phần đối tượng bị cắt bởi cạnh trên, dưới, trái hoặc phải của ảnh.

**3. `can_review` – Đánh dấu cần xem lại**

- `false`: Người gán nhãn tự tin với quyết định của mình.
- `true`: Đối tượng có đặc điểm mơ hồ, khó phân loại hoặc chưa thống nhất được cách vẽ Bounding Box.

Khi gặp trường hợp chưa chắc chắn, người gán nhãn cần đánh dấu `can_review = true`, không tự ý đưa ra quyết định thiếu căn cứ.

## 3. Quy tắc vẽ Bounding Box

### 3.1. Quy tắc chung

1. Gán nhãn tất cả người và phương tiện thuộc phạm vi taxonomy có thể nhận diện được trong ảnh.
2. Mỗi đối tượng tương ứng với một Bounding Box riêng biệt.
3. Bounding Box phải bao sát phạm vi đối tượng, hạn chế chứa nền hoặc các vật thể xung quanh.
4. Không gộp nhiều người hoặc nhiều phương tiện vào một Bounding Box.
5. Không tạo Bounding Box cho các đối tượng không thuộc taxonomy.
6. Đối tượng bị che khuất vẫn được gán nhãn nếu có đủ căn cứ nhận diện.
7. Đối tượng bị cắt ở mép ảnh phải được đánh dấu `truncated = yes`.

### 3.2. Quy tắc phân biệt người và phương tiện

- Người điều khiển xe máy và phương tiện phải được gán thành hai Bounding Box riêng biệt.
- Người ngồi phía sau xe máy cũng phải có Bounding Box `person` riêng nếu có thể nhận diện.
- Không gộp người và xe máy thành một đối tượng.
- Phần Bounding Box của người và phương tiện có thể chồng lấn khi hai đối tượng nằm gần nhau.
- Đối với người đi bộ, Bounding Box cần bao trọn cơ thể trong phạm vi nhìn thấy.

### 3.3. Quy tắc đối với phương tiện bị che khuất

- Xe bị che bởi phương tiện khác vẫn cần được gán nhãn nếu nhận diện được.
- Không vẽ phần Bounding Box vượt quá phạm vi có căn cứ của đối tượng.
- Thiết lập `occluded_level` tương ứng với mức độ che khuất.
- Không suy đoán và tạo nhãn cho phương tiện chỉ xuất hiện một phần quá nhỏ, không đủ đặc điểm nhận dạng.

### 3.4. Quy tắc đối với đối tượng ở mép ảnh

- Đối tượng nằm sát mép ảnh nhưng vẫn nhìn thấy đầy đủ không được đánh dấu `truncated`.
- Đối tượng bị cạnh ảnh cắt mất một phần phải đặt `truncated = yes`.
- Bounding Box chỉ được vẽ trong phạm vi kích thước ảnh, không vượt ra ngoài khung hình.

### 3.5. Quy tắc đối với đối tượng nhỏ

- Ưu tiên gán nhãn những đối tượng có thể quan sát và nhận diện rõ ràng.
- Không tự ý bỏ qua người hoặc phương tiện chỉ vì chúng xuất hiện ở hậu cảnh.
- Với đối tượng quá nhỏ, mờ hoặc không đủ thông tin để xác định lớp, đánh dấu `can_review` hoặc xử lý theo quy tắc `ignore_region` đã thống nhất.

## 4. Các trường hợp khó (Edge Cases)

| Trường hợp | Cách xử lý | Lý do |
|---|---|---|
| Xe máy bị che khuất bởi ô tô | Vẫn gán nhãn `motorcycle` nếu nhận diện được, thiết lập `occluded_level` phù hợp. | Tránh bỏ sót phương tiện trong ảnh. |
| Nhiều xe máy đứng sát nhau | Mỗi xe có một Bounding Box riêng. | Đảm bảo từng phương tiện là một đối tượng độc lập. |
| Người ngồi trên xe máy | Gán riêng `person` và `motorcycle`. | Hai đối tượng có đặc điểm và mục tiêu nhận diện khác nhau. |
| Người chỉ xuất hiện một phần ở mép ảnh | Gán nhãn nếu nhận diện được và đặt `truncated = yes`. | Đối tượng vẫn thuộc phạm vi dữ liệu. |
| Xe máy điện | Gán lớp `motorcycle`. | Là phương tiện có động cơ thuộc nhóm xe máy. |
| Xe đạp hoặc xích lô | Không gán vào `motorcycle`; chỉ gán `person` nếu có người. | Taxonomy chưa có lớp dành cho phương tiện thô sơ. |
| Xe tuk-tuk hoặc xe ba bánh có động cơ | Đánh dấu `can_review = true` nếu chưa thống nhất lớp. | Cần xác nhận quy tắc phân loại giữa các thành viên. |
| Xe tải có cabin và thùng hàng | Gán lớp `truck`. | Đặc điểm nhận dạng phù hợp với phương tiện chuyên chở hàng hóa. |
| Xe van chở hàng | Gán lớp `van`. | Khoang chở hàng liền với cabin. |
| Tượng người hoặc tượng trang trí | Không gán `person`. | Không phải người thật tham gia giao thông. |
| Ma-nơ-canh trong cửa hàng | Không gán `person`. | Là vật thể trưng bày, không phải con người. |
| Hình người trên poster, biển quảng cáo | Không gán `person`. | Là hình ảnh in hoặc hiển thị trên bề mặt. |
| Hình ảnh phản chiếu trong gương | Không gán nhãn người hoặc phương tiện trong ảnh phản chiếu. | Tránh nhận diện nhầm hình ảnh ảo thành đối tượng thực. |
| Đối tượng không xác định rõ | Đánh dấu `can_review = true`. | Cần người khác kiểm tra trước khi thống nhất nhãn. |

### 4.1. Nguyên tắc xử lý ca khó

- Không tự ý tạo thêm lớp mới khi taxonomy chưa cho phép.
- Không gán nhãn theo cảm tính khi chưa đủ căn cứ nhận diện.
- Các trường hợp có nhiều cách phân loại cần được đưa ra thảo luận trong buổi Calibration.
- Sau khi nhóm thống nhất, cần cập nhật quy tắc vào guideline để các thành viên áp dụng đồng nhất.

## 5. QC và Quản lý phiên bản

### 5.1. Tiêu chí kiểm soát chất lượng cá nhân (Self-QC)

Sau khi hoàn thành annotation, cần tự kiểm tra các tiêu chí sau:

- **Class Accuracy:** Tất cả đối tượng được phân loại đúng theo taxonomy.
- **Bounding Box Accuracy:** Box bao sát đối tượng, không bị thiếu hoặc thừa phạm vi không hợp lý.
- **Completeness:** Không bỏ sót các đối tượng thuộc phạm vi gán nhãn.
- **Attribute Accuracy:** Các thuộc tính `occluded_level`, `truncated`, `can_review` được thiết lập chính xác.
- **Consistency:** Những trường hợp tương tự được xử lý theo cùng một quy tắc.
- **Duplicate Check:** Không có nhiều Bounding Box trùng lặp cho cùng một đối tượng.
- **Review Check:** Các đối tượng có `can_review = true` phải được kiểm tra lại.

### 5.2. Quy trình kiểm tra

1. Kiểm tra lại toàn bộ ảnh sau khi hoàn thành annotation.
2. Đối chiếu class của từng đối tượng với định nghĩa trong guideline.
3. Kiểm tra vị trí và kích thước Bounding Box.
4. Kiểm tra các thuộc tính của từng đối tượng.
5. Rà soát các trường hợp bị bỏ sót, gán nhầm hoặc gán trùng.
6. Xuất dữ liệu từ CVAT theo định dạng COCO 1.0.
7. Chạy script kiểm tra dữ liệu và xử lý các lỗi được phát hiện.

### 5.3. Xử lý lỗi và trường hợp chưa chắc chắn

- Khi phát hiện nhãn sai, cần chỉnh sửa trực tiếp trên CVAT.
- Khi không chắc chắn về class hoặc quy tắc xử lý, đánh dấu `can_review = true`.
- Những trường hợp cần thống nhất giữa các thành viên nên được tạo Issue hoặc đưa ra Calibration.
- Sau khi có quyết định cuối cùng, cập nhật nhãn và bổ sung quy tắc tương ứng vào guideline.

### 5.4. Quản lý phiên bản

| Phiên bản | Ngày | Nội dung thay đổi |
|---|---|---|
| `v0` | 2026-11-16 | Guideline khởi đầu do giảng viên cung cấp. |
| `v1.0-individual` | 2026-11-16 | Hoàn thiện định nghĩa lớp, thuộc tính, quy tắc Bounding Box, các trường hợp khó và quy trình QC. |

Mọi thay đổi ảnh hưởng đến định nghĩa lớp, thuộc tính hoặc cách gán nhãn cần được cập nhật phiên bản guideline. Các thành viên phải sử dụng cùng một phiên bản quy tắc đã được thống nhất để đảm bảo tính nhất quán của bộ dữ liệu.

---

**Kết quả mong muốn:** Hoàn thành bộ dữ liệu ảnh đường phố có nhãn Bounding Box chính xác, đầy đủ và nhất quán, đáp ứng yêu cầu sử dụng trong huấn luyện và đánh giá mô hình Object Detection 2D.
