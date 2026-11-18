"""Reusable AAC true-peak headroom guard."""
import subprocess
from pathlib import Path

def render(source: Path, target: Path, margin_db: float = 1.5):
    if not 0 < margin_db <= 6:
        raise ValueError("margin_db must be within (0, 6]")
    subprocess.run(["ffmpeg","-hide_banner","-loglevel","error","-y","-i",str(source),"-map","0:v:0","-map","0:a:0","-c:v","copy","-af",f"volume=-{margin_db}dB","-c:a","aac","-b:a","192k","-ar","48000","-movflags","+faststart",str(target)],check=True)
