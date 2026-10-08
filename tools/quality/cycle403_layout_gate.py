"""Cycle403: reusable Japanese vertical-slide layout contract (zero-cost, offline)."""
from __future__ import annotations

SAFE_MARGIN = 80
WIDTH, HEIGHT = 1080, 1920
ZONES = {
    "header": (80, 75, 1000, 182),
    "title": (80, 240, 1000, 560),
    "graphic": (88, 580, 992, 1380),
    "caption": (80, 1460, 1000, 1785),
    "footer": (80, 1810, 1000, 1870),
}
GRAPHICS = {"hook", "deck", "research", "writing", "ideas", "automation"}

def _overlap(a, b):
    return max(a[0], b[0]) < min(a[2], b[2]) and max(a[1], b[1]) < min(a[3], b[3])

def validate_layout(zones=ZONES):
    for name, (x1, y1, x2, y2) in zones.items():
        if not (SAFE_MARGIN <= x1 < x2 <= WIDTH-SAFE_MARGIN and 0 <= y1 < y2 <= HEIGHT-40):
            raise ValueError("unsafe zone: " + name)
    for a, box_a in zones.items():
        for b, box_b in zones.items():
            if a < b and _overlap(box_a, box_b):
                raise ValueError("overlapping zones: " + a + ", " + b)
    return True

def validate_scenes(scenes):
    if not scenes:
        raise ValueError("empty scenes")
    total = 0
    for i, s in enumerate(scenes):
        if not isinstance(s.get("frames"), int) or s["frames"] < 1:
            raise ValueError("invalid frame count at " + str(i))
        if s.get("graphic") not in GRAPHICS:
            raise ValueError("unknown graphic at " + str(i))
        for field, max_chars in (("title", 18), ("caption", 24)):
            lines = s.get(field)
            if not isinstance(lines, list) or not 1 <= len(lines) <= 2:
                raise ValueError("invalid " + field + " lines at " + str(i))
            if any(not isinstance(x, str) or not x.strip() or len(x) > max_chars for x in lines):
                raise ValueError("unsafe " + field + " length at " + str(i))
        total += s["frames"]
    validate_layout()
    return total

def validate_genres(genres):
    if len(genres) != 10 or len(set(genres)) != 10:
        raise ValueError("expected 10 unique genres")
    return True
