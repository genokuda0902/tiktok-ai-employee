"""Zero-cost first-frame hook overlay for image-first TikTok renders.

Genre-independent visual hierarchy helper. No posting, paid API, or asset upload.
"""
from dataclasses import dataclass

@dataclass(frozen=True)
class HookOverlay:
    text: str
    start: float = 0.0
    end: float = 1.35
    font_size: int = 76
    top_band_height: int = 240

    def validate(self) -> None:
        if not self.text.strip():
            raise ValueError("hook text is required")
        if self.start != 0.0:
            raise ValueError("hook must start on frame zero")
        if not 0.8 <= self.end <= 1.5:
            raise ValueError("hook must clear quickly")
        if not 56 <= self.font_size <= 92:
            raise ValueError("font size outside mobile-safe range")
        if not 180 <= self.top_band_height <= 300:
            raise ValueError("top band outside safe range")

    def ffmpeg_filter(self, fontfile: str) -> str:
        self.validate()
        safe = self.text.replace("\\", "\\\\").replace("'", "\\'").replace(":", "\\:")
        return (
            f"drawbox=x=0:y=0:w=iw:h={self.top_band_height}:"
            f"color=black@0.22:t=fill:enable='between(t,{self.start},{self.end})',"
            f"drawtext=fontfile='{fontfile}':text='{safe}':fontcolor=white:"
            f"fontsize={self.font_size}:borderw=5:bordercolor=black:"
            f"x=(w-text_w)/2:y=72:enable='between(t,{self.start},{self.end})'"
        )
