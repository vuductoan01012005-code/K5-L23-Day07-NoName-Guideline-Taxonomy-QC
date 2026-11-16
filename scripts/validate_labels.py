"""Kiểm cấu trúc, ảnh được giao, lớp, thuộc tính và bbox của COCO trước khi nộp."""
from __future__ import annotations

import argparse
from pathlib import Path

from common import MEMBER_RE, die, list_label_files, load_taxonomy, rel, require_assignment, require_valid_labels

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("files", nargs="*", type=Path)
    parser.add_argument("--all", action="store_true")
    args = parser.parse_args()
    paths = args.files or (list_label_files() if args.all else [])
    if not paths:
        parser.error("Truyền file COCO hoặc dùng --all.")
    assignment = require_assignment()
    tax = load_taxonomy()
    for path in paths:
        if path.suffix != ".json" or not MEMBER_RE.fullmatch(path.stem):
            die("Đặt file theo mã thành viên, ví dụ 101.json.")
        labels = require_valid_labels(path, tax)
        expected = {image for image, members in assignment.items() if labels.member in members}
        if not expected or expected != labels.images.keys():
            die(f"{rel(path.resolve())}: ảnh thiếu {sorted(expected - labels.images.keys())}, "
                f"ảnh thừa {sorted(labels.images.keys() - expected)}.")
        print(f"{rel(path.resolve())}: hợp lệ về cấu trúc, {len(expected)} ảnh.")
        for image, objects in labels.objects.items():
            for obj in objects:
                if obj.cls != tax.ignore and obj.box[3] - obj.box[1] < tax.rules["min_box_height_px"]:
                    print(f"[WARN] {image} #{obj.id}: rà lại quy tắc vật nhỏ.")
    print("Reviewer kiểm box có đúng vật, đúng lớp, ôm sát và có bỏ sót hay không.")


if __name__ == "__main__":
    main()
