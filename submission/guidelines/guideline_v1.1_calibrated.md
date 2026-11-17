# Guideline gán nhãn chung — v1.1 — Nhóm NoName

- Phiên bản: `v1.1`
- Ngày: 2026-11-17
- Tác giả: Nhóm NoName (Hợp nhất từ 5 bản cá nhân 995, 996, 997, 998, 999 và hiệu chuẩn sau phiên họp Calibration)
- Người duyệt: Nguyễn Văn Hùng (Reviewer) & Vũ Đức Toàn (Coordinator)
- Loại nhãn: 2D Bounding Box (Rectangle) + Attributes theo chuẩn COCO 1.0 (trên công cụ CVAT)
- Trạng thái: **Bản đặc tả hiệu chuẩn sau Calibration (Áp dụng cho tập nhãn bàn giao cuối cùng)**

---

## 1. Mục tiêu và Mô hình sử dụng nhãn

Bộ dữ liệu gán nhãn nhằm phục vụ việc huấn luyện và đánh giá mô hình phát hiện đối tượng 2D (Object Detection) và định vị không gian thời gian thực trên 40 ảnh giao thông đường phố, ứng dụng cho hệ thống xe tự lái và camera giám sát giao thông thông minh.

Với mỗi người hoặc phương tiện nhìn thấy được trên ảnh, người gán nhãn xác định: **đúng một bounding box**, **đúng một lớp nhãn** và **đầy đủ các thuộc tính đi kèm**.

### Đánh giá rủi ro an toàn và tác động của lỗi gán nhãn:

| Loại lỗi | Tình huống ví dụ | Hậu quả đối với hệ thống an toàn |
|---|---|---|
| **Bỏ sót (False Negative - FN)** | Không gán box cho người đi bộ qua đường, xe máy đi sát lề hoặc ô tô con trên sàn xe tải. | Mô hình bỏ lọt đối tượng nguy hiểm nhất; hệ thống điều khiển không kích hoạt giảm tốc/phanh khẩn cấp, dẫn đến va chạm trực tiếp. |
| **Gán thừa (False Positive - FP)** | Gán `person` cho tượng điêu khắc, ma-nơ-canh, poster quảng cáo 2D; gán xe cho hình phản chiếu qua gương chiếu hậu hoặc xe đồ chơi trong tủ kính. | Xe tự lái nhận diện vật cản ảo trên làn đường và kích hoạt phanh gấp vô căn cứ (phantom braking), gây nguy cơ tai nạn dây chuyền từ các xe phía sau. |
| **Sai ranh giới Bounding Box** | Box lỏng lẻo, cắt lẹm thân xe, kéo trùm hàng cồng kềnh, hoặc vẽ 1 box gộp chung nhiều xe đứng sát nhau. | Làm sai lệch nghiêm trọng thuật toán ước lượng khoảng cách từ camera 2D sang không gian 3D, giảm chất lượng học của mô hình. |

**Nguyên tắc sau Calibration:** Toàn bộ các ca mơ hồ đã được họp thống nhất và chuẩn hóa theo quy tắc v1.1. Mọi nhãn bàn giao cuối cùng đều hạ cờ `can_review = false`.

---

## 2. Định nghĩa Lớp (Classes) và Thuộc tính (Attributes)

### 2.1. Danh sách Lớp (10 lớp chuẩn theo Taxonomy v1.0 / v1.1)

