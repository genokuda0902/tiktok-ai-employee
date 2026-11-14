"""Reusable visual end-fade for 10 content genres; audio copied without changes."""
import subprocess
import sys

def apply(src, dst, fade_seconds=0.35):
    duration = float(subprocess.check_output(
        ["ffprobe","-v","error","-show_entries","format=duration","-of","default=nw=1:nk=1",src],text=True).strip())
    if duration <= fade_seconds:
        raise ValueError("Video shorter than fade")
    start = duration - fade_seconds
    subprocess.run(["ffmpeg","-y","-i",src,"-vf",f"fade=t=out:st={start:.3f}:d={fade_seconds}",
                    "-c:v","libx264","-preset","veryfast","-crf","19","-pix_fmt","yuv420p",
                    "-c:a","copy","-movflags","+faststart",dst],check=True)

if __name__ == "__main__":
    apply(sys.argv[1],sys.argv[2])
