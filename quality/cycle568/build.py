"""Cycle568: use the original scene04 running/success PNGs from the user ZIP.
Requires ffmpeg and the ZIP's assets/cycle567.mp4.
Do not post automatically. Existing media rights require human review.
"""
from pathlib import Path
import shutil
import subprocess

START_FRAME = 215
N = 29

def build(root: Path):
    root = Path(root)
    frames = root / "output" / "frames"
    frames.mkdir(parents=True, exist_ok=True)
    states = [
        root / "assets" / "scene04_running.png",
        root / "assets" / "scene04_success.png",
    ]
    for i in range(N):
        dest = frames / f"frame{i:03d}.png"
        shutil.copyfile(states[0 if i < 14 else 1], dest)
    source = root / "assets" / "cycle567.mp4"
    target = root / "output" / "cycle568_CODE_REVEAL_JA_HUMAN_REVIEW.mp4"
    graph = (
        "[1:v]format=rgba,setpts=PTS+215/30/TB[p];"
        "[0:v][p]overlay=50:375:eof_action=pass:repeatlast=0:"
        "format=auto,format=yuv420p[v]"
    )
    subprocess.run([
        "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
        "-i", str(source), "-framerate", "30", "-start_number", "0",
        "-i", str(frames / "frame%03d.png"),
        "-filter_complex", graph, "-map", "[v]", "-map", "0:a:0",
        "-c:v", "libx264", "-preset", "ultrafast", "-crf", "19",
        "-r", "30", "-pix_fmt", "yuv420p", "-c:a", "copy",
        "-t", "15.6", "-movflags", "+faststart", str(target)
    ], check=True)
    return target

if __name__ == "__main__":
    print(build(Path(__file__).resolve().parent))
