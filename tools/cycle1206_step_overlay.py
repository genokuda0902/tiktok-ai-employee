"""Review-only reusable three-step visual guide for vertical MP4 videos."""
import argparse
import subprocess
from pathlib import Path

FONT = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"

def build_filter(start=15.0, end=20.0):
    if not 0 <= start < end:
        raise ValueError("invalid time window")
    e = f"between(t\\,{start:g}\\,{end:g})"
    boxes = [
        f"drawbox=x=90:y=300:w=900:h=750:color=0x07152d@0.93:t=fill:enable={e}",
        f"drawbox=x=90:y=300:w=12:h=750:color=0x22d3ee:t=fill:enable={e}",
    ]
    lines = ["3ステップで実践", "① 目的を決める", "② 条件を伝える", "③ 結果を確認する"]
    for i, line in enumerate(lines):
        boxes.append(
            f"drawtext=fontfile={FONT}:text='{line}':fontcolor=white:"
            f"fontsize={60 if i == 0 else 51}:x=140:y={370 + i * 160}:enable={e}"
        )
    return ",".join(boxes)

def render(src, dst):
    src, dst = Path(src), Path(dst)
    if not src.is_file():
        raise FileNotFoundError(src)
    if not Path(FONT).is_file():
        raise FileNotFoundError(FONT)
    dst.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run([
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-i", str(src), "-vf", build_filter(), "-map", "0:v:0",
        "-map", "0:a:0", "-c:v", "libx264", "-preset", "veryfast",
        "-crf", "21", "-pix_fmt", "yuv420p", "-c:a", "copy",
        "-movflags", "+faststart", str(dst)
    ], check=True)

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("src")
    p.add_argument("dst")
    a = p.parse_args()
    render(a.src, a.dst)
