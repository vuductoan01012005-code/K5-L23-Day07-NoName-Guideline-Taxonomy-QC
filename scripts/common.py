"""Hàm dùng chung cho các script của lab (đọc taxonomy, đọc nhãn COCO của CVAT, IoU, ghép box...).

Học viên KHÔNG cần sửa file này. Nhóm chỉ sửa submission/taxonomy.json khi đổi lớp/thuộc tính.
"""
from __future__ import annotations

import csv
import hashlib
import json
import math
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Tuple

ROOT = Path(__file__).resolve().parent.parent
TAXONOMY_PATH = ROOT / "submission" / "taxonomy.json"
FINAL_TAXONOMY_PATH = ROOT / "submission" / "taxonomy_v1.1.json"
GUIDELINE_PATH = ROOT / "submission" / "guidelines" / "guideline_v1.0_agreed.md"
FINAL_GUIDELINE_PATH = ROOT / "submission" / "guidelines" / "guideline_v1.1_calibrated.md"
ASSIGNMENT_PATH = ROOT / "submission" / "qc" / "assignment.csv"
MEMBER_RE = re.compile(r"\d{3}", re.ASCII)
LABELS_DIR = ROOT / "submission" / "labels"
QC_DIR = ROOT / "submission" / "qc"
IMAGES_DIR = ROOT / "data" / "images"
WORK_DIR = ROOT / "work"
IMG_EXT = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}

Box = Tuple[float, float, float, float]  # (x1, y1, x2, y2)


def die(msg: str, code: int = 2) -> None:
    print(f"\nLỖI: {msg}", file=sys.stderr)
    sys.exit(code)


# --------------------------------------------------------------------------- taxonomy
class Taxonomy:
    def __init__(self, d: dict):
        self.raw = d
        self.version = d.get("version", "?")
        self.classes: List[str] = [c["name"] for c in d["classes"]]
        self.attrs: Dict[str, dict] = {a["name"]: a for a in d.get("attributes", [])}
        self.rules: dict = d["rules"]
        self.ignore: str = d.get("ignore_class", "ignore_region")

    @property
    def object_classes(self) -> List[str]:
        return [c for c in self.classes if c != self.ignore]

    def default(self, name: str) -> str:
        return self.norm_attr(name, self.attrs[name].get("default"))

    def norm_attr(self, name: str, value) -> str:
        """Chuẩn hoá giá trị thuộc tính về chuỗi thường để so sánh được giữa các người gán."""
        a = self.attrs.get(name, {})
        vals = [str(v).lower() for v in a.get("values", [])]
        if a.get("type") == "checkbox":
            if value is None:
                return "false"
            return "true" if str(value).strip().lower() in ("true", "1", "yes", "on", "1.0") else "false"
        if value is None:
            value = a.get("default", "")
        if isinstance(value, bool):
            if "yes" in vals:
                return "yes" if value else "no"
            return "true" if value else "false"
        if isinstance(value, float) and value.is_integer():
            value = int(value)
        s = str(value).strip().lower()
        if s in ("true", "false") and "yes" in vals:
            s = "yes" if s == "true" else "no"
        if s.endswith(".0") and s[:-2].isdigit():
            s = s[:-2]
        return s

    def valid(self, name: str, norm_value: str) -> bool:
        a = self.attrs[name]
        if a.get("type") == "checkbox":
            return norm_value in ("true", "false")
        return norm_value in [str(v).lower() for v in a.get("values", [])]

    def to_coco_value(self, name: str, norm_value: str):
        if self.attrs[name].get("type") == "checkbox":
            return norm_value == "true"
        return norm_value


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_taxonomy(path: Path = TAXONOMY_PATH) -> Taxonomy:
    from jsonschema import Draft202012Validator

    try:
        data = json.loads(path.read_text(encoding="utf8"))
        schema = json.loads((ROOT / "schemas" / "taxonomy.schema.json").read_text(encoding="utf8"))
    except (OSError, ValueError) as exc:
        die(f"Không đọc được taxonomy {rel(path)}: {exc}")
    errors = list(Draft202012Validator(schema).iter_errors(data))
    if errors:
        die(f"{rel(path)}: " + "\n".join(f"{e.json_path}: {e.message}" for e in errors))
    tax = Taxonomy(data)
    if len(tax.classes) != len(set(tax.classes)) or tax.ignore not in tax.classes:
        die("Tên lớp phải duy nhất và ignore_class phải có trong classes.")
    if len(tax.attrs) != len(data["attributes"]):
        die("Tên thuộc tính phải duy nhất.")
    for name, attr in tax.attrs.items():
        if attr["type"] == "select" and (
            not tax.valid(name, tax.default(name))
            or len({value.lower() for value in attr["values"]}) != len(attr["values"])
        ):
            die(f"{name}: default phải thuộc values và các mức phải phân biệt được.")
    if tax.attrs.get("can_review", {}).get("type") != "checkbox":
        die("Giữ thuộc tính can_review kiểu checkbox.")
    return tax


