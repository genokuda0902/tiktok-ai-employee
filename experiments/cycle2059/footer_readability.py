"""Apply a readable review-status footer to a 1080x1920 MP4."""
import subprocess
from pathlib import Path

def render(source: Path, output: Path, font: str):
    vf = ("drawbox=x=75:y=1745:w=930:h=85:color=0x001719@0.95:t=fill,"
          f"drawtext=fontfile={font}:text='社内レビュー用 ・ 公開品質未承認':"
          "fontcolor=white:fontsize=35:x=100:y=1765")
    subprocess.run(["ffmpeg","-y","-i",str(source),"-vf",vf,"-c:v","libx264",
                    "-crf","21","-c:a","copy","-movflags","+faststart",str(output)],check=True)
