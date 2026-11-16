# Guideline gán nhãn chung — v1.0-draft (tổng hợp từ thành viên 995, 996, 997, 998, 999)

- Phiên bản: `v1.0-draft`
- Ngày: 2026-11-16
- Nguồn: 5 guideline cá nhân (995, 996, 997, 998, 999) + `v0` của giảng viên
- Loại nhãn: 2D Bounding Box + thuộc tính (CVAT, xuất COCO 1.0)
- Trạng thái: **bản nháp để họp Calibration**. Các mục đánh dấu 🔶 là chỗ các guideline cá nhân mâu thuẫn nhau, đã chọn tạm một phương án và cần cả nhóm xác nhận (xem Phụ lục A).

---

## 1. Mục tiêu

Bộ nhãn dùng để huấn luyện và đánh giá mô hình phát hiện đối tượng 2D trên 40 ảnh giao thông đường phố, phục vụ xe tự lái và giám sát giao thông.

Với mỗi người/phương tiện nhìn thấy được, người gán nhãn xác định: **một bounding box**, **một lớp** và **các thuộc tính**.

Hậu quả của gán sai:

| Lỗi | Ví dụ | Hậu quả |
|---|---|---|
| Bỏ sót (False Negative) | Không gán người đi bộ, xe máy sát xe | Mô hình không học được đối tượng nguy hiểm nhất, hệ thống không giảm tốc |
| Gán thừa (False Positive) | Gán `person` cho tượng, ma-nơ-canh, poster; gán xe cho hình phản chiếu, đồ chơi | Phanh gấp ảo (phantom braking) |
| Box sai ranh giới | Box lỏng, cắt lẹm, gộp nhiều xe | Sai lệch ước lượng khoảng cách, giảm chất lượng huấn luyện |

**Nguyên tắc chung khi không chắc:** không đoán. Chọn phương án an toàn nhất theo guideline và bật `can_review = true` để đưa ra Calibration.

---

## 2. Lớp và thuộc tính

### 2.1. Lớp (8 lớp)

Gồm 6 lớp gốc của bài (`car`, `truck`, `van`, `motorcycle`, `person`, `ignore_region`) và 2 lớp đề xuất mở rộng (`bus`, `three_wheeler`) 🔶.

| Lớp | Định nghĩa (một câu) | Ví dụ | Phản ví dụ / dễ nhầm |
|---|---|---|---|
| `car` | Ô tô con 4–9 chỗ chở người, kể cả bán tải (pickup) dùng cá nhân. | Sedan, hatchback, SUV, MPV, taxi, bán tải có hoặc không nắp thùng, xe cảnh sát/xe ưu tiên dáng ô tô con | Xe tải (`truck`), xe thùng kín (`van`), xe buýt (`bus`), tượng hoặc mô hình xe |
| `truck` | Xe cơ giới chở hàng có cabin và thùng hàng riêng. | Xe tải nhẹ/nặng, xe ben, xe bồn, đầu kéo container, xe chở ô tô | Bán tải cá nhân (`car`), xe thùng liền cabin (`van`), xe ba gác máy (`three_wheeler`) |
| `van` | Xe thùng kín cỡ nhỏ đến trung bình, cabin và khoang hàng/khách liền một khối. | Minivan chở khách, xe van giao hàng kín thùng, xe 16 chỗ dáng hộp | SUV (`car`), xe tải thùng rời cabin (`truck`), xe buýt lớn (`bus`) |
| `bus` 🔶 | Xe buýt công cộng, xe khách, xe du lịch từ 16 chỗ trở lên, thân dài. | Xe buýt nội đô, xe khách liên tỉnh | Minivan/van 7–16 chỗ dáng hộp (`van`) |
| `motorcycle` | Xe hai bánh có động cơ (hoặc xe máy điện), **không gồm người ngồi** (người gán `person` riêng). | Xe số, xe tay ga, mô tô, xe máy điện, xe máy có sidecar | Xe đạp, xe đạp điện có bàn đạp, xích lô đạp chân |
| `three_wheeler` 🔶 | Xe ba bánh có động cơ chở người hoặc hàng. | Tuk-tuk, xe lam, auto rickshaw, xe ba gác máy | Xe máy hai bánh, xích lô đạp chân |
| `person` | Người thật ở mọi tư thế trong không gian đường phố. | Người đi bộ, người lái và người ngồi sau xe (kể cả xe đạp/xích lô), người đứng/ngồi bên đường | Tượng, ma-nơ-canh, poster/billboard, búp bê, hình phản chiếu |
| `ignore_region` | Vùng không đánh giá, chứa cụm vật thể quá nhỏ hoặc không tách được. | Đám đông xa, hàng xe nhỏ mờ ở chân trời, cụm xe dày đặc không tách được biên | Bất kỳ vật thể rõ, đủ lớn (kể cả ở hậu cảnh) |

