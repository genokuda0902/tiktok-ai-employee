"""Apply short audio fades aligned with existing video fades. Zero paid dependencies."""
import json
import subprocess
from pathlib import Path

def render(source: Path, target: Path, fade: float = 0.25) -> float:
    metadata = json.loads(subprocess.check_output(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "json", str(source)]))
    duration = float(metadata["format"]["duration"])
    if duration <= fade * 2:
        raise ValueError("Video too short for fades")
    filter_chain = (
        f"afade=t=in:st=0:d={fade},"
        f"afade=t=out:st={duration-fade:.4f}:d={fade}")
    subprocess.run(
        ["ffmpeg", "-y", "-v", "error", "-i", str(source),
         "-map", "0:v:0", "-map", "0:a:0", "-c:v", "copy",
         "-af", filter_chain, "-c:a", "aac", "-b:a", "192k",
         "-ar", "48000", "-movflags", "+faststart", str(target)],
        check=True)
    return duration