| Lớp (`name`) | Định nghĩa cốt lõi (một câu) | Ví dụ bao gồm | Phản ví dụ / Dễ nhầm lẫn (KHÔNG gán) |
|---|---|---|---|
| `car` | Ô tô con từ 4–9 chỗ phục vụ chở người, bao gồm cả xe bán tải (pickup) chở khách/dân sự có nắp thùng cao (`img_016`, `img_037`). | Sedan, hatchback, SUV, MPV, taxi, xe bán tải có hoặc không có nắp thùng, xe con chở trên sàn xe tải (`img_002`). | Xe tải (`truck`), xe van thùng kín (`van`), xe buýt (`bus`), tượng xe bán tải bằng đá (`img_027`), xe mô hình đồ chơi (`img_038`), xác vỏ xe ô tô phế liệu trên nóc (`img_024`). |
| `truck` | Xe cơ giới chở hàng có buồng lái (cabin) và thùng chở hàng tách biệt. | Xe tải nhẹ, xe tải nặng, xe ben, xe bồn, xe đầu kéo container, xe chuyên dụng chở ô tô (`img_002`, `img_008`). | Xe bán tải cá nhân (xếp vào `car`), xe van thùng liền cabin (`van`), xe ba gác máy chở hàng (`three_wheeler`). |
| `van` | Xe thùng kín cỡ nhỏ đến trung bình, có cabin và khoang chứa hàng/khách chung một khối vỏ liền. | Xe minivan chở khách, xe van giao hàng thư báo kín thùng (`img_005`), xe 16 chỗ dáng hộp trung chuyển (`img_030`). | Xe SUV/MPV dân sự (`car`), xe tải thùng rời cabin (`truck`), xe buýt lớn (`bus`). |
| `bus` | Xe buýt công cộng, xe khách liên tỉnh, xe du lịch cỡ lớn từ 16 chỗ ngồi trở lên, thân dài. | Xe buýt nội đô, xe khách liên tỉnh (`img_009`, `img_031`, `img_037`, `img_040`). | Xe minivan/van 7–16 chỗ dáng hộp cỡ nhỏ (`van`). |
| `motorcycle` | Xe hai bánh gắn động cơ xăng hoặc điện, **chỉ tính thân xe** (người ngồi trên xe gán `person` riêng). | Xe số, xe tay ga, mô tô phân khối lớn, xe máy điện, xe máy có thùng phụ sidecar (`img_001`, `img_010`, `img_022`, `img_023`). | Xe đạp không động cơ, xe đạp điện có bàn đạp, xe xích lô đạp chân (`img_006`, `img_039`). |
| `three_wheeler` | Phương tiện ba bánh có động cơ dùng để chở người hoặc chở hàng hóa. | Xe tuk-tuk chở khách (`img_004`, `img_016`), xe lam, auto rickshaw, xe ba gác máy chở hàng (`img_035`). | Xe máy 2 bánh kéo xe cải tiến phía sau, xe xích lô đạp chân (`img_039`). |
| `bicycle` | Xe đạp thông thường, xe đạp điện có bàn đạp, xe đạp thể thao (chỉ gán khung xe; người đạp gán `person`). | Xe đạp leo núi, xe đạp trẻ em, xe đạp điện dáng thanh mảnh có bàn đạp (`img_006`, `img_039`). | Xe máy điện, xe máy tay ga (`motorcycle`). |
| `other` | Phương tiện giao thông đặc thù phi tiêu chuẩn: xe thô sơ tự chế, xe công trình (xe lu, máy xúc), xe kéo súc vật. | Xe máy xúc trên công trường, xe bò kéo hàng trên đường nông thôn. | Ô tô con (`car`), xe tải chở hàng tiêu chuẩn (`truck`). |
| `person` | Con người còn sống ở mọi tư thế trong không gian giao thông đường phố. | Người đi bộ, người lái và người ngồi sau xe máy (`img_001`), người đạp xe/xích lô, tài xế trên xe hở, người đứng/ngồi trên vỉa hè. | Tượng người bằng đồng/đá (`img_011`, `img_017`), ma-nơ-canh (`img_033`), poster/biển quảng cáo in hình người (`img_018`), hình người phản chiếu qua gương (`img_020`). |
| `ignore_region` | Vùng không gian chứa cụm vật thể quá nhỏ (< 20px ở hậu cảnh), đám đông dày đặc hoặc cụm xe mờ không thể phân tách biên chuẩn xác. | Đám đông dày đặc ở hậu cảnh quảng trường (`img_011`), hàng loạt xe đỗ mờ ảo ở đường chân trời (`img_003`). | Bất kỳ vật thể nào có chiều cao >= 20px, rõ ràng ở tiền cảnh hoặc trung cảnh. |

---

### 2.2. Danh sách Thuộc tính (3 thuộc tính chuẩn)

