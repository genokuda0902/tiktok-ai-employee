"""Genre-neutral ending fade for portrait TikTok slides."""
import subprocess

def render(src, dst, duration, fade_seconds=0.36):
    if not 0 < fade_seconds < duration:
        raise ValueError("invalid fade duration")
    start=duration-fade_seconds
    subprocess.run(["ffmpeg","-y","-i",src,"-vf",f"fade=t=out:st={start:.3f}:d={fade_seconds:.3f}","-c:v","libx264","-crf","19","-pix_fmt","yuv420p","-c:a","copy","-movflags","+faststart",dst],check=True)