**Phương án dự phòng nếu giảng viên chốt chỉ còn 6 lớp (không có `bus`, `three_wheeler`):**
- `bus` gán `truck` và bật `can_review = true`.
- `three_wheeler` gán `motorcycle` và bật `can_review = true` (định nghĩa gốc của lab cho `motorcycle` là xe 2–3 bánh có động cơ).

**Phương tiện ngoài taxonomy** (xe đạp, xích lô đạp chân, xe súc vật kéo, xe đẩy tay): không tạo lớp riêng, không ép vào `motorcycle` hay `car`. Chỉ gán `person` cho người điều khiển/đẩy (xem R-05, R-15). 🔶

### 2.2. Thuộc tính (3 thuộc tính, bắt buộc cho mọi box trừ `ignore_region`)

**`occluded_level`** (mức che khuất, tính theo diện tích của chính đối tượng):

| Giá trị | Mức che | Gợi ý nhận biết |
|---|---|---|
| `0` | 0% (dưới 1%) | Thấy trọn vẹn |
| `1` | 1% – 30% | Che nhẹ, hình dáng vẫn rõ |
| `2` | 31% – 70% | Che vừa, mất phần đáng kể nhưng nhận ra lớp |
| `3` | trên 70% | Chỉ lộ phần đặc trưng nhỏ (ví dụ đầu xe + đèn) nhưng vẫn khẳng định được lớp |

Che trên 90% hoặc không đủ căn cứ nhận lớp thì **không gán**.

**`truncated`**: `no` (nằm trọn trong ảnh) / `yes` (bị mép ảnh cắt). Đối tượng chỉ sát mép nhưng vẫn thấy đủ thì là `no`.

**`can_review`**: `false` (mặc định) / `true` (ca mơ hồ, đưa ra Calibration).

*Không đưa vào v1.0:* `motion_state`, `orientation`, `oversized_cargo` (chỉ 995/998 đề xuất, tăng khối lượng gán nhãn). Có thể xét cho v1.1.

---

## 3. Quy tắc vẽ box

