"""Shared scene timeline checks. Reimplementation; not recovered v33 code."""
def scene_at(t, durations):
    if t < 0 or not durations or any(x <= 0 for x in durations):
        raise ValueError("invalid timeline")
    elapsed = 0
    for i, seconds in enumerate(durations):
        elapsed += seconds
        if t < elapsed:
            return i
    return len(durations)-1

def step_label(t, durations):
    i = scene_at(t, durations)
    return f"STEP {i+1:02d} / {len(durations):02d}"
