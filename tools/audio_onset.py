"""Reusable MP4 audio onset fade for ten categories; manual publishing only."""
import subprocess
from pathlib import Path

def smooth_onset(source: str, target: str, seconds: float = 0.12) -> None:
    if not 0 < seconds <= 0.5:
        raise ValueError("fade seconds must be in (0, 0.5]")
    if not Path(source).is_file():
        raise FileNotFoundError(source)
    subprocess.run(["ffmpeg","-hide_banner","-loglevel","error","-y","-i",source,"-map","0:v:0","-map","0:a:0","-c:v","copy","-af",f"afade=t=in:st=0:d={seconds}","-c:a","aac","-b:a","192k","-ar","48000","-movflags","+faststart",target],check=True)
