"""Review-only mild upper-frame denoise, protecting burned-in captions."""
import subprocess
import sys
from pathlib import Path

def video_filter(height=1350):
    if not 0 < height < 1920:
        raise ValueError("upper crop must fit within 1920px")
    return (f"[0:v]split=2[orig][work];[work]crop=iw:{height}:0:0,"
            "hqdn3d=1.2:1.2:2.4:2.4[clean];"
            "[orig][clean]overlay=0:0:format=auto[v]")

def render(source, target):
    subprocess.run(["ffmpeg","-hide_banner","-y","-i",str(source),
        "-filter_complex",video_filter(),"-map","[v]","-map","0:a:0",
        "-c:v","libx264","-preset","veryfast","-crf","19",
        "-pix_fmt","yuv420p","-c:a","copy","-movflags","+faststart",str(target)],check=True)

if __name__ == "__main__":
    render(Path(sys.argv[1]),Path(sys.argv[2]))
