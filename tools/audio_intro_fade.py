"""Reusable, zero-cost narration intro fade for slide videos."""
import subprocess
from pathlib import Path

def build(input_mp4: Path, output_mp4: Path, seconds: float = 0.18) -> None:
    if not 0.05 <= seconds <= 1.0:
        raise ValueError("fade duration must be between 0.05 and 1.0 seconds")
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", str(input_mp4), "-map", "0:v:0", "-map", "0:a:0", "-c:v", "copy", "-af", f"afade=t=in:st=0:d={seconds}", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", str(output_mp4)], check=True)
