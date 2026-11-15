"""Conservative brightness correction for 10-category slide videos."""
import subprocess
def enhance(src, dst, gamma=1.10):
    if not 1.0 <= gamma <= 1.15:
        raise ValueError("gamma outside conservative range")
    subprocess.run(["ffmpeg","-y","-i",str(src),"-vf",f"eq=gamma={gamma}:contrast=1.015","-c:v","libx264","-preset","veryfast","-crf","19","-pix_fmt","yuv420p","-c:a","copy","-movflags","+faststart",str(dst)],check=True)
