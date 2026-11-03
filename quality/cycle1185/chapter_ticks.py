"""Add non-text chapter boundaries to an existing progress bar (reimplementation)."""
import argparse
import subprocess

def chapter_filter(width=1080, chapters=4, height=14):
    if width < 16 or chapters < 2 or chapters > 20 or height < 1:
        raise ValueError("invalid geometry")
    positions = [round(width * i / chapters) for i in range(1, chapters)]
    return ",".join(f"drawbox=x={x}:y=0:w=3:h={height}:color=black@0.85:t=fill" for x in positions)

def render(source, output, width=1080, chapters=4):
    subprocess.run(["ffmpeg","-hide_banner","-y","-i",source,"-vf",chapter_filter(width,chapters),"-c:v","libx264","-preset","ultrafast","-crf","19","-c:a","copy",output],check=True)

if __name__ == "__main__":
    p=argparse.ArgumentParser()
    p.add_argument("source");p.add_argument("output")
    p.add_argument("--width",type=int,default=1080)
    p.add_argument("--chapters",type=int,default=4)
    a=p.parse_args()
    render(a.source,a.output,a.width,a.chapters)
