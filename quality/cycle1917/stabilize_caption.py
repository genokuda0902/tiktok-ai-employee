"""Stabilize the bottom caption-safe region using a pre-motion master video."""
import argparse
import subprocess
from pathlib import Path

def render(moving: Path, fixed: Path, output: Path, top: int = 1520):
    if not 0 <= top < 1920:
        raise ValueError("invalid caption top")
    output.parent.mkdir(parents=True, exist_ok=True)
    graph = f"[1:v]crop=1080:{1920-top}:0:{top}[captions];[0:v][captions]overlay=0:{top}:shortest=1[v]"
    subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
                    "-i", str(moving), "-i", str(fixed),
                    "-filter_complex", graph, "-map", "[v]", "-map", "0:a:0",
                    "-c:v", "libx264", "-preset", "veryfast", "-crf", "20",
                    "-pix_fmt", "yuv420p", "-c:a", "copy", "-movflags", "+faststart",
                    str(output)], check=True)

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("moving", type=Path)
    p.add_argument("fixed", type=Path)
    p.add_argument("output", type=Path)
    p.add_argument("--top", type=int, default=1520)
    a = p.parse_args()
    render(a.moving, a.fixed, a.output, a.top)
