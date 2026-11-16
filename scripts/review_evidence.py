"""Kiểm bằng chứng và tạo đường dẫn dùng chung cho mỗi vòng duyệt."""
from __future__ import annotations

import json
from pathlib import Path

from calibration import require_iaa
from common import IMAGES_DIR, QC_DIR, ROOT, digest, final_taxonomy_path, load_taxonomy, rel, require_valid_labels

LABELS_PATH = QC_DIR / "labels_calibrated.json"
MANIFEST_PATH = QC_DIR / "batch_manifest.json"
REVIEW_COLUMNS = ["image", "object_id", "error_type", "reviewer", "rule_id", "region", "note"]
SAMPLE_COLUMNS = ["image", "group", "so_doi_tuong"]


def round_dir(number: int) -> Path:
    return QC_DIR / "reviews" / f"round-{number:02d}"


def current_batch():
    require_iaa()
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    taxonomy = final_taxonomy_path()
    tax = load_taxonomy(taxonomy)
    if manifest["taxonomy"] != rel(taxonomy) or manifest["taxonomy_version"] != tax.version:
        raise ValueError("Taxonomy hiện tại lệch hồ sơ bàn giao. Chạy build_final.py.")
    labels = require_valid_labels(LABELS_PATH, tax)
    if manifest["labels"]["sha256"] != digest(LABELS_PATH):
        raise ValueError("Nhãn cuối lệch batch_manifest.json. Chạy build_final.py.")
    if manifest["csv_sha256"] != digest(QC_DIR / "labels_calibrated.csv"):
        raise ValueError("CSV nhãn cuối lệch batch_manifest.json. Chạy build_final.py.")
    for name, expected in manifest["inputs_sha256"].items():
        path = ROOT / name
        if not path.is_file() or digest(path) != expected:
            raise ValueError(f"Đầu vào lô thiếu hoặc đã đổi: {name}. Chạy build_final.py.")
    entries = {entry["file"]: entry["sha256"] for entry in manifest["images"]}
    if entries.keys() != labels.images.keys() or any(
        digest(IMAGES_DIR / name) != expected for name, expected in entries.items()
    ):
        raise ValueError("Ảnh lô không khớp batch_manifest.json.")
    return tax, labels
