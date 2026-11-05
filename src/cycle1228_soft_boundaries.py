"""Genre-neutral fade-in/out for review-only MP4s. Does not certify audio/caption quality."""
from pathlib import Path
import subprocess


def render_soft_boundaries(source: Path, destination: Path, duration: float, fade: float = 0.35) -> None:
    if duration <= 2 * fade or fade <= 0:
        raise ValueError("fade must fit inside positive duration")
    if not source.is_file():
        raise FileNotFoundError(source)
    destination.parent.mkdir(parents=True, exist_ok=True)
    end = duration - fade
    vf = f"fade=t=in:st=0:d={fade},fade=t=out:st={end}:d={fade}"
    af = f"afade=t=in:st=0:d={fade},afade=t=out:st={end}:d={fade}"
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", str(source),
                    "-vf", vf, "-af", af, "-c:v", "libx264", "-crf", "24",
                    "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", str(destination)], check=True)
