"""Zero-cost caption readability guard for vertical image-slide videos.

Adds a subtle lower-third luminance guard behind already-burned captions without
changing narration, caption text, timing, posting policy, or source rights.
Designed as a genre-independent final-pass helper for 1080x1920 output.
"""
from dataclasses import dataclass

@dataclass(frozen=True)
class CaptionGuard:
    y: int = 1180
    height: int = 500
    opacity: float = 0.10

    def validate(self) -> None:
        if self.y < 0 or self.height <= 0 or self.y + self.height > 1920:
            raise ValueError("caption guard must stay inside 1080x1920 frame")
        if not (0.0 <= self.opacity <= 0.14):
            raise ValueError("opacity exceeds subtle readability limit")

    def ffmpeg_filter(self) -> str:
        self.validate()
        return f"drawbox=x=0:y={self.y}:w=iw:h={self.height}:color=black@{self.opacity}:t=fill"


def posting_policy() -> dict:
    return {"zero_cost": True, "human_approval_required": True, "auto_post": False}