Mỗi Bounding Box khi gán nhãn (trừ lớp `ignore_region`) bắt buộc phải có đầy đủ 3 thuộc tính sau:

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
   * `false`: Bắt buộc là `false` cho toàn bộ nhãn ở bản bàn giao v1.1.

---

## 3. Quy tắc vẽ Bounding Box (Hình học & Ngữ nghĩa)

1. **Nguyên tắc bao phần nhìn thấy (Tight Visible Box)**: Bounding box phải ôm sát các điểm ngoài cùng **nhìn thấy được** của vật thể trên ảnh 2D (bao gồm thân vỏ, bánh xe, gương chiếu hậu ngoài cùng). **Tuyệt đối không vẽ ngoại suy (không amodal)** phần bị che khuất dưới mặt đất, dưới nước hoặc sau vật cản khác. Sai số cạnh box không vượt quá 2–3 pixels.
2. **Quy tắc phân tách Người và Xe hai bánh (`person` & `motorcycle` / `bicycle`)**:
   * Khi có người điều khiển hoặc người ngồi trên xe (`img_001`, `img_005`, `img_026`): **Bắt buộc vẽ các bounding box độc lập**:
     * 01 box phương tiện (`motorcycle` hoặc `bicycle`) ôm trọn thân xe, tay lái, bánh xe và biển số xe.
     * 01 box `person` riêng cho mỗi người (người lái, người ngồi sau). Box `person` bao từ đỉnh đầu/mũ bảo hiểm xuống đến hết bàn chân (trong phạm vi nhìn thấy), bao gồm cả balo/túi xách đeo liền trên người.
   * Các box này được phép chồng lấn tự nhiên lên nhau.
3. **Quy tắc Xe chuyên dụng chở ô tô (`truck` và `car`)**:
   * Trên các xe tải chuyên dụng chở ô tô (`img_002`): Vẽ 01 box lớn `truck` bao toàn bộ xe tải sàn. Đồng thời, vẽ từng box `car` riêng biệt cho mỗi chiếc ô tô con trên sàn xe (nếu nhìn thấy rõ và đạt kích thước $\ge 20\text{px}$).
4. **Quy tắc Hàng hóa trên phương tiện (Quy tắc hiệu chuẩn sau Calibration)**:
   * Hàng hóa chở trên xe (`img_029`, `img_035`): Bounding box của phương tiện chỉ bao phần thân xe, giá chở hàng và hàng hóa gọn gàng theo thân xe. **Tuyệt đối KHÔNG kéo box trùm lên khối hàng hóa cồng kềnh, nhô cao quá khổ bất thường** (`img_035.jpg`) để bảo toàn tỷ lệ khung hình thực của phương tiện cho thuật toán phát hiện đối tượng.
