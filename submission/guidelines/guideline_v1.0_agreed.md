# Guideline gán nhãn chung — v1.0 — Nhóm NoName

- Phiên bản: `v1.0`
- Ngày: 2026-11-16
- Tác giả: Nhóm NoName (Hợp nhất từ 5 bản cá nhân 995, 996, 997, 998, 999)
- Người duyệt: Nguyễn Văn Hùng (Reviewer) & Vũ Đức Toàn (Coordinator)
- Loại nhãn: 2D Bounding Box (Rectangle) + Attributes theo chuẩn COCO 1.0 (trên công cụ CVAT)
- Trạng thái: **Bản đặc tả thống nhất của nhóm (Khóa cứng cho lượt gán độc lập Pha 3)**

---

## 1. Mục tiêu và Mô hình sử dụng nhãn

Bộ dữ liệu gán nhãn nhằm phục vụ việc huấn luyện và đánh giá mô hình phát hiện đối tượng 2D (Object Detection) và định vị không gian thời gian thực trên 40 ảnh giao thông đường phố, ứng dụng cho hệ thống xe tự lái và camera giám sát giao thông thông minh.

Với mỗi người hoặc phương tiện nhìn thấy được trên ảnh, người gán nhãn xác định: **đúng một bounding box**, **đúng một lớp nhãn** và **đầy đủ các thuộc tính đi kèm**.

### Đánh giá rủi ro an toàn và tác động của lỗi gán nhãn:

| Loại lỗi | Tình huống ví dụ | Hậu quả đối với hệ thống an toàn |
|---|---|---|
| **Bỏ sót (False Negative - FN)** | Không gán box cho người đi bộ qua đường, xe máy đi sát lề hoặc ô tô con trên sàn xe tải. | Mô hình bỏ lọt đối tượng nguy hiểm nhất; hệ thống điều khiển không kích hoạt giảm tốc/phanh khẩn cấp, dẫn đến va chạm trực tiếp. |
| **Gán thừa (False Positive - FP)** | Gán `person` cho tượng điêu khắc, ma-nơ-canh, poster quảng cáo 2D; gán xe cho hình phản chiếu qua gương chiếu hậu hoặc xe đồ chơi trong tủ kính. | Xe tự lái nhận diện vật cản ảo trên làn đường và kích hoạt phanh gấp vô căn cứ (phantom braking), gây nguy cơ tai nạn dây chuyền từ các xe phía sau. |
| **Sai ranh giới Bounding Box** | Box lỏng lẻo, cắt lẹm thân xe, hoặc vẽ 1 box gộp chung nhiều xe đứng sát nhau. | Làm sai lệch nghiêm trọng thuật toán ước lượng khoảng cách từ camera 2D sang không gian 3D, giảm chất lượng học của mô hình. |

**Nguyên tắc ứng xử khi gặp ca mơ hồ:** Người gán tuyệt đối không đoán mò và không hỏi người khác trong lúc gán độc lập. Chọn phương án an toàn nhất theo guideline và tick chọn thuộc tính `can_review = true` để đưa ra phiên họp Calibration của nhóm.

---

## 2. Định nghĩa Lớp (Classes) và Thuộc tính (Attributes)

### 2.1. Danh sách Lớp (10 lớp chuẩn theo taxonomy v1.0)

Gồm 6 lớp gốc của bài lab (`car`, `truck`, `van`, `motorcycle`, `person`, `ignore_region`) và 4 lớp mở rộng đã được nhóm thống nhất đưa vào đặc tả (`bus`, `three_wheeler`, `bicycle`, `other`).

