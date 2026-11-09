"""Corrected cycle1565 onset-aware fade; supersedes audio_onset.py (which faded silence)."""
import subprocess
from pathlib import Path

def render(source,target,fade_seconds=0.18,onset_seconds=0.32):
    if not 0 < fade_seconds <= 0.5: raise ValueError("invalid fade")
    if not Path(source).is_file(): raise FileNotFoundError(source)
    subprocess.run(["ffmpeg","-hide_banner","-loglevel","error","-y","-i",str(source),"-map","0","-c:v","copy","-c:s","copy","-c:a","aac","-b:a","192k","-af",f"afade=t=in:st={onset_seconds}:d={fade_seconds}","-movflags","+faststart",str(target)],check=True)
