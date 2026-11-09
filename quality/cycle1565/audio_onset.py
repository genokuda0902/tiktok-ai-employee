"""Reusable 0.18s narration onset fade for image-slide videos (10 genres)."""
import subprocess
from pathlib import Path

def render(source, target, fade_seconds=0.18):
    if not 0 < fade_seconds <= 0.5:
        raise ValueError("fade_seconds must be in (0, 0.5]")
    if not Path(source).is_file():
        raise FileNotFoundError(source)
    subprocess.run(["ffmpeg","-hide_banner","-loglevel","error","-y","-i",str(source),"-map","0","-c:v","copy","-c:s","copy","-c:a","aac","-b:a","192k","-af",f"afade=t=in:st=0:d={fade_seconds}","-movflags","+faststart",str(target)],check=True)