| Lớp (`name`) | Định nghĩa cốt lõi (một câu) | Ví dụ bao gồm | Phản ví dụ / Dễ nhầm lẫn (KHÔNG gán) |
|---|---|---|---|
| `car` | Ô tô con từ 4–9 chỗ phục vụ chở người, bao gồm cả xe bán tải (pickup) chở khách/dân sự. | Sedan, hatchback, SUV, MPV, taxi, xe bán tải có hoặc không có nắp thùng (`img_001`, `img_037`), xe con chở trên sàn xe tải (`img_002`). | Xe tải (`truck`), xe van thùng kín (`van`), xe buýt (`bus`), tượng xe bán tải bằng đá (`img_027`), xe mô hình đồ chơi (`img_038`). |
| `truck` | Xe cơ giới chở hàng có buồng lái (cabin) và thùng chở hàng tách biệt. | Xe tải nhẹ, xe tải nặng, xe ben, xe bồn, xe đầu kéo container, xe chuyên dụng chở ô tô (`img_002`, `img_008`). | Xe bán tải cá nhân (xếp vào `car`), xe van thùng liền cabin (`van`), xe ba gác máy chở hàng (`three_wheeler`). |
| `van` | Xe thùng kín cỡ nhỏ đến trung bình, có cabin và khoang chứa hàng/khách chung một khối vỏ liền. | Xe minivan chở khách, xe van giao hàng thư báo kín thùng (`img_005`), xe 16 chỗ dáng hộp trung chuyển (`img_030`). | Xe SUV/MPV dân sự (`car`), xe tải thùng rời cabin (`truck`), xe buýt lớn (`bus`). |
| `bus` | Xe buýt công cộng, xe khách liên tỉnh, xe du lịch cỡ lớn từ 16 chỗ ngồi trở lên, thân dài. | Xe buýt nội đô, xe khách liên tỉnh (`img_009`, `img_031`, `img_037`, `img_040`). | Xe minivan/van 7–16 chỗ dáng hộp cỡ nhỏ (`van`). |
| `motorcycle` | Xe hai bánh gắn động cơ xăng hoặc điện, **chỉ tính thân xe** (người ngồi trên xe gán `person` riêng). | Xe số, xe tay ga, mô tô phân khối lớn, xe máy điện, xe máy có thùng phụ sidecar (`img_001`, `img_010`, `img_022`, `img_023`). | Xe đạp không động cơ, xe đạp điện có bàn đạp, xe xích lô đạp chân (`img_006`, `img_039`). |
| `three_wheeler` | Phương tiện ba bánh có động cơ dùng để chở người hoặc chở hàng hóa. | Xe tuk-tuk chở khách (`img_004`, `img_016`), xe lam, auto rickshaw, xe ba gác máy chở hàng (`img_035`). | Xe máy 2 bánh kéo xe cải tiến phía sau, xe xích lô đạp chân (`img_039`). |
| `person` | Con người còn sống ở mọi tư thế trong không gian giao thông đường phố. | Người đi bộ, người lái và người ngồi sau xe máy (`img_001`), người đạp xe/xích lô, tài xế trên xe hở, người đứng/ngồi trên vỉa hè. | Tượng người bằng đồng/đá (`img_011`, `img_017`), ma-nơ-canh (`img_033`), poster/biển quảng cáo in hình người (`img_018`), hình người phản chiếu qua gương (`img_020`). |
| `ignore_region` | Vùng không gian chứa cụm vật thể quá nhỏ (< 20px ở hậu cảnh), đám đông dày đặc hoặc cụm xe mờ không thể phân tách biên chuẩn xác. | Đám đông dày đặc ở hậu cảnh quảng trường (`img_011`), hàng loạt xe đỗ mờ ảo ở đường chân trời (`img_003`). | Bất kỳ vật thể nào có chiều cao >= 20px, rõ ràng ở tiền cảnh hoặc trung cảnh. |
| `bicycle` | Xe đạp thông thường, xe đạp điện, xe đạp thể thao, chỉ tính thân xe (người điều khiển gán `person` riêng). | Xe đạp mini, xe đạp thể thao, xe đạp cào cào (`img_006`). | Xe máy gắn động cơ cơ giới (`motorcycle`), xe 3 bánh (`three_wheeler`). |
| `other` | Phương tiện đặc thù, xe thô sơ tự chế, xe kéo súc vật (xe bò kéo), xe xích lô chở khách, xe công trình. | Xe xích lô du lịch (`img_006`, `img_009`, `img_023`, `img_034`, `img_039`), xe kéo tự chế, xe bò. | Xe ô tô con (`car`), xe tải (`truck`), xe van (`van`). |



