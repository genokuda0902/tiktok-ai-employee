"""Shared, zero-cost narration-aligned scene pacing for vertical TikTok slides."""
from __future__ import annotations
from dataclasses import dataclass

FPS = 30
CAPTION_CUES = ((0.00, 0.88), (0.88, 1.77), (1.87, 3.52),
                (3.62, 5.50), (5.50, 6.55), (6.55, 7.66),
                (7.76, 9.48), (9.48, 11.18))
SCENE_CUTS = (1.77, 3.52, 5.50, 6.55, 7.66, 9.48, 11.18)
GENRES = ("AI時短", "仕事術", "営業", "ビジネスマナー", "勉強",
          "お金の管理", "暮らし", "旅行", "ガジェット", "雑学")

def cuts_inside_spoken_phrases(cuts, cues=CAPTION_CUES, tolerance=0.03):
    """Return cuts that split an active subtitle phrase."""
    return [cut for cut in cuts if any(a + tolerance < cut < b - tolerance for a, b in cues)]

def scene_frame_counts(cuts=SCENE_CUTS, duration=12.5, fps=FPS):
    """Round cumulative timestamps so all scene frame counts sum exactly."""
    boundaries = (0.0, *cuts, duration)
    return tuple(round(b * fps) - round(a * fps)
                 for a, b in zip(boundaries[:-1], boundaries[1:]))

def validate():
    assert len(GENRES) == 10
    assert not cuts_inside_spoken_phrases(SCENE_CUTS)
    assert sum(scene_frame_counts()) == 375
    assert min(scene_frame_counts()) > 0
    return True
