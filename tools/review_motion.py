"""Review-only gentle camera motion. Requires FFmpeg; never claims narration."""
import argparse
import subprocess
from pathlib import Path

def filtergraph(width=1080, height=1920, fps=30, max_zoom=1.045):
    if width < 1 or height < 1 or fps < 1 or not 1 <= max_zoom <= 1.10:
        raise ValueError("invalid motion settings")
    step = (max_zoom - 1) / (15 * fps)
    return (f"zoompan=z='min(zoom+{step:.9f},{max_zoom})':"
            f"x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':"
            f"d=1:s={width}x{height}:fps={fps},format=yuv420p")

def render(source, output):
    source, output = Path(source), Path(output)
    if not source.is_file() or source.resolve() == output.resolve():
        raise ValueError("source missing or output overwrites source")
    output.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["ffmpeg", "-y", "-i", str(source), "-vf", filtergraph(),
                    "-an", "-c:v", "libx264", "-pix_fmt", "yuv420p",
                    "-movflags", "+faststart", str(output)], check=True)

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("source")
    p.add_argument("output")
    a = p.parse_args()
    render(a.source, a.output)