---

### 2.2. Danh sách Thuộc tính (3 thuộc tính chuẩn)

Mỗi Bounding Box khi gán nhãn (trừ lớp `ignore_region`) bắt buộc phải chọn đầy đủ 3 thuộc tính sau:

1. **`occluded_level`** (Mức độ bị che khuất theo diện tích nhìn thấy của chính vật thể):
   * `0`: **Thấy rõ hoàn toàn** ($< 1\%$ bị che khuất).
   * `1`: **Che khuất nhẹ (1% – 30%)**: Vật thể bị che khuất một phần nhỏ biên dạng (ví dụ bánh xe bị che bởi lề đường, chân người bị che một phần) nhưng tổng thể nhận dạng rất rõ ràng.
   * `2`: **Che khuất trung bình đến nặng (31% – 70%)**: Bị che khuất đáng kể bởi phương tiện khác hoặc chướng ngại vật (ví dụ ô tô đi sau ô tô khác, người lái xe máy bị ghi-đông và yếm xe che khuất chân).
   * `3`: **Che khuất nghiêm trọng (> 70%)**: Chỉ còn lộ một phần đặc trưng nhỏ (ví dụ chỉ thấy đầu xe + đèn pha, hoặc nửa trên mũ bảo hiểm) nhưng vẫn đủ cơ sở khẳng định lớp.
   * *(Quy ước: Nếu vật thể bị che > 90% không còn đủ đặc trưng nhận dạng chắc chắn thì KHÔNG gán box).*

2. **`truncated`** (Vật thể bị cắt cụt bởi mép viền ảnh):
   * `no`: Vật thể nằm trọn vẹn bên trong khung ảnh.
   * `yes`: Vật thể bị cắt bởi ít nhất một trong 4 cạnh biên của khung hình (trên, dưới, trái, phải).

3. **`can_review`** (Cờ đánh dấu ca phân vân cần xem lại):
   * `false`: Mặc định (người gán tự tin với nhãn và box của mình).
   * `true`: Đánh dấu ca biên mơ hồ, cần đưa ra phiên họp Calibration của nhóm.

---

## 3. Quy tắc vẽ Bounding Box (Hình học & Ngữ nghĩa)

1. **Nguyên tắc bao phần nhìn thấy (Tight Visible Box)**: Bounding box phải ôm sát các điểm ngoài cùng **nhìn thấy được** của vật thể trên ảnh 2D (bao gồm thân vỏ, bánh xe, gương chiếu hậu ngoài cùng). **Tuyệt đối không vẽ ngoại suy (không amodal)** phần bị che khuất dưới mặt đất, dưới nước hoặc sau vật cản khác. Sai số cạnh box không vượt quá 2–3 pixels.
2. **Quy tắc phân tách Người và Xe máy (`person` & `motorcycle`)**:
   * Khi có người điều khiển hoặc người ngồi sau xe máy (`img_001`, `img_005`, `img_026`): **Bắt buộc vẽ các bounding box độc lập**:
     * 01 box `motorcycle` ôm trọn thân xe, tay lái, bánh xe và biển số xe.
     * 01 box `person` riêng cho mỗi người (người lái, người ngồi sau). Box `person` bao từ đỉnh đầu/mũ bảo hiểm xuống đến hết bàn chân (trong phạm vi nhìn thấy), bao gồm cả balo/túi xách đeo liền trên người.
   * Các box này được phép chồng lấn tự nhiên lên nhau.
3. **Quy tắc Xe chuyên dụng chở ô tô (`truck` và `car`)**:
   * Trên các xe tải chuyên dụng chở ô tô (`img_002`): Vẽ 01 box lớn `truck` bao toàn bộ xe tải sàn. Đồng thời, vẽ từng box `car` riêng biệt cho mỗi chiếc ô tô con trên sàn xe (nếu nhìn thấy rõ và đạt kích thước $\ge 20\text{px}$).
