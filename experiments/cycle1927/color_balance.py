"""Gentle slide color adjustment, common to all genres."""
import subprocess
from pathlib import Path

def render(source, destination, saturation=1.035, contrast=1.008):
    if not 0.95 <= saturation <= 1.08 or not 0.98 <= contrast <= 1.04:
        raise ValueError("Adjustment outside conservative limits")
    if not Path(source).is_file():
        raise FileNotFoundError(source)
    subprocess.run(["ffmpeg","-y","-i",source,"-vf",f"eq=saturation={saturation}:contrast={contrast}","-c:v","libx264","-preset","ultrafast","-crf","19","-pix_fmt","yuv420p","-c:a","copy","-movflags","+faststart",destination],check=True)
    return destination
