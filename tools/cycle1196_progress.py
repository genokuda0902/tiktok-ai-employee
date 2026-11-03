"""Review-only playback progress cue for ten genre templates. No publishing."""
import subprocess
from pathlib import Path


def progress_filter(duration: float, width: int = 1080, height: int = 1920) -> str:
    if duration <= 0 or width < 320 or height < 480:
        raise ValueError("invalid video dimensions or duration")
    left = round(width * 80 / 1080)
    bar_width = width - 2 * left
    y = round(height * 1830 / 1920)
    return (f"drawbox=x={left}:y={y}:w={bar_width}:h=8:color=white@0.18:t=fill,"
            f"drawbox=x={left}:y={y}:w='min({bar_width},{bar_width}*t/{duration:.6f})':h=8:"
            "color=0x38bdf8@0.85:t=fill")


def render(source: Path, output: Path, duration: float) -> None:
    if not source.is_file() or source.resolve() == output.resolve():
        raise ValueError("source missing or output equals source")
    subprocess.run(["ffmpeg", "-y", "-i", str(source), "-vf", progress_filter(duration),
                    "-c:v", "libx264", "-preset", "ultrafast", "-crf", "20",
                    "-pix_fmt", "yuv420p", "-c:a", "copy", "-movflags", "+faststart",
                    str(output)], check=True)
