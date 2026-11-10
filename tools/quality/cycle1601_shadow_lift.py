"""Subtle brightness lift for dark 1080x1920 Japanese slides; zero-cost ffmpeg."""
import subprocess
import sys
from pathlib import Path

def render(source: Path, target: Path):
    target.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", str(source),
        "-vf", "eq=brightness=0.012:gamma=1.02:saturation=1.0,format=yuv420p",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
        "-c:a", "copy", "-movflags", "+faststart", str(target)], check=True)

if __name__ == "__main__":
    render(Path(sys.argv[1]), Path(sys.argv[2]))
