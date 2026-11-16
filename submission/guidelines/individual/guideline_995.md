<<<<<<< HEAD

# Guideline gán nhãn — <phiên bản> — <mã hoặc nhóm>

=======

# Guideline gán nhãn — v0 — Thành viên 995

> > > > > > > 692d623780a60455fa85e64d151743336f2a28a6

> Copy file này (hoặc `guideline_v0_starter.md`) rồi viết. Một guideline đủ gồm **5 phần**. Câu nào của v0
> làm hai người đọc ra hai cách khác nhau thì phải viết lại cho một cách hiểu duy nhất.

- Phiên bản: v0
- Ngày: 16/11/2026
  <<<<<<< HEAD
- # Người viết / duyệt: Vũ Đức Toàn
- Người viết / duyệt: Vũ Đức Toàn (Mã 995)
  > > > > > > > 692d623780a60455fa85e64d151743336f2a28a6

## 1. Mục tiêu

Xây dựng bộ dữ liệu gán nhãn phương tiện giao thông trên đường phố nhằm hỗ trợ hệ thống xe tự lái nhận diện các phương tiện xung quanh và chủ động tránh va chạm.

Mỗi phương tiện xuất hiện trong ảnh cần được gán:
<<<<<<< HEAD

=======

> > > > > > > 692d623780a60455fa85e64d151743336f2a28a6

- Một bounding box bao quanh phương tiện.
- Một class label tương ứng với loại phương tiện.
- Các thuộc tính bổ sung nếu cần thiết.

## 2. Lớp và thuộc tính

### Lớp

| Lớp | Định nghĩa (một câu) | Ví dụ | Phản ví dụ / dễ nhầm với |
<<<<<<< HEAD

| motobike | Xe gắn máy 2 bánh có động cơ, xe máy điện (bao gồm cả người lái). Mật độ cao, di chuyển linh hoạt, thường xuyên chuyển làn hoặc tạt đầu đột ngột.| ----- | bicycle |

| bicycle| Xe đạp thông thường, xe đạp điện, xe đạp thể thao (bao gồm cả người lái). Tốc độ thấp, dễ mất thăng bằng, quỹ đạo di chuyển kém ổn định.| | motobike|

|car |Xe ô tô con Các dòng xe từ 4–7 chỗ (Sedan, Hatchback, SUV, MPV, bán tải Pickup). Kích thước tiêu chuẩn, di chuyển theo làn đường ổn định. | |van |

|bus |Xe buýt công cộng, xe khách từ 16 đến 45 chỗ. Thân xe dài, điểm mù lớn, thường xuyên tấp vào lề đường đón/trả khách. | | van|

|truck |Xe tải nhẹ, tải nặng, xe ben, xe đầu kéo, xe container. Quán tính lớn, quãng đường phanh dài, vùng nguy hiểm cao khi chuyển hướng. | | |

|three_wheeler |Xe ba bánh Xe ba gác chở hàng, xe lam, xe tuk-tuk, xích lô (bao gồm cả người lái). Kết cấu không đối xứng, tốc độ chậm, dễ lật hoặc chở hàng cồng kềnh. | | motobike|

|special_vehicle |Phương tiện đặc thù Xe thô sơ tự chế, xe kéo súc vật (xe bò kéo), xe công trình (máy xúc, xe lu). Tốc độ cực chậm hoặc hình dáng phi tiêu chuẩn, cần cảnh báo giảm tốc từ xa. | |three_wheeler |

### Thuộc tính

Bảng Thuộc tính đi kèm (Attributes)
Mỗi Bounding Box khi gán nhãn cần gắn kèm các thuộc tính sau để thuật toán dự đoán rủi ro va chạm:
Tên thuộc tính Giá trị (Values) Ý nghĩa đối với xe tự lái
occluded (Mức độ bị che khuất) none (0%)

partial (1% – 50%)

heavy (> 50%) Giúp mô hình hiểu vật thể bị khuất một phần nhưng vẫn có khả năng lao ra khỏi điểm mù.

