"""Reusable loss-conscious review export for ten slide-video genres."""
import subprocess
from pathlib import Path

def encode(source: Path, output: Path, crf: int = 16):
    if not 0 <= crf <= 51:
        raise ValueError("CRF out of range")
    subprocess.run(["ffmpeg","-hide_banner","-loglevel","error","-y","-i",str(source),"-map","0:v:0","-map","0:a:0","-c:v","libx264","-preset","medium","-crf",str(crf),"-pix_fmt","yuv420p","-movflags","+faststart","-c:a","copy",str(output)],check=True)
