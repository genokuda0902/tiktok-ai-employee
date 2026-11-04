"""Overlay a clearly disclosed illustrative example on a review-only MP4.

This is not a recording of real PC operation. Requires FFmpeg and Noto CJK.
"""
import subprocess
from pathlib import Path

def build_filter(font: str) -> str:
    if not Path(font).is_file():
        raise FileNotFoundError(font)
    window = "enable='between(t,8,15)'"
    return ",".join([
        f"drawbox=x=100:y=950:w=880:h=310:color=0x0b1220@0.93:t=fill:{window}",
        f"drawbox=x=100:y=950:w=12:h=310:color=0x38bdf8:t=fill:{window}",
        f"drawtext=fontfile={font}:text='操作イメージ（実演ではありません）':fontsize=36:fontcolor=white:x=150:y=985:{window}",
        f"drawtext=fontfile={font}:text='目的 → 条件 → 出力形式':fontsize=47:fontcolor=0x7dd3fc:x=150:y=1085:{window}",
    ])

def render(source: Path, target: Path, font: str) -> None:
    if not source.is_file():
        raise FileNotFoundError(source)
    target.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["ffmpeg","-hide_banner","-loglevel","error","-y",
        "-i",str(source),"-vf",build_filter(font),"-c:v","libx264",
        "-preset","veryfast","-crf","21","-pix_fmt","yuv420p",
        "-c:a","copy","-movflags","+faststart",str(target)],check=True)

if __name__ == "__main__":
    import argparse
    p=argparse.ArgumentParser()
    p.add_argument("source",type=Path); p.add_argument("target",type=Path)
    p.add_argument("--font",default="/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc")
    a=p.parse_args()
    render(a.source,a.target,a.font)
