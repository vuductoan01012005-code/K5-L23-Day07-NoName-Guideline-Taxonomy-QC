# Báo cáo QC — Nhóm NoName

- Nhóm: NoName
- Thành viên: 995, 996, 997, 998, 999
- Người điều phối: Vũ Đức Toàn
- Người review bản cuối: Nguyễn Văn Hùng

---

## 1. Mục đích, dữ liệu và phiên bản

- Mục đích và giới hạn sử dụng: Đặc tả quy tắc gán nhãn, đo lường độ đồng thuận (IAA) và kiểm soát chất lượng (QC) cho tập dữ liệu 40 ảnh đường phố 2D bounding box phục vụ huấn luyện mô hình xe tự lái / giám sát giao thông. Giới hạn sử dụng cho môi trường nghiên cứu và kiểm thử thực hành.
- Nguồn và phép sử dụng dữ liệu: Dữ liệu ảnh thực tế thu thập từ camera giao thông và đường phố mở, tuân thủ giấy phép quy định tại data/ATTRIBUTION.csv.
- Manifest và checksum nhãn cuối: <<Điền sau khi chạy scripts/build_final.py ở Pha 5: SHA-256 từ batch_manifest.json>>
- Guideline và taxonomy khi gán / khi bàn giao: Khi gán độc lập dùng Guideline v1.0 và Taxonomy v1.0 (10 lớp: car, truck, van, bus, motorcycle, three_wheeler, bicycle, other, person, ignore_region); khi bàn giao: <<Điền v1.0 hoặc v1.1 sau Calibration>>.

---

## 2. Phân công và đồng thuận trước calibration

- Lượt hoàn thành / được giao: <<Điền sau khi cả nhóm nộp đủ nhãn, ví dụ 120/120 lượt gán>>
- Số cặp box ghép, IoU TB, đồng thuận lớp và mẫu số: <<Điền từ submission/qc/iaa_summary.md>>
- Box chưa ghép, loại do ignore, bất đồng vùng ignore: <<Điền từ submission/qc/iaa_summary.md>>
- Ca hai người có thể cùng sai sau khi đối chiếu tham chiếu: img_020.jpg (hình phản chiếu qua gương chiếu hậu: kiểm tra xem có ai cùng vẽ box car không), img_017.jpg (tượng người: kiểm tra xem có ai cùng vẽ person không).

---

## 3. Calibration và kiểm lại

- Ca đã xử lý, rule ID, bản sửa và người xác nhận: Dẫn chiếu toàn bộ các ca trong submission/qc/calibration_decisions.csv kèm Rule ID (R-01 đến R-17), người chốt và kết quả kiểm lại.
- Tác động v1.1 lên nhãn và ảnh: <<Phạm vi ảnh hoặc lô sau khi cập nhật guideline v1.1>>.
- Tham chiếu bằng chứng khi Rework: <<Ghi vết vòng QC nếu có Rework>>.

---

## 4. Kết quả duyệt

- Vòng QC: 1
- Người review và ngày: 999 (hoặc Nguyễn Văn Hùng), 2026-11-17
- Đã duyệt / cả lô: 40/40 ảnh (duyệt toàn bộ lô)
- Ảnh lỗi / ảnh đã duyệt: <<Điền từ qc_report.py --round 1>>
- Annotation đối tượng hiện có bị lỗi / annotation đối tượng đã duyệt: <<Điền từ qc_report.py --round 1>>
- Vật bỏ sót, ảnh và vùng: <<Điền từ phiếu review round-01>>
- Ca khó / phần còn lại, lỗi lặp và ví dụ: <<Dẫn phiếu submission/qc/reviews/round-01/qc_review.csv>>
- Một lỗi máy chặn được và một lỗi cần người đọc ảnh: Máy chặn được lỗi kích thước box < 20px, lỗi ngoài taxonomy, box vượt mép ảnh; Người đọc ảnh phát hiện được lỗi vẽ box lên hình phản chiếu gương (img_020.jpg) hoặc bỏ sót người lái xe máy.

---

## 5. Quyết định bàn giao

- Quyết định: <<Release / Hold / Rework>>
- Lý do, người nhận và phạm vi sử dụng: <<Ghi lý do dựa trên tỷ lệ lỗi <= 2% và chất lượng lô dữ liệu>>.
- Nếu còn việc: <<Ghi việc còn tồn đọng nếu có>>.
- Kiểm ngược từ báo cáo tới ảnh, rule và nhãn: <<Mã ca, đường dẫn ảnh, rule ID và kết quả kiểm chứng>>.
