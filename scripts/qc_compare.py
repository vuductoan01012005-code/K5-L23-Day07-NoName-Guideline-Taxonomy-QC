"""So sánh nhãn của các người gán độc lập: đo IAA, tìm ca bất thường cần calibration, dựng bản đồng thuận nháp.

    python scripts/qc_compare.py

Đầu ra (submission/qc/): iaa_summary.json/.md, calibration_candidates.csv, image_scores.csv,
consensus_draft.json, flagged_images.txt.
"""
from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from itertools import combinations

from common import (QC_DIR, Taxonomy, build_coco, cluster_objects, covered_by, digest, die, input_hashes, iou,
                    iou_threshold, label_errors, load_all_labels, load_taxonomy, make_ann, match_boxes,
                    mean_box, read_csv, rel, require_assignment, write_csv, xyxy_to_xywh)

ISSUE_WEIGHT = {"bo_sot_thua": 2, "sai_lop": 2, "iou_thap": 1, "sai_thuoc_tinh": 1, "co_can_review": 1,
                "bat_dong_ignore": 1, "can_review_anh": 1}
CAND_COLS = ["case_id", "image", "issue_type", "annotators", "class_a", "class_b", "box_a", "box_b", "iou",
             "ghi_chu_tu_dong"]


def fmt_box(b) -> str:
    return "" if b is None else "[" + ",".join(f"{v:.0f}" for v in xyxy_to_xywh(b)) + "]"  # x,y,w,h


def pair_stats() -> dict:
    return {"images": 0, "matched": 0, "sum_iou": 0.0, "same_class": 0, "same_attr": Counter(),
            "unmatched_a": 0, "unmatched_b": 0, "skipped_ignore": 0, "below_thr": 0, "objects_a": 0, "objects_b": 0}


def finalize(st: dict, tax: Taxonomy) -> dict:
    n = st["matched"]
    r = tax.rules
    mi = st["sum_iou"] / n if n else None
    ca = st["same_class"] / n if n else None
    out = {
        "n_images": st["images"], "n_matched_pairs": n,
        "n_unmatched_a": st["unmatched_a"], "n_unmatched_b": st["unmatched_b"],
        "n_skipped_in_ignore": st["skipped_ignore"],
        "mean_iou": mi, "class_agreement": ca,
        "attr_agreement": {a: (st["same_attr"][a] / n if n else None) for a in tax.attrs if a != "can_review"},
        "n_below_iou_thr": st["below_thr"],
        "iou_pass": None if mi is None else mi >= r["iaa_iou"],
        "class_pass": None if ca is None else ca >= r["iaa_class"],
    }
    out["pass"] = None if not n else out["iou_pass"] and out["class_pass"]
    return out


def pct(v) -> str:
    return "n/a" if v is None else f"{v * 100:.1f}%"


