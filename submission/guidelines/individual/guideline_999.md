# Guideline gán nhãn — v1.0-individual — Thành viên 999

- Phiên bản: v1.0-individual
- Ngày: 2026-11-16
- Người viết: Thành viên 999 (hải nam)

---

## 1. Mục tiêu

Tài liệu này cung cấp bộ quy chuẩn gán nhãn bounding box (hộp bao 2D) cho 40 ảnh giao thông đường phố, phục vụ huấn luyện mô hình thị giác máy tính phát hiện đối tượng (Object Detection 2D) trong hệ thống xe tự lái và camera giám sát giao thông thông minh.

* **Nhiệm vụ của mô hình:** Phát hiện chính xác vị trí, phân loại phương tiện và người tham gia giao thông trong mọi điều kiện ánh sáng (ngày, đêm, mưa, chói sáng).
* **Mức độ rủi ro khi gán sai:**
  * **Bỏ sót (False Negative):** Cực kỳ nguy hiểm, có thể dẫn đến tai nạn giao thông nghiêm trọng nếu xe tự lái không phát hiện người đi bộ, người đi xe máy hoặc xe đang di chuyển trên đường.
  * **Báo giả / Nhầm lẫn (False Positive):** Nhầm tượng đài, tranh quảng cáo, ma-nơ-canh hoặc hình phản chiếu qua gương thành người thật/xe thật sẽ gây phanh gấp ảo nguy hiểm (phantom braking) hoặc làm gián đoạn lưu thông.

---

## 2. Lớp và thuộc tính

### 2.1. Định nghĩa các lớp đối tượng (Classes)

Hệ thống sử dụng đúng 6 lớp theo chuẩn taxonomy khởi đầu, được định nghĩa rõ ràng kèm ví dụ và phản ví dụ đối chiếu:

| Lớp (class) | Định nghĩa chuẩn (1 câu) | Ví dụ bao gồm | Phản ví dụ / Dễ nhầm lẫn |
|---|---|---|---|
| `car` | Phương tiện giao thông cơ giới 4–9 chỗ ngồi dùng chở người hoặc bán tải cá nhân. | Xe sedan, hatchback, SUV, MPV, xe bán tải cá nhân (pickup). | Không gán xe tải lớn (`truck`), xe van chở hàng (`van`), hoặc tượng mô hình xe (`img_027`). |
| `truck` | Xe cơ giới chuyên dụng chở hàng hóa nặng, có cabin tách biệt hoặc thùng chở hàng riêng. | Xe tải thùng, xe ben, xe đầu kéo container, xe cẩu tự hành, xe chở xe chuyên dụng (`img_002`). | Không gán xe bán tải gia đình 5 chỗ cỡ nhỏ, xe van nhỏ thùng liền. |
| `van` | Xe tải nhỏ hoặc xe chở khách có khoang hành khách/hàng hóa liền một khối với cabin. | Xe minivan chở khách, xe van bưu chính/giao hàng kín thùng (`img_036`). | Không gán xe SUV (`car`) hoặc xe tải thùng rời (`truck`). |
| `motorcycle` | Phương tiện cơ giới 2–3 bánh gắn động cơ dùng để chở người/hàng. | Xe máy số, xe tay ga, mô tô phân khối lớn, xe máy có thuyền phụ/sidecar (`img_022`), xe tuk-tuk/rickshaw (`img_004`, `img_035`). | Không gán xe đạp truyền thống, xe xích lô đạp chân (`img_006`, `img_009`). |
| `person` | Con người bằng xương bằng thịt ở mọi tư thế đang có mặt trong không gian đường phố. | Người đi bộ, người điều khiển xe máy, người ngồi sau xe, người đứng/ngồi bên vỉa hè (`img_001`, `img_005`). | Tuyệt đối không gán ma-nơ-canh (`img_033`), tượng người (`img_017`), poster/billboard quảng cáo (`img_018`), búp bê đồ chơi (`img_038`). |
| `ignore_region` | Vùng bỏ qua không đánh giá chất lượng gán nhãn chi tiết; bỏ sót trong vùng này không tính là lỗi. | Cụm đám đông quá xa, xe nhỏ dưới 20 px, vùng ảnh phản chiếu qua gương gây nhiễu (`img_020`). | Không dùng để che lấp các phương tiện lớn, rõ ràng ở tiền cảnh. |

