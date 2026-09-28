"""Cycle 153: zero-cost first-second pattern interrupt for image-slide videos.

Keeps claims/captions unchanged and applies a short visual punch-in only.
Designed as a shared post-process primitive across content genres.
"""
from dataclasses import dataclass

@dataclass(frozen=True)
class PatternInterrupt:
    start: float = 0.75
    end: float = 1.05
    zoom: float = 1.02
    contrast: float = 1.035

    def validate(self) -> None:
        if not (0 <= self.start < self.end <= 3.0):
            raise ValueError("pattern interrupt must stay inside first 3 seconds")
        if not (1.0 <= self.zoom <= 1.05):
            raise ValueError("zoom must be subtle (1.00-1.05)")
        if not (1.0 <= self.contrast <= 1.10):
            raise ValueError("contrast must be subtle (1.00-1.10)")

def ffmpeg_values(cfg: PatternInterrupt = PatternInterrupt()) -> dict[str, float]:
    cfg.validate()
    return {"start": cfg.start, "end": cfg.end, "zoom": cfg.zoom, "contrast": cfg.contrast}
