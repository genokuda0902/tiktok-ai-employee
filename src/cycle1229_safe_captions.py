"""Review-only timed labels in TikTok safe area; NOT speech-synchronized subtitles."""
import argparse
import subprocess
from pathlib import Path

CAPTIONS = [(4.0, 6.8, "目的を先に伝える"), (9.0, 11.8, "条件を具体的にする"), (15.0, 17.8, "最後に内容を確認")]
FONT = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"

def filtergraph():
    filters = []
    for start, end, txt in CAPTIONS:
        enable = f"between(t\\,{start}\\,{end})"
        filters.append(f"drawbox=x=110:y=1450:w=860:h=125:color=black@0.78:t=fill:enable={enable}")
        filters.append(f"drawtext=fontfile={FONT}:text='{txt}':fontcolor=white:fontsize=56:x=(w-text_w)/2:y=1480:enable={enable}")
    return ",".join(filters)

def render(source, output):
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", str(source),
        "-vf", filtergraph(), "-map", "0:v:0", "-map", "0:a:0",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "23", "-pix_fmt", "yuv420p",
        "-c:a", "copy", "-movflags", "+faststart", str(output)], check=True)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    render(args.source, args.output)