* **Xử lý đối tượng ngoài taxonomy (Xích lô, xe đạp, xe kéo thô sơ):**
  * Với người đạp xích lô, người đẩy xe hàng: Gán box `person` cho người.
  * Phần khung xe đạp, thùng xích lô: **Không gán box riêng** vì chưa có lớp `bicycle`. Nếu phương tiện chiếm dụng diện tích lớn phức tạp thì khoanh `ignore_region` quanh phần xe.

---

### 2.2. Định nghĩa các thuộc tính (Attributes)

Mỗi box (trừ `ignore_region`) bắt buộc phải được gán đầy đủ 3 thuộc tính:

1. **`occluded_level` (Mức độ che khuất):**
   * `0` (Không bị che): Thấy rõ trọn vẹn 100% đường bao của đối tượng.
   * `1` (Che khuất nhẹ): Bị che khuất từ 1% đến 35% diện tích bề mặt (ví dụ: bánh xe bị che bởi vỉa hè hoặc cản trước xe khác).
   * `2` (Che khuất vừa/nhiều): Bị che khuất từ 36% đến 70% diện tích (chỉ còn thấy nửa thân trên hoặc nửa thân trước).
   * `3` (Che khuất nghiêm trọng): Bị che khuất trên 70% diện tích, chỉ còn lộ một phần nhỏ đặc trưng nhận dạng nhưng người nhìn vẫn khẳng định được sự tồn tại của vật thể.

2. **`truncated` (Bị cắt bởi mép ảnh):**
   * `no`: Đối tượng nằm hoàn toàn bên trong khung hình ảnh.
   * `yes`: Đối tượng bị đường biên viền của ảnh cắt ngang qua thân thể/phương tiện.

3. **`can_review` (Đánh dấu cần xem lại):**
   * `false` (mặc định): Tự tin với quyết định gán nhãn.
   * `true`: Đánh dấu ca nghi vấn, ca biên mơ hồ cần đưa ra thảo luận trong buổi họp Calibration của nhóm.

---

## 3. Quy tắc vẽ Bounding Box

1. **Độ ôm sát phần nhìn thấy (Visible Bounding Box):**
   * Box chỉ bao trùm phần nhìn thấy thực tế của vật thể. Không vẽ suy đoán (amodal box) ăn sâu vào vùng bị vật cản che khuất.
   * Box phải tiếp xúc sát 4 mép biên ngoài cùng (trên, dưới, trái, phải) của vật thể. Sai số chừa mép hoặc lẹm mép không được vượt quá 2–3 pixel.

2. **Quy tắc phân tách Người và Xe máy (`person` vs `motorcycle`):**
   * **Bắt buộc tách làm 2 box độc lập:**
     * 1 box gán nhãn `person`: Bao trọn người lái (từ mũ bảo hiểm/đầu đến bàn chân).
     * 1 box gán nhãn `motorcycle`: Bao trọn thân xe (bánh xe, yếm, pô xe, ghi-đông).
   * Nếu có người ngồi sau (hành khách): Vẽ thêm 1 box `person` riêng cho người ngồi sau.
   * Phần diện tích chồng lấn giữa người và xe là hợp lệ và tự nhiên.

3. **Hàng hóa và kiện hàng cồng kềnh chở trên phương tiện:**
   * Với xe máy chở hàng cồng kềnh (`img_029`): Bounding box của `motorcycle` phải bao trùm cả kiện hàng gắn liền trên giá chở hàng, vì kiện hàng tạo thành một khối chiếm dụng lòng đường.
   * Với người đi bộ gánh hàng, mang balo lớn: Box `person` bao trùm cả balo và gánh hàng liền thân.

