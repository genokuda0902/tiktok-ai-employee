"""Zero-cost micro-parallax profile for the approved image-slide route.

Reimplementation helper: adds restrained continuous motion without changing
narration/caption timing. Human quality/rights approval remains mandatory.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class MicroParallaxProfile:
    width: int = 1080
    height: int = 1920
    scale_width: int = 1110
    scale_height: int = 1973
    x_amplitude_px: int = 8
    y_amplitude_px: int = 6
    x_period_frames: int = 120
    y_period_frames: int = 150

    def validate(self) -> None:
        if (self.width, self.height) != (1080, 1920):
            raise ValueError("TikTok image-slide output must be 1080x1920")
        if self.scale_width < self.width or self.scale_height < self.height:
            raise ValueError("scaled canvas must cover output")
        if self.x_amplitude_px > 12 or self.y_amplitude_px > 10:
            raise ValueError("parallax exceeds restrained mobile-safe motion")

    def ffmpeg_filter(self) -> str:
        self.validate()
        return (
            f"scale={self.scale_width}:{self.scale_height}:flags=lanczos,"
            f"crop={self.width}:{self.height}:"
            f"x='15+{self.x_amplitude_px}*sin(2*PI*n/{self.x_period_frames})':"
            f"y='26+{self.y_amplitude_px}*cos(2*PI*n/{self.y_period_frames})'"
        )


def require_human_approval(approved: bool) -> None:
    if not approved:
        raise PermissionError("Human quality/rights approval required; no auto-posting")
