"""Render 4 timed Japanese instruction overlays on a preapproved review-only MP4.

Usage: python tools/cycle1545_overlay.py INPUT.mp4 OUTPUT.mp4
Never use confidential or unapproved input. Does not provide narration.
"""
import argparse
import subprocess
from pathlib import Path

FONT = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
STEPS = (("① 数字を選ぶ", 0, 3), ("② SUM関数を入力", 3, 6),
         ("③ Enterで計算", 6, 9), ("④ 結果を確認", 9, 12))


def build_filter(font=FONT):
    parts = []
    for i, (text, start, end) in enumerate(STEPS):
        parts.append(f"drawbox=x=65:y={365+i*95}:w=590:h=80:color=0x22d3ee@0.55:t=5:enable='between(t,{start},{end})'")
        parts.append(f"drawtext=fontfile={font}:text='{text}':fontsize=38:fontcolor=white:box=1:boxcolor=0x142438@0.93:boxborderw=16:x=80:y=930:enable='between(t,{start},{end})'")
    parts.append(f"drawtext=fontfile={font}:text='REVIEW ONLY / 音声未完成':fontsize=23:fontcolor=white:box=1:boxcolor=0x7f1d1d@0.95:boxborderw=8:x=20:y=20")
    return ",".join(parts)


def render(source, output):
    source, output = Path(source), Path(output)
    if not source.is_file():
        raise FileNotFoundError(source)
    if source.resolve() == output.resolve():
        raise ValueError("Input and output must differ")
    output.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["ffmpeg", "-y", "-i", str(source), "-f", "lavfi",
                    "-i", "sine=frequency=520:sample_rate=44100:duration=12",
                    "-filter_complex", f"[0:v]{build_filter()}[v];[1:a]volume=0.09[a]",
                    "-map", "[v]", "-map", "[a]", "-t", "12",
                    "-c:v", "libx264", "-pix_fmt", "yuv420p",
                    "-c:a", "aac", "-movflags", "+faststart", str(output)], check=True)
    return output


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("source")
    parser.add_argument("output")
    args = parser.parse_args()
    render(args.source, args.output)