4. **Ngưỡng kích thước tối thiểu (Min Box Size):**
   * Chỉ gán nhãn cho đối tượng có chiều cao **≥ 20 pixel**.
   * Đối tượng có kích thước < 20 px ở hậu cảnh xa: Bỏ qua không gán, hoặc gom vào vùng `ignore_region` nếu nằm thành cụm dày đặc.

---

## 4. Các ca khó & Quyết định xử lý (Edge Cases)

| Mã ảnh | Tình huống thực tế | Rule ID | Quyết định xử lý của 999 | Lập luận & Căn cứ kỹ thuật |
|---|---|---|---|---|
| `img_002.jpg` | Xe chuyên dụng chở ô tô (Car carrier) chở nhiều xe con trên tầng xe | **R-01** | Vẽ 1 box `truck` cho xe tải chở hàng (chỉ ôm khung vỏ xe tải). Từng xe con ở tầng trên nếu cao ≥ 50px gán riêng từng box `car` (`occluded_level=1`). | Xe con trên sàn xe vẫn có hình thái ô tô hoàn chỉnh; hệ thống xe tự lái cần nhận biết có vật thể ô tô trên cao để tránh va chạm tầm cao. |
| `img_005.jpg`, `img_026.jpg` | Đôi nam nữ / Dòng xe máy ùn tắc trong hầm và đường phố | **R-02** | Tách riêng: Mỗi người 1 box `person`, mỗi xe 1 box `motorcycle`. Đánh giá `occluded_level` tương ứng (0, 1 hoặc 2). | Người và xe có thuộc tính động học khác nhau, người có thể bước xuống xe; mô hình cần học nhận diện độc lập hai thực thể. |
| `img_011.jpg` | Tượng quái thú Predator đứng cạnh dàn xe mô tô | **R-03** | **KHÔNG gán** nhãn `person` cho tượng Predator. Các xe máy thật xung quanh vẫn gán nhãn `motorcycle`. | Đây là tượng mô hình trang trí bằng kim loại, không phải người thật. Gán `person` sẽ gây dương tính giả (false positive). |
| `img_017.jpg` | Tượng Công tước Wellington cưỡi ngựa đội nón giao thông ở Glasgow | **R-04** | **KHÔNG gán** nhãn `person` cho tượng người cưỡi ngựa đá. | Tượng đài điêu khắc công cộng cố định trên bệ đá, không tham gia giao thông. |
| `img_018.jpg` | Biển quảng cáo (billboard) chính trị in hình chân dung người lớn | **R-05** | **KHÔNG gán** nhãn `person` cho hình ảnh in 2D trên biển bạt. | Hình in 2D trên mặt phẳng tĩnh, không phải đối tượng thực tế trên đường. |
| `img_020.jpg` | Cầu vồng và hậu cảnh phản chiếu qua gương chiếu hậu xe ô tô | **R-06** | **Khoanh 1 box `ignore_region`** trùm lên toàn bộ mặt gương phản chiếu. | Ảnh ảo phản chiếu trong gương dễ đánh lừa mô hình phát hiện chiều sâu; dùng `ignore_region` để vô hiệu hóa tính lỗi vùng này. |
| `img_022.jpg` | Xe máy có thuyền phụ chở người bên cạnh (Motorcycle with sidecar) | **R-07** | Gán 1 box `motorcycle` bao trùm cả xe và thùng thuyền phụ. Người ngồi lái và người ngồi trong thuyền phụ gán các box `person` riêng. | Thuyền phụ được lắp cố định thành một kết cấu xe 3 bánh chiếm dụng diện tích làn đường. |
| `img_027.jpg` | Tượng đài đục bằng đá hình xe bán tải trong nghĩa viên | **R-08** | **KHÔNG gán** nhãn `car` hay `truck` cho khối đá điêu khắc. | Đây là bia mộ điêu khắc tĩnh, đặt trên bệ cỏ nghĩa trang, không phải phương tiện giao thông. |
| `img_029.jpg` | Xe máy chở kiện hàng khổng lồ che gần hết người và thân xe | **R-09** | Gán box `motorcycle` bao trùm toàn bộ kiện hàng và bánh xe. Người lái nếu thò đầu ra vẫn gán 1 box `person` (`occluded_level=3`). | Kiện hàng gắn chặt vào xe làm thay đổi kích thước vật lý chiếm làn; bắt buộc bao trọn để cảnh báo an toàn va chạm. |
| `img_033.jpg` | Ma-nơ-canh mặc váy áo đứng sau cửa kính tiệm thời trang | **R-10** | **KHÔNG gán** nhãn `person` cho ma-nơ-canh. | Ma-nơ-canh là vật thể trưng bày sau kính, không phải người tham gia giao thông. |
| `img_004.jpg`, `img_035.jpg` | Xe Tuk-tuk và xe Auto Rickshaw 3 bánh chở khách | **R-11** | Tạm thời phân loại vào `motorcycle` (hoặc `van`), tick `can_review=true` để đưa ra biểu quyết tại Pha 2 của nhóm. | Phương tiện 3 bánh đặc thù châu Á, cabin mở một phần; cần thống nhất toàn nhóm để tránh phân mảnh nhãn. |
| `img_037.jpg` | Xe bán tải có gắn nắp thùng cao kín (Truck cap) | **R-12** | Gán nhãn `car` (hoặc `truck` nếu thùng hàng chuyên dụng chở hàng), tick `can_review=true` để chốt đồng thuận. | Xe bán tải lắp thêm mui che thùng sau dễ nhầm với SUV lớn hoặc xe van nhỏ. |
| `img_038.jpg` | Tủ kính bày bán đồ chơi, búp bê, mô hình xe hơi nhỏ | **R-13** | **Khoanh vùng `ignore_region`** bao trùm toàn bộ tủ kính hoặc bỏ qua không vẽ. | Toàn bộ là đồ chơi kích thước mini trong tủ kính, không phải phương tiện hay người thật. |

