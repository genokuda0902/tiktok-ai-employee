"""Reusable subtle progress indicator for vertical videos."""
import argparse
import json
import subprocess
from pathlib import Path

def progress_filter(duration: float, segments: int = 24, height: int = 5) -> str:
    if duration <= 0 or not 1 <= segments <= 100 or height < 1:
        raise ValueError("invalid progress settings")
    return ",".join(
        f"drawbox=x=iw*{i}/{segments}:y=0:w=iw/{segments}+1:h={height}:"
        f"color=white@0.85:t=fill:enable='gte(t,{duration*i/segments:.4f})'"
        for i in range(segments)
    )

def render(source: Path, target: Path):
    info = json.loads(subprocess.check_output(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "json", str(source)]))
    subprocess.run(
        ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", str(source),
         "-vf", progress_filter(float(info["format"]["duration"])),
         "-c:v", "libx264", "-preset", "veryfast", "-crf", "19",
         "-pix_fmt", "yuv420p", "-c:a", "copy",
         "-movflags", "+faststart", str(target)], check=True)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("target", type=Path)
    args = parser.parse_args()
    render(args.source, args.target)
