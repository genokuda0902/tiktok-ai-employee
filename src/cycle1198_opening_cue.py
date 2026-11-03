"""Review-only opening cue; never implies publication approval."""
from pathlib import Path
import argparse
import subprocess

def render(source: Path, target: Path, font: str = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"):
    if not source.is_file():
        raise FileNotFoundError(source)
    if not Path(font).is_file():
        raise FileNotFoundError(font)
    target.parent.mkdir(parents=True, exist_ok=True)
    vf = ("drawbox=x=830:y=120:w=200:h=66:color=0x111827@0.80:t=fill:enable='between(t,0,2.4)',"
          f"drawtext=fontfile={font}:text='注目':fontcolor=white:fontsize=35:x=891:y=133:enable='between(t,0,2.4)'")
    subprocess.run(["ffmpeg","-hide_banner","-loglevel","error","-y","-i",str(source),"-vf",vf,
                    "-map","0:v:0","-map","0:a:0","-c:v","libx264","-preset","veryfast",
                    "-crf","19","-pix_fmt","yuv420p","-c:a","copy","-movflags","+faststart",str(target)],check=True)

if __name__ == "__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("source",type=Path)
    parser.add_argument("target",type=Path)
    args=parser.parse_args()
    render(args.source,args.target)
