"""Review-only reimplementation: burn timed Japanese SRT onto an approved synthetic MP4.
Requires ffmpeg with libass. Never posts or delivers automatically.
"""
from pathlib import Path
import subprocess
import sys

def render(source: Path, captions: Path, output: Path) -> None:
    if not source.is_file() or not captions.is_file():
        raise FileNotFoundError("source video and SRT are required")
    if output.resolve() == source.resolve():
        raise ValueError("refuse to overwrite source")
    output.parent.mkdir(parents=True, exist_ok=True)
    filter_arg = ("subtitles=" + str(captions.resolve()).replace("\\", "\\\\").replace(":", "\\:")
                  + ":force_style='FontName=Noto Sans CJK JP,FontSize=17,"
                    "PrimaryColour=&H00FFFFFF,OutlineColour=&H00101010,"
                    "BorderStyle=3,BackColour=&H99000000,MarginV=140,Alignment=2'")
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
                    "-i", str(source), "-vf", filter_arg, "-c:v", "libx264",
                    "-preset", "veryfast", "-crf", "22", "-pix_fmt", "yuv420p",
                    "-movflags", "+faststart", "-an", str(output)], check=True)
if __name__ == "__main__":
    if len(sys.argv) != 4:
        raise SystemExit("usage: render.py INPUT.mp4 CAPTIONS.srt OUTPUT.mp4")
    render(*(Path(arg) for arg in sys.argv[1:]))
