"""Bằng chứng đầu vào và phạm vi ảnh cần sửa theo quyết định calibration."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from common import (FINAL_GUIDELINE_PATH, QC_DIR, ROOT, digest, die, final_taxonomy_path,
                    input_hashes, load_taxonomy, read_csv, read_flagged, require_assignment, write_csv)

CALIBRATION_CONTEXT_PATH = QC_DIR / "calibration_context.json"
GUIDELINE_CHANGE_PATH = ROOT / "submission" / "guideline_change.json"

DECISION_COLUMNS = [
    "case_id", "image", "quyet_dinh", "quy_tac_ghi_vao_guideline",
    "phien_ban_guideline", "nguoi_chot", "phieu_sua", "kiem_lai", "pham_vi",
]


def calibration_export_path(scope) -> Path:
    """Derive the handoff filename from the inputs reviewed for this correction."""
    inputs = {
        "iaa": digest(QC_DIR / "iaa_summary.json"),
        "decisions": digest(QC_DIR / "calibration_decisions.csv"),
        "guideline": digest(FINAL_GUIDELINE_PATH),
        "guideline_change": digest(GUIDELINE_CHANGE_PATH),
        "taxonomy": digest(final_taxonomy_path()),
        "images": sorted(scope),
    }
    revision = hashlib.sha256(json.dumps(inputs, sort_keys=True).encode("utf-8")).hexdigest()[:16]
    return QC_DIR / f"labels_calibrated_{revision}.json"


def require_iaa() -> dict:
    source = QC_DIR / "iaa_summary.json"
    if not source.is_file():
        raise ValueError("Thiếu iaa_summary.json. Chạy qc_compare.py trước.")
    summary = json.loads(source.read_text(encoding="utf-8"))
    if summary.get("inputs") != input_hashes():
        raise ValueError("Đầu vào IAA đã thay đổi. Khôi phục bản đã khóa hoặc chạy lại qc_compare.py.")
    for name in ("consensus_draft.json", "flagged_images.txt", "calibration_candidates.csv"):
        artifact = QC_DIR / name
        if not artifact.is_file() or summary.get("artifacts", {}).get(name) != digest(artifact):
            raise ValueError(f"Thiếu hoặc đã thay đổi: {name}. Chạy lại qc_compare.py.")
    return summary


def calibration_scope():
    original = load_taxonomy()
    final = load_taxonomy(final_taxonomy_path())
    if final.raw != original.raw and final.version == original.version:
        die("Đổi taxonomy cần phiên bản mới.")
    semantic_change = any(
        original.raw[key] != final.raw[key] for key in ("classes", "attributes", "ignore_class")
    )
    batch = set(require_assignment())
    flagged = set(read_flagged())
    candidates = read_csv(QC_DIR / "calibration_candidates.csv")
    decisions_file = QC_DIR / "calibration_decisions.csv"
    context = {"iaa_summary_sha256": digest(QC_DIR / "iaa_summary.json")}
    if not decisions_file.exists():
        CALIBRATION_CONTEXT_PATH.write_text(json.dumps(context, indent=2) + "\n", encoding="utf-8")
        write_csv(decisions_file, DECISION_COLUMNS, [
            {"case_id": row["case_id"], "image": row["image"], "pham_vi": "anh"}
            for row in candidates
        ])
    try:
        recorded_context = json.loads(CALIBRATION_CONTEXT_PATH.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        recorded_context = None
    if recorded_context != context:
        die("IAA đã đổi so với bảng quyết định. Lưu bản cũ ra chỗ khác, tạo lại bảng và rà các ca mới.")
    try:
        change = json.loads(GUIDELINE_CHANGE_PATH.read_text(encoding="utf-8"))
        if change["kind"] not in {"editorial", "semantic"} or not change["summary"].strip():
            raise ValueError("Cần kind editorial/semantic và summary giải thích.")
    except (OSError, ValueError, KeyError, TypeError, AttributeError) as exc:
        die(f"guideline_change.json: {exc}")
    decisions = read_csv(decisions_file)
    errors = []
    candidate_ids = {row["case_id"]: row["image"] for row in candidates}
    closed = set()
    seen = set()
    scope = set(flagged)
    for row in decisions:
        case = (row.get("case_id") or "").strip()
        image = (row.get("image") or "").strip()
        impact = (row.get("pham_vi") or "").strip()
        required = DECISION_COLUMNS[:-1]
        if (
            not all((row.get(key) or "").strip() for key in required)
            or not case or case in seen or image not in batch
            or impact not in {"anh", "lo"}
        ):
            errors.append(f"{case or image}: điền đủ trường, ID duy nhất, ảnh trong lô, phạm vi anh hoặc lo.")
            continue
        if case in candidate_ids and candidate_ids[case] != image:
            errors.append(f"{case}: ảnh không khớp với ca IAA.")
            continue
        seen.add(case)
        if impact == "lo":
            scope.update(batch)
        else:
            scope.add(image)
        if case in candidate_ids:
            closed.add(case)
    missing_cases = sorted(set(candidate_ids) - closed)
    if missing_cases:
        errors.append("Ca IAA chưa xác nhận: " + ", ".join(missing_cases))
    if semantic_change or change["kind"] == "semantic":
        scope.update(batch)
        if not any(row.get("pham_vi") == "lo" for row in decisions):
            errors.append("Đổi nghĩa guideline/taxonomy cần quyết định phạm vi lo, mô tả tác động và kiểm lại cả lô.")
    if not FINAL_GUIDELINE_PATH.is_file():
        errors.append("Thiếu guideline_v1.1_calibrated.md.")
    if errors:
        die("Hoàn thiện calibration_decisions.csv và guideline:\n" + "\n".join(errors))
    return original, final, scope, batch
