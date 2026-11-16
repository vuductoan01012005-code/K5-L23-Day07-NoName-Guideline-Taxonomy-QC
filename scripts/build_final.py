"""Gộp nhãn sau calibration, xác thực phạm vi và ghi hồ sơ bàn giao máy đọc được."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from calibration import (CALIBRATION_CONTEXT_PATH, GUIDELINE_CHANGE_PATH, calibration_export_path,
                         calibration_scope, require_iaa)
from common import (FINAL_GUIDELINE_PATH, IMAGES_DIR, QC_DIR, ROOT, build_coco, digest, die,
                    final_taxonomy_path, make_ann, read_csv, rel, require_valid_labels, write_csv, xyxy_to_xywh)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--calibrated", type=Path,
                        help="COCO sau sửa có đúng tên phiên bản do prepare_calibration.py in ra.")
    args = parser.parse_args()
    try:
        require_iaa()
    except (OSError, ValueError) as exc:
        die(str(exc))
    prior, tax, scope, batch = calibration_scope()
    consensus = require_valid_labels(QC_DIR / "consensus_draft.json", prior)
    if set(consensus.images) != batch:
        die("Ảnh đồng thuận không khớp lô đã phân công.")
    corrected = None
    if scope:
        expected = calibration_export_path(scope)
        corrected_path = (args.calibrated or expected).resolve()
        if not corrected_path.is_relative_to(QC_DIR.resolve()) or corrected_path.name != expected.name:
            die(f"COCO sau sửa không khớp phiên bản hiện tại. Dùng {rel(expected)}.")
        if not corrected_path.is_file():
            die(f"Thiếu COCO sau sửa: {rel(expected)}. Chạy prepare_calibration.py để xem phạm vi.")
        corrected = require_valid_labels(corrected_path, tax)
        if set(corrected.images) != scope:
            die(f"COCO sau sửa thiếu {sorted(scope - corrected.images.keys())}, "
                f"thừa {sorted(corrected.images.keys() - scope)}.")

    images, annotations, rows = [], [], []
    for image_id, image in enumerate(sorted(batch), 1):
        source = corrected if image in scope else consensus
        width, height = source.images[image]
        images.append({"id": image_id, "file_name": image, "width": width, "height": height})
        for obj in source.objects[image]:
            if obj.cls not in tax.classes:
                die(f"{image} #{obj.id}: lớp cũ '{obj.cls}' chưa được xử lý.")
            annotations.append(make_ann(tax, len(annotations) + 1, image_id, obj.cls, obj.box, obj.attrs))
            if obj.cls != tax.ignore:
                x, y, w, h = xyxy_to_xywh(obj.box)
                rows.append({"image": image, "class": obj.cls, "x": x, "y": y, "w": w, "h": h,
                             **{name: obj.attrs[name] for name in tax.attrs if name != "can_review"},
                             "nguon": "calibration" if image in scope else "consensus"})

    attribution = ROOT / "data" / "ATTRIBUTION.csv"
    records = read_csv(attribution)
    sources = {row["file"]: row for row in records if row["file"] in batch}
    if len(sources) != len(batch) or any(
        not source.get(key) for source in sources.values() for key in ("author", "license", "source_url")
    ):
        die("ATTRIBUTION.csv thiếu thông tin nguồn cho ảnh trong lô.")
    source_hashes = {image: digest(IMAGES_DIR / image) for image in batch}
    label_path = QC_DIR / "labels_calibrated.json"
    data = build_coco(tax, images, annotations, {"description": "Nhãn lô thực hành Day 07", "taxonomy": tax.version})
    label_path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf8")
    write_csv(QC_DIR / "labels_calibrated.csv",
              ["image", "class", "x", "y", "w", "h", *[key for key in tax.attrs if key != "can_review"], "nguon"],
              rows)

    inputs = [
        QC_DIR / "assignment.csv", QC_DIR / "iaa_summary.json", QC_DIR / "calibration_decisions.csv", CALIBRATION_CONTEXT_PATH,
        FINAL_GUIDELINE_PATH, GUIDELINE_CHANGE_PATH, final_taxonomy_path(), attribution,
    ]
    if corrected:
        inputs.append(corrected_path)
    manifest = {
        "intended_use": "Thực hành đặc tả và QC nhãn 2D trong Day 07.",
        "limitations": "Tập ảnh tuyển chọn để luyện ca biên; độ đại diện cho dữ liệu vận hành chưa được đánh giá.",
        "format": "COCO 1.0 bbox góc trên trái [x, y, w, h] theo pixel",
        "taxonomy_version": tax.version,
        "taxonomy": rel(final_taxonomy_path()),
        "guideline": rel(FINAL_GUIDELINE_PATH),
        "labels": {"path": rel(label_path), "sha256": digest(label_path)},
        "inputs_sha256": {rel(path.resolve()): digest(path) for path in inputs},
        "csv_sha256": digest(QC_DIR / "labels_calibrated.csv"),
        "images": [{"file": image, "sha256": source_hashes[image], "source": sources[image]}
                   for image in sorted(batch)],
    }
    manifest_path = QC_DIR / "batch_manifest.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf8")
    print(f"Đã gộp {len(images)} ảnh, {len(annotations)} annotation. Bước tiếp: python scripts/qc_sample.py.")


if __name__ == "__main__":
    main()
