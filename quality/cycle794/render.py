#!/usr/bin/env python3
"""Cycle794: artwork-only wipe transitions, retaining original captions and AAC audio.
Requires ffmpeg; inputs must be cleared for rights and reviewed before publication.
"""
from pathlib import Path
import argparse, subprocess

GENRE_THEMES={
 "ai_work":"#9B90FF","beauty":"#E5ACD7","love_psychology":"#C0A2FF",
 "money_saving":"#6BE1B8","sales_business":"#58C5F6","career":"#83C5F9",
 "health_life":"#6EE7BE","science":"#39E7D3","travel_food":"#70D6EA",
 "product_life":"#C6A0F5"}
DEFAULT_FRAMES=[57,63,58,63,40,47,48,53]

def build_filter(frames, transition_frames=6, fps=30):
    assert len(frames)>=2 and all(isinstance(n,int) and n>transition_frames for n in frames)
    d=transition_frames/fps
    filters=["[0:v]split=2[base][art]",
       f"[art]crop=900:620:90:560,split={len(frames)}"+ "".join(f"[v{i}]" for i in range(len(frames)))]
    pos=0
    for i,n in enumerate(frames):
        filters.append(f"[v{i}]trim=start_frame={pos}:end_frame={pos+n},setpts=PTS-STARTPTS,fps={fps},format=yuv420p,tpad=stop_mode=clone:stop_duration={d:.6f}[s{i}]")
        pos+=n
    prev="s0";acc=0
    for i in range(1,len(frames)):
        acc+=frames[i-1];out=f"x{i}"
        filters.append(f"[{prev}][s{i}]xfade=transition=wipeleft:duration={d:.6f}:offset={acc/fps:.6f}[{out}]")
        prev=out
    filters.append(f"[{prev}]trim=end_frame={sum(frames)},setpts=PTS-STARTPTS,format=yuv420p[artout]")
    filters.append("[base][artout]overlay=90:560:shortest=1,format=yuv420p[vout]")
    return ";".join(filters)

def render(src,dst,frames=DEFAULT_FRAMES):
    src,dst=Path(src),Path(dst)
    dst.parent.mkdir(parents=True,exist_ok=True)
    subprocess.run(["ffmpeg","-hide_banner","-loglevel","error","-y","-i",str(src),
      "-filter_complex",build_filter(frames),"-map","[vout]","-map","0:a:0",
      "-c:v","libx264","-preset","ultrafast","-crf","19","-pix_fmt","yuv420p",
      "-r","30","-c:a","copy","-movflags","+faststart",str(dst)],check=True)
    return dst

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--input",required=True,type=Path)
    p.add_argument("--output",required=True,type=Path)
    args=p.parse_args()
    print(render(args.input,args.output))
