"""Review-only: add high-contrast Japanese captions without replacing audio."""
from pathlib import Path
import subprocess
import sys

def render(source: Path, srt: Path, output: Path):
    if not source.is_file() or not srt.is_file():
        raise FileNotFoundError("approved input and SRT required")
    vf = ("scale=1080:1920:flags=lanczos,"
          "drawbox=x=60:y=1420:w=960:h=230:color=black@0.82:t=fill,"
          f"subtitles='{srt}':force_style='FontName=Noto Sans CJK JP,FontSize=19,"
          "PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,"
          "BorderStyle=1,Outline=2,Shadow=0,Alignment=2,MarginV=165'")
    subprocess.run(["ffmpeg","-y","-v","error","-i",str(source),"-vf",vf,
                    "-map","0:v:0","-map","0:a:0","-map","0:s:0",
                    "-c:v","libx264","-preset","veryfast","-crf","22",
                    "-pix_fmt","yuv420p","-c:a","copy","-c:s","mov_text",
                    "-movflags","+faststart",str(output)],check=True)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        raise SystemExit("usage: render.py input.mp4 captions.srt output.mp4")
    render(*map(Path,sys.argv[1:]))
