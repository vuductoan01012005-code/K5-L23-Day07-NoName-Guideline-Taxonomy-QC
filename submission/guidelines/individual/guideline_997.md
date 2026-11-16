# Guideline gán nhãn cá nhân — Thành viên 997

- Phiên bản: `v0.1_indiv_997`
- Ngày: 2026-11-16
- Tác giả: Thành viên 997 (Nhóm NoName)
- Định dạng nhãn: 2D Bounding Box (Rectangle) & Attributes theo chuẩn COCO 1.0 trên công cụ CVAT

---

## 1. Mục tiêu và Mô hình sử dụng nhãn

* **Hệ thống đích**: Nhãn phục vụ huấn luyện mô hình phát hiện vật thể 2D (Object Detection) và định vị không gian thời gian thực trên xe tự lái / hệ thống camera giám sát giao thông thông minh.
* **Tác động an toàn và rủi ro nhận diện**:
  * **Bỏ sót vật thể (False Negative - FN)**: Cực kỳ nguy hiểm. Nếu bỏ sót người đi bộ (`person`) hoặc phương tiện đang di chuyển sát xe (`motorcycle`, `car`), hệ thống lập kế hoạch đường đi sẽ không kích hoạt phanh hoặc giảm tốc, dẫn đến nguy cơ va chạm trực tiếp.
  * **Nhận diện sai lớp / Gán thừa (False Positive - FP)**: Gán box lên hình phản chiếu qua gương, tượng điêu khắc hoặc tranh quảng cáo 2D sẽ khiến xe tự lái kích hoạt phanh khẩn cấp vô căn cứ (phantom braking), gây nguy cơ va chạm dây chuyền từ phía sau.
  * **Sai số ranh giới Bounding Box**: Box lỏng lẻo hoặc cắt lẹm thân xe sẽ làm sai lệch ước lượng khoảng cách từ camera 2D đến vật thể thực tế trong không gian 3D.

---

## 2. Định nghĩa Lớp (Classes) và Thuộc tính (Attributes)

### 2.1. Danh sách Lớp nhãn

| Tên lớp (`class_name`) | Định nghĩa cốt lõi | Ví dụ thực tế trong bộ ảnh | Phản ví dụ / Dễ nhầm với (KHÔNG gán) |
|---|---|---|---|
| `car` | Ô tô con 4–9 chỗ, sedan, hatchback, SUV, MPV, xe bán tải (pickup) chở khách/gia đình. | Xe con lưu thông (`img_001`), ô tô con chở trên sàn xe tải (`img_002`), taxi (`img_010`). | Tượng xe bán tải bằng đá (`img_027`), xe mô hình đồ chơi trong tủ kính (`img_038`). |
| `truck` | Xe tải chở hàng, xe bồn, xe đầu kéo container, xe ben chuyên dụng có buồng lái và thùng hàng riêng biệt. | Xe chở ô tô 2 tầng (`img_002`), xe tải nhẹ chở hàng (`img_008`). | Xe bán tải nhỏ phục vụ gia đình (xếp vào `car`), xe ba gác chở hàng (xếp vào `three_wheeler`/`tuk_tuk`). |
| `van` | Xe thùng kín cỡ nhỏ đến trung bình, có thân xe liền khối, cabin và khoang chứa hàng/khách chung khung vỏ. | Xe van giao hàng thư báo (`img_005`), xe 16 chỗ dáng hộp trung chuyển (`img_030`). | Xe buýt lớn chở khách công cộng (`img_009`), xe tải thùng tách rời cabin (`img_008`). |
| `bus` *(Đề xuất mở rộng)* | Xe buýt công cộng, xe khách liên tỉnh, xe du lịch cỡ lớn từ 16 chỗ ngồi trở lên. | Xe buýt lớn chở khách (`img_009`, `img_031`, `img_037`, `img_040`). | Xe minivan 7–9 chỗ gia đình (gán `car`/`van`). |
| `motorcycle` | Xe hai bánh gắn động cơ xăng hoặc điện (xe máy, xe tay ga, xe số, mô tô phân khối lớn). | Xe máy đi trên đường (`img_001`, `img_010`, `img_023`). | Xe đạp không động cơ (`img_006`, `img_029`, `img_039`), xe máy ba bánh tuk-tuk (`img_004`). |
| `tuk_tuk` *(Đề xuất mở rộng)* | Phương tiện ba bánh có động cơ dùng để chở khách hoặc chở hàng (tuk-tuk, xe lam, xe ba gác máy). | Xe tuk-tuk chở khách (`img_004`, `img_016`), xe tuk-tuk chở hàng cồng kềnh (`img_035`). | Xe máy 2 bánh kéo xe kéo nhỏ phía sau, xe xích lô đạp chân (`img_039`). |
| `person` | Con người còn sống (người đi bộ, người đứng/ngồi bên lề đường, người lái và người ngồi sau phương tiện). | Người đi bộ qua đường (`img_001`), người lái xe máy (`img_001`, `img_004`), tài xế trên xe con (`img_005`). | Tượng đồng/đá hình người (`img_011`, `img_017`), ma-nơ-canh trong tủ kính (`img_033`), hình người in trên biển quảng cáo (`img_018`). |
| `ignore_region` | Vùng không gian chứa cụm vật thể quá nhỏ (< 20px), đám đông dày đặc ở hậu cảnh hoặc vùng mờ nhạt không thể phân tách chính xác. | Đám đông dày đặc ở hậu cảnh quảng trường (`img_011`), hàng loạt xe đỗ mờ ảo ở đường chân trời (`img_003`). | Bất kỳ vật thể nào có chiều cao >= 20px và nhận dạng rõ ràng. |