def main() -> None:
    argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter).parse_args()
    tax = load_taxonomy()
    r = tax.rules
    files = load_all_labels(tax)
    assignment = require_assignment()
    check_attrs = [a for a in tax.attrs if a != "can_review"]
    expected = {(image, member) for image, members in assignment.items() for member in members}
    actual = {(image, member) for member, labels in files.items() for image in labels.images}
    missing = sorted(expected - actual)
    extra = sorted(actual - expected)
    validation_errors = [f"{member}: {error}" for member, labels in files.items()
                         for error in label_errors(labels, tax)]
    if missing or extra or validation_errors:
        die(f"Lượt gán thiếu: {missing}; lượt gán ngoài phân công: {extra}.\n"
            + "\n".join(validation_errors))
    images = sorted(assignment)
    try:
        hashes = input_hashes()
    except ValueError as exc:
        die(str(exc))
    issues, per_pair, total = [], defaultdict(pair_stats), pair_stats()
    for img in images:
        anns = sorted(assignment[img])
        for a, b in combinations(anns, 2):
            key = f"{a}|{b}"
            oa = [o for o in files[a].objects[img] if o.cls != tax.ignore]
            ob = [o for o in files[b].objects[img] if o.cls != tax.ignore]
            ignore_a = [o for o in files[a].objects[img] if o.cls == tax.ignore]
            ignore_b = [o for o in files[b].objects[img] if o.cls == tax.ignore]
            ia = [o.box for o in ignore_a]
            ib = [o.box for o in ignore_b]
            _, missing_a, missing_b = match_boxes(ignore_a, ignore_b, r["match_iou"])
            for side, unmatched_regions in (("a", missing_a), ("b", missing_b)):
                for region in unmatched_regions:
                    issues.append({"image": img, "annotators": key, "issue_type": "bat_dong_ignore",
                                   f"box_{side}": fmt_box(region.box),
                                   "ghi_chu_tu_dong": "Vùng ignore không ghép được với vùng của người kia."})
            pairs, ua, ub = match_boxes(oa, ob, r["match_iou"])
            for st in (per_pair[key], total):
                st["images"] += 1
                st["objects_a"] += len(oa)
                st["objects_b"] += len(ob)
                st["matched"] += len(pairs)
            for x, y, v in pairs:
                same_cls = x.cls == y.cls
                thr = iou_threshold(tax, x.box, y.box)
                diff_attrs = [n for n in check_attrs if x.attrs[n] != y.attrs[n]]
                for st in (per_pair[key], total):
                    st["sum_iou"] += v
                    st["same_class"] += same_cls
                    for n in check_attrs:
                        st["same_attr"][n] += x.attrs[n] == y.attrs[n]
                    st["below_thr"] += v < thr
                base = {"image": img, "annotators": key, "class_a": x.cls, "class_b": y.cls,
                        "box_a": fmt_box(x.box), "box_b": fmt_box(y.box), "iou": f"{v:.2f}"}
                if not same_cls:
                    issues.append({**base, "issue_type": "sai_lop",
                                   "ghi_chu_tu_dong": f"{a} gán {x.cls}, {b} gán {y.cls} cho cùng một vật"})
                if v < thr:
                    issues.append({**base, "issue_type": "iou_thap",
                                   "ghi_chu_tu_dong": f"IoU {v:.2f} < ngưỡng {thr} (box lệch/lỏng/thiếu phần vật)"})
                if diff_attrs:
                    d = "; ".join(f"{n}: {a}={x.attrs[n]} vs {b}={y.attrs[n]}" for n in diff_attrs)
                    issues.append({**base, "issue_type": "sai_thuoc_tinh", "ghi_chu_tu_dong": d})
            for side, un, mine_ign, other_ign, who, other in (("a", ua, ia, ib, a, b), ("b", ub, ib, ia, b, a)):
                for o in un:
                    ignored_here = covered_by(o.box, mine_ign)
                    ignored_there = covered_by(o.box, other_ign)
                    if ignored_here and ignored_there:
                        for st in (per_pair[key], total):
                            st["skipped_ignore"] += 1
                        continue
                    for st in (per_pair[key], total):
                        st["unmatched_" + side] += 1
                    asymmetric = ignored_here != ignored_there
                    note = (
                        f"Chỉ vùng ignore của {who if ignored_here else other} phủ box của {who}."
                        if asymmetric else f"Chỉ {who} vẽ {o.cls} này. {other} bỏ sót hoặc {who} vẽ thừa."
                    )
                    issues.append({
                        "image": img, "annotators": key,
                        "issue_type": "bat_dong_ignore" if asymmetric else "bo_sot_thua",
                        f"class_{side}": o.cls, f"box_{side}": fmt_box(o.box),
                        "ghi_chu_tu_dong": note,
                    })
        # ca có cờ can_review (mỗi đối tượng 1 dòng/ảnh)
        for m in anns:
            for o in files[m].objects[img]:
                if o.attrs.get("can_review") == "true":
                    issues.append({"image": img, "annotators": m, "issue_type": "co_can_review", "class_a": o.cls,
                                   "class_b": "", "box_a": fmt_box(o.box), "box_b": "", "iou": "",
                                   "ghi_chu_tu_dong": f"{m} gắn cờ can_review (ca mơ hồ, cần chốt quy tắc)"})

    issue_path = QC_DIR / "image_issues.csv"
    if issue_path.exists():
        for row in read_csv(issue_path):
            img, member = row.get("image"), row.get("annotator")
            region = (row.get("region") or "").strip()
            note = (row.get("note") or "").strip()
            if (img, member) not in expected or not region or not note:
                die("image_issues.csv: mỗi dòng cần ảnh đã giao, mã người gán, vùng ảnh và lý do.")
            issues.append({"image": img, "annotators": member, "issue_type": "can_review_anh",
                           "ghi_chu_tu_dong": f"{region} — {note}"})
    order = {img: i for i, img in enumerate(images)}
    issues.sort(key=lambda x: (order[x["image"]], x["issue_type"], x["annotators"]))
    for i, x in enumerate(issues, 1):
        x["case_id"] = f"C{i:03d}"
    write_csv(QC_DIR / "calibration_candidates.csv", CAND_COLS, issues)

    # ----- điểm theo ảnh
    by_img = defaultdict(list)
    for x in issues:
        by_img[x["image"]].append(x)
    score_rows = []
    for img in images:
        its = by_img.get(img, [])
        sc = sum(ISSUE_WEIGHT[x["issue_type"]] for x in its)
        score_rows.append({"image": img, "n_annotators": len(assignment[img]), "n_issues": len(its),
                           "score": sc, "needs_calibration": "yes" if its else "no"})
    score_rows.sort(key=lambda x: (-x["score"], x["image"]))
    write_csv(QC_DIR / "image_scores.csv", ["image", "n_annotators", "n_issues", "score", "needs_calibration"], score_rows)
    flagged = sorted((x["image"] for x in score_rows if x["needs_calibration"] == "yes"), key=lambda i: order[i])
    (QC_DIR / "flagged_images.txt").write_text("".join(i + "\n" for i in flagged), encoding="utf8")

    # ----- consensus
    cimages, canns, aid = [], [], 1
    for img in images:
        anns = sorted(assignment[img])
        w, h = next(files[m].images[img] for m in anns)
        iid = len(cimages) + 1
        cimages.append({"id": iid, "file_name": img, "width": w, "height": h})
        n, maj = len(anns), len(anns) // 2 + 1
        ign = {m: [o.box for o in files[m].objects[img] if o.cls == tax.ignore] for m in anns}
        objs = {m: [o for o in files[m].objects[img] if o.cls != tax.ignore] for m in anns}
        for cl in cluster_objects(objs, r["match_iou"]):
            box = mean_box([o.box for o in cl.values()])
            missing = [m for m in anns if m not in cl]
            if len(cl) < maj and all(covered_by(box, ign[member]) for member in anns):
                continue
            cls_c = Counter(o.cls for o in cl.values())
            cls = sorted(cls_c.items(), key=lambda t: (-t[1], t[0]))[0][0]
            attrs, need = {}, False
            for nme in tax.attrs:
                c = Counter(o.attrs[nme] for o in cl.values())
                attrs[nme] = sorted(c.items(), key=lambda t: (-t[1], t[0]))[0][0]
                if nme != "can_review" and len(c) > 1:
                    need = True
            if any(o.attrs.get("can_review") == "true" for o in cl.values()):
                attrs["can_review"] = "true"
                need = True
            if len(cls_c) > 1:
                need = True
            if any(not covered_by(box, ign[m]) for m in missing):
                need = True
            bl = [o.box for o in cl.values()]
            if any(iou(p, q) < iou_threshold(tax, p, q) for p, q in combinations(bl, 2)):
                need = True
            if len(cl) < maj:
                need = True
            canns.append(make_ann(tax, aid, iid, cls, box, attrs, {"needs_calibration": need}))
            aid += 1
        # vùng ignore: gom với ngưỡng IoU thấp hơn, giữ cụm đạt đa số
        for cl in cluster_objects({m: [o for o in files[m].objects[img] if o.cls == tax.ignore] for m in anns}, 0.3):
            if len(cl) >= maj:
                canns.append(make_ann(tax, aid, iid, tax.ignore, mean_box([o.box for o in cl.values()]), {},
                                      {"needs_calibration": False}))
                aid += 1
    (QC_DIR / "consensus_draft.json").write_text(json.dumps(
        build_coco(tax, cimages, canns, {"description": "Đồng thuận NHÁP tự động - chưa phải nhãn cuối",
                                         "guideline_taxonomy": tax.version, "flagged_images": flagged}),
        ensure_ascii=False, indent=1), encoding="utf8")

    # ----- tổng kết
    summary = {"taxonomy_version": tax.version, "thresholds": {k: r[k] for k in ("iaa_iou", "iaa_class", "match_iou")},
               "n_annotators": len(files), "n_images_compared": len(images),
               "coverage": {"completed": len(actual), "assigned": len(expected)},
               "inputs": hashes,
               "artifacts": {name: digest(QC_DIR / name) for name in (
                   "consensus_draft.json", "flagged_images.txt", "calibration_candidates.csv"
               )},
               "overall": finalize(total, tax), "per_pair": {k: finalize(v, tax) for k, v in sorted(per_pair.items())},
               "n_issues": len(issues), "issues_by_type": dict(Counter(x["issue_type"] for x in issues)),
               "n_flagged_images": len(flagged)}
    (QC_DIR / "iaa_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf8")

    ov = summary["overall"]
    md = [f"# Tóm tắt IAA (taxonomy {tax.version})", "",
          f"- Ảnh được so sánh (có >=2 người gán): **{len(images)}**; số người gán: {len(files)}",
          f"- Lượt gán đủ **{len(actual)}/{len(expected)}**.",
          f"- IoU trung bình và % cùng lớp **chỉ tính trên các cặp box đã ghép** (IoU >= {r['match_iou']}, ghép 1-1 không phân biệt lớp). "
          f"Box chưa ghép được thống kê riêng ở cột bỏ sót/thừa.",
          f"- Mẫu số: {ov['n_matched_pairs']} cặp box ghép (tổng mọi cặp người gán, ảnh chung).", "",
          "| Cặp | Ảnh | Cặp box ghép | IoU TB | Cùng lớp | " + " | ".join(f"Cùng {a}" for a in check_attrs) +
          " | Chưa ghép (A/B) | Bỏ qua do ignore | Đạt IAA |",
          "|---|---|---|---|---|" + "---|" * len(check_attrs) + "---|---|---|"]
    for k, v in [("**TỔNG**", ov)] + list(summary["per_pair"].items()):
        mi_s = "n/a" if v["mean_iou"] is None else "%.3f" % v["mean_iou"]
        md.append(f"| {k} | {v['n_images']} | {v['n_matched_pairs']} | "
                  f"{mi_s} | {pct(v['class_agreement'])} | " +
                  " | ".join(pct(v['attr_agreement'][a]) for a in check_attrs) +
                  f" | {v['n_unmatched_a']}/{v['n_unmatched_b']} | {v['n_skipped_in_ignore']} | "
                  f"{'N/A' if v['pass'] is None else ('ĐẠT' if v['pass'] else 'CHƯA ĐẠT')} |")
    md += ["", f"Ngưỡng IAA: IoU TB >= {r['iaa_iou']}, đồng thuận lớp >= {r['iaa_class'] * 100:.0f}%.", "",
           f"Số ca bất thường: {len(issues)} ({summary['issues_by_type']}), trên {len(flagged)} ảnh cần calibration."]
    (QC_DIR / "iaa_summary.md").write_text("\n".join(md) + "\n", encoding="utf8")

    # ----- console
    print(f"Đã so sánh {len(images)} ảnh, {len(files)} người gán, {ov['n_matched_pairs']} cặp box ghép.")
    print(f"Lượt gán: {len(actual)}/{len(expected)}. Ca cần xem: {len(issues)} trên {len(flagged)} ảnh.")
    print("Đối chiếu guideline và ảnh tham chiếu để tìm lỗi chung của nhiều người.")
    print(f"\nĐã ghi vào {rel(QC_DIR)}/: iaa_summary.json|md, calibration_candidates.csv, image_scores.csv, "
          f"consensus_draft.json, flagged_images.txt")
    print("Bước tiếp: python scripts/viz_disagreement.py --images flagged")


if __name__ == "__main__":
    main()
