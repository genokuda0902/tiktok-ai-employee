"""Conservative, reusable TikTok speech cleanup."""
import subprocess
from pathlib import Path

def build_command(source: str, destination: str) -> list[str]:
    if Path(source).resolve() == Path(destination).resolve():
        raise ValueError("Input and output must differ")
    return ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", source,
            "-map", "0:v:0", "-map", "0:a:0", "-c:v", "copy",
            "-af", "highpass=f=75,alimiter=limit=0.95",
            "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
            "-movflags", "+faststart", destination]

def render(source: str, destination: str) -> None:
    subprocess.run(build_command(source, destination), check=True)