* **Xử lý đối tượng ngoài Taxonomy**: Xe đạp (`bicycle`), xe xích lô đạp chân, xe súc vật kéo hiện tại không thuộc 5 lớp của bài lab. Không tự ý ép vào `motorcycle` hay `car`; nếu đối tượng nằm lẻ loi và không cản trở thì bỏ qua, nếu nằm trong cụm ùn tắc dày đặc thì đưa vào `ignore_region`.

---

### 2.2. Danh sách Thuộc tính với Ngưỡng đo lường cụ thể

| Thuộc tính (`attribute`) | Kiểu dữ liệu | Giá trị hợp lệ | Ngưỡng định lượng & Định nghĩa kỹ thuật |
|---|---|---|---|
| `occluded_level` | `select` | `0` | **Thấy rõ hoàn toàn**: Diện tích bề mặt vật thể không bị che khuất hoặc bị che < 1% bởi vật thể khác. |
| | | `1` | **Che khuất nhẹ (1% – 30%)**: Vật thể bị che khuất một phần nhỏ (ví dụ lốp xe bị che bởi vỉa hè, chân người bị che bởi bồn hoa) nhưng toàn bộ hình dáng nhận dạng rõ ràng. |
| | | `2` | **Che khuất trung bình đến nặng (31% – 70%)**: Vật thể bị che khuất từ một phần ba đến hơn một nửa diện tích (ví dụ xe con đi sau xe tải, người lái xe máy bị tay lái và chắn bùn che khuất phần chân). |
| | | `3` | **Che khuất nghiêm trọng (> 70%)**: Vật thể bị che khuất trên 70% diện tích nhưng phần còn lại vẫn đủ đặc trưng chắc chắn để con người nhận biết lớp (ví dụ chỉ lộ đầu xe và đèn pha). Nếu bị che > 90% không thể nhận diện chắc chắn thì bỏ qua không gán. |
| `truncated` | `select` | `no` | Vật thể nằm trọn vẹn bên trong khung hình ảnh, không bị cắt bởi bất kỳ cạnh nào của ảnh. |
| | | `yes` | Vật thể bị cắt cụt bởi ít nhất một trong bốn mép biên của bức ảnh (trên, dưới, trái, phải). |
| `can_review` | `checkbox` | `true` / `false` | Đánh dấu `true` khi người gán gặp tình huống biên không chắc chắn, cần đưa ra phiên họp Calibration của nhóm hoặc xin ý kiến Reviewer. |

