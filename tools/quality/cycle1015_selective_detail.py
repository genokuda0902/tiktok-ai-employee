"""Selective luma detail enhancement for image-first vertical slides; 10-genre compatible."""
import argparse
import subprocess
from pathlib import Path

GENRES = ("ai_work","business","education","career","finance","wellness","science","history","productivity","daily_tips")
ROI = (0,180,1080,1100)  # Only screenshot area; captions start below 1400

def make_filter(genre="ai_work",strength=0.32):
    if genre not in GENRES:
        raise ValueError("Unknown genre")
    if not (0 < strength <= 0.6):
        raise ValueError("Excessive sharpening")
    x,y,w,h=ROI
    assert y+h<1400
    return (f"[0:v]split=2[base][roi];"
            f"[roi]crop={w}:{h}:{x}:{y},unsharp=5:5:{strength:.2f}:3:3:0[detail];"
            f"[base][detail]overlay={x}:{y}:format=auto,format=yuv420p[v]")

def render(source,target,genre="ai_work",strength=0.32):
    target=Path(target)
    target.parent.mkdir(parents=True,exist_ok=True)
    subprocess.run(["ffmpeg","-hide_banner","-loglevel","error","-y","-i",str(source),
      "-filter_complex",make_filter(genre,strength),"-map","[v]","-map","0:a:0",
      "-map_metadata","0","-map_chapters","0","-c:v","libx264","-preset","veryfast",
      "-crf","18","-pix_fmt","yuv420p","-r","30","-c:a","copy",
      "-movflags","+faststart",str(target)],check=True)

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("source")
    p.add_argument("target")
    p.add_argument("--genre",choices=GENRES,default="ai_work")
    p.add_argument("--strength",type=float,default=0.32)
    a=p.parse_args()
    render(a.source,a.target,a.genre,a.strength)
