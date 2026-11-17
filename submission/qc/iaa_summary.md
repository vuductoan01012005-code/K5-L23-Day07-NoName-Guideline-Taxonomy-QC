# Tóm tắt IAA (taxonomy v1.0)

- Ảnh được so sánh (có >=2 người gán): **40**; số người gán: 5
- Lượt gán đủ **120/120**.
- IoU trung bình và % cùng lớp **chỉ tính trên các cặp box đã ghép** (IoU >= 0.5, ghép 1-1 không phân biệt lớp). Box chưa ghép được thống kê riêng ở cột bỏ sót/thừa.
- Mẫu số: 822 cặp box ghép (tổng mọi cặp người gán, ảnh chung).

| Cặp | Ảnh | Cặp box ghép | IoU TB | Cùng lớp | Cùng occluded_level | Cùng truncated | Chưa ghép (A/B) | Bỏ qua do ignore | Đạt IAA |
|---|---|---|---|---|---|---|---|---|---|
| **TỔNG** | 120 | 822 | 0.832 | 94.3% | 47.1% | 91.4% | 202/272 | 2 | CHƯA ĐẠT |
| 995|996 | 13 | 76 | 0.868 | 94.7% | 60.5% | 92.1% | 8/46 | 0 | CHƯA ĐẠT |
| 995|997 | 12 | 97 | 0.827 | 96.9% | 48.5% | 88.7% | 13/56 | 0 | CHƯA ĐẠT |
| 995|998 | 12 | 81 | 0.827 | 96.3% | 48.1% | 90.1% | 16/35 | 0 | CHƯA ĐẠT |
| 995|999 | 11 | 59 | 0.873 | 96.6% | 30.5% | 88.1% | 8/35 | 0 | ĐẠT |
| 996|997 | 13 | 114 | 0.821 | 97.4% | 62.3% | 97.4% | 29/26 | 0 | CHƯA ĐẠT |
| 996|998 | 11 | 72 | 0.785 | 94.4% | 44.4% | 94.4% | 21/10 | 0 | CHƯA ĐẠT |
| 996|999 | 11 | 65 | 0.821 | 93.8% | 32.3% | 98.5% | 11/11 | 0 | CHƯA ĐẠT |
| 997|998 | 11 | 71 | 0.803 | 87.3% | 52.1% | 90.1% | 49/14 | 2 | CHƯA ĐẠT |
| 997|999 | 12 | 80 | 0.842 | 91.2% | 40.0% | 86.2% | 34/13 | 0 | CHƯA ĐẠT |
| 998|999 | 14 | 107 | 0.852 | 92.5% | 41.1% | 87.9% | 13/26 | 0 | CHƯA ĐẠT |

Ngưỡng IAA: IoU TB >= 0.85, đồng thuận lớp >= 95%.

Số ca bất thường: 1446 ({'bo_sot_thua': 429, 'co_can_review': 62, 'iou_thap': 329, 'sai_lop': 47, 'sai_thuoc_tinh': 470, 'bat_dong_ignore': 109}), trên 35 ảnh cần calibration.
