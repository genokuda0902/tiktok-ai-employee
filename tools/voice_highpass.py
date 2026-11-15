"""Optional narration rumble reduction for 10-genre video pipeline."""
import subprocess
from pathlib import Path

def process(source: str, target: str, cutoff_hz: int = 75) -> None:
    if not 50 <= cutoff_hz <= 120:
        raise ValueError("cutoff_hz must be between 50 and 120")
    if not Path(source).is_file():
        raise FileNotFoundError(source)
    subprocess.run(["ffmpeg", "-y", "-i", source, "-map", "0:v:0", "-map", "0:a:0", "-c:v", "copy", "-af", f"highpass=f={cutoff_hz}", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", target], check=True)
