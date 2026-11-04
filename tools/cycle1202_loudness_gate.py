"""Reusable FFmpeg loudness normalization for approved review-only video."""
import subprocess
from pathlib import Path

def normalize(input_path: Path, output_path: Path, target_lufs: int = -16):
    if not -24 <= target_lufs <= -12:
        raise ValueError("target LUFS outside safe configured range")
    if input_path.resolve() == output_path.resolve():
        raise ValueError("input and output must differ")
    if not input_path.is_file():
        raise FileNotFoundError(input_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    command = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i",
               str(input_path), "-map", "0:v:0", "-map", "0:a:0",
               "-c:v", "copy", "-af", f"loudnorm=I={target_lufs}:TP=-1.5:LRA=11",
               "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart",
               str(output_path)]
    subprocess.run(command, check=True)
    return output_path