def final_taxonomy_path() -> Path:
    return FINAL_TAXONOMY_PATH if FINAL_TAXONOMY_PATH.exists() else TAXONOMY_PATH


def input_hashes() -> dict:
    paths = [TAXONOMY_PATH, GUIDELINE_PATH, ASSIGNMENT_PATH, *list_label_files()]
    paths.extend(IMAGES_DIR / name for name in sorted(require_assignment()))
    issues = QC_DIR / "image_issues.csv"
    if issues.exists():
        paths.append(issues)
    missing = [rel(path) for path in paths if not path.is_file()]
    if missing:
        raise ValueError("Thiếu dữ liệu đầu vào: " + ", ".join(missing))
    return {rel(path): digest(path) for path in paths}


# --------------------------------------------------------------------------- hình học
def xywh_to_xyxy(b) -> Box:
    return (float(b[0]), float(b[1]), float(b[0]) + float(b[2]), float(b[1]) + float(b[3]))


def xyxy_to_xywh(b: Box) -> List[float]:
    return [round(b[0], 2), round(b[1], 2), round(b[2] - b[0], 2), round(b[3] - b[1], 2)]


def area(b: Box) -> float:
    return max(0.0, b[2] - b[0]) * max(0.0, b[3] - b[1])


def inter_area(a: Box, b: Box) -> float:
    return max(0.0, min(a[2], b[2]) - max(a[0], b[0])) * max(0.0, min(a[3], b[3]) - max(a[1], b[1]))


def iou(a: Box, b: Box) -> float:
    inter = inter_area(a, b)
    u = area(a) + area(b) - inter
    return inter / u if u > 0 else 0.0


def covered_by(box: Box, regions: List[Box], frac: float = 0.5) -> bool:
    """True nếu >= frac diện tích box nằm trong một vùng ignore."""
    a = area(box)
    return a > 0 and any(inter_area(box, r) / a >= frac for r in regions)


def mean_box(boxes: List[Box]) -> Box:
    n = len(boxes)
    return tuple(sum(b[i] for b in boxes) / n for i in range(4))  # type: ignore


def iou_threshold(tax: Taxonomy, a: Box, b: Box) -> float:
    h = ((a[3] - a[1]) + (b[3] - b[1])) / 2
    r = tax.rules
    return r["iou_thr_large"] if h >= r["large_px"] else r["iou_thr_small"]


# --------------------------------------------------------------------------- đọc COCO
@dataclass
class Obj:
    id: int
    cls: str
    box: Box
    attrs: Dict[str, str]
    raw_attrs: dict = field(default_factory=dict)


@dataclass
class LabelFile:
    path: Path
    member: str
    images: Dict[str, Tuple[int, int]]          # basename -> (w, h)
    objects: Dict[str, List[Obj]]               # basename -> objects (kể cả ignore_region)
    problems: List[str] = field(default_factory=list)


def load_coco(path: Path, tax: Taxonomy) -> LabelFile:
    data = json.loads(Path(path).read_text(encoding="utf8"))
    if not isinstance(data, dict) or any(not isinstance(data.get(key), list)
                                         for key in ("images", "categories", "annotations")):
        raise ValueError("COCO cần mảng images, categories và annotations.")
    cats = {c["id"]: c["name"] for c in data["categories"]}
    if len(cats) != len(data["categories"]) or len(set(cats.values())) != len(cats):
        raise ValueError("COCO có ID hoặc tên category trùng.")
    imgs = {}
    lf = LabelFile(Path(path), Path(path).stem, {}, {})
    for im in data.get("images", []):
        base = Path(im["file_name"]).name
        if base in lf.images or im["id"] in imgs:
            lf.problems.append(f"ảnh {base} có tên hoặc image_id trùng")
        imgs[im["id"]] = base
        lf.images[base] = (int(im.get("width", 0)), int(im.get("height", 0)))
        lf.objects.setdefault(base, [])
    annotation_ids = set()
    for an in data["annotations"]:
        ann_id = an["id"]
        if type(ann_id) is not int or ann_id in annotation_ids:
            lf.problems.append(f"annotation_id không hợp lệ hoặc trùng: {ann_id}")
        annotation_ids.add(ann_id)
        base = imgs.get(an.get("image_id"))
        if base is None:
            lf.problems.append(f"annotation {an.get('id')} trỏ tới image_id không có trong 'images'")
            continue
        cls = cats.get(an.get("category_id"), f"?category_id={an.get('category_id')}")
        raw = an.get("attributes", {}) or {}
        if not isinstance(raw, dict):
            raise ValueError(f"annotation {ann_id}: attributes phải là object.")
        bbox = an["bbox"]
        if not isinstance(bbox, list) or len(bbox) != 4 or any(
            type(coord) not in (int, float) or not math.isfinite(coord) for coord in bbox
        ):
            raise ValueError(f"annotation {ann_id}: bbox phải gồm bốn số hữu hạn.")
        attrs = {n: tax.norm_attr(n, raw.get(n)) for n in tax.attrs}
        lf.objects[base].append(Obj(ann_id, cls, xywh_to_xyxy(bbox), attrs, raw))
    return lf


