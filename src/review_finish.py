"""Review-only video finishing, never publication approval."""
import subprocess
from pathlib import Path


def finish_review(source: Path, target: Path, fps: int = 30) -> None:
    if fps not in (24, 30):
        raise ValueError("fps must be 24 or 30")
    if not source.is_file() or source.resolve() == target.resolve():
        raise ValueError("source must exist and target must differ")
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", str(source), "-vf", f"fps={fps},fade=t=in:st=0:d=0.35", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "copy", "-movflags", "+faststart", str(target)], check=True)
