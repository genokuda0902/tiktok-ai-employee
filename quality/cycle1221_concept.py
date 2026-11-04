"""Cycle1221: review-only conceptual BEFORE/AFTER overlay. Requires approved local review MP4; never posts."""
from pathlib import Path
import argparse, subprocess

def build_filter(font="/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"):
    parts = [
        "drawbox=x=65:y=465:w=950:h=900:color=0x071426@0.98:t=fill",
        "drawbox=x=95:y=620:w=885:h=250:color=0x343f55@1:t=fill",
        "drawbox=x=95:y=905:w=885:h=320:color=0x114c57@1:t=fill",
    ]
    texts = [
        ("入力の違いで出力が変わる",53,120,505),
        ("BEFORE  あいまいな依頼",39,130,655),
        ("資料をまとめて",51,130,735),
        ("AFTER  条件を指定",39,130,940),
        ("目的・対象・形式を伝える",47,130,1030),
        ("※ 概念図／実操作映像ではありません",27,115,1275),
    ]
    parts += [f"drawtext=fontfile={font}:text='{text}':fontcolor=white:fontsize={size}:x={x}:y={y}"
              for text,size,x,y in texts]
    return ",".join(p+":enable='between(t,6,14)'" for p in parts)

def render(src, dst):
    src, dst = Path(src), Path(dst)
    if not src.is_file():
        raise FileNotFoundError(src)
    dst.parent.mkdir(parents=True,exist_ok=True)
    subprocess.run(["ffmpeg","-hide_banner","-loglevel","error","-y","-i",str(src),
                    "-vf",build_filter(),"-c:v","libx264","-preset","veryfast",
                    "-crf","24","-pix_fmt","yuv420p","-c:a","copy",
                    "-movflags","+faststart",str(dst)],check=True)
    return dst

if __name__ == "__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--input",required=True)
    p.add_argument("--output",required=True)
    a=p.parse_args()
    print(render(a.input,a.output))
