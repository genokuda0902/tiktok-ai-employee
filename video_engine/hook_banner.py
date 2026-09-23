"""Zero-cost first-1.8s hook banner for the image-slide route.

Human approval remains mandatory. This module never posts to TikTok.
"""
from dataclasses import dataclass

@dataclass(frozen=True)
class HookBanner:
    text: str = "知らないと損する"
    start: float = 0.0
    end: float = 1.8
    y: int = 255
    height: int = 150
    font_size: int = 78

    def validate(self, width: int, height: int) -> None:
        if (width, height) != (1080, 1920):
            raise ValueError("hook banner requires 1080x1920")
        if not self.text.strip():
            raise ValueError("hook text is required")
        if not (0 <= self.start < self.end <= 3.0):
            raise ValueError("hook banner must stay within first 3 seconds")

    def ffmpeg_filters(self) -> str:
        safe = self.text.replace("'", "\\'").replace(":", "\\:")
        enable = f"between(t,{self.start:g},{self.end:g})"
        return (
            f"drawbox=x=90:y={self.y}:w=900:h={self.height}:"
            f"color=black@0.48:t=fill:enable='{enable}',"
            f"drawtext=text='{safe}':fontcolor=white:fontsize={self.font_size}:"
            f"borderw=3:bordercolor=black:x=(w-text_w)/2:y={self.y + 30}:"
            f"enable='{enable}'"
        )


def require_human_approval(approved: bool) -> None:
    if not approved:
        raise PermissionError("human quality/rights approval required before handoff")
