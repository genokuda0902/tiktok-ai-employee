"""Reusable 10-category vertical video encoder. Uses local FFmpeg only."""
import subprocess
from pathlib import Path

def encode(source: Path, destination: Path, crf: int = 19):
    if not 0 <= crf <= 51:
        raise ValueError("CRF must be 0..51")
    subprocess.run(["ffmpeg","-y","-v","error","-i",str(source),"-map","0:v:0","-map","0:a:0","-c:v","libx264","-preset","medium","-crf",str(crf),"-pix_fmt","yuv420p","-g","60","-keyint_min","60","-sc_threshold","0","-c:a","copy","-movflags","+faststart",str(destination)],check=True)
