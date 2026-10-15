"""Verified synthetic proof totals and caption geometry for cycle595."""

SAFE_TOP = 192
SAFE_BOTTOM = 1536

def verified_total(values):
    if len(values) != 4:
        raise ValueError('four inputs required')
    if any(type(v) is not int or v < 0 for v in values):
        raise ValueError('positive integer inputs required')
    return sum(values)

def caption_safe(y1, y2):
    return SAFE_TOP <= y1 < y2 <= SAFE_BOTTOM
