"""Review-only narration edge smoothing. No automatic publishing."""
import argparse
import subprocess
from pathlib import Path

def build_command(source: Path, target: Path, duration: float, fade_in: float = .12, fade_out: float = .25):
    if not source.is_file() or source.resolve() == target.resolve():
        raise ValueError("Missing input or unsafe same-path output")
    if duration <= 0 or not (0 <= fade_in < duration) or not (0 <= fade_out < duration):
        raise ValueError("Invalid fade duration")
    af = f"afade=t=in:st=0:d={fade_in},afade=t=out:st={duration-fade_out:.3f}:d={fade_out}"
    return ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", str(source), "-map", "0:v:0", "-map", "0:a:0", "-c:v", "copy", "-af", af, "-c:a", "aac", "-b:a", "160k", "-ar", "48000", "-metadata:s:a:0", "language=jpn", "-movflags", "+faststart", str(target)]

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("source", type=Path)
    p.add_argument("target", type=Path)
    p.add_argument("--duration", type=float, required=True)
    a = p.parse_args()
    subprocess.run(build_command(a.source, a.target, a.duration), check=True)
