"""Small scene timing and caption validation for review-only videos."""
def check(scenes, duration=20):
    if len(scenes) < 6 or len(scenes) > 10:
        raise ValueError("scene count")
    previous = 0.0
    for scene in scenes:
        start, end, caption = scene
        if abs(start - previous) > 0.04:
            raise ValueError("timeline gap")
        if end <= start or not caption or len(caption) > 28:
            raise ValueError("caption timing")
        previous = end
    if abs(previous - duration) > 0.04:
        raise ValueError("duration")
    return {"timeline": "PASS", "approval": "HUMAN_REVIEW"}
