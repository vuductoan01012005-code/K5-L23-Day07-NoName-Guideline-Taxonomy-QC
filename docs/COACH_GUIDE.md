# Chuẩn bị Day 07 cho Lab Coach

## Trước khi mở bài

1. Chuẩn bị kênh nộp riêng, mã thành viên và một lần chạy với nhóm hai người. Dùng cả 40 ảnh để khảo sát guideline, gán và duyệt trọn lô. Ghi thời gian tạo Task, gán, export và review trước khi chốt nhịp lớp.
2. Trên đúng instance CVAT của lớp, thử hai ảnh, một ảnh có box và thuộc tính, một ảnh không có đối tượng theo phạm vi. Export → import vào Task mới → export lại. So lớp, tọa độ, thuộc tính và số ảnh. Thử mở issue cấp vùng ảnh bằng tài khoản reviewer. Dùng CSV nếu tài khoản thiếu quyền Review.
3. Chuẩn bị bộ tham chiếu riêng theo bảng dưới. Coach xem ảnh gốc, chốt quy tắc sử dụng cho ca và ghi chú nếu taxonomy của nhóm dùng phạm vi khác. Nếu dùng COCO tham chiếu, lưu người duyệt, ngày, phiên bản guideline và SHA-256. Chỉ mở sau khi đã thu nhãn độc lập. Bộ ca này phục vụ thảo luận và kiểm chung kết quả học, còn rubric chấm dựa trên bằng chứng của nhóm.

| Ảnh gợi ý | Câu hỏi để coach xác nhận trước khi dạy |
|---|---|
| `img_017.jpg` | Xác nhận vùng tượng người cưỡi ngựa. Nếu guideline chỉ gán người thật, hai annotator cùng vẽ `person` ở vùng này vẫn cần sửa dù IAA cao. |
| `img_005.jpg`, `img_026.jpg` | So người và xe khi bị che/cắt mép với góc nhìn khác. Chốt số box, cách phân lớp và vẽ phần nhìn thấy theo mục đích của nhóm. |
| `img_002.jpg` | Chốt riêng phạm vi xe chở và xe được chở. Yêu cầu người học chỉ ra ảnh khác có thể bị ảnh hưởng nếu đổi quy tắc. |

Người mới có thể làm thêm một ca có hướng dẫn, chẳng hạn soi kỹ một ảnh đường phố chưa nằm trong bảng trên. Nhóm làm nhanh có thể giải thích một ca bỏ sót không ảnh hưởng IoU trung bình trên box đã ghép, hoặc so vòng lấy mẫu demo với duyệt toàn lô.

## Tài liệu đối chiếu

- Dùng ISO/IEC 5259 để thảo luận cách ghi số đo, truy vết và kiểm lại sau thay đổi. NIST AI RMF giúp đặt bối cảnh mục đích sử dụng, dữ liệu và giới hạn. Tiêu chí trong lab dành cho lớp học. [ISO/IEC 5259-2](https://www.iso.org/standard/81860.html) · [ISO/IEC 5259-3](https://webstore.iec.ch/en/publication/96734) · [ISO/IEC 5259-4](https://www.iso.org/standard/81093.html) · [ISO/IEC 5259-5](https://www.iso.org/standard/5259-5) · [NIST AI RMF](https://airc.nist.gov/airmf-resources/playbook/)
- Đối chiếu ca người đi xe máy với quy ước 2D của Waymo. Thử đổi COCO `[10,20,40,60]` sang OpenLABEL `[30,50,40,60]` để thấy điểm gốc của box. Manifest trong lab ghi phiên bản và checksum, có thể dùng Croissant 1.1 khi dạy mở rộng về metadata. [Waymo](https://github.com/waymo-research/waymo-open-dataset/blob/master/docs/labeling_specifications.md#2d-labeling-specifications) · [OpenLABEL](https://www.asam.net/fileadmin/Standards/OpenLABEL/ASAM_OpenLABEL_BS_V1-0-0.html) · [Croissant 1.1](https://docs.mlcommons.org/croissant/docs/croissant-spec-1.1.html)
- Khi sang Day 08, coach có thể chạy Grounding DINO trước để người học review box, lưu phiên bản, prompt và ngưỡng. FiftyOne phù hợp để demo ưu tiên ca nghi sai từ dự đoán. SAM 3/3.1 phù hợp với buổi mở rộng có mục tiêu mask hoặc theo dõi đối tượng. [Grounding DINO](https://github.com/IDEA-Research/GroundingDINO) · [FiftyOne](https://docs.voxel51.com/api/fiftyone.brain.html#fiftyone.brain.compute_mistakenness) · [SAM 3/3.1](https://ai.meta.com/blog/segment-anything-model-3/)
