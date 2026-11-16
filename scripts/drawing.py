"""Hàm vẽ box lên ảnh bằng Pillow (dùng chung cho viz_disagreement.py và qc_sample.py)."""
from __future__ import annotations

from typing import List, Optional, Tuple

try:
    from PIL import Image, ImageDraw
except ImportError:  # pragma: no cover
    raise SystemExit("Thiếu thư viện Pillow. Cài bằng: pip install -r requirements.txt")

from common import Obj, Taxonomy

PALETTE = [(230, 25, 75), (60, 120, 255), (30, 160, 60), (245, 130, 48), (145, 30, 180), (0, 170, 190)]


def obj_label(o: Obj, tax: Taxonomy, show_id: bool = False) -> str:
    parts = [f"#{o.id} " if show_id else "", o.cls]
    for n, a in tax.attrs.items():
        v = o.attrs.get(n)
        if v is not None and v != tax.default(n) and o.cls != tax.ignore:
            parts.append(f" {n}={v}" if n != "can_review" else " ?review")
    return "".join(parts)


def draw_layers(img_path, layers: List[Tuple[str, Tuple[int, int, int], List[Obj]]], tax: Taxonomy,
                show_id: bool = False, title: Optional[str] = None) -> "Image.Image":
    """layers = [(tên lớp vẽ, màu RGB, [Obj...]), ...]. Trả về ảnh đã vẽ."""
    im = Image.open(img_path).convert("RGB")
    dr = ImageDraw.Draw(im, "RGBA")
    for li, (_, col, objs) in enumerate(layers):
        for o in objs:
            x1, y1, x2, y2 = o.box
            if o.cls == tax.ignore:
                dr.rectangle([x1, y1, x2, y2], fill=col + (40,), outline=col + (255,), width=2)
            else:
                dr.rectangle([x1, y1, x2, y2], outline=col, width=3 if len(layers) == 1 else 2)
            text = obj_label(o, tax, show_id)
            tw = dr.textlength(text)
            ty = max(0, y1 - 12 - 11 * li)
            dr.rectangle([x1, ty, x1 + tw + 4, ty + 11], fill=col + (200,))
            dr.text((x1 + 2, ty), text, fill=(255, 255, 255))
    # chú thích (legend)
    lines = ([title] if title else []) + [n for n, _, _ in layers if len(layers) > 1]
    if lines:
        h = 13 * len(lines) + 6
        dr.rectangle([0, 0, 260, h], fill=(0, 0, 0, 170))
        y = 3
        if title:
            dr.text((4, y), title, fill=(255, 255, 255))
            y += 13
        if len(layers) > 1:
            for n, col, _ in layers:
                dr.rectangle([4, y + 2, 14, y + 10], fill=col)
                dr.text((19, y), n, fill=(255, 255, 255))
                y += 13
    return im
