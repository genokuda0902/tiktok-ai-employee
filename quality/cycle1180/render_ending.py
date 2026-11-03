"""Review-only closing fade. Uses an already approved-for-review source; never publishes."""
import argparse
import subprocess
from pathlib import Path

def render(source: Path, output: Path, duration: float = 23.033333, fade_seconds: float = 0.45):
    if not source.is_file():
        raise FileNotFoundError(source)
    if not 0.15 <= fade_seconds <= 1.0 or duration <= fade_seconds:
        raise ValueError("Invalid fade timing")
    output.parent.mkdir(parents=True, exist_ok=True)
    cmd = ["ffmpeg", "-y", "-i", str(source), "-vf",
           f"fade=t=out:st={duration-fade_seconds:.4f}:d={fade_seconds:.4f}",
           "-c:v", "libx264", "-preset", "veryfast", "-crf", "19",
           "-pix_fmt", "yuv420p", "-c:a", "copy", "-movflags", "+faststart", str(output)]
    subprocess.run(cmd, check=True)

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("source", type=Path)
    p.add_argument("output", type=Path)
    args = p.parse_args()
    render(args.source, args.output)
