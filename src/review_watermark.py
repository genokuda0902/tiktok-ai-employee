"""Review-only watermark: never implies publication approval."""
from pathlib import Path
import subprocess

def render(source: Path, target: Path):
    if not source.is_file():
        raise FileNotFoundError(source)
    target.parent.mkdir(parents=True, exist_ok=True)
    vf = (
        "drawbox=x=55:y=105:w=970:h=95:color=black@0.82:t=fill,"
        "drawbox=x=55:y=105:w=12:h=95:color=0x00d4ff:t=fill,"
        "drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf:"
        "text='REVIEW ONLY  -  AUDIO MISSING':fontcolor=white:fontsize=32:x=90:y=132,"
        "drawbox=x=55:y=1730:w=970:h=75:color=black@0.72:t=fill,"
        "drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf:"
        "text='NOT APPROVED FOR POSTING':fontcolor=white:fontsize=28:x=95:y=1750"
    )
    subprocess.run(["ffmpeg","-hide_banner","-loglevel","error","-y","-i",str(source),
                    "-vf",vf,"-map","0:v:0","-c:v","libx264","-preset","veryfast",
                    "-crf","23","-pix_fmt","yuv420p","-an","-movflags","+faststart",str(target)],
                   check=True)
    return target
