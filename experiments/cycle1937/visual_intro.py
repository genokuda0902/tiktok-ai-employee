"""Reusable silent visual fade-in for image-slide videos."""
import argparse
import subprocess
from pathlib import Path

def build_command(source: str, output: str, seconds: float = 0.32):
    if not (0.1 <= seconds <= 1.0):
        raise ValueError("fade duration must be between 0.1 and 1.0 seconds")
    if Path(source).resolve() == Path(output).resolve():
        raise ValueError("input and output must differ")
    return ["ffmpeg", "-hide_banner", "-y", "-i", source, "-vf", f"fade=t=in:st=0:d={seconds:.3f}", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p", "-c:a", "copy", "-movflags", "+faststart", output]

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("source"); p.add_argument("output"); p.add_argument("--seconds", type=float, default=0.32)
    a = p.parse_args()
    subprocess.run(build_command(a.source, a.output, a.seconds), check=True)
