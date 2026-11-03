"""Review-only transition renderer; approved local input only."""
import argparse
import subprocess
from pathlib import Path

def fade_filter(cuts=(3.0, 6.0, 20.5), half=0.12):
    if half <= 0 or any(t <= half for t in cuts):
        raise ValueError("invalid transition time")
    if list(cuts) != sorted(set(cuts)):
        raise ValueError("cuts must be sorted and unique")
    return ",".join(
        f"fade=t=out:st={t-half:.3f}:d={half:.3f},fade=t=in:st={t:.3f}:d={half:.3f}"
        for t in cuts
    )

def render(src, dst, approved_local_review=False):
    if not approved_local_review:
        raise ValueError("local review authorization required")
    subprocess.run([
        "ffmpeg", "-hide_banner", "-y", "-i", str(src),
        "-vf", fade_filter(), "-c:v", "libx264", "-preset", "veryfast",
        "-crf", "19", "-pix_fmt", "yuv420p", "-c:a", "copy",
        "-movflags", "+faststart", str(dst)
    ], check=True)

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("source", type=Path)
    p.add_argument("output", type=Path)
    p.add_argument("--local-review-only", action="store_true")
    a = p.parse_args()
    render(a.source, a.output, a.local_review_only)
