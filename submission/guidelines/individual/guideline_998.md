## I. Thiết kế Danh sách Lớp (Classes) và Thuộc tính (Attributes)

Việc phân tách lớp được thiết kế dựa trên đặc điểm, công năng thiết kế, kích thước chiếm dụng làn đường, đặc tính động học và mức độ ưu tiên/rủi ro va chạm đối với xe tự lái.

### 1. Danh sách Lớp nhãn

| STT | Tên lớp (`class_name`) | Mô tả & Phạm vi bao gồm |
| :--- | :--- | :--- |
| 1 | `motorcycle` | Xe máy, xe tay ga, xe mô tô, xe máy điện, quad, xe điện cưỡi (bao gồm cả người lái, người ngồi sau và hàng hóa gắn trên xe). |
| 2 | `bicycle` | Xe đạp truyền thống, xe đạp điện, xích lô (bao gồm cả người điều khiển và hàng hóa). |
| 3 | `car` | Ô tô con 4–9 chỗ (Sedan, Hatchback, SUV, MPV, bán tải, taxi dân sự, xe điện kính 4 bánh). |
| 4 | `bus` | Xe buýt nội đô, xe khách liên tỉnh, xe du lịch từ 16 chỗ trở lên. |
| 5 | `truck` | Xe tải nhẹ, xe tải nặng, xe đầu kéo container, xe bồn, xe ben chuyên dụng. |
| 6 | `three_wheeler` | Xe ba bánh gắn máy, xe ba gác chở hàng, xe lam, tuk-tuk. |
| 7 | `special_vehicle` | Xe ưu tiên và xe công vụ đang làm nhiệm vụ (xe cảnh sát, xe cứu thương...). |
| 8 | `other_vehicle` | Phương tiện thô sơ, xe súc vật kéo (xe bò, xe ngựa), xe đẩy hàng tự chế lưu thông dưới lòng đường. |
| 9 | `person` | Người đi bộ, người đứng/ngồi sát lòng đường hoặc trên vỉa hè, người đẩy xe nôi/xe hàng bộ hành, người ngồi trên phương tiện. |
| 10 | `van` | **Xe van cỡ nhỏ:** Xe chở hàng thùng kín có cabin và khoang hàng liền một khối; **Minivan:** Xe dáng hộp cao, kích thước trung bình phục vụ chở khách/trung chuyển. |

### 2. Danh sách Thuộc tính (5 Attributes)

| Tên thuộc tính (`attribute`) | Giá trị hợp lệ (`values`) | Ý nghĩa đối với hệ thống xe tự lái |
| :--- | :--- | :--- |
| `motion_state` | `moving` / `parked` | Phân biệt xe đang tham gia giao thông (kể cả dừng chờ đèn đỏ trên làn) với xe đỗ tĩnh sát lề/vỉa hè. |
| `occluded` | `0` - Thấy rõ<br>`1` - Bị che dưới 50%<br>`2` - Bị che từ 50% trở lên<br>`3` - Không xác định | Đánh giá mức độ bị che khuất của object. |
| `truncated` | `false` / `true` | Phương tiện bị cắt một phần bởi rìa khung ảnh. |
| `bulky` | `false` / `true` | Cảnh báo xe chở hàng quá khổ/cồng kềnh. |
| `orientation` | `front` / `rear` / `side` | Xác định hướng xe đối đầu, cùng chiều hay cắt ngang để ước lượng thời gian va chạm. |

---

## II. Annotation Guideline

### 1. Mục tiêu & Mô hình sử dụng nhãn

* **Ứng dụng trong hệ thống tránh va chạm:** Tọa độ hộp giới hạn (`[x_min, y_min, x_max, y_max]`), nhãn lớp và thuộc tính đầu ra được truyền trực tiếp vào Multi-Object Tracking và module Đánh giá rủi ro va chạm để tính toán khoảng cách tương đối, dự đoán quỹ đạo và ra quyết định phanh khẩn cấp hoặc chuyển làn.

### 2. Quy tắc gán nhãn theo loại nhãn (2D Bounding Box & Attributes)

* **Loại nhãn hình học:** 2D Bounding Box kết hợp gán đầy đủ thuộc tính cho mỗi đối tượng.
* **Quy tắc độ ôm sát:** Khung bao phải chạm điểm ngoài cùng (bao gồm cả người điều khiển và hàng hóa nhô ra), không chừa khoảng trống trong đó vật bị che thì chỉ bao phần thấy; sai số khoảng trống hoặc cắt lẹm không vượt quá **3 pixels** (với vật thể gần) và **2 pixels** (với vật thể ở xa).
* **Quy tắc gộp người lái và hàng hóa:**
  * Với `motorcycle`, `bicycle`, `three_wheeler`, `other_vehicle`: Bounding Box bắt buộc bao trùm toàn bộ cụm phương tiện + người lái + người ngồi sau + hàng hóa/giá đèo hàng. Không tách người lái hay hàng hóa thành các box riêng lẻ.
  * Với `car`, `bus`, `truck`, `special_vehicle`: Bounding Box ôm sát phần khung vỏ kim loại và gương chiếu hậu ngoài cùng.