---

## 3. Quy tắc vẽ Bounding Box (Hình học & Ngữ nghĩa)

1. **Nguyên tắc ôm sát phần nhìn thấy (Tight Visible Box)**: Bounding box phải bao trọn các điểm ngoài cùng của phần vật thể **nhìn thấy được** trên ảnh 2D (bao gồm thân vỏ, bánh xe, gương chiếu hậu ngoài cùng, người ngồi bên trong nếu hở). Không vẽ phần dự đoán bị che khuất (không áp dụng amodal box dự đoán mù dưới lòng đất/nước). Sai số cạnh box không vượt quá 2–3 pixels.
2. **Quy tắc phân tách Người và Xe máy (`motorcycle` & `person`)**:
   * Khi có người điều khiển hoặc ngồi sau xe máy (`img_001.jpg`): **Bắt buộc vẽ 2 bounding box riêng biệt**:
     * 01 box `motorcycle`: Ôm sát toàn bộ thân xe, tay lái, bánh xe và biển số xe.
     * 01 box `person`: Ôm sát từ đỉnh đầu/mũ bảo hiểm xuống đến hết bàn chân của người đó.
   * Hai bounding box này được phép chồng lấn tự nhiên lên nhau (Intersection Over Union cục bộ).
3. **Quy tắc Xe chở xe (`truck` và `car`)**:
   * Trên các xe chuyên dụng chở ô tô (`img_002.jpg`): Vẽ 01 box lớn nhãn `truck` bao toàn bộ xe tải chuyên dụng (gồm cabin và giàn sàn chở hàng). Đồng thời, **vẽ từng bounding box độc lập nhãn `car`** cho mỗi chiếc ô tô con nằm trên giàn sàn (nếu ô tô đó thấy rõ và đạt chiều cao >= 20px).
4. **Quy tắc Hàng hóa cồng kềnh trên phương tiện**:
   * Với xe chở hàng cồng kềnh (`img_035.jpg`): Bounding box của phương tiện (`tuk_tuk` hoặc `motorcycle`) chỉ ôm khung xe, bánh xe và phần hàng hóa nằm gọn trong lòng xe; các bao tải/khối hàng cồng kềnh vươn quá khổ cao gấp đôi thân xe **không** được kéo box trùm lên để tránh làm méo tỷ lệ hình học chuẩn của phương tiện.
5. **Quy tắc Phản ví dụ (Tượng, Đồ chơi, Ma-nơ-canh, Tranh ảnh 2D)**:
   * **Tuyệt đối không gán box** cho:
     * Tượng điêu khắc bằng đá/đồng/kim loại (`img_011.jpg`, `img_017.jpg`, `img_027.jpg`).
     * Ma-nơ-canh trưng bày trong cửa hàng kính (`img_033.jpg`).
     * Xe mô hình, đồ chơi trẻ em (`img_038.jpg`).
     * Tranh ảnh, biển quảng cáo tấm lớn in hình người hoặc phương tiện (`img_018.jpg`).
   * Nếu một bức ảnh chỉ chứa toàn các đối tượng phản ví dụ này, bức ảnh đó vẫn phải có mặt trong file COCO xuất ra với `0 annotation`.
6. **Quy tắc Phản chiếu qua gương**:
   * Hình ảnh người và phương tiện xuất hiện qua gương chiếu hậu (`img_020.jpg`) hoặc kính tòa nhà không phải là thực thể vật lý trong làn đường $\rightarrow$ **Tuyệt đối không gán box**.
7. **Quy tắc Ngưỡng kích thước tối thiểu & Đám đông**:
   * Mọi vật thể có chiều cao hoặc chiều rộng **nhỏ hơn 20 pixels** đều không gán box riêng lẻ. Nếu chúng nằm tụ tập thành đám đông ở xa thì dùng 01 box `ignore_region` bao quanh toàn bộ cụm.

