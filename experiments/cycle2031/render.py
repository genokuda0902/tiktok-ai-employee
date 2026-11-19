"""Reusable visual intro fade for image slides, independent of genre."""
import subprocess
import sys

def render(source, target, seconds=0.35):
    if not 0.1 <= seconds <= 1.0:
        raise ValueError("fade duration outside supported range")
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
        "-i", source, "-vf", f"fade=t=in:st=0:d={seconds}",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "19",
        "-pix_fmt", "yuv420p", "-c:a", "copy", "-movflags", "+faststart", target], check=True)

if __name__ == "__main__":
    render(sys.argv[1], sys.argv[2])
