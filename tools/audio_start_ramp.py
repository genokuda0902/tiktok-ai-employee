"""Reusable zero-cost audio start ramp for image-slide TikTok videos."""
import subprocess
from pathlib import Path

def render(source: Path, target: Path, fade_seconds: float = 0.12):
    if not (0 < fade_seconds <= 0.5):
        raise ValueError("fade_seconds must be between 0 and 0.5")
    subprocess.run(["ffmpeg","-hide_banner","-loglevel","error","-y","-i",str(source),"-map","0:v:0","-map","0:a:0","-c:v","copy","-af",f"afade=t=in:st=0:d={fade_seconds}","-c:a","aac","-b:a","192k","-ar","48000","-movflags","+faststart",str(target)],check=True)