1. **Chỉ bao phần nhìn thấy (visible box).** Box ôm sát các điểm ngoài cùng nhìn thấy của đối tượng, kể cả gương chiếu hậu ngoài cùng; **không** vẽ ngoại suy phần bị che (không amodal). 🔶
2. **Độ ôm sát:** sai số mỗi cạnh không quá 3 px. Không gồm bóng đổ, không gồm người đứng cạnh hay vật không thuộc đối tượng.
3. **Một đối tượng = một box.** Không gộp nhiều xe/người vào một box, kể cả khi đứng sát nhau.
4. **Người và xe máy tách riêng:** 1 box `person` cho mỗi người (người lái, người ngồi sau) và 1 box `motorcycle` cho thân xe. Hai box được phép chồng lấn. Box `person` bao từ đỉnh đầu/mũ đến bàn chân trong phạm vi nhìn thấy, gồm cả balo/gánh hàng đeo liền thân. 🔶
5. **Hàng hóa chở trên xe:** hàng cố định trên xe máy / xe ba bánh thì **được bao trong box phương tiện**, vì nó chiếm làn thực tế. 🔶
6. **Mép ảnh:** box không vượt ra ngoài khung ảnh; đối tượng bị cắt thì vẽ đến đúng mép ảnh và đặt `truncated = yes`.
7. **Kích thước tối thiểu:** nếu **cạnh dài nhất của box dưới 20 px** thì không gán box riêng lẻ; nếu chúng tụ thành cụm thì dùng 1 `ignore_region` bao cụm. Không bỏ qua đối tượng chỉ vì ở xa nếu từ 20 px trở lên và nhận diện được. 🔶
8. **Che khuất:** đối tượng bị che vẫn gán nếu còn đủ đặc trưng nhận lớp; chỉ box phần thấy; đặt `occluded_level` tương ứng.
9. **Không gán** (0 box): tượng, ma-nơ-canh, poster/billboard, búp bê/đồ chơi/xe mô hình, hình phản chiếu trong gương hoặc kính. Ảnh chỉ chứa các thứ này vẫn phải có trong file COCO với 0 annotation.
10. **`ignore_region`** chỉ dùng cho vật nhỏ/dày đặc/không tách được. Không dùng để bỏ qua vật lớn, rõ ở tiền cảnh. `ignore_region` không cần thuộc tính.

---

## 4. Ca khó

| Rule ID | Tình huống | Quyết định | Lý do | Ảnh tham chiếu |
|---|---|---|---|---|
| R-01 | Người lái/ngồi sau xe máy | Box `person` riêng cho mỗi người + box `motorcycle` riêng | Người và xe là hai thực thể; người có thể rời xe | img_001, img_005, img_026 |
| R-02 | Xe chuyên dụng chở nhiều ô tô | 1 box `truck` ôm xe tải; mỗi ô tô con trên sàn thấy rõ 1 box `car` riêng | Xe tự lái cần nhận ra vật thể ở độ cao đó | img_002 |
| R-03 | Tượng người, tượng xe, ma-nơ-canh, poster, đồ chơi/xe mô hình | Không gán box | Vật tĩnh/giả, gán sẽ gây false positive | img_011, img_017, img_018, img_027, img_033, img_038 |
| R-04 | Hình phản chiếu trong gương chiếu hậu / kính | Không gán box, không tạo `ignore_region` riêng cho gương 🔶 | Không phải thực thể trên làn đường | img_020 |
| R-05 | Xe đạp, xích lô đạp chân | Chỉ gán `person` cho người đạp/đẩy; không gán box cho xe | Chưa có lớp `bicycle` 🔶 | img_006, img_039 |
| R-06 | Tuk-tuk, xe lam, xe ba gác máy | Lớp `three_wheeler`. Nếu nhóm chưa có lớp này: `motorcycle` + `can_review` | Hình thái khác xe 2 bánh | img_004, img_035 |
| R-07 | Xe máy/xe ba bánh chở hàng cồng kềnh | Giữ lớp phương tiện, box bao cả hàng gắn liền; `can_review = true` cho tới khi nhóm chốt 🔶 | Hàng làm thay đổi bề ngang chiếm làn | img_029, img_035 |
| R-08 | Xe máy có thùng phụ (sidecar) | 1 box `motorcycle` bao cả xe và thùng phụ; người lái và người trong thùng mỗi người 1 box `person` | Thùng phụ là một phần kết cấu xe | img_022 |
| R-09 | Bán tải có nắp thùng cao | Gán `car`, `can_review = true` | Dễ nhầm với SUV/van | img_037 |
| R-10 | Xe buýt, xe khách lớn | `bus` (hoặc `truck` + `can_review` nếu chưa có lớp) | Kích thước, điểm mù, quán tính khác `van` | các ảnh xe buýt |
| R-11 | Ùn tắc xe máy dày đặc, che nhiều lớp | Gán từng xe còn thấy đặc trưng rõ (đầu xe/tay lái hoặc yên/bánh sau) và đủ 20 px; xe lớp sâu chỉ lộ mảng màu nhỏ thì bỏ qua hoặc gom `ignore_region` | Tránh nhiễu nhãn | img_005, img_026 |
| R-12 | Xe chạy nhanh, mờ chuyển động | Box ôm vệt mờ nhìn thấy, `can_review = true` | Xe thật trên đường | img_014 |
| R-13 | Vỏ xe phế liệu chất trên xe/mái nhà | Không gán `car` cho vỏ xe; chỉ gán phương tiện chuyên chở | Không phải phương tiện đang hoạt động | img_024 |
| R-14 | Xe ngập nước một phần | Box phần nhìn thấy (không ngoại suy đáy bánh), `occluded_level` phù hợp | Thống nhất quy tắc visible box | — |
| R-15 | Xe ưu tiên, xe súc vật kéo | Xe cảnh sát/cứu thương: gán `car` hoặc `van` theo hình dáng. Xe bò/ngựa kéo: không gán xe, chỉ gán `person` điều khiển; `can_review = true` 🔶 | Chưa có lớp riêng | — |
| R-16 | Xe/người bị mép ảnh cắt | Box đến sát mép ảnh, `truncated = yes` | Đúng ranh giới khung hình | — |
| R-17 | Xe đạp điện vs xe máy điện | Có bàn đạp, khung xe đạp: coi như xe đạp (R-05). Có yên dài, chắn bùn, bệ để chân như xe máy: `motorcycle`. Không rõ: `can_review` | Hai loại dễ lẫn | — |

