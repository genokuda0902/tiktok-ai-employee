"""Reusable non-destructive opening fade for review-only MP4 files."""
import argparse
import subprocess
from pathlib import Path

def command(source: str, output: str, duration: float = 0.30) -> list[str]:
    if not 0.05 <= duration <= 1.0:
        raise ValueError("opening fade must be between 0.05 and 1.0 seconds")
    if Path(source).resolve() == Path(output).resolve():
        raise ValueError("never overwrite the source")
    return ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
            "-i", source, "-vf", f"fade=t=in:st=0:d={duration:.2f}",
            "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
            "-pix_fmt", "yuv420p", "-c:a", "copy", "-movflags", "+faststart", output]

def main():
    p = argparse.ArgumentParser()
    p.add_argument("source")
    p.add_argument("output")
    p.add_argument("--duration", type=float, default=0.30)
    a = p.parse_args()
    subprocess.run(command(a.source, a.output, a.duration), check=True)

if __name__ == "__main__":
    main()
