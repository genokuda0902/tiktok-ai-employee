"""Burn timed Japanese SRT captions into a review-only MP4. Input video is never bundled."""
import argparse
import subprocess
from pathlib import Path

def burn(source: Path, captions: Path, output: Path):
    if not source.is_file() or not captions.is_file():
        raise FileNotFoundError("Both input video and subtitle file are required")
    if source.resolve() == output.resolve():
        raise ValueError("Do not overwrite source")
    vf = f"subtitles={captions}:force_style='FontName=Noto Sans CJK JP,FontSize=20,PrimaryColour=&H00FFFFFF,OutlineColour=&H00101010,BorderStyle=3,Outline=2,MarginV=220'"
    subprocess.run(["ffmpeg","-y","-i",str(source),"-vf",vf,"-map","0:v:0","-map","0:a:0","-c:v","libx264","-preset","ultrafast","-crf","25","-c:a","copy","-movflags","+faststart",str(output)],check=True)
    subprocess.run(["ffmpeg","-v","error","-i",str(output),"-f","null","-"],check=True)

if __name__ == "__main__":
    p=argparse.ArgumentParser()
    p.add_argument("source",type=Path);p.add_argument("captions",type=Path);p.add_argument("output",type=Path)
    a=p.parse_args();burn(a.source,a.captions,a.output)
