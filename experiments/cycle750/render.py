"""Overlay final 51 frames; stream-copy inherited Japanese AAC."""
from pathlib import Path
import subprocess
FPS=30
FRAMES=429
SPLITS=(378,395,405,429)
def command(previous,slides,output):
    previous=Path(previous);slides=[Path(p) for p in slides];output=Path(output)
    if len(slides)!=3:raise ValueError("need three slides")
    for p in [previous,*slides]:
        if not p.is_file():raise FileNotFoundError(p)
    args=["ffmpeg","-hide_banner","-nostdin","-y","-loglevel","error","-i",str(previous)]
    for p in slides:args+=["-loop","1","-framerate","30","-i",str(p)]
    g=["[0:v]format=yuv420p[base]"];last="base"
    for i in range(3):
        g.append(f"[{i+1}:v]format=rgba[s{i}]")
        g.append(f"[{last}][s{i}]overlay=0:0:enable='between(n,{SPLITS[i]},{SPLITS[i+1]-1})'[v{i}]")
        last=f"v{i}"
    g.append(f"[{last}]format=yuv420p[v]")
    args+=["-filter_complex",";".join(g),"-map","[v]","-map","0:a:0",
           "-c:v","libx264","-preset","veryfast","-crf","17","-pix_fmt","yuv420p",
           "-r","30","-frames:v",str(FRAMES),"-c:a","copy","-movflags","+faststart",str(output)]
    return args
if __name__=="__main__":
    root=Path(__file__).resolve().parent
    source=root/"input"/"previous.mp4"
    slides=[root/"assets"/f"endcard_stage{i}.png" for i in range(3)]
    output=root/"output"/"cycle750_ENDCARD_REVEAL_HUMAN_REVIEW.mp4"
    output.parent.mkdir(exist_ok=True)
    subprocess.run(command(source,slides,output),check=True,timeout=240)
    print(output)