4. **Quy tắc Hàng hóa cồng kềnh trên phương tiện**:
   * Hàng hóa chở trên xe máy / xe ba bánh (`img_029`, `img_035`): Nếu hàng hóa được chằng buộc cố định trên giá xe, thùng xe và tham gia chiếm dụng diện tích làn đường thực tế thì **được bao trong bounding box của phương tiện**. Nếu hàng hóa quá khổ nhô cao bất thường thì tick `can_review = true` để chốt ở Calibration.
5. **Quy tắc Phản ví dụ (Tượng, Đồ chơi, Ma-nơ-canh, Tranh ảnh 2D, Phản chiếu)**:
   * **Tuyệt đối KHÔNG gán box** cho:
     * Tượng điêu khắc bằng đá/đồng/kim loại (`img_011`, `img_017`, `img_027`).
     * Ma-nơ-canh mặc quần áo sau tủ kính (`img_033`).
     * Xe mô hình, đồ chơi trẻ em trưng bày (`img_038`).
     * Tranh ảnh, biển quảng cáo tấm lớn in hình người hoặc phương tiện (`img_018`).
     * Hình ảnh người và phương tiện phản chiếu qua gương chiếu hậu (`img_020`) hoặc kính cửa sổ.
   * Nếu một bức ảnh chỉ chứa toàn các đối tượng phản ví dụ này, bức ảnh đó vẫn phải có mặt trong file COCO xuất ra với `0 annotation`.
6. **Quy tắc Mép ảnh và Biên giới hạn**:
   * Bounding box không được phép vượt ra ngoài tọa độ ảnh ($x_{max} \le \text{width}$, $y_{max} \le \text{height}$). Đối tượng bị cắt cụt thì vẽ sát đến đúng mép ảnh và đặt `truncated = yes`.
7. **Quy tắc Ngưỡng kích thước tối thiểu & Đám đông**:
   * Nếu cạnh dài nhất của box **nhỏ hơn 20 pixels**: Không vẽ box riêng lẻ. Nếu chúng tụ tập thành cụm dày đặc ở hậu cảnh thì dùng 01 box `ignore_region` bao quanh toàn bộ cụm.
8. **Quy tắc Phân tách đối tượng**:
   * Tuyệt đối không vẽ một box gộp nhiều xe đứng sát nhau. Mỗi đối tượng phải có một box riêng biệt. Trong vùng ùn tắc dày đặc (`img_005`, `img_026`), chỉ gán những xe còn lộ rõ các bộ phận đặc trưng (đầu xe, tay lái, bánh xe).

---

## 4. Danh mục Ca khó & Quy tắc ánh xạ (Edge Cases Matrix)

Bảng tổng hợp các tình huống biên thực tế trên 40 ảnh kèm mã quy tắc chuẩn từ `R-01` đến `R-17`:

