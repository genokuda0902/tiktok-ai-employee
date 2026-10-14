#!/usr/bin/env python3
"""Cycle562: 15.6-second vertical video with pitch-preserving Japanese narration."""
from pathlib import Path
import argparse
import subprocess

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "assets" / "cycle561.mp4"
OUTPUT = ROOT / "output" / "cycle562_READABLE_PACING_JA_HUMAN_REVIEW.mp4"

def build(source=SOURCE, output=OUTPUT):
    source, output = Path(source), Path(output)
    if not source.is_file():
        raise FileNotFoundError(source)
    output.parent.mkdir(parents=True, exist_ok=True)
    command = [
        "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
        "-i", str(source),
        "-filter_complex",
        "[0:v]setpts=1.25*(PTS-STARTPTS),fps=30,format=yuv420p[v];"
        "[0:a]rubberband=tempo=0.8:transients=crisp:detector=compound[a]",
        "-map", "[v]", "-map", "[a]",
        "-t", "15.6", "-r", "30",
        "-c:v", "libx264", "-preset", "medium", "-crf", "18",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-ar", "48000", "-b:a", "192k",
        "-movflags", "+faststart", str(output)
    ]
    proc = subprocess.run(command, capture_output=True, text=True)
    if proc.returncode:
        raise RuntimeError(proc.stderr[-3000:])
    return output

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, default=SOURCE)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    print(build(args.source, args.output))
