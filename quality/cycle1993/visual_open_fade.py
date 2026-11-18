"""Subtle opening fade for vertical MP4. Preserve original narration."""
import subprocess
from pathlib import Path

def render(src, dst, fade_seconds=0.20):
    if not 0.05 <= fade_seconds <= 0.5:
        raise ValueError("fade_seconds must be 0.05..0.5")
    Path(dst).parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["ffmpeg","-hide_banner","-loglevel","error","-y","-i",src,"-vf",f"fade=t=in:st=0:d={fade_seconds:.3f}","-c:v","libx264","-preset","veryfast","-crf","19","-pix_fmt","yuv420p","-c:a","copy","-movflags","+faststart",dst],check=True)
