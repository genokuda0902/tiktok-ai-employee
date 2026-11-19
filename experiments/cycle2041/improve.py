"""Safe-zone playback progress indicator for 1080x1920 review videos."""
import subprocess
from pathlib import Path

def filtergraph(duration):
    if duration <= 0:
        raise ValueError("duration must be positive")
    return ("drawbox=x=104:y=1662:w=872:h=9:color=white@0.18:t=fill,"
            f"drawbox=x=104:y=1662:w='max(1,min(872,872*t/{duration:.3f}))':h=9:color=0x63E6CA@0.95:t=fill")

def render(source, destination, duration):
    Path(destination).parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["ffmpeg","-y","-hide_banner","-loglevel","error","-i",str(source),
        "-vf",filtergraph(duration),"-c:v","libx264","-preset","veryfast",
        "-crf","20","-pix_fmt","yuv420p","-c:a","copy",
        "-movflags","+faststart",str(destination)],check=True)