def list_label_files() -> List[Path]:
    return sorted(p for p in LABELS_DIR.glob("*.json"))


def load_all_labels(tax: Taxonomy) -> Dict[str, LabelFile]:
    files = list_label_files()
    if not files:
        die("Chưa có file nhãn nào trong submission/labels/. Mỗi thành viên export COCO 1.0 từ CVAT, "
            "đặt tên theo mã, ví dụ 101.json.")
    out: Dict[str, LabelFile] = {}
    for p in files:
        if not MEMBER_RE.fullmatch(p.stem):
            die(f"{p.name}: đặt tên theo mã ba chữ số, ví dụ 101.json.")
        try:
            lf = load_coco(p, tax)
        except Exception as e:  # noqa
            die(f"Không đọc được {p.name}: {e}. Chạy `python scripts/validate_labels.py` để xem chi tiết.")
            raise
        if lf.member in out:
            die(f"Trùng file nhãn cho mã thành viên {lf.member}.")
        out[lf.member] = lf
    return out


def load_assignment() -> Optional[Dict[str, List[str]]]:
    if not ASSIGNMENT_PATH.exists():
        return None
    assignment = {}
    known = set(list_images())
    for row in read_csv(ASSIGNMENT_PATH):
        image = row.get("image")
        codes = (row.get("annotators") or "").split("|")
        if image not in known or image in assignment:
            die(f"assignment.csv: ảnh không hợp lệ hoặc trùng: {image}.")
        if len(set(codes)) != len(codes) or not all(MEMBER_RE.fullmatch(code) for code in codes):
            die(f"assignment.csv: mã thành viên sai hoặc trùng ở {image}.")
        if row.get("n_annotators") != str(len(codes)):
            die(f"assignment.csv: n_annotators không khớp ở {image}.")
        assignment[image] = codes
    members = {code for codes in assignment.values() for code in codes}
    if not 2 <= len(members) <= 5:
        die("assignment.csv phải có từ 2 đến 5 thành viên.")
    minimum = 3 if len(members) == 5 else 2
    if any(len(codes) < minimum for codes in assignment.values()):
        die(f"assignment.csv: mỗi ảnh cần ít nhất {minimum} lượt gán.")
    return assignment


def require_assignment() -> Dict[str, List[str]]:
    assignment = load_assignment()
    if assignment is None:
        die("Thiếu assignment.csv. Chạy split_assign.py trước.")
    return assignment


def label_errors(labels: LabelFile, tax: Taxonomy) -> List[str]:
    from PIL import Image

    errors = list(labels.problems)
    for image, objects in labels.objects.items():
        width, height = labels.images[image]
        try:
            with Image.open(IMAGES_DIR / image) as source:
                source.load()
                if source.size != (width, height):
                    errors.append(f"{image}: kích thước COCO lệch ảnh gốc.")
        except OSError:
            errors.append(f"{image}: không đọc được ảnh gốc.")
        for obj in objects:
            tag = f"{image} #{obj.id}"
            if obj.cls not in tax.classes:
                errors.append(f"{tag}: lớp '{obj.cls}' ngoài taxonomy.")
                continue
            x1, y1, x2, y2 = obj.box
            if not (0 <= x1 < x2 <= width and 0 <= y1 < y2 <= height):
                errors.append(f"{tag}: bbox không hợp lệ hoặc vượt ảnh.")
            if obj.cls == tax.ignore:
                continue
            for name, attr in tax.attrs.items():
                if name not in obj.raw_attrs or obj.raw_attrs[name] is None:
                    errors.append(f"{tag}: thiếu thuộc tính '{name}'.")
                elif not tax.valid(name, obj.attrs[name]) or (
                    attr["type"] == "checkbox"
                    and str(obj.raw_attrs[name]).strip().lower()
                    not in {"true", "false", "1", "0", "yes", "no", "on", "off", "1.0", "0.0"}
                ):
                    errors.append(f"{tag}: thuộc tính '{name}' không hợp lệ.")
    return errors


