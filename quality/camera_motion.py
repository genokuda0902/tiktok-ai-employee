"""Shared gentle camera motion for image-first, review-only videos."""
def camera_filter(seconds=2.5, fps=24):
    if seconds <= 0 or fps <= 0:
        raise ValueError("duration and fps must be positive")
    return (f"zoompan=z='min(zoom+0.00028,1.021)':"
            f"x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':"
            f"d={round(seconds*fps)}:s=1080x1920:fps={fps},format=yuv420p")
