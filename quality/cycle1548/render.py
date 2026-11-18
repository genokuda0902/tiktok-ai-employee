"""Review-only: add quiet non-speech cues to a locally approved synthetic MP4.
Never infer Japanese narration from the presence of AAC audio.
"""
from pathlib import Path
import argparse
import subprocess

def render(src: Path, dst: Path):
    if not src.is_file():
        raise FileNotFoundError(src)
    dst.parent.mkdir(parents=True, exist_ok=True)
    audio = r"aevalsrc=0.025*sin(2*PI*660*t)*exp(-18*mod(t\,3)):s=48000:d=12"
    subprocess.run([
        "ffmpeg", "-y", "-v", "error", "-i", str(src),
        "-f", "lavfi", "-i", audio,
        "-map", "0:v:0", "-map", "1:a:0",
        "-c:v", "copy", "-c:a", "aac", "-b:a", "128k",
        "-t", "12", "-movflags", "+faststart", str(dst)
    ], check=True)
    return dst

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("source", type=Path)
    p.add_argument("output", type=Path)
    a = p.parse_args()
    render(a.source, a.output)
