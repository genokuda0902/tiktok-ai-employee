"""Genre-neutral evidence-focus animation cues (review-only, original visuals).

A cue highlights the exact on-screen evidence behind a claim. Coordinates are
in source 1080x1920 frame pixels. Missing rights/voice gates remain independent.
"""
from dataclasses import dataclass

W, H = 1080, 1920

@dataclass(frozen=True)
class FocusCue:
    scene: int
    start: float
    end: float
    rect: tuple[int, int, int, int]
    color: str = '0x3de0cc'


def validate_cues(cues, scene_count=8, scene_seconds=2.5):
    for c in cues:
        if not (0 <= c.scene < scene_count):
            raise ValueError('Invalid scene index')
        if not (0 <= c.start < c.end <= scene_seconds):
            raise ValueError('Invalid cue timing')
        x, y, w, h = c.rect
        if not (0 <= x < W and 0 <= y < H and w >= 12 and h >= 12 and x+w <= W and y+h <= H):
            raise ValueError('Focus rectangle out of frame')
        if c.color not in ('0x3de0cc', '0xffba55', '0xff5270'):
            raise ValueError('Unsupported focus color')
    for scene in range(scene_count):
        a = sorted((c for c in cues if c.scene == scene), key=lambda c: c.start)
        if any(p.end > n.start for p, n in zip(a, a[1:])):
            raise ValueError('Overlapping cues in a scene')
    return True


def ffmpeg_focus_filter(scene, cues):
    """FFmpeg filter graph fragment; highlight windows with precise reveal times."""
    validate_cues(cues)
    s = ''
    for c in cues:
        if c.scene != scene:
            continue
        x, y, w, h = c.rect
        s += (f",drawbox=x={x}:y={y}:w={w}:h={h}:color={c.color}@0.16:t=fill:"
              f"enable='between(t,{c.start:.3f},{c.end:.3f})'")
        s += (f",drawbox=x={x}:y={y}:w={w}:h={h}:color={c.color}@0.90:t=5:"
              f"enable='between(t,{c.start:.3f},{c.end:.3f})'")
    return s


CUES = [
    FocusCue(1, .30, 1.08, (110,560,820,220), '0xffba55'),
    FocusCue(1, 1.18, 2.23, (110,960,820,220), '0xff5270'),
    FocusCue(2, .20, 1.07, (110,690,820,145), '0xff5270'),
    FocusCue(2, 1.18, 2.26, (110,940,820,145), '0xff5270'),
    FocusCue(5, .42, 1.15, (128,740,808,152), '0x3de0cc'),
    FocusCue(5, 1.24, 2.30, (128,1190,808,122), '0x3de0cc'),
    FocusCue(6, .15, 1.00, (120,520,842,305), '0xff5270'),
    FocusCue(6, 1.15, 2.32, (120,980,842,300), '0x3de0cc'),
]
validate_cues(CUES)
