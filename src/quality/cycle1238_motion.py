"""Review-only common punch-in effect. No asset approval or publication implied."""
import subprocess
from pathlib import Path

def punch_in(source: str, destination: str, start: float = 7, end: float = 15, zoom: float = 1.0588):
    if not (0 <= start < end and 1 <= zoom <= 1.12):
        raise ValueError("invalid motion interval or zoom")
    if not Path(source).is_file():
        raise FileNotFoundError(source)
    # Crop is always even-sized for yuv420p; keep subtitles within safe zones.
    width = int(1080 / zoom) // 2 * 2
    height = int(1920 / zoom) // 2 * 2
    vf = (f"crop=w='if(between(t,{start},{end}),{width},1080)':"
          f"h='if(between(t,{start},{end}),{height},1920)':"
          "x='(iw-out_w)/2':y='(ih-out_h)/2',scale=1080:1920,format=yuv420p")
    subprocess.run(["ffmpeg","-y","-i",source,"-vf",vf,"-c:v","libx264",
                    "-crf","27","-c:a","copy","-movflags","+faststart",destination],check=True)
    return destination
