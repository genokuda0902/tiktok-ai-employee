"""Zero-cost image-first Ken Burns motion contract.

Keeps motion subtle so generated image copy stays readable.
Human approval remains mandatory; this module never posts.
"""

from dataclasses import dataclass

@dataclass(frozen=True)
class MotionProfile:
    zoom_per_frame: float = 0.0007
    max_zoom: float = 1.035
    fps: int = 30
    width: int = 1080
    height: int = 1920

    def validate(self) -> None:
        if not (0 < self.zoom_per_frame <= 0.001):
            raise ValueError("zoom_per_frame must stay subtle")
        if not (1.0 < self.max_zoom <= 1.04):
            raise ValueError("max_zoom exceeds readability guard")
        if (self.width, self.height) != (1080, 1920):
            raise ValueError("TikTok portrait output must be 1080x1920")
        if self.fps != 30:
            raise ValueError("delivery fps must be 30")

def ffmpeg_filter(profile: MotionProfile = MotionProfile()) -> str:
    profile.validate()
    return (
        "scale=1200:2134:force_original_aspect_ratio=increase,"
        "crop=1200:2134,"
        f"zoompan=z='min(zoom+{profile.zoom_per_frame},{profile.max_zoom})':"
        "x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':"
        f"d=1:s={profile.width}x{profile.height}:fps={profile.fps},"
        "format=yuv420p"
    )