5. **Quy tắc Phản ví dụ (Tượng, Đồ chơi, Ma-nơ-canh, Tranh ảnh 2D, Phản chiếu, Xác xe phế liệu)**:
   * **Tuyệt đối KHÔNG gán box** cho:
     * Tượng điêu khắc bằng đá/đồng/kim loại (`img_011`, `img_017`, `img_027`).
     * Ma-nơ-canh mặc quần áo sau tủ kính (`img_033`).
     * Xe mô hình, đồ chơi trẻ em trưng bày (`img_038`).
     * Tranh ảnh, biển quảng cáo tấm lớn in hình người hoặc phương tiện (`img_018`).
     * Hình ảnh người và phương tiện phản chiếu qua gương chiếu hậu (`img_020`) hoặc kính cửa sổ.
     * Thân vỏ xe phế liệu/xác xe gắn trên nóc nhà (`img_024`).
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
| **R-01** | Người điều khiển hoặc ngồi sau xe máy/xe đạp. | Gán 01 box `person` cho mỗi người + 01 box `motorcycle`/`bicycle` cho xe. Hai box chồng lấn tự nhiên. | Người và xe là hai thực thể độc lập; người có thể rời xe. | `img_001.jpg`, `img_005.jpg`, `img_026.jpg` |
| **R-02** | Xe tải chuyên dụng chở nhiều ô tô con trên sàn. | Gán 01 box `truck` bao xe tải sàn; gán thêm từng box `car` riêng cho mỗi ô tô con trên sàn (8 car trong `img_002.jpg`). | Mô hình xe tự lái cần nhận diện ô tô con ở mọi vị trí không gian để tránh va chạm tầm cao. | `img_002.jpg` |
| **R-03** | Tượng người, tượng xe, ma-nơ-canh, poster, xe đồ chơi/mô hình. | **Tuyệt đối KHÔNG gán box**. Xuất ảnh với 0 annotation nếu không có vật thật. | Vật thể tĩnh, không di chuyển; gán nhãn sẽ gây cảnh báo giả (phantom braking). | `img_011.jpg`, `img_017.jpg`, `img_018.jpg`, `img_027.jpg`, `img_033.jpg`, `img_038.jpg` |
| **R-04** | Hình ảnh phản chiếu qua gương chiếu hậu hoặc kính tòa nhà. | **Tuyệt đối KHÔNG gán box**, không tạo `ignore_region` cho gương. | Hình ảnh phản chiếu không phải thực thể vật lý trên làn xe chạy. | `img_020.jpg` |
| **R-05** | Người đi xe đạp, xe xích lô đạp chân. | Gán 01 box `person` cho người đạp/đẩy; gán 01 box `bicycle` cho khung xe nếu phân tách được. | Chuẩn hóa theo taxonomy mở rộng 10 lớp. | `img_006.jpg`, `img_039.jpg` |
| **R-06** | Xe tuk-tuk 3 bánh, xe lam, xe ba gác máy chở hàng. | Gán nhãn `three_wheeler`. Box ôm thân xe và bánh xe. | Hình thái và động học 3 bánh khác biệt rõ rệt so với xe 2 bánh `motorcycle`. | `img_004.jpg`, `img_016.jpg`, `img_035.jpg` |
| **R-07** | Xe máy hoặc xe ba bánh chở hàng cồng kềnh. | Box chỉ ôm thân xe và hàng chằng buộc phẳng theo xe. **Không bao hàng hóa cồng kềnh quá khổ** (`img_035.jpg`). | Tránh làm méo tỷ lệ bounding box xe ba bánh / xe máy trong mô hình phát hiện đối tượng. | `img_029.jpg`, `img_035.jpg` |
| **R-08** | Xe mô tô có thùng phụ gắn bên cạnh (sidecar). | 01 box `motorcycle` bao trọn cả xe và thùng phụ; người lái và người trong thùng mỗi người 01 box `person`. | Thùng phụ là một phần kết cấu liền của phương tiện cơ giới. | `img_022.jpg` |
| **R-09** | Xe bán tải có nắp thùng hàng sau kín cao bằng cabin. | Thống nhất gán lớp `car` (thuộc dòng pickup đa dụng dân sự), không gán `truck` hay `van`. | Chuẩn hóa nhất quán trên toàn lô dữ liệu để tránh chia tách nhãn phân tán. | `img_016.jpg`, `img_037.jpg` |
| **R-10** | Xe buýt nội đô, xe khách liên tỉnh lớn từ 16 chỗ trở lên. | Gán nhãn `bus`. | Kích thước lớn, điểm mù rộng, quán tính phanh khác biệt hoàn toàn với `van`. | `img_009.jpg`, `img_031.jpg`, `img_037.jpg`, `img_040.jpg` |
| **R-11** | Ùn tắc xe máy dày đặc, chồng lấn nhiều lớp. | Gán từng xe còn lộ rõ đặc trưng (đầu xe, tay lái, bánh xe) và đạt $\ge 20\text{px}$. Xe ở lớp sâu chỉ lộ mảng màu nhỏ thì bỏ qua hoặc gom vào `ignore_region`. | Tránh gây nhiễu nhãn cho các mẫu không thể phân tách biên. | `img_005.jpg`, `img_026.jpg` |
| **R-12** | Phương tiện di chuyển nhanh bị nhòe chuyển động (motion blur). | Box ôm toàn bộ vệt mờ có thể quan sát được của xe, hạ cờ `can_review = false`. | Vật thể thực sự đang lưu thông trên đường. | `img_014.jpg`, `img_015.jpg` |
| **R-13** | Thân vỏ xe ô tô cũ phế liệu chất trên nóc xe/mái nhà. | **Tuyệt đối KHÔNG gán `car`** cho phần thân vỏ phế liệu; chỉ gán box cho phương tiện chuyên chở bên dưới. | Thân vỏ phế liệu không phải phương tiện giao thông đang hoạt động. | `img_024.jpg` |
| **R-14** | Phương tiện di chuyển trong vùng ngập nước một phần. | Box chỉ bao phần thân xe nhìn thấy nổi trên mặt nước (không ngoại suy đáy bánh xe dưới nước), chọn `occluded_level` phù hợp. | Tuân thủ tuyệt đối nguyên tắc tight visible box 2D. | — |
| **R-15** | Xe ưu tiên và xe thô sơ kéo bởi súc vật. | Xe cảnh sát/cứu thương: gán `car` hoặc `van` theo hình dáng thân xe. Xe súc vật kéo (xe bò, xe ngựa): gán `other` cho xe hoặc chỉ gán `person` cho người điều khiển. | Phù hợp với năng lực nhận diện của taxonomy 2D. | — |
| **R-16** | Vật thể bị cắt cụt bởi mép ảnh. | Vẽ box đến đúng mép viền ảnh (không vượt ra ngoài), gán `truncated = yes`. | Chuẩn hóa ranh giới khung ảnh. | — |
| **R-17** | Phân biệt xe máy điện và xe đạp điện. | Xe có bàn đạp, khung thanh mảnh: gán `bicycle`. Xe có yên dài, bệ để chân, chắn bùn to: gán `motorcycle`. | Tránh nhầm lẫn giữa hai loại phương tiện 2 bánh. | — |

