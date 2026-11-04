"""Review-only timed focus card overlay. No automatic publishing."""
import argparse
import subprocess
from pathlib import Path

def focus_filter(start=12.0, end=16.0, font="/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"):
    if not 0 <= start < end:
        raise ValueError("focus interval must have positive duration")
    enabled = f"between(t,{start:g},{end:g})"
    return ",".join([
        f"drawbox=x=105:y=1030:w=870:h=280:color=black@0.78:t=fill:enable='{enabled}'",
        f"drawbox=x=105:y=1030:w=14:h=280:color=0x22d3ee:t=fill:enable='{enabled}'",
        f"drawtext=fontfile={font}:text='確認してから使う':fontcolor=white:fontsize=64:x=(w-text_w)/2:y=1100:enable='{enabled}'",
        f"drawtext=fontfile={font}:text='AIの出力は必ず見直す':fontcolor=0x67e8f9:fontsize=39:x=(w-text_w)/2:y=1200:enable='{enabled}'",
    ])

def render(source: Path, output: Path, start=12.0, end=16.0):
    if not source.is_file():
        raise FileNotFoundError(source)
    output.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["ffmpeg","-hide_banner","-loglevel","error","-y","-i",str(source),
        "-vf",focus_filter(start,end),"-map","0:v:0","-map","0:a:0",
        "-c:v","libx264","-preset","veryfast","-crf","22","-pix_fmt","yuv420p",
        "-c:a","copy","-movflags","+faststart",str(output)],check=True)

if __name__ == "__main__":
    p=argparse.ArgumentParser()
    p.add_argument("source",type=Path)
    p.add_argument("output",type=Path)
    args=p.parse_args()
    render(args.source,args.output)
