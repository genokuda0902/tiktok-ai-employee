"""Reusable subtitle visibility contract for 10 genres; no external dependencies."""
from dataclasses import dataclass

SAFE_X_MIN, SAFE_X_MAX = 56, 894
SAFE_Y_MIN, SAFE_Y_MAX = 1405, 1685

@dataclass(frozen=True)
class CaptionScene:
    start: float
    end: float
    spoken_text: str
    lines: tuple[str, ...]

def validate_caption(scene: CaptionScene, *, maximum_lines: int = 2) -> None:
    if scene.end <= scene.start:
        raise ValueError("Scene duration must be positive")
    if len(scene.lines) > maximum_lines:
        raise ValueError("Caption exceeds maximum line count")
    if "".join(scene.lines) != scene.spoken_text:
        raise ValueError("Caption must preserve complete script")
    if scene.spoken_text and not scene.lines:
        raise ValueError("Spoken text cannot have missing caption lines")

def caption_visibility_at(scene: CaptionScene, time_s: float) -> tuple[str, ...]:
    """Always show the entire caption; do not delay the second line by RMS.
    RMS is loudness only and cannot establish word alignment."""
    if not (scene.start <= time_s < scene.end):
        return ()
    return scene.lines

def meter_heights(rms: float, phase: float) -> tuple[int, ...]:
    """Small non-linguistic loudness visualization. Never word highlighting."""
    import math
    energy = max(0.0, min(1.0, (rms - 0.015) / 0.23))
    return tuple(8 + int(32 * energy * (0.38 + 0.62 * abs(math.sin(phase * 7 + i * 1.2)))) for i in range(5))
