"""Reusable caption contrast guard for vertical video."""
import subprocess
from pathlib import Path

def render(source: Path, target: Path, *, start_y: int = 1530, height: int = 250, opacity: float = 0.20):
    if not 0 <= opacity <= 0.4:
        raise ValueError("opacity out of range")
    if start_y < 0 or start_y + height > 1920:
        raise ValueError("caption zone outside canvas")
    vf = f"drawbox=x=0:y={start_y}:w=iw:h={height}:color=black@{opacity}:t=fill"
    subprocess.run(["ffmpeg","-y","-i",str(source),"-vf",vf,"-c:v","libx264","-crf","19","-pix_fmt","yuv420p","-c:a","copy","-movflags","+faststart",str(target)],check=True)