---

## 5. Quy trình QC và Lịch sử Phiên bản

### 5.1. Bộ chỉ số và Ngưỡng chấp nhận (Acceptance Criteria):

| Chỉ số QC | Ngưỡng đạt chuẩn của bài lab | Ghi chú áp dụng |
|---|---|---|
| **IoU trung bình (IAA IoU)** | $\ge 0.85$ (với box $\ge 50\text{px}$)<br>$\ge 0.70$ (với box $< 50\text{px}$) | Đo ở Pha 4: Đạt 0.832 (cần hiệu chuẩn ở Pha 5). |
| **Độ đồng thuận lớp (IAA Class)** | $\ge 95\%$ | Đo ở Pha 4: Đạt 94.3% (cần hiệu chuẩn ở Pha 5). |
| **Độ phủ phân công (Coverage)** | $100\%$ ($120/120$ lượt gán) | Hoàn thành 120/120 lượt gán trên cả 40 ảnh. |
| **Tỷ lệ ảnh có lỗi ở vòng QC cuối** | $\le 2\%$ | Với tập 40 ảnh: yêu cầu đạt **0 ảnh lỗi (0.0%)** mới được quyết định **Release**. |

### 5.2. Lịch sử thay đổi:

| Phiên bản | Ngày | Nội dung thay đổi chính | Căn cứ & Lý do |
|---|---|---|---|
| `v0` | 2026-11-16 | Bản khởi đầu của ban giảng huấn (sơ lược 5 lớp, thiếu quy tắc ca khó, thuộc tính định tính). | — |
| `v1.0` | 2026-11-16 | **Bản thống nhất của nhóm**: Bổ sung 2 lớp `bus`, `three_wheeler`; định lượng 4 mức `occluded_level`; chốt 17 quy tắc ca khó gắn mã `R-01` đến `R-17`; giải quyết toàn bộ 13 điểm mâu thuẫn giữa 5 bản cá nhân. | Tổng hợp và đối chiếu từ 5 bản cá nhân 995, 996, 997, 998, 999. |
| `v1.1` | 2026-11-17 | **Bản hiệu chuẩn sau Calibration**: Chốt quy tắc không bao hàng cồng kềnh quá khổ (R-07), bỏ thân vỏ phế liệu trên nóc (R-08/R-13), chuẩn hóa bán tải nắp cao thành `car` (R-09), hạ toàn bộ cờ `can_review` về `false` trên toàn bộ 40 ảnh. | Dựa trên kết quả đo IAA (1446 ca bất thường trên 35 ảnh) và biên bản họp `calibration_decisions.csv`. |
