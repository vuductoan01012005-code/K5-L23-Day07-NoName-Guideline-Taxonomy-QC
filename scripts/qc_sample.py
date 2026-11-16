"""Tạo phiếu QC cho một vòng mới. Mặc định duyệt toàn bộ lô."""
from __future__ import annotations

import argparse
import json
import random
import shutil
from pathlib import Path
from tempfile import TemporaryDirectory

from common import IMAGES_DIR, QC_DIR, WORK_DIR, digest, die, read_flagged, rel, write_csv
from drawing import PALETTE, draw_layers
from review_evidence import LABELS_PATH, MANIFEST_PATH, REVIEW_COLUMNS, SAMPLE_COLUMNS, current_batch, round_dir


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--round", type=int, default=1, help="Số vòng QC, bắt đầu từ 1.")
    parser.add_argument("--n", type=int, help="Demo lấy thêm n ảnh ngẫu nhiên ngoài ca bị cờ.")
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()
    if args.round < 1 or (args.n is not None and args.n < 1):
        parser.error("--round và --n phải là số nguyên dương.")
    directory = round_dir(args.round)
    if directory.exists():
        die(f"{rel(directory)} đã tồn tại. Dùng vòng mới để giữ nguyên kết quả cũ.")
    try:
        tax, labels = current_batch()
    except (OSError, ValueError, KeyError) as exc:
        die(f"Chưa thể mở vòng QC: {exc}")

    flagged = set(read_flagged()) & labels.images.keys()
    pool = sorted(labels.images.keys() - flagged)
    remaining = pool if args.n is None else random.Random(args.seed).sample(pool, min(args.n, len(pool)))
    groups = {image: "ca_kho" for image in flagged}
    groups.update({image: "con_lai" if args.n is None else "ngau_nhien" for image in remaining})
    images = sorted(groups)
    counts = {image: sum(obj.cls != tax.ignore for obj in labels.objects[image]) for image in images}
    out = WORK_DIR / "review" / directory.name
    try:
        out.mkdir(parents=True, exist_ok=True)
        for image in images:
            layer = ("final", PALETTE[1], labels.objects[image])
            draw_layers(IMAGES_DIR / image, [layer], tax, show_id=True, title=image).save(out / f"{image}.png")

        directory.parent.mkdir(parents=True, exist_ok=True)
        with TemporaryDirectory(dir=directory.parent) as temporary:
            staging = Path(temporary)
            sample_path = staging / "qc_sample.csv"
            write_csv(sample_path, SAMPLE_COLUMNS, [
                {"image": image, "group": groups[image], "so_doi_tuong": counts[image]} for image in images
            ])
            write_csv(staging / "qc_review.csv", REVIEW_COLUMNS, [{"image": image} for image in images])
            shutil.copyfile(LABELS_PATH, staging / "labels_snapshot.json")
            shutil.copyfile(MANIFEST_PATH, staging / "batch_manifest_snapshot.json")
            decisions = QC_DIR / "calibration_decisions.csv"
            shutil.copyfile(decisions, staging / "calibration_decisions_snapshot.csv")
            metadata = {
                "round": args.round, "mode": "full" if args.n is None else "demo",
                "seed": None if args.n is None else args.seed,
                "labels_sha256": digest(staging / "labels_snapshot.json"),
                "batch_manifest_sha256": digest(staging / "batch_manifest_snapshot.json"),
                "sample_sha256": digest(sample_path),
                "calibration_decisions_sha256": digest(staging / "calibration_decisions_snapshot.csv"),
            }
            (staging / "review_manifest.json").write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")
            staging.rename(directory)
    except OSError as exc:
        die(f"Chưa thể tạo vòng QC {args.round}: {exc}")
    print(f"Vòng {args.round}: {len(images)}/{len(labels.images)} ảnh. Phiếu: {rel(directory / 'qc_review.csv')}.")
    print(f"Đối chiếu ảnh tại {rel(out)} rồi chạy python scripts/qc_report.py --round {args.round}.")


if __name__ == "__main__":
    main()
