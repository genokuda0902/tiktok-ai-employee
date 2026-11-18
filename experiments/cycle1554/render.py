"""Review-only MP4 from prior locally approved synthetic demo; adds original cue tones, NOT speech."""
import subprocess
from pathlib import Path
BASE = Path(__file__).resolve().parent
SOURCE = BASE.parent / "cycle1553" / "cycle1553_REVIEW_ONLY.mp4"
OUTPUT = BASE / "cycle1554_REVIEW_ONLY.mp4"

def render():
    if not SOURCE.is_file():
        raise FileNotFoundError("Prior synthetic MP4 missing: " + str(SOURCE))
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
        "-i", str(SOURCE), "-f", "lavfi", "-i",
        "sine=frequency=660:sample_rate=48000:duration=12",
        "-filter_complex", "[1:a]volume='if(lt(mod(t,3),0.12),0.10,0)':eval=frame[a]",
        "-map", "0:v:0", "-map", "[a]", "-c:v", "copy",
        "-c:a", "aac", "-b:a", "96k", "-movflags", "+faststart", str(OUTPUT)], check=True)

if __name__ == "__main__":
    render()
