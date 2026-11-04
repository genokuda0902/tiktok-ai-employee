"""Review-only TikTok caption geometry gate. No publication authorization.

Checks rendered caption bounding boxes against conservative platform UI margins.
Works across all genres; fail closed for missing/malformed geometry.
Coordinates are pixels in the encoded video (not the source image).
"""
from dataclasses import dataclass

@dataclass(frozen=True)
class CaptionBox:
    x: int
    y: int
    width: int
    height: int

def validate_caption_boxes(boxes, frame_width=1080, frame_height=1920,
                           side_margin=90, top_margin=240, bottom_margin=420):
    if not isinstance(boxes, (list, tuple)) or not boxes:
        raise ValueError("caption boxes required")
    if frame_width <= 0 or frame_height <= 0:
        raise ValueError("invalid frame size")
    if min(side_margin, top_margin, bottom_margin) < 0:
        raise ValueError("invalid safe margins")
    if 2 * side_margin >= frame_width or top_margin + bottom_margin >= frame_height:
        raise ValueError("safe area is empty")
    for i, box in enumerate(boxes):
        if not isinstance(box, CaptionBox):
            raise ValueError(f"caption {i}: missing geometry")
        values = (box.x, box.y, box.width, box.height)
        if any(type(v) is not int for v in values) or box.width <= 0 or box.height <= 0:
            raise ValueError(f"caption {i}: invalid geometry")
        if (box.x < side_margin or box.y < top_margin or
            box.x + box.width > frame_width - side_margin or
            box.y + box.height > frame_height - bottom_margin):
            raise ValueError(f"caption {i}: overlaps unsafe UI region")
    return True
