"""Vẽ chồng box của các người gán (mỗi người một màu) để xem ảnh bất đồng.

    python scripts/viz_disagreement.py --images flagged            # mọi ảnh bị cờ (mặc định)
    python scripts/viz_disagreement.py --images img_003.jpg img_010.jpg
    python scripts/viz_disagreement.py --images all --source consensus

Kết quả: work/viz/<ảnh>.png và work/viz/_overview.png (thư mục work/ không bị commit).
--source labels (mặc định): nhãn từng người; consensus: bản đồng thuận nháp; final: labels_calibrated.json
"""
from __future__ import annotations

import argparse

from PIL import Image

from common import (IMAGES_DIR, QC_DIR, WORK_DIR, annotators_of_image, die, list_images, load_all_labels,
                    final_taxonomy_path, load_assignment, load_coco, load_taxonomy, read_flagged, rel)
from drawing import PALETTE, draw_layers


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--images", nargs="+", default=["flagged"],
                    help="'flagged' | 'all' | danh sách tên ảnh (VD: img_003.jpg)")
    ap.add_argument("--source", choices=["labels", "consensus", "final"], default="labels")
    args = ap.parse_args()
    tax = load_taxonomy(final_taxonomy_path()) if args.source == "final" else load_taxonomy()

    if args.images == ["flagged"]:
        if not (QC_DIR / "flagged_images.txt").is_file():
            die("Chưa có flagged_images.txt. Chạy python scripts/qc_compare.py trước.")
        names = read_flagged()
        if not names:
            print("Không có ảnh bị cờ. Dùng --images img_017.jpg để xem ca tham chiếu nếu ảnh thuộc lô.")
            return
    elif args.images == ["all"]:
        names = list_images()
    else:
        names = args.images

    if args.source == "labels":
        files = load_all_labels(tax)
        assignment = load_assignment()
    else:
        p = QC_DIR / ("consensus_draft.json" if args.source == "consensus" else "labels_calibrated.json")
        if not p.exists():
            die(f"Chưa có {rel(p)}. Chạy bước trước đó của pipeline (xem scripts/README.md).")
        one = load_coco(p, tax)

    out = WORK_DIR / "viz"
    out.mkdir(parents=True, exist_ok=True)
    made = []
    for img in names:
        src = IMAGES_DIR / img
        if not src.exists():
            print(f"  bỏ qua {img}: không có trong data/images/")
            continue
        if args.source == "labels":
            layers = [(m, PALETTE[i % len(PALETTE)], files[m].objects[img])
                      for i, m in enumerate(annotators_of_image(files, img, assignment))]
        else:
            layers = [(args.source, PALETTE[0], one.objects.get(img, []))]
        if not layers:
            print(f"  bỏ qua {img}: không có nhãn")
            continue
        im = draw_layers(src, layers, tax, show_id=(args.source != "labels"), title=img)
        dst = out / (img.rsplit(".", 1)[0] + ".png")
        im.save(dst)
        made.append(dst)
    if made:
        thumbs = []
        for p in made:
            t = Image.open(p)
            t.thumbnail((360, 360))
            thumbs.append(t)
        cols = min(4, len(thumbs))
        rows = (len(thumbs) + cols - 1) // cols
        sheet = Image.new("RGB", (cols * 364, rows * 364), (30, 30, 30))
        for i, t in enumerate(thumbs):
            sheet.paste(t, ((i % cols) * 364 + 2, (i // cols) * 364 + 2))
        sheet.save(out / "_overview.png")
    print(f"Đã vẽ {len(made)} ảnh vào {rel(out)}/ (mở _overview.png để xem tổng quan).")


if __name__ == "__main__":
    main()
