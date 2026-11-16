"""Tạo gói CVAT cho đúng phạm vi sửa và in tên ảnh cần kiểm lại."""
from __future__ import annotations

import json
from pathlib import Path
import shutil

from calibration import calibration_export_path, calibration_scope, require_iaa
from common import IMAGES_DIR, QC_DIR, WORK_DIR, digest, die, final_taxonomy_path, rel
from review_evidence import LABELS_PATH, MANIFEST_PATH


def draft_source(prior, final):
    if LABELS_PATH.is_file() and MANIFEST_PATH.is_file():
        manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        taxonomy = final_taxonomy_path()
        if (
            manifest.get("labels", {}).get("sha256") == digest(LABELS_PATH)
            and manifest.get("inputs_sha256", {}).get(rel(taxonomy)) == digest(taxonomy)
        ):
            return LABELS_PATH
    if prior.classes == final.classes and prior.attrs == final.attrs:
        return QC_DIR / "consensus_draft.json"
    return None


def main() -> None:
    try:
        require_iaa()
    except (OSError, ValueError) as exc:
        die(str(exc))
    prior, final, scope, _ = calibration_scope()
    if not scope:
        print("Không cần sửa ảnh. Chạy python scripts/build_final.py.")
        return
    out = WORK_DIR / "calib"
    images = out / "images"
    images.mkdir(parents=True, exist_ok=True)
    for stale in images.iterdir():
        if stale.is_file() and stale.name not in scope:
            stale.unlink()
    for name in sorted(scope):
        shutil.copy2(IMAGES_DIR / name, images / name)
    output = out / "consensus_flagged.json"
    source = draft_source(prior, final)
    if source is None:
        output.unlink(missing_ok=True)
        print("Schema lớp/thuộc tính đã đổi. Tạo task với taxonomy mới, rồi áp dụng mapping đã ghi.")
    else:
        draft = json.loads(source.read_text(encoding="utf-8"))
        draft["images"] = [image for image in draft["images"] if Path(image["file_name"]).name in scope]
        keep = {image["id"] for image in draft["images"]}
        draft["annotations"] = [annotation for annotation in draft["annotations"] if annotation["image_id"] in keep]
        for annotation in draft["annotations"]:
            annotation["attributes"].pop("needs_calibration", None)
        output.write_text(json.dumps(draft, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print("Có thể nạp nhãn nháp từ work/calib/consensus_flagged.json.")
    print(f"Đã chuẩn bị {len(scope)} ảnh ở work/calib/images/.")
    print(f"COCO sau sửa: {rel(calibration_export_path(scope))}")


if __name__ == "__main__":
    main()
