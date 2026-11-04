"""Genre-neutral, review-only illustrative comparison overlay."""
import argparse
import subprocess
from pathlib import Path

def filtergraph(start=10.0, end=15.0):
    if not 0 <= start < end:
        raise ValueError("invalid comparison interval")
    enable=fr"between(t\,{start:g}\,{end:g})"
    return ",".join([
        f"drawbox=x=65:y=500:w=950:h=670:color=0x07101f@0.91:t=fill:enable={enable}",
        f"drawbox=x=85:y=540:w=430:h=560:color=0x253044@0.97:t=fill:enable={enable}",
        f"drawbox=x=565:y=540:w=430:h=560:color=0x123d45@0.97:t=fill:enable={enable}",
        f"drawtext=fontfile=/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc:text='BEFORE':fontcolor=white:fontsize=52:x=175:y=640:enable={enable}",
        f"drawtext=fontfile=/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc:text='AFTER':fontcolor=white:fontsize=52:x=675:y=640:enable={enable}",
        f"drawtext=fontfile=/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc:text='手順が曖昧':fontcolor=white:fontsize=43:x=135:y=815:enable={enable}",
        f"drawtext=fontfile=/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc:text='3段階で整理':fontcolor=white:fontsize=43:x=615:y=815:enable={enable}",
        f"drawtext=fontfile=/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc:text='説明用イメージ・実績ではありません':fontcolor=yellow:fontsize=31:x=125:y=1130:enable={enable}",
    ])

def render(source, target):
    source, target = Path(source), Path(target)
    if not source.is_file():
        raise FileNotFoundError(source)
    target.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["ffmpeg","-hide_banner","-loglevel","error","-y","-i",str(source),
        "-vf",filtergraph(),"-map","0:v:0","-map","0:a:0","-c:v","libx264",
        "-preset","veryfast","-crf","23","-pix_fmt","yuv420p",
        "-c:a","copy","-movflags","+faststart",str(target)],check=True)
    return target

if __name__ == "__main__":
    p=argparse.ArgumentParser()
    p.add_argument("source")
    p.add_argument("target")
    a=p.parse_args()
    render(a.source,a.target)
