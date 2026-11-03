"""Review-only caption-region contrast treatment; not a subtitle-sync validator."""
from pathlib import Path
import subprocess

def caption_contrast_filter(width=1080, height=1920, start_ratio=1370/1920, opacity=0.12):
    if width <= 0 or height <= 0 or not (0 <= start_ratio < 1) or not (0 <= opacity <= 0.3):
        raise ValueError("invalid caption-region settings")
    start = round(height * start_ratio)
    return f"drawbox=x=0:y={start}:w=iw:h={height-start}:color=black@{opacity}:t=fill"

def render(source: Path, target: Path):
    if not source.is_file():
        raise FileNotFoundError(source)
    target.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["ffmpeg","-y","-i",str(source),"-vf",caption_contrast_filter(),
                    "-c:v","libx264","-preset","veryfast","-crf","18",
                    "-pix_fmt","yuv420p","-c:a","copy","-movflags","+faststart",str(target)],check=True)
