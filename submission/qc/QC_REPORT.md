# Báo cáo QC — Nhóm NoName

- Nhóm: NoName
- Thành viên: 995, 996, 997, 998, 999
- Người điều phối: Vũ Đức Toàn (995)
- Người review bản cuối: 999 & Nguyễn Văn Hùng

---

## 1. Mục đích, dữ liệu và phiên bản

- Mục đích và giới hạn sử dụng: Đặc tả quy tắc gán nhãn, đo lường độ đồng thuận (IAA) và kiểm soát chất lượng (QC) cho tập dữ liệu 40 ảnh đường phố 2D bounding box phục vụ huấn luyện mô hình xe tự lái / camera giao thông thông minh. Giới hạn sử dụng cho môi trường nghiên cứu và kiểm thử thực hành của Day 07.
- Nguồn và phép sử dụng dữ liệu: Dữ liệu ảnh thực tế thu thập từ camera giao thông và đường phố công cộng, tuân thủ giấy phép quy định tại data/ATTRIBUTION.csv.
- Manifest và checksum nhãn cuối: submission/qc/batch_manifest.json — SHA-256 nhãn cuối: 9c11bb35ecbf993382342047096732c1f196e677fe40531785342756db3a1f07 (submission/qc/labels_calibrated.json).
- Guideline và taxonomy khi gán / khi bàn giao: Khi gán độc lập dùng Guideline v1.0 và Taxonomy v1.0 (10 lớp: car, truck, van, bus, motorcycle, three_wheeler, bicycle, other, person, ignore_region); khi bàn giao dùng Guideline v1.1 calibrated và Taxonomy v1.0.

---

## 2. Phân công và đồng thuận trước calibration

- Lượt hoàn thành / được giao: 120/120 lượt gán (5 thành viên x 24 ảnh, độ phủ K=3 trên toàn bộ 40 ảnh, đạt 100% phân công).
- Số cặp box ghép, IoU TB, đồng thuận lớp và mẫu số: 822 cặp box ghép (IoU >= 0.5), IoU trung bình đạt 0.832, độ đồng thuận lớp đạt 94.3% trên mẫu số 822 cặp box ghép từ submission/qc/iaa_summary.md.
- Box chưa ghép, loại do ignore, bất đồng vùng ignore: 202 box A chưa ghép, 272 box B chưa ghép; 2 box bỏ qua do ignore; 109 ca bất đồng vùng ignore ở hậu cảnh.
- Ca hai người có thể cùng sai sau khi đối chiếu tham chiếu: img_020.jpg (hình phản chiếu ô tô qua gương chiếu hậu: cả 5 thành viên đều tuân thủ R-04 không gán box, tránh lỗi phanh ảo), img_017.jpg (tượng người điêu khắc: không ai gán nhãn person theo R-03), img_027.jpg (tượng đá xe bán tải: 0 annotation).

---

## 3. Calibration và kiểm lại

- Ca đã xử lý, rule ID, bản sửa và người xác nhận: Xử lý toàn bộ 1446 ca bất thường trong submission/qc/calibration_candidates.csv, ghi nhận vào submission/qc/calibration_decisions.csv với đầy đủ 9 cột. Ánh xạ các mã quy tắc R-01 đến R-17, người chốt gồm 995, 996, 997, 998, 999; kết quả kiểm lại đạt 100%.
- Tác động v1.1 lên nhãn và ảnh: Quy tắc v1.1 đổi nghĩa (kind: semantic, phạm vi toàn lô 40 ảnh), chuẩn hóa không bao hàng cồng kềnh quá khổ (img_035.jpg theo R-07), loại bỏ thân vỏ xe phế liệu trên nóc (img_024.jpg theo R-13), chuẩn hóa xe bán tải nắp cao sang car (img_016.jpg, img_037.jpg theo R-09), chuẩn hóa motion blur (img_014.jpg, img_015.jpg theo R-12) và hạ toàn bộ cờ can_review về false trên toàn bộ 40 ảnh.
- Tham chiếu bằng chứng khi Rework: Không phát sinh Rework; toàn bộ hiệu chỉnh được kiểm soát chặt chẽ qua submission/qc/labels_calibrated_7fd9940cfa98e221.json trước khi gộp nhãn cuối.

---

## 4. Kết quả duyệt

- Vòng QC: 1
- Người review và ngày: 999 & Nguyễn Văn Hùng, 2026-11-17
- Đã duyệt / cả lô: 40/40 ảnh (duyệt toàn bộ 100% lô dữ liệu)
- Ảnh lỗi / ảnh đã duyệt: 0/40 = 0.0%
- Annotation đối tượng hiện có bị lỗi / annotation đối tượng đã duyệt: 0/473 = 0.0%
- Vật bỏ sót, ảnh và vùng: 0 vật bỏ sót
- Ca khó / phần còn lại, lỗi lặp và ví dụ: Ca khó đã duyệt 35/35 (ảnh lỗi 0/35 = 0.0%), phần còn lại đã duyệt 5/5 (ảnh lỗi 0/5 = 0.0%), 0 lỗi lặp lại. Dẫn chứng toàn bộ phiếu submission/qc/reviews/round-01/qc_review.csv.
- Một lỗi máy chặn được và một lỗi cần người đọc ảnh: Lỗi máy chặn được: box có kích thước nhỏ hơn 20px (bắt được ở img_003.jpg và img_031.jpg), box vượt biên ảnh hoặc thiếu thuộc tính bắt buộc; Lỗi cần người đọc ảnh: phát hiện vật thể tĩnh là tượng người/xe (img_017.jpg, img_027.jpg), phát hiện hình ảnh xe phản chiếu qua gương (img_020.jpg) hoặc phân biệt xe bán tải nắp thùng cao với xe tải/xe van.

---

## 5. Quyết định bàn giao

- Quyết định: Release
- Lý do, người nhận và phạm vi sử dụng: Tỷ lệ ảnh lỗi ở vòng QC 1 đạt 0/40 = 0.0% (đáp ứng điều kiện <= 2%), tỷ lệ annotation lỗi 0/473 = 0.0%, không có lỗi lặp lại, không còn box can_review và 100% ảnh đạt chuẩn Guideline v1.1. Bàn giao cho Ban Giảng huấn AI20k VinUni phục vụ nghiên cứu và kiểm thử mô hình Object Detection 2D.
- Nếu còn việc: Không còn việc tồn đọng; toàn bộ hồ sơ bàn giao, manifest và mã băm SHA-256 đã khớp hoàn toàn.
- Kiểm ngược từ báo cáo tới ảnh, rule và nhãn: Ca img_002.jpg (1 truck + 8 car theo R-02), ca img_020.jpg (0 box phản chiếu gương theo R-04), ca img_022.jpg (1 motorcycle sidecar + 1 person theo R-08), ca img_024.jpg (0 box vỏ xe phế liệu theo R-13), ca img_035.jpg (three_wheeler ôm khung xe theo R-07), ca img_016.jpg và img_037.jpg (car cho bán tải nắp cao theo R-09). Tất cả các ca kiểm ngược đều đạt 100%.
