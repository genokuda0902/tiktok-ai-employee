"""Reusable zero-cost audio normalization; keep video and subtitle streams."""
import subprocess
from pathlib import Path

def normalize(src: Path, dst: Path):
    if src.resolve() == dst.resolve():
        raise ValueError("Input and output must differ")
    subprocess.run(["ffmpeg","-hide_banner","-y","-i",str(src),"-map","0:v:0","-map","0:a:0","-map","0:s?","-c:v","copy","-af","loudnorm=I=-16:TP=-1.5:LRA=11","-c:a","aac","-b:a","192k","-c:s","copy","-movflags","+faststart",str(dst)],check=True)
