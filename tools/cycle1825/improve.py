"""Optional luma-only slide-text sharpening; review-only."""
import subprocess
import sys

def render(source, target):
    subprocess.run(["ffmpeg","-y","-i",source,"-vf","unsharp=5:5:0.32:5:5:0.0","-c:v","libx264","-preset","veryfast","-crf","19","-pix_fmt","yuv420p","-c:a","copy","-movflags","+faststart",target],check=True)

if __name__=="__main__":
    render(sys.argv[1],sys.argv[2])