truncated (Bị cắt bởi khung hình) true / false Vật thể nằm sát mép ảnh (đang tiến vào hoặc rời khỏi vùng quan sát của camera).
oversized_cargo (Chở hàng cồng kềnh) true / false Rất quan trọng: Dùng khi xe máy, xe ba gác, xe tải chở hàng vượt quá kích thước khung xe chuẩn (ví dụ: xe máy chở lồng sắt lớn, xe tuk-tuk chất hàng cao ngất). Xe tự lái cần mở rộng biên độ an toàn ngang/dọc.
motion_state (Trạng thái chuyển động)

moving (Đang chạy)

# stopped (Dừng/đỗ) Phân biệt xe đang tham gia giao thông với xe đỗ ven đường (nhận diện qua đèn phanh, vị trí đỗ sát lề, không có người lái).

|---|---|---|---|
| `motobike` | Xe gắn máy 2 bánh có động cơ, xe máy điện (bao gồm cả người lái). Mật độ cao, di chuyển linh hoạt, thường xuyên chuyển làn hoặc tạt đầu đột ngột. | | `bicycle` |
| `bicycle` | Xe đạp thông thường, xe đạp điện, xe đạp thể thao (bao gồm cả người lái). Tốc độ thấp, dễ mất thăng bằng, quỹ đạo di chuyển kém ổn định. | | `motobike` |
| `car` | Xe ô tô con các dòng từ 4–7 chỗ (Sedan, Hatchback, SUV, MPV, bán tải Pickup). Kích thước tiêu chuẩn, di chuyển theo làn đường ổn định. | | `van` |
| `bus` | Xe buýt công cộng, xe khách từ 16 đến 45 chỗ. Thân xe dài, điểm mù lớn, thường xuyên tấp vào lề đường đón/trả khách. | | `van` |
| `truck` | Xe tải nhẹ, tải nặng, xe ben, xe đầu kéo, xe container. Quán tính lớn, quãng đường phanh dài, vùng nguy hiểm cao khi chuyển hướng. | | |
| `three_wheeler` | Xe ba bánh, xe ba gác chở hàng, xe lam, xe tuk-tuk, xích lô (bao gồm cả người lái). Kết cấu không đối xứng, tốc độ chậm, dễ lật hoặc chở hàng cồng kềnh. | | `motobike` |
| `special_vehicle` | Phương tiện đặc thù, xe thô sơ tự chế, xe kéo súc vật (xe bò kéo), xe công trình (máy xúc, xe lu). Tốc độ cực chậm hoặc hình dáng phi tiêu chuẩn, cần cảnh báo giảm tốc từ xa. | | `three_wheeler` |

### Thuộc tính

Mỗi Bounding Box khi gán nhãn cần gắn kèm các thuộc tính sau để thuật toán dự đoán rủi ro va chạm:

| Tên thuộc tính    | Giá trị (Values)                                       | Ý nghĩa đối với xe tự lái                                                                                                                                                                                        |
| ----------------- | ------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `occluded`        | `none` (0%)<br>`partial` (1% – 50%)<br>`heavy` (> 50%) | Giúp mô hình hiểu vật thể bị khuất một phần nhưng vẫn có khả năng lao ra khỏi điểm mù.                                                                                                                           |
| `truncated`       | `true` / `false`                                       | Vật thể nằm sát mép ảnh (đang tiến vào hoặc rời khỏi vùng quan sát của camera).                                                                                                                                  |
| `oversized_cargo` | `true` / `false`                                       | Rất quan trọng: Dùng khi xe máy, xe ba gác, xe tải chở hàng vượt quá kích thước khung xe chuẩn (ví dụ: xe máy chở lồng sắt lớn, xe tuk-tuk chất hàng cao ngất). Xe tự lái cần mở rộng biên độ an toàn ngang/dọc. |
| `motion_state`    | `moving`<br>`stopped`                                  | Phân biệt xe đang tham gia giao thông với xe đỗ ven đường (nhận diện qua đèn phanh, vị trí đỗ sát lề, không có người lái).                                                                                       |

> > > > > > > 692d623780a60455fa85e64d151743336f2a28a6

## 3. Quy tắc vẽ box

1. Vẽ bounding box bao quanh toàn bộ phần phương tiện có thể nhìn thấy và xác định được.
   <<<<<<< HEAD

2. Bounding box phải sát với đường viền phương tiện nhất có thể.