* **Quy tắc ngoại suy khi bị che khuất:** Khi phương tiện bị che khuất một phần bởi vật cản hoặc nước ngập, Annotator phải ước lượng kích thước toàn phần dựa trên tỷ lệ hình học chuẩn của xe thay vì chỉ khoanh phần nhìn thấy.
* **Ngưỡng kích thước tối thiểu:** Chỉ gán nhãn các phương tiện có chiều rộng `15px` hoặc chiều cao `15px`.
* **Quy tắc phân tách đối tượng:** Tuyệt đối không vẽ một khung bao lớn gộp nhiều xe đứng sát nhau; mỗi phương tiện phải có một Bounding Box riêng biệt.

### 3. Các ca khó & Quyết định xử lý (Edge Cases)

| STT | Tình huống ca khó (Kèm ảnh tham chiếu) | Vấn đề nhận diện | Quyết định xử lý chuẩn |
| :--- | :--- | :--- | :--- |
| 1 | Xe máy/xe ba bánh chở hàng cồng kềnh, quá khổ | Hàng hóa nhô rộng sang hai bên hoặc cao quá đầu người lái, che khuất thân xe và làm thay đổi hoàn toàn bề ngang chiếm dụng làn đường. | Giữ nguyên lớp phương tiện chính (`motorbike` hoặc `three_wheeler`), kéo rộng Bounding Box bao trùm toàn bộ mép ngoài cùng của hàng hóa, đồng thời gán `carrying_bulky_cargo = true`. |
| 2 | Phương tiện di chuyển trong vùng ngập nước | Nước ngập che mất 30–50% phần bánh xe và gầm xe, làm mất điểm tiếp xúc giữa lốp xe và mặt đường. | Áp dụng Amodal Box: ước lượng vị trí đáy lốp xe dưới mặt nước dựa trên tỷ lệ thân xe phía trên để đặt cạnh đáy `y_max`, gán `occlusion = partial`. (Giúp mô hình không ước lượng sai khoảng cách 2D-to-3D). |
| 3 | Ùn tắc xe máy dày đặc, chồng lấn nhiều lớp | Hàng chục xe máy san sát, xe phía trước che khuất 60–80% xe phía sau. | Gán nhãn độc lập từng xe nếu nhận diện được 20% diện tích đặc trưng (thấy rõ đầu xe + tay lái hoặc cụm bánh sau + yên xe) và đạt kích thước `15px`, gán `occlusion = heavy`. Bỏ qua các xe ở lớp sâu chỉ lộ mảng màu nhỏ không xác định được biên để tránh nhiễu nhãn. |
| 4 | Xe cảnh sát chắn ngang đường & Xe súc vật kéo | (a) Xe cảnh sát có hình dáng xe con nhưng đang làm nhiệm vụ chặn đường.<br>(b) Xe bò kéo gồm con vật ở trước và thùng xe gỗ ở sau. | (a) Ưu tiên gán lớp `special_vehicle` (thay vì `car`) với `motion_state = parked` để hệ thống lập kế hoạch đường đi nhận biết điểm chặn.<br>(b) Gán lớp `other_vehicle`, vẽ 1 Bounding Box duy nhất bao trùm cả con bò kéo lẫn thùng xe và người điều khiển. |

### 4. Quy trình Kiểm soát Chất lượng (Quality Control — QC)

**Quy trình kiểm duyệt 3 bước:**

1. **Tự kiểm tra (Self-Check — 100%):** Annotator kiểm tra tự động bằng script trên công cụ gán nhãn để loại bỏ box rỗng, box dưới ngưỡng `15px` hoặc thiếu thuộc tính.
2. **Kiểm tra chéo (QA Review — 100% ảnh ở giai đoạn đầu, 30% ngẫu nhiên + 100% ảnh ca khó ở giai đoạn ổn định):** Đội ngũ QA kiểm tra toàn bộ khung bao và thuộc tính theo từng lô (batch).
3. **Nghiệm thu đầu ra (Lead Audit — 15% mẫu ngẫu nhiên toàn tập):** Đánh giá chất lượng trước khi đưa dữ liệu vào huấn luyện mô hình.

**Bộ chỉ số & Ngưỡng đạt chuẩn (Acceptance Criteria):**

| Chỉ số đánh giá (Metric) | Ngưỡng đạt chuẩn | Ghi chú áp dụng |
| :--- | :--- | :--- |
| **Độ chính xác vị trí (mIoU)** | `0.85%` (không che khuất)<br>`75%` (bị che khuất/ngập nước) | So sánh Bounding Box của Annotator với Ground Truth chuẩn của QA. |
| **Độ phủ đối tượng (Recall)** | `97%` (toàn ảnh)<br>`99%` (vùng làn xe chạy — Ego-lane) | Tuyệt đối không bỏ sót phương tiện nằm trực diện phía trước xe tự lái. |
| **Độ chính xác phân loại (Class Precision)** | `98%` | Không nhầm lẫn giữa các nhóm phương tiện có kích thước/tốc độ khác biệt lớn. |
| **Độ chính xác thuộc tính (Attribute Acc.)** | `95%` (chung)<br>`97%` (`motion_state`, `carrying_bulky_cargo`) | Hai thuộc tính ảnh hưởng trực tiếp tới biên an toàn và quyết định vượt. |

* **Cơ chế xử lý lỗi (Rework Policy):** Bất kỳ lô dữ liệu nào không đạt một trong các ngưỡng trên sẽ bị từ chối toàn bộ lô (Reject Batch), trả về sửa lại kèm báo cáo lỗi chi tiết, đồng thời cập nhật thêm các ví dụ lỗi vào tài liệu Guideline để đồng bộ lại toàn đội ngũ.
