"""Cycle2065: top safe-margin time-progress overlay. Requires ffmpeg."""
import subprocess
from pathlib import Path
def render(source, destination, duration=22.682):
    source, destination = map(Path, (source, destination))
    assert source.is_file()
    filt = ("[0:v]drawbox=x=88:y=75:w=904:h=16:color=black@0.7:t=fill,"
            f"drawbox=x=88:y=75:w='904*min(t/{duration},1)':h=16:"
            "color=0xF4C56A:t=fill,format=yuv420p[v]")
    subprocess.run(["ffmpeg","-y","-i",str(source),"-filter_complex",filt,
                    "-map","[v]","-map","0:a:0","-c:v","libx264",
                    "-c:a","copy","-movflags","+faststart",str(destination)],check=True)
