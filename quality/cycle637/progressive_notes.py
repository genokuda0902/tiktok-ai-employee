"""Deterministic, zero-cost progressive disclosure schedule for 8-scene videos.

No publishing or network operations. The returned alpha level is 0..10.
"""
FPS = 30
BOUNDS = (0, 63, 130, 183, 230, 278, 362, 415, 468)
DELAY = 0.45
FADE = 0.28

def scene_for_frame(frame):
    if not isinstance(frame, int) or not (BOUNDS[0] <= frame < BOUNDS[-1]):
        raise ValueError('Frame is outside video duration')
    return next(i for i in range(8) if BOUNDS[i] <= frame < BOUNDS[i + 1])

def alpha_level_for_frame(frame):
    scene = scene_for_frame(frame)
    elapsed = (frame - BOUNDS[scene]) / FPS
    progress = min(1.0, max(0.0, (elapsed - DELAY) / FADE))
    return round(progress * 10)

def validate_schedule():
    assert len(BOUNDS) == 9 and BOUNDS[0] == 0 and BOUNDS[-1] == 468
    assert all(a < b for a, b in zip(BOUNDS, BOUNDS[1:]))
    assert all((b - a) / FPS > DELAY + FADE + 0.6 for a, b in zip(BOUNDS, BOUNDS[1:]))
    return True