*Phân loại hành động:*
* **Loại trừ dứt khoát theo quy tắc (Rule-based Exclusion):** R-03, R-04, R-05, R-08, R-10, R-13 (tượng, tranh ảnh, đồ chơi, ma-nơ-canh, phản chiếu gương -> dứt khoát không gán nhãn người/xe).
* **Cần đưa ra thảo luận với Reviewer / Nhóm (Needs Calibration):** R-11 (tuk-tuk xếp vào `motorcycle` hay lớp riêng), R-12 (bán tải nắp cao).

---

## 5. QC và Quản lý phiên bản

### 5.1. Tiêu chí kiểm soát chất lượng cá nhân (Self-QC)
* **100% đối tượng hợp lệ** được gán đúng nhãn và đủ 3 thuộc tính.
* **Độ ôm sát:** Bbox chạm sát các mép nhìn thấy của đối tượng, không lệch quá 3 px.
* **Ngưỡng kích thước:** Không tồn tại box nào dưới 20 px (chiều cao hoặc chiều rộng) mà không gắn `ignore_region`.
* Kiểm tra tính toàn vẹn của file xuất COCO bằng script kiểm thử `python scripts/validate_labels.py`.

### 5.2. Lịch sử phiên bản

| Phiên bản | Ngày | Nội dung thay đổi | Căn cứ điều chỉnh |
|---|---|---|---|
| `v0` | 2026-11-16 | Bản starter khởi đầu của giảng viên | Khung ban đầu, thiếu quy tắc ca khó. |
| `v1.0-individual` | 2026-11-16 | Thành viên 999 hoàn thiện 13 quy tắc ca khó, phân tách người và xe máy, quy chuẩn ngưỡng thuộc tính và xử lý tượng/ma-nơ-canh/xe cõng xe. | Khảo sát thực tế trên toàn bộ 40 ảnh `data/images/`. |