---

## 4. Danh mục Ca khó thực tế (Edge Cases) trong 40 ảnh

Bảng tổng hợp các tình huống biên được khảo sát trực tiếp từ bộ ảnh `data/images/img_001.jpg` đến `img_040.jpg`:

| Tên ảnh (`image_id`) | Tình huống phát hiện trên ảnh | Đề xuất Rule ID | Quyết định gán nhãn | Lập luận kỹ thuật |
|---|---|---|---|---|
| `img_001.jpg` | Người điều khiển xe máy trên làn đường giao thông. | `R-01` | Gán 01 box `person` ôm trọn người lái + 01 box `motorcycle` ôm trọn xe máy. `occluded_level=2` cho người, `1` cho xe. | Tách bạch tác nhân sinh học có thể rời xe và phương tiện cơ giới; cho phép mô hình học cả 2 thực thể. |
| `img_002.jpg` | Xe tải chuyên dụng chở 8 ô tô con trên giàn 2 tầng. | `R-02` | Gán 01 box lớn `truck` bao toàn bộ xe tải sàn; gán thêm 8 box `car` riêng cho từng ô tô con trên sàn. | Mô hình xe tự lái cần nhận diện ô tô con dù nó đang đỗ trên sàn xe khác để tránh va chạm tầm cao. |
| `img_004.jpg` | Xe tuk-tuk 3 bánh chở người lưu thông giữa phố. | `R-03` | Gán nhãn `tuk_tuk` (nếu có trong taxonomy v1.0) hoặc tạm thời gán `car` kèm tick `can_review=true`. | Xe 3 bánh có kích thước lớn hơn xe máy nhưng nhỏ hơn ô tô; cần thống nhất lớp ở Pha 2. |
| `img_006.jpg` | Người đi xe đạp không động cơ ở lề đường. | `R-04` | KHÔNG gán nhãn cho xe đạp; gán 01 box `person` cho người đi xe đạp (`occluded_level=2`). | `bicycle` không có trong taxonomy v0/v1.0 của lab; người đi xe đạp vẫn là người tham gia giao thông. |
| `img_009.jpg` | Xe buýt chở khách cỡ lớn 45 chỗ lưu thông. | `R-05` | Gán nhãn `bus` (nếu bổ sung lớp) hoặc gán `truck` kèm tick `can_review=true`. | Không thể gán `van` vì kích thước quá lớn, khác biệt hoàn toàn về điểm mù và quán tính phanh. |
| `img_011.jpg` | Tượng đài người bằng đá/kim loại tại quảng trường. | `R-06` | KHÔNG gán box `person`. | Tượng là vật tĩnh, không di chuyển; gán nhãn sẽ gây lỗi cảnh báo giả nghiêm trọng cho xe tự lái. |
| `img_014.jpg` | Ô tô con di chuyển tốc độ cao bị nhòe chuyển động (motion blur). | `R-07` | Gán box `car` ôm toàn bộ vệt mờ có thể quan sát được của xe, gán `occluded_level=1`, `can_review=true`. | Xe thực sự đang chạy trên đường; cần định vị vùng chiếm chỗ an toàn. |
| `img_017.jpg` | Tượng đồng nhân vật lịch sử đứng trên bệ đá công viên. | `R-06` | KHÔNG gán box `person`. Xuất ảnh này với 0 annotation. | Phản ví dụ chuẩn theo tiêu chí an toàn của lab. |
| `img_018.jpg` | Biển quảng cáo tấm lớn in hình người mẫu và xe ô tô. | `R-08` | KHÔNG gán box `person` hay `car` lên mặt biển quảng cáo. | Hình ảnh đồ họa 2D phẳng không phải vật thể 3D chiếm dụng không gian vật lý. |
| `img_020.jpg` | Xe ô tô và người đi đường phản chiếu trong gương chiếu hậu. | `R-09` | KHÔNG gán box cho các hình phản chiếu trong gương. | Vật thể trong gương nằm phía sau xe, việc gán box ở vị trí gương sẽ làm sai lệch không gian điều hướng. |
| `img_024.jpg` | Thân vỏ xe ô tô cũ phế liệu chất trên nóc xe tải/mái nhà. | `R-10` | KHÔNG gán `car` cho phần thân vỏ phế liệu không thể vận hành; chỉ gán phương tiện chuyên chở. | Tránh nhiễu dữ liệu cho bài toán phát hiện phương tiện chủ động. |
| `img_027.jpg` | Tượng điêu khắc mô phỏng xe bán tải bằng đá nguyên khối. | `R-06` | KHÔNG gán box `car` hay `truck`. | Là tác phẩm điêu khắc nghệ thuật tĩnh, không tham gia giao thông. |
| `img_033.jpg` | Ma-nơ-canh mặc quần áo đứng sau cửa kính shop thời trang. | `R-06` | KHÔNG gán box `person`. | Vật giả định dạng người tĩnh sau lớp kính. |
| `img_035.jpg` | Xe tuk-tuk chở các bao tải hàng hóa chất cao gấp đôi nóc xe. | `R-11` | Gán box `tuk_tuk` ôm thân xe và bánh xe; KHÔNG kéo box bao trọn khối bao tải nhô cao. | Bao trọn cả hàng hóa sẽ làm sai lệch tâm box và tỷ lệ khung hình đặc trưng của phương tiện 3 bánh. |
| `img_037.jpg` | Xe bán tải lắp nắp thùng sau kín cao bằng nóc cabin (Master 75). | `R-12` | Gán lớp `car` (thuộc dòng pickup đa dụng), gán `can_review=true` để đưa ra thảo luận Pha 2. | Bán tải nắp thùng cao dễ bị nhầm lẫn giữa `car`, `van` và `truck`; cần quy tắc nhóm rõ ràng. |
| `img_038.jpg` | Ô tô mô hình đồ chơi trẻ em trưng bày trong tủ kính. | `R-06` | KHÔNG gán box `car`. | Đồ chơi kích thước nhỏ không phải phương tiện giao thông thực tế. |

