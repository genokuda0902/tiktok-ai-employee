"""Fail-closed timing validation for 10-category short-form videos."""
def validate_scenes(scenes, duration, min_scene=1.0):
    if not scenes or duration <= 0:
        raise ValueError("empty timeline")
    cursor = 0.0
    for scene in scenes:
        start, end, caption = scene
        if abs(start - cursor) > 0.05:
            raise ValueError("gap or overlap")
        if end - start < min_scene:
            raise ValueError("scene too short")
        if not isinstance(caption, str) or not caption.strip():
            raise ValueError("missing caption")
        cursor = end
    if abs(cursor - duration) > 0.05:
        raise ValueError("duration mismatch")
    return True