3. Không bao gồm bóng đổ của phương tiện.

4. Không bao gồm người đứng cạnh hoặc các vật thể không thuộc phương tiện.

5. Không vẽ một bounding box cho nhiều phương tiện.

6. Mỗi phương tiện riêng biệt phải có một bounding box riêng.

7. Không bỏ qua phương tiện chỉ vì nó nhỏ, ở xa hoặc bị che khuất một phần, miễn là vẫn có thể nhận diện được.

======= 2. Bounding box phải sát với đường viền phương tiện nhất có thể. 3. Không bao gồm bóng đổ của phương tiện. 4. Không bao gồm người đứng cạnh hoặc các vật thể không thuộc phương tiện. 5. Không vẽ một bounding box cho nhiều phương tiện. 6. Mỗi phương tiện riêng biệt phải có một bounding box riêng. 7. Không bỏ qua phương tiện chỉ vì nó nhỏ, ở xa hoặc bị che khuất một phần, miễn là vẫn có thể nhận diện được.

> > > > > > > 692d623780a60455fa85e64d151743336f2a28a6 8. Đối với phương tiện bị cắt bởi cạnh ảnh, vẽ bounding box đến đúng ranh giới ảnh.

## 4. Ca khó

### Case 1: Phương tiện bị che khuất một phần

**Tình huống:** Một chiếc ô tô bị xe khác che khuất một phần nhưng vẫn nhận diện được.

**Quyết định:**

- Vẫn tạo bounding box cho chiếc ô tô.
- Bounding box bao quanh phần phương tiện nhìn thấy được.
- Gán class `car`.
- Đánh dấu `occluded = true`.

### Case 2: Phương tiện nằm sát hoặc bị cắt bởi cạnh ảnh

**Tình huống:** Một chiếc xe máy chỉ xuất hiện một phần ở mép bên trái hoặc bên phải của ảnh.

**Quyết định:**

- Nếu phần nhìn thấy đủ để xác định đây là xe máy, vẫn tiến hành gán nhãn.
- Bounding box kéo đến ranh giới của ảnh.
- Gán class `motorcycle`.
- Đánh dấu `truncated = true`.

### Case 3: Nhiều phương tiện nằm sát nhau

**Tình huống:** Một chiếc ô tô, xe máy và xe đạp xuất hiện gần nhau hoặc chồng lấn trong ảnh.

**Quyết định:**

- Mỗi phương tiện phải có một bounding box riêng.
- Không gộp nhiều phương tiện thành một bounding box.
- Gán class độc lập cho từng phương tiện.
- Không để bounding box của phương tiện này bao gồm phần lớn diện tích của phương tiện khác.

### Case 4: Phương tiện khó phân biệt giữa các lớp

**Tình huống:** Một phương tiện ba bánh có hình dáng gần giống xe máy hoặc tuk tuk.

**Quyết định:**

- Nếu có khoang chở khách hoặc cấu trúc đặc trưng của tuk tuk, gán `tuk_tuk`.
- Nếu có cấu trúc xe máy thông thường, gán `motorcycle`.
- Nếu không đủ thông tin để xác định chính xác nhưng chắc chắn là phương tiện giao thông, gán `other_vehicle`.

### Case 5: Phương tiện có kích thước rất nhỏ hoặc ở xa

**Tình huống:** Một phương tiện xuất hiện ở xa, chiếm diện tích rất nhỏ trong ảnh.

**Quyết định:**

- Nếu vẫn có thể xác định loại phương tiện, tiến hành gán nhãn.
- Vẽ bounding box sát phần phương tiện có thể nhìn thấy.
- Không tự ý bỏ qua chỉ vì phương tiện có kích thước nhỏ.
- Nếu không thể xác định chắc chắn loại phương tiện, sử dụng `other_vehicle` nếu vẫn xác định được đó là phương tiện.

## 5. QC và phiên bản

## 7. Phiên bản (Version History)

| Version | Date       | Description                                                                                          |
| ------- | ---------- | ---------------------------------------------------------------------------------------------------- |
| v1.0    | 2026-11-16 | Initial annotation guideline. Defined 7 classes, attributes, bounding box rules and difficult cases. |
