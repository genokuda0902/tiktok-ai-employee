"""Optional low-strength debanding for 1080x1920 slide videos; free FFmpeg only."""
import argparse
import subprocess

def render(source, output):
    subprocess.run([
        "ffmpeg", "-hide_banner", "-y", "-i", source,
        "-vf", "deband=1thr=0.012:2thr=0.012:3thr=0.012:4thr=0.012:range=12:blur=1",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "19",
        "-pix_fmt", "yuv420p", "-c:a", "copy", "-movflags", "+faststart", output
    ], check=True)

if __name__ == "__main__":
    p=argparse.ArgumentParser()
    p.add_argument("source")
    p.add_argument("output")
    a=p.parse_args()
    render(a.source,a.output)