| Mã Rule | Tình huống phát hiện trên ảnh | Quyết định gán nhãn của nhóm | Lập luận kỹ thuật | Ảnh tham chiếu |
|---|---|---|---|---|
| **R-01** | Người điều khiển hoặc ngồi sau xe máy. | Gán 01 box `person` cho mỗi người + 01 box `motorcycle` cho xe. Hai box chồng lấn tự nhiên. | Người và xe là hai thực thể độc lập; người có thể rời xe. | `img_001.jpg`, `img_005.jpg`, `img_026.jpg` |
| **R-02** | Xe tải chuyên dụng chở nhiều ô tô con trên sàn. | Gán 01 box `truck` bao xe tải sàn; gán thêm từng box `car` riêng cho mỗi ô tô con trên sàn. | Mô hình xe tự lái cần nhận diện ô tô con ở mọi vị trí không gian để tránh va chạm tầm cao. | `img_002.jpg` |
| **R-03** | Tượng người, tượng xe, ma-nơ-canh, poster, xe đồ chơi/mô hình. | **Tuyệt đối KHÔNG gán box**. Xuất ảnh với 0 annotation nếu không có vật thật. | Vật thể tĩnh, không di chuyển; gán nhãn sẽ gây cảnh báo giả (phantom braking). | `img_011.jpg`, `img_017.jpg`, `img_018.jpg`, `img_027.jpg`, `img_033.jpg`, `img_038.jpg` |
| **R-04** | Hình ảnh phản chiếu qua gương chiếu hậu hoặc kính tòa nhà. | **Tuyệt đối KHÔNG gán box**, không tạo `ignore_region` cho gương. | Hình ảnh phản chiếu không phải thực thể vật lý trên làn xe chạy. | `img_020.jpg` |
| **R-05** | Người đi xe đạp, xe xích lô đạp chân. | Gán 01 box `person` cho người điều khiển; gán 01 box `bicycle` cho thân xe đạp (với xe đạp thông thường) hoặc gán 01 box `other` cho thân xe xích lô. Hai box chồng lấn tự nhiên tương tự xe máy. | Phù hợp với taxonomy 10 lớp (`bicycle`, `other`, `person`). | `img_006.jpg`, `img_009.jpg`, `img_023.jpg`, `img_034.jpg`, `img_039.jpg` |
| **R-06** | Xe tuk-tuk 3 bánh, xe lam, xe ba gác máy chở hàng. | Gán nhãn `three_wheeler`. Box ôm thân xe và bánh xe. | Hình thái và động học 3 bánh khác biệt rõ rệt so với xe 2 bánh `motorcycle`. | `img_004.jpg`, `img_016.jpg`, `img_035.jpg` |
| **R-07** | Xe máy hoặc xe ba bánh chở hàng cồng kềnh. | Giữ nguyên lớp phương tiện, box bao trùm cả phần hàng chằng cố định; nếu hàng quá khổ nhô cao thì tick `can_review = true`. | Hàng hóa làm thay đổi kích thước chiếm làn thực tế của phương tiện. | `img_029.jpg`, `img_035.jpg` |
| **R-08** | Xe mô tô có thùng phụ gắn bên cạnh (sidecar). | 01 box `motorcycle` bao trọn cả xe và thùng phụ; người lái và người trong thùng mỗi người 01 box `person`. | Thùng phụ là một phần kết cấu liền của phương tiện cơ giới. | `img_022.jpg` |
| **R-09** | Xe bán tải có nắp thùng hàng sau kín cao bằng cabin. | Gán lớp `car` (thuộc dòng pickup đa dụng), tick `can_review = true`. | Dễ gây tranh cãi giữa `car`, `van` và `truck`; nhóm thống nhất gán `car`. | `img_037.jpg` |
| **R-10** | Xe buýt nội đô, xe khách liên tỉnh lớn từ 16 chỗ trở lên. | Gán nhãn `bus`. | Kích thước lớn, điểm mù rộng, quán tính phanh khác biệt hoàn toàn với `van`. | `img_009.jpg`, `img_031.jpg`, `img_037.jpg`, `img_040.jpg` |
| **R-11** | Ùn tắc xe máy dày đặc, chồng lấn nhiều lớp. | Gán từng xe còn lộ rõ đặc trưng (đầu xe, tay lái, bánh xe) và đạt $\ge 20\text{px}$. Xe ở lớp sâu chỉ lộ mảng màu nhỏ thì bỏ qua hoặc gom vào `ignore_region`. | Tránh gây nhiễu nhãn cho các mẫu không thể phân tách biên. | `img_005.jpg`, `img_026.jpg` |
| **R-12** | Phương tiện di chuyển nhanh bị nhòe chuyển động (motion blur). | Box ôm toàn bộ vệt mờ có thể quan sát được của xe, gán `can_review = true`. | Vật thể thực sự đang lưu thông trên đường. | `img_014.jpg`, `img_015.jpg` |
| **R-13** | Thân vỏ xe ô tô cũ phế liệu chất trên nóc xe/mái nhà. | KHÔNG gán `car` cho phần thân vỏ phế liệu; chỉ gán box cho phương tiện chuyên chở bên dưới. | Thân vỏ phế liệu không phải phương tiện giao thông đang hoạt động. | `img_024.jpg` |
| **R-14** | Phương tiện di chuyển trong vùng ngập nước một phần. | Box chỉ bao phần thân xe nhìn thấy nổi trên mặt nước (không ngoại suy đáy bánh xe dưới nước), chọn `occluded_level` phù hợp. | Tuân thủ tuyệt đối nguyên tắc tight visible box 2D. | — |
| **R-15** | Xe ưu tiên và xe thô sơ kéo bởi súc vật. | Xe cảnh sát/cứu thương: gán `car` hoặc `van` theo hình dáng thân xe. Xe súc vật kéo (xe bò, xe ngựa): không gán xe, chỉ gán `person` cho người điều khiển kèm `can_review = true`. | Phù hợp với năng lực nhận diện của taxonomy 2D. | — |
| **R-16** | Vật thể bị cắt cụt bởi mép ảnh. | Vẽ box đến đúng mép viền ảnh (không vượt ra ngoài), gán `truncated = yes`. | Chuẩn hóa ranh giới khung ảnh. | — |
| **R-17** | Phân biệt xe máy điện và xe đạp điện. | Xe có bàn đạp, khung thanh mảnh: coi như xe đạp (R-05). Xe có yên dài, bệ để chân, chắn bùn to: gán `motorcycle`. Nếu không rõ: tick `can_review = true`. | Tránh nhầm lẫn giữa hai loại phương tiện 2 bánh. | — |

