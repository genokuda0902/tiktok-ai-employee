"""Cycle1535 review-only chapter overlay; source MP4 is an explicit input."""
import json
import subprocess
import sys
from pathlib import Path

FONT = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
CHAPTERS = [(0, 1.5, "課題を確認"), (1.5, 5, "操作を実演"), (5, 9, "結果を確認"), (9, 12, "手順を復習")]

def chapter(t):
    return next((label for start, end, label in CHAPTERS if start <= t < end), CHAPTERS[-1][2])

def render(source, output):
    source, output = Path(source), Path(output)
    info = json.loads(subprocess.check_output(["ffprobe", "-v", "error", "-show_format", "-of", "json", str(source)]))
    duration = float(info["format"]["duration"])
    if not 11.5 <= duration <= 12.5:
        raise ValueError("expected 12-second source")
    filters = []
    for start, end, label in CHAPTERS:
        enable = f"between(t,{start},{end})"
        filters += [
            f"drawbox=x=32:y=36:w=340:h=66:color=0x071827@0.85:t=fill:enable='{enable}'",
            f"drawtext=fontfile={FONT}:text='{label}':fontsize=29:fontcolor=white:x=50:y=49:enable='{enable}'",
        ]
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(source), "-vf", ",".join(filters),
                    "-map", "0:v:0", "-map", "0:s?", "-c:v", "libx264", "-preset", "veryfast",
                    "-crf", "21", "-pix_fmt", "yuv420p", "-c:s", "copy",
                    "-movflags", "+faststart", str(output)], check=True)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit("usage: python chapter_overlay.py SOURCE.mp4 OUTPUT.mp4")
    render(sys.argv[1], sys.argv[2])
