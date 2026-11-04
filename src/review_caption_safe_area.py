"""Review-only caption placement overlay; never claims speech synchronization."""
import argparse
import subprocess
from pathlib import Path

def render(source: Path, output: Path, font: Path):
    if not source.is_file() or not font.is_file():
        raise FileNotFoundError("Source MP4 and Japanese font are required")
    if source.resolve() == output.resolve():
        raise ValueError("Output must differ from input")
    vf = (
        "drawbox=enable='between(t,16,20)':x=100:y=1260:w=880:h=200:color=black@0.72:t=fill,"
        f"drawtext=enable='between(t,16,20)':fontfile={font}:text='字幕の位置を確認':fontsize=54:fontcolor=white:x=(w-text_w)/2:y=1305,"
        f"drawtext=enable='between(t,16,20)':fontfile={font}:text='音声との同期は未確認':fontsize=39:fontcolor=yellow:x=(w-text_w)/2:y=1380"
    )
    subprocess.run(["ffmpeg","-hide_banner","-loglevel","error","-y","-i",str(source),"-vf",vf,
                    "-c:v","libx264","-preset","veryfast","-crf","25","-pix_fmt","yuv420p",
                    "-c:a","copy","-movflags","+faststart",str(output)],check=True)

if __name__ == "__main__":
    p=argparse.ArgumentParser()
    p.add_argument("source",type=Path); p.add_argument("output",type=Path)
    p.add_argument("--font",type=Path,default=Path("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"))
    a=p.parse_args()
    render(a.source,a.output,a.font)