def require_valid_labels(path: Path, tax: Taxonomy) -> LabelFile:
    try:
        labels = load_coco(path, tax)
    except (OSError, TypeError, ValueError, KeyError) as exc:
        die(f"Không đọc được {rel(path)}: {exc}")
    errors = label_errors(labels, tax)
    if errors:
        die(f"{rel(path)}:\n" + "\n".join(errors))
    return labels


def list_images() -> List[str]:
    if not IMAGES_DIR.exists():
        return []
    return sorted(p.name for p in IMAGES_DIR.iterdir() if p.suffix.lower() in IMG_EXT)


def read_flagged() -> List[str]:
    p = QC_DIR / "flagged_images.txt"
    if not p.exists():
        return []
    return [l.strip() for l in p.read_text(encoding="utf8").splitlines() if l.strip()]


# --------------------------------------------------------------------------- ghép box
def match_boxes(A: List[Obj], B: List[Obj], thr: float):
    """Ghép 1-1 tham lam theo IoU giảm dần (không quan tâm lớp). Trả về (cặp, A chưa ghép, B chưa ghép)."""
    cands = []
    for i, a in enumerate(A):
        for j, b in enumerate(B):
            v = iou(a.box, b.box)
            if v >= thr:
                cands.append((v, i, j))
    cands.sort(key=lambda t: (-t[0], t[1], t[2]))
    ua, ub, pairs = set(), set(), []
    for v, i, j in cands:
        if i in ua or j in ub:
            continue
        ua.add(i)
        ub.add(j)
        pairs.append((A[i], B[j], v))
    return pairs, [a for i, a in enumerate(A) if i not in ua], [b for j, b in enumerate(B) if j not in ub]


def cluster_objects(per_ann: Dict[str, List[Obj]], thr: float) -> List[Dict[str, Obj]]:
    """Gom box của các người gán thành cụm (mỗi cụm tối đa 1 box/người). Class-agnostic."""
    clusters: List[Dict[str, Obj]] = []
    for m in sorted(per_ann):
        objs = per_ann[m]
        cands = []
        for oi, o in enumerate(objs):
            for ci, c in enumerate(clusters):
                v = iou(o.box, mean_box([x.box for x in c.values()]))
                if v >= thr:
                    cands.append((v, oi, ci))
        cands.sort(key=lambda t: (-t[0], t[1], t[2]))
        used_o, used_c = set(), set()
        for v, oi, ci in cands:
            if oi in used_o or ci in used_c:
                continue
            clusters[ci][m] = objs[oi]
            used_o.add(oi)
            used_c.add(ci)
        for oi, o in enumerate(objs):
            if oi not in used_o:
                clusters.append({m: o})
    return clusters


def annotators_of_image(files: Dict[str, LabelFile], img: str,
                        assignment: Optional[Dict[str, List[str]]]) -> List[str]:
    """Người đã gán ảnh img (có ảnh trong file của họ, và — nếu có assignment — được giao ảnh đó)."""
    if assignment is not None and img not in assignment:
        return []
    return [m for m in sorted(files)
            if img in files[m].objects and (assignment is None or m in assignment[img])]


# --------------------------------------------------------------------------- ghi COCO
def build_coco(tax: Taxonomy, images: List[dict], annotations: List[dict], info: Optional[dict] = None) -> dict:
    return {
        "info": info or {},
        "licenses": [],
        "categories": [{"id": i + 1, "name": n} for i, n in enumerate(tax.classes)],
        "images": images,
        "annotations": annotations,
    }


def make_ann(tax: Taxonomy, ann_id: int, image_id: int, cls: str, box: Box, attrs: Dict[str, str],
             extra: Optional[dict] = None) -> dict:
    xywh = xyxy_to_xywh(box)
    at = {n: tax.to_coco_value(n, attrs.get(n, tax.default(n))) for n in tax.attrs}
    at.update(extra or {})
    return {"id": ann_id, "image_id": image_id, "category_id": tax.classes.index(cls) + 1,
            "bbox": xywh, "area": round(xywh[2] * xywh[3], 2), "iscrowd": 0, "attributes": at}


def read_csv(path: Path) -> List[dict]:
    with path.open(encoding="utf8", newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, header: List[str], rows: List[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=header, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)


def rel(p: Path) -> str:
    try:
        return str(p.relative_to(ROOT))
    except ValueError:
        return str(p)
