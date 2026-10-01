"""TikTok 9:16 safe-area validator for review-only scene plans.

Coordinates use a 1080x1920 canvas. This validator intentionally fails closed:
important text/interaction targets must stay away from top/bottom chrome and the
right-side TikTok action rail. No publication action is performed here.
"""

CANVAS_WIDTH = 1080
CANVAS_HEIGHT = 1920
SAFE_LEFT = 60
SAFE_RIGHT = 900
SAFE_TOP = 180
SAFE_BOTTOM = 1600

def validate_box(box):
    """Return [] when an important bounding box is inside the conservative safe area."""
    errors = []
    required = ("x", "y", "w", "h")
    if not isinstance(box, dict) or any(k not in box for k in required):
        return ["box requires x,y,w,h"]
    x, y, w, h = (box[k] for k in required)
    if not all(isinstance(v, (int, float)) for v in (x, y, w, h)):
        return ["box coordinates must be numeric"]
    if w <= 0 or h <= 0:
        errors.append("box dimensions must be positive")
    if x < SAFE_LEFT:
        errors.append("box enters left unsafe margin")
    if y < SAFE_TOP:
        errors.append("box enters top unsafe margin")
    if x + w > SAFE_RIGHT:
        errors.append("box enters right TikTok UI rail")
    if y + h > SAFE_BOTTOM:
        errors.append("box enters bottom TikTok UI area")
    return errors

def validate_scene_safe_area(scene):
    errors = []
    for i, box in enumerate(scene.get("important_boxes") or []):
        for err in validate_box(box):
            errors.append(f"important_box {i}: {err}")
    return errors