---

## 5. Quy trình QC và Lịch sử Phiên bản

* **Ngưỡng chất lượng đề xuất áp dụng cho nhóm**:
  * Tỷ lệ đồng thuận IoU trung bình giữa 2 người gán (IAA IoU): $\ge 0.85$ (với box $\ge 50\text{px}$) và $\ge 0.70$ (với box $< 50\text{px}$).
  * Tỷ lệ đồng thuận phân loại lớp (IAA Class Agreement): $\ge 95\%$.
  * Tỷ lệ ảnh có lỗi ở vòng QC cuối: $\le 2\%$ (với tập 40 ảnh: yêu cầu đạt $0\%$ lỗi mới được quyết định Release).
* **Cơ chế xử lý bất đồng**:
  * Các ca có gắn cờ `can_review` hoặc bất đồng IoU/Class sẽ được tổng hợp tự động vào `calibration_candidates.csv`.
  * Nhóm tổ chức họp trực tiếp tại Pha 2 và Pha 5 để chốt phương án, người chốt ghi rõ mã thành viên và mã quy tắc tương ứng.

* **Lịch sử sửa đổi**:

| Phiên bản | Ngày | Nội dung thay đổi | Căn cứ & Ảnh áp dụng |
|---|---|---|---|
| `v0` | 2026-11-16 | Bản khởi đầu của ban giảng huấn (sơ sài, chưa có quy tắc ca khó, thiếu ngưỡng đo được). | - |
| `v0.1_indiv_997` | 2026-11-16 | Khởi tạo guideline cá nhân: định nghĩa rõ 5 lớp gốc + 2 lớp đề xuất (`bus`, `tuk_tuk`), định lượng 4 mức `occluded_level`, chuẩn hóa 12 quy tắc ca khó với dẫn chứng ảnh cụ thể. | Khảo sát toàn bộ 40 ảnh (`img_001.jpg` – `img_040.jpg`). |
