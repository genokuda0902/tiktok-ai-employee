"""Cycle1573: improve midtone legibility while preserving Japanese audio/subtitles."""
import subprocess
from pathlib import Path

def render(source: Path, output: Path) -> None:
    subprocess.run([
        "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
        "-i", str(source), "-map", "0:v:0", "-map", "0:a?", "-map", "0:s?",
        "-vf", "eq=gamma=1.13:contrast=1.02:saturation=1.02",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "19",
        "-pix_fmt", "yuv420p", "-r", "30", "-c:a", "copy", "-c:s", "copy",
        "-movflags", "+faststart", str(output),
    ], check=True)

if __name__ == "__main__":
    import sys
    render(Path(sys.argv[1]), Path(sys.argv[2]))
