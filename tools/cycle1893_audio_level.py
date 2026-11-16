"""Normalize voice loudness without altering video frames."""
from pathlib import Path
import subprocess

def normalize(source: Path, output: Path):
    if not source.is_file():
        raise FileNotFoundError(source)
    subprocess.run(["ffmpeg","-y","-i",str(source),"-map","0:v:0","-map","0:a:0","-c:v","copy","-af","loudnorm=I=-16:TP=-1.5:LRA=11","-c:a","aac","-b:a","192k","-ar","48000","-movflags","+faststart",str(output)],check=True)