Ca chưa chốt: bật `can_review = true` trên box (hoặc ghi vấn đề cấp ảnh) và ghi mã quy tắc trong nhật ký QC.

---

## 5. QC và phiên bản

**Quy trình 3 bước**
1. **Self-QC (100% ảnh của mình):** chạy `python scripts/validate_labels.py`; kiểm tra thiếu thuộc tính, box dưới 20 px không thuộc `ignore_region`, box vượt mép ảnh, box trùng, nhãn khác định nghĩa. Xuất COCO 1.0 từ CVAT.
2. **Kiểm chéo (2 người gán độc lập trên cùng ảnh):** tính IoU và đồng thuận lớp.
3. **Calibration:** gom ca `can_review` và ca bất đồng vào `calibration_candidates.csv`, họp để chốt, ghi rõ mã thành viên chốt và Rule ID.

**Ngưỡng đề xuất** (cần nhóm xác nhận)

| Chỉ số | Ngưỡng |
|---|---|
| IoU trung bình giữa 2 người gán | ≥ 0.85 (box ≥ 50 px, ít che); ≥ 0.70 (box < 50 px hoặc `occluded_level` ≥ 2) |
| Đồng thuận lớp | ≥ 95% |
| Đồng thuận thuộc tính | ≥ 95% |
| Recall (không bỏ sót đối tượng đủ điều kiện) | ≥ 97% |
| Ảnh lỗi ở QC cuối (40 ảnh) | 0 ảnh lỗi mới release |

**Ai quyết ca mơ hồ:** cuộc họp Calibration của nhóm (đa số, có ghi Rule ID); ca không chốt được chuyển giảng viên.

**Lịch sử thay đổi**

| Phiên bản | Thay đổi | Lý do |
|---|---|---|
| `v0` | Bản starter của giảng viên | Ban đầu |
| 995, 996, 997, 998, 999 | Các bản cá nhân | Mỗi người tự khảo sát |
| `v1.0-draft` | Hợp nhất 5 bản: 8 lớp, 3 thuộc tính, 10 quy tắc box, 17 ca khó | Chuẩn hóa các điểm mâu thuẫn (Phụ lục A) |

