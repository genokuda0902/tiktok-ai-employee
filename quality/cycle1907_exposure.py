"""Conservative exposure adjustment for vertical review MP4."""
import subprocess

def render(source: str, output: str, gamma: float = 1.07) -> None:
    if not 1.0 <= gamma <= 1.15:
        raise ValueError("gamma outside conservative review range")
    subprocess.run(["ffmpeg","-hide_banner","-loglevel","error","-y","-i",source,"-vf",f"eq=gamma={gamma}:saturation=1.0","-c:v","libx264","-preset","veryfast","-crf","19","-pix_fmt","yuv420p","-c:a","copy","-movflags","+faststart",output],check=True)
