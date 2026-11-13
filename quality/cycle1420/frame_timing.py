"""Genre-independent frame sampling and typing cursor timing. Review-only."""
def frame_times(duration_s=15, fps=10):
    if duration_s <= 0 or fps <= 0 or int(duration_s * fps) != duration_s * fps:
        raise ValueError("positive integral frame count required")
    return [i / fps for i in range(int(duration_s * fps))]

def scene_at(seconds, scene_seconds=3, scene_count=5):
    if not 0 <= seconds < scene_seconds * scene_count:
        raise ValueError("time outside scene timeline")
    return int(seconds // scene_seconds), seconds % scene_seconds

def cursor_visible(local_seconds, blink_hz=2.5):
    return int(local_seconds * blink_hz * 2) % 2 == 0