---

## 5. Quy trình QC và Lịch sử Phiên bản

### 5.1. Quy trình Kiểm soát Chất lượng 3 bước:
1. **Tự kiểm tra (Self-Check — 100% ảnh cá nhân)**:
   * Sau khi export COCO 1.0 từ CVAT, mỗi thành viên chạy lệnh:
     `python scripts/validate_labels.py submission/labels/<mã>.json`
   * Kiểm tra không có box nào vượt biên ảnh, không có box $< 20\text{px}$ thiếu `ignore_region`, đầy đủ thuộc tính và đúng 24 ảnh được giao.
2. **Kiểm tra chéo và đo độ đồng thuận (Cross-check & IAA — 100% lượt gán)**:
   * Khi cả nhóm hoàn thành, chạy `python scripts/qc_compare.py` để tính IoU trung bình và tỷ lệ cùng lớp trên các cặp box ghép đôi.
3. **Hiệu chuẩn và duyệt toàn lô (Calibration & Final QC)**:
   * Họp Calibration xử lý toàn bộ các ca bất thường trong `calibration_candidates.csv`, sửa nhãn và xuất bản calibrated.
   * Reviewer độc lập duyệt toàn bộ 40/40 ảnh ở Pha 6 để đưa ra quyết định bàn giao.

### 5.2. Bộ chỉ số và Ngưỡng chấp nhận (Acceptance Criteria):

| Chỉ số QC | Ngưỡng đạt chuẩn của bài lab | Ghi chú áp dụng |
|---|---|---|
| **IoU trung bình (IAA IoU)** | $\ge 0.85$ (với box $\ge 50\text{px}$)<br>$\ge 0.70$ (với box $< 50\text{px}$) | Chỉ tính trên các cặp box ghép đôi 1–1 (IoU $\ge 0.5$). |
| **Độ đồng thuận lớp (IAA Class)** | $\ge 95\%$ | Tỷ lệ gán cùng tên lớp trên các cặp box ghép đôi. |
| **Độ phủ phân công (Coverage)** | $100\%$ ($120/120$ lượt gán) | Đủ 100% lượt gán mới được chạy đo IAA. |
| **Tỷ lệ ảnh có lỗi ở vòng QC cuối** | $\le 2\%$ | Với tập 40 ảnh: yêu cầu đạt **0 ảnh lỗi (0.0%)** mới được quyết định **Release**. |

### 5.3. Lịch sử thay đổi:

