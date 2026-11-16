# Guideline gán nhãn — <phiên bản> — <mã hoặc nhóm>

> Copy file này (hoặc `guideline_v0_starter.md`) rồi viết. Một guideline đủ gồm **5 phần**. Câu nào của v0
> làm hai người đọc ra hai cách khác nhau thì phải viết lại cho một cách hiểu duy nhất.

- Phiên bản: v0
- Ngày: 16/11/2026
- Người viết / duyệt: Vũ Đức Toàn

## 1. Mục tiêu

Xây dựng bộ dữ liệu gán nhãn phương tiện giao thông trên đường phố nhằm hỗ trợ hệ thống xe tự lái nhận diện các phương tiện xung quanh và chủ động tránh va chạm.

Mỗi phương tiện xuất hiện trong ảnh cần được gán:

- Một bounding box bao quanh phương tiện.
- Một class label tương ứng với loại phương tiện.
- Các thuộc tính bổ sung nếu cần thiết.

## 2. Lớp và thuộc tính

### Lớp

| Lớp | Định nghĩa (một câu) | Ví dụ | Phản ví dụ / dễ nhầm với |

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

stopped (Dừng/đỗ) Phân biệt xe đang tham gia giao thông với xe đỗ ven đường (nhận diện qua đèn phanh, vị trí đỗ sát lề, không có người lái).

## 3. Quy tắc vẽ box

1. Vẽ bounding box bao quanh toàn bộ phần phương tiện có thể nhìn thấy và xác định được.

2. Bounding box phải sát với đường viền phương tiện nhất có thể.

3. Không bao gồm bóng đổ của phương tiện.

4. Không bao gồm người đứng cạnh hoặc các vật thể không thuộc phương tiện.

5. Không vẽ một bounding box cho nhiều phương tiện.

6. Mỗi phương tiện riêng biệt phải có một bounding box riêng.

7. Không bỏ qua phương tiện chỉ vì nó nhỏ, ở xa hoặc bị che khuất một phần, miễn là vẫn có thể nhận diện được.

8. Đối với phương tiện bị cắt bởi cạnh ảnh, vẽ bounding box đến đúng ranh giới ảnh.

## 4. Ca khó

| Ảnh     | Tình huống | Rule ID | Quyết định | Lý do |
| ------- | ---------- | ------- | ---------- | ----- |
| img_0xx |            |         |            |       |

Nếu chưa chốt, đánh dấu `can_review` trên box hoặc ghi vấn đề cấp ảnh. Dùng mã quy tắc trong nhật ký QC.

## 5. QC và phiên bản

Ngưỡng QC áp dụng, ai quyết ca mơ hồ, lịch sử thay đổi:

| Phiên bản | Thay đổi | Lý do (ca nào) |
| --------- | -------- | -------------- |
|           |          |                |
