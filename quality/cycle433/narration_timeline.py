"""Check planned Japanese captions and narration timing."""
def scene_plan(data):
    scenes = data["scenes"]
    if not scenes or any(not s.get("voice") or not s.get("caption") or float(s.get("seconds", 0)) <= 0 for s in scenes):
        raise ValueError("Invalid scene plan")
    return scenes

def speed_ratio(source, target):
    if source <= 0 or target <= 0:
        raise ValueError("Invalid timing")
    ratio = source / max(0.1, target - 0.10)
    if ratio < 0.5 or ratio > 2:
        raise ValueError("Unsupported timing")
    return ratio
