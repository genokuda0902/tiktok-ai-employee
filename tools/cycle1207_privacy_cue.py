"""Review-only privacy reminder overlay, applicable to all content genres."""
import argparse
import subprocess
from pathlib import Path

FONT = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
MESSAGE = "実践前チェック：個人情報を入力しない"

def video_filter(start=6.0, end=9.0):
    if not (0 <= start < end):
        raise ValueError("invalid display interval")
    gate = f"between(t,{start:g},{end:g})"
    return (
        f"drawbox=x=72:y=250:w=936:h=168:color=black@0.78:t=fill:enable='{gate}',"
        f"drawbox=x=72:y=250:w=12:h=168:color=0x34d399@1:t=fill:enable='{gate}',"
        f"drawtext=fontfile={FONT}:text='{MESSAGE}':fontcolor=white:"
        f"fontsize=42:x=108:y=310:enable='{gate}'"
    )

def render(source, destination):
    source, destination = Path(source), Path(destination)
    if not source.is_file():
        raise FileNotFoundError(source)
    destination.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
                    "-i", str(source), "-vf", video_filter(),
                    "-c:v", "libx264", "-preset", "veryfast", "-crf", "23",
                    "-c:a", "copy", "-movflags", "+faststart", str(destination)],
                   check=True)
    return destination

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("source")
    parser.add_argument("destination")
    args = parser.parse_args()
    render(args.source, args.destination)
