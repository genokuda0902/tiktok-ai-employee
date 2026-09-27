"""Cycle154: subtle rhythm-progress overlay for vertical TikTok slides.

Adds a low-distraction progress cue so viewers can perceive remaining length.
Fail-closed: only accepts the project 1080x1920 / 30fps contract.
"""
from dataclasses import dataclass

@dataclass(frozen=True)
class RhythmProgress:
    width: int = 1080
    height: int = 1920
    fps: int = 30
    top_height: int = 10
    lower_y: int = 1620

    def validate(self) -> None:
        if (self.width, self.height, self.fps) != (1080, 1920, 30):
            raise ValueError("unsupported render contract")
        if not (1 <= self.top_height <= 16):
            raise ValueError("progress bar too intrusive")
        if not (1500 <= self.lower_y <= 1700):
            raise ValueError("lower cue outside safe band")

    def ffmpeg_filter(self, duration: float) -> str:
        self.validate()
        if duration <= 0:
            raise ValueError("duration must be positive")
        return (
            "drawbox=x=0:y=0:w='iw*min(t/{d},1)':h={h}:color=white@0.82:t=fill,"
            "drawbox=x=54:y={y}:w=972:h=2:color=white@0.14:t=fill,"
            "drawbox=x=54:y={y}:w='972*min(t/{d},1)':h=2:color=white@0.45:t=fill"
        ).format(d=duration, h=self.top_height, y=self.lower_y)