| Phiên bản | Ngày | Nội dung thay đổi chính | Căn cứ & Lý do |
|---|---|---|---|
| `v0` | 2026-11-16 | Bản khởi đầu của ban giảng huấn (sơ lược 5 lớp, thiếu quy tắc ca khó, thuộc tính định tính). | — |
| `v1.0` | 2026-11-16 | **Bản thống nhất của nhóm**: Bổ sung 4 lớp `bus`, `three_wheeler`, `bicycle`, `other`; định lượng 4 mức `occluded_level`; chốt 17 quy tắc ca khó gắn mã `R-01` đến `R-17`; giải quyết toàn bộ 13 điểm mâu thuẫn giữa 5 bản cá nhân. | Tổng hợp và đối chiếu từ 5 bản cá nhân 995, 996, 997, 998, 999. |

---

## Phụ lục: Bảng giải quyết 13 điểm mâu thuẫn giữa 5 bản cá nhân

| # | Vấn đề tranh luận | Bản 995 | Bản 996 | Bản 997 (Bạn) | Bản 998 | Bản 999 | **Quyết định chốt cho v1.0** |
|---|---|---|---|---|---|---|---|
| 1 | **Danh sách lớp** | 7 lớp | 6 lớp gốc | 6 lớp + `bus`, `tuk_tuk` | 10 lớp | 6 lớp gốc | **10 lớp**: 6 lớp gốc + `bus` + `three_wheeler` + `bicycle` + `other` |
| 2 | **Lớp xe đạp (`bicycle`)** | Có | Không | Không | Có | Không | **Có lớp `bicycle`** (chỉ thân xe, người đạp gán `person` riêng, R-05) |
| 3 | **Tên lớp xe máy** | `motobike` | `motorcycle` | `motorcycle` | `motorcycle` | `motorcycle` | **`motorcycle`** (theo chuẩn COCO/CVAT) |
| 4 | **Người lái và xe máy** | Gộp 1 box | Tách riêng | Tách riêng | Gộp 1 box | Tách riêng | **Tách 2 box riêng** (`person` và `motorcycle`) (R-01) |
| 5 | **Box phần thấy vs ngoại suy** | Phần thấy | Phần thấy | Phần thấy | Ngoại suy (amodal) | Phần thấy | **Chỉ bao phần nhìn thấy (Tight Visible Box)** |
| 6 | **Hàng hóa cồng kềnh** | Thuộc tính thêm | Chưa nêu | Không bao hàng | Bao trong box + thuộc tính | Bao trong box | **Bao trong box phương tiện**, tick `can_review` nếu quá khổ |
| 7 | **Kích thước tối thiểu** | Không nêu | Không nêu | 20 px | 15 px | 20 px | **Cạnh dài nhất $\ge 20\text{px}$**; nhỏ hơn gom vào `ignore_region` |
| 8 | **Ngưỡng `occluded_level`** | 3 mức (50%) | 4 mức định tính | 4 mức (30/70) | 4 mức (50%) | 4 mức (35/70) | **4 mức định lượng chuẩn**: 0 (0%), 1 (1–30%), 2 (31–70%), 3 (>70%) |
| 9 | **Giá trị `truncated`** | `true/false` | `yes/no` | `yes/no` | `true/false` | `yes/no` | **`yes` / `no`** (theo taxonomy schema) |
| 10 | **Thuộc tính mở rộng** | `motion_state`... | `can_review` | `can_review` | 5 thuộc tính | `can_review` | **Giữ 3 thuộc tính chuẩn** (`occluded_level`, `truncated`, `can_review`) |
| 11 | **Phản chiếu qua gương** | Không nói | Không gán | Không gán | Không nói | `ignore_region` | **Tuyệt đối KHÔNG gán box** (R-04) |
| 12 | **Xe ba bánh (Tuk-tuk)** | Lớp riêng | `can_review` | Lớp riêng | Lớp riêng | `motorcycle` | **Thêm lớp riêng `three_wheeler`** (R-06) |
| 13 | **Xe buýt lớn** | Lớp riêng | Không nói | Lớp riêng | Lớp riêng | Không nói | **Thêm lớp riêng `bus`** (R-10) |
