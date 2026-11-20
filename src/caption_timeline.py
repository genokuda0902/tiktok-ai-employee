"""Reusable 10-genre caption timeline validator (review-only)."""
def validate_captions(captions, duration):
    if duration <= 0 or not captions:
        return False
    cursor = 0.0
    for start, end, text in captions:
        if not isinstance(text, str) or not text.strip():
            return False
        if abs(start - cursor) > 0.05 or end <= start or end > duration + 0.05:
            return False
        cursor = end
    return abs(cursor - duration) <= 0.05

REVIEW_CAPTIONS = [
    (0.0, 3.0, "数字を毎回手入力していませんか？"),
    (3.0, 6.0, "=SUM(B2:B5) を入力"),
    (6.0, 9.0, "合計 120 になるか確認"),
]
