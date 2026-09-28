"""Zero-cost retention progress overlay for image-slide videos.

The overlay is intentionally tiny and genre-independent: it gives viewers a
continuous sense of progress without changing narration, captions, source
images, or posting state. Human quality/rights approval remains mandatory.
"""

TARGET_WIDTH = 1080
TARGET_HEIGHT = 1920
DEFAULT_HEIGHT = 10


def progress_filter(duration_s: float, *, height: int = DEFAULT_HEIGHT) -> str:
    """Return an ffmpeg filter for a subtle top-edge progress indicator."""
    if duration_s <= 0:
        raise ValueError("duration_s must be positive")
    if not 2 <= height <= 24:
        raise ValueError("height must be between 2 and 24 pixels")
    return (
        f"drawbox=x=0:y=0:w=iw:h={height}:color=black@0.12:t=fill,"
        f"drawbox=x=0:y=0:w='iw*min(t/{duration_s:.6f},1)':h={height}:"
        "color=white@0.95:t=fill"
    )


def validate_delivery(width: int, height: int, has_audio: bool, black_segment_s: float) -> None:
    """Fail closed on the technical conditions required by this route."""
    if (width, height) != (TARGET_WIDTH, TARGET_HEIGHT):
        raise ValueError("image-slide delivery must be 1080x1920")
    if not has_audio:
        raise ValueError("Japanese narration/audio stream is required")
    if black_segment_s >= 0.5:
        raise ValueError("long black segment detected")


REQUIRES_HUMAN_APPROVAL = True
AUTO_POST_ALLOWED = False
