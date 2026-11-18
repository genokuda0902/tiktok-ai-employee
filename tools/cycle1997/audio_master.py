"""Reusable zero-cost TikTok audio master, all 10 genres."""
import argparse
import subprocess
from pathlib import Path

def master(src: Path, dst: Path):
    if not src.is_file():
        raise FileNotFoundError(src)
    dst.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run([
        "ffmpeg", "-hide_banner", "-y", "-i", str(src),
        "-map", "0:v:0", "-map", "0:a:0", "-c:v", "copy",
        "-af", "loudnorm=I=-16:TP=-3.0:LRA=11,aresample=48000",
        "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart",
        str(dst),
    ], check=True)
    return dst

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("input", type=Path)
    p.add_argument("output", type=Path)
    a = p.parse_args()
    master(a.input, a.output)
