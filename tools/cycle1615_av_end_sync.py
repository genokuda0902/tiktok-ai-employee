"""Reusable audio/video end fade for slide-based videos (10 genres)."""
import subprocess
from pathlib import Path

def render(source: Path, destination: Path, duration: float, fade_seconds: float = 0.5):
    if not 0 < fade_seconds <= duration:
        raise ValueError("invalid fade duration")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(source),
        "-map", "0:v:0", "-map", "0:a:0", "-c:v", "copy",
        "-af", f"afade=t=out:st={duration-fade_seconds:.3f}:d={fade_seconds:.3f}",
        "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart",
        str(destination)], check=True)