---

## Phụ lục A. Các điểm mâu thuẫn giữa 5 guideline và phương án đã chọn

| # | Vấn đề | 995 | 996 | 997 | 998 | 999 | Chọn tạm cho v1.0 |
|---|---|---|---|---|---|---|---|
| 1 | Danh sách lớp | 7 lớp tự thiết kế (không có `person`, `van`), có `bicycle`, `special_vehicle` | 6 lớp gốc | 6 lớp + `bus`, `tuk_tuk` | 10 lớp (có `bicycle`, `special_vehicle`, `other_vehicle`) | 6 lớp gốc | 6 lớp gốc + `bus` + `three_wheeler` |
| 2 | Có lớp `bicycle` | Có | Không | Không | Có (gồm xích lô) | Không | Không; chỉ gán `person` |
| 3 | Tên lớp xe máy | `motobike` | `motorcycle` | `motorcycle` | `motorcycle` | `motorcycle` | `motorcycle` |
| 4 | Người lái và xe | Gộp một box | Tách | Tách | Gộp một box | Tách | Tách |
| 5 | Box phần thấy hay ngoại suy | Thấy | Thấy | Thấy | Ngoại suy (amodal) | Thấy | Chỉ phần thấy |
| 6 | Hàng cồng kềnh | Thuộc tính `oversized_cargo` | Chưa nói | Không bao trong box | Bao trong box + thuộc tính | Bao trong box | Bao trong box, `can_review` đến khi chốt |
| 7 | Kích thước tối thiểu | Không nêu | Không nêu số | 20 px | 15 px | 20 px | Cạnh dài nhất ≥ 20 px |
| 8 | Ngưỡng `occluded` | 3 mức (50%) | 4 mức định tính | 4 mức (30/70) | 4 mức (50%, có "không xác định") | 4 mức (35/70) | 4 mức: 0 / 1–30 / 31–70 / >70 |
| 9 | Giá trị `truncated` | `true/false` | `yes/no` | `yes/no` | `true/false` | `yes/no` | `yes/no` |
| 10 | Thuộc tính thêm | `motion_state`, `oversized_cargo` | `can_review` | `can_review` | `motion_state`, `bulky`, `orientation` | `can_review` | Chỉ 3 thuộc tính |
| 11 | Phản chiếu gương | Không nói | Không gán | Không gán | Không nói | `ignore_region` | Không gán |
| 12 | Tuk-tuk | Lớp riêng | `can_review` | Lớp riêng (hoặc `car`) | Lớp riêng | `motorcycle` + `can_review` | Lớp `three_wheeler` |
| 13 | Xe buýt | Lớp riêng | Không nói | Lớp riêng (hoặc `truck`) | Lớp riêng | Không nói | Lớp `bus` |

## Phụ lục B. Cần kiểm tra lại số hiệu ảnh

Các guideline mô tả cùng một số ảnh không khớp nhau, cần mở ảnh đối chiếu trước khi ghi Rule ID cho từng ảnh:

- `img_005`: 997 mô tả là tài xế trên xe con/xe van thư báo, 999 mô tả là đôi nam nữ trên xe máy.
- `img_006`: 997 là người đi xe đạp, 999 là xích lô (cùng với `img_009`).
- `img_009`: 997 là xe buýt, 999 liệt kê cùng nhóm xe đạp/xích lô.
- `img_029`: 997 liệt kê là xe đạp, 999 là xe máy chở kiện hàng khổng lồ.
- `img_037`: 997 vừa đưa vào ví dụ `bus`, vừa mô tả là bán tải có nắp thùng.
- `img_011`: tượng Predator cạnh xe mô tô (999) hay tượng đài ở quảng trường có đám đông (997).

Các ảnh `img_014`, `img_024` (chỉ 997 nêu), `img_022` (chỉ 999 nêu) cần ít nhất một người khác xác nhận.
