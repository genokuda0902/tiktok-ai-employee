"""Cycle2039: conservative luma-only unsharp for slide typography.
Usage: python tools/cycle2039_text_clarity.py INPUT.mp4 OUTPUT.mp4
Never changes audio stream. Review only; no automatic publishing.
"""
import subprocess
import sys
from pathlib import Path

FILTER = "unsharp=5:5:0.42:3:3:0.0"

def enhance(source: Path, output: Path):
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
        "-i", str(source), "-vf", FILTER, "-c:v", "libx264",
        "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p",
        "-c:a", "copy", "-movflags", "+faststart", str(output)], check=True)

if __name__ == "__main__":
    enhance(Path(sys.argv[1]), Path(sys.argv[2]))
