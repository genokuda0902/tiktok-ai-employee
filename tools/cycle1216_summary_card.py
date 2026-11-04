"""Review-only summary-card overlay for approved/local MP4 input.

Never publish without separate human QA and asset clearance.
Usage: python tools/cycle1216_summary_card.py input.mp4 output.mp4
"""
import argparse
import subprocess

FONT = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"

def filtergraph(font=FONT, start=17, end=22):
    if start < 0 or end <= start:
        raise ValueError("invalid summary interval")
    visible = f"between(t,{start},{end})"
    items = [
        f"drawbox=x=100:y=420:w=880:h=680:color=0x071629@0.92:t=fill:enable='{visible}'",
        f"drawbox=x=100:y=420:w=14:h=680:color=0x25d0c5:t=fill:enable='{visible}'",
    ]
    for label, y, size in [("今日のまとめ",505,66),("① 目的を明確に",650,48),("② 条件を具体的に",760,48),("③ 結果を確認",870,48)]:
        items.append(f"drawtext=fontfile={font}:text='{label}':fontsize={size}:fontcolor=white:x=165:y={y}:enable='{visible}'")
    return ",".join(items)

def render(source, target):
    subprocess.run(["ffmpeg","-y","-hide_banner","-loglevel","error","-i",str(source),
                    "-vf",filtergraph(),"-map","0:v:0","-map","0:a:0",
                    "-c:v","libx264","-preset","veryfast","-crf","22","-pix_fmt","yuv420p",
                    "-c:a","copy","-movflags","+faststart",str(target)],check=True)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("source")
    parser.add_argument("target")
    args = parser.parse_args()
    render(args.source,args.target)
