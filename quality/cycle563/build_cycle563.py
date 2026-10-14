#!/usr/bin/env python3
"""Cycle563: retain original Japanese voice cadence and improve illustration detail.

Previous cycle562 slowed all speech 0.8x. This version uses the unmodified
12.5-second source narration, inserting 3.1 seconds of reading pauses only
at measured near-silent intervals. Text/subtitle region is untouched.
No external services; publication requires human review.
"""
from pathlib import Path
import argparse, subprocess

ROOT=Path(__file__).resolve().parents[1]
INPUT=ROOT/'assets'/'cycle561.mp4'
OUTPUT=ROOT/'output'/'cycle563_NATURAL_CADENCE_DETAIL_JA_HUMAN_REVIEW.mp4'
FPS=30
PAUSES=[(16,12),(87,14),(109,10),(158,14),(233,14),(304,16),(338,13)]
assert sum(n for _,n in PAUSES)==93

def filter_graph():
    parts=[];prev=0;cuts=PAUSES+[(375,0)];concat=[]
    for i,(end,hold) in enumerate(cuts):
        if end<=prev:raise ValueError('non-increasing cuts')
        start_t=prev/FPS;end_t=end/FPS;duration=hold/FPS
        v=f'[0:v]trim=start_frame={prev}:end_frame={end},setpts=PTS-STARTPTS'
        if hold:v+=f',tpad=stop_mode=clone:stop_duration={duration:.9f}'
        parts.append(v+f',fps={FPS}[v{i}]')
        a=f'[0:a]atrim=start={start_t:.9f}:end={end_t:.9f},asetpts=PTS-STARTPTS'
        if hold:a+=f',apad=pad_dur={duration:.9f}'
        parts.append(a+f'[a{i}]')
        concat.extend([f'[v{i}]',f'[a{i}]']);prev=end
    parts.append(''.join(concat)+f'concat=n={len(cuts)}:v=1:a=1[vraw][araw]')
    parts.append('[vraw]split=2[base][roi_src]')
    parts.append('[roi_src]crop=950:680:65:610,unsharp=5:5:0.60:3:3:0.0,eq=contrast=1.025:saturation=1.045[roi]')
    parts.append('[base][roi]overlay=65:610:shortest=1,format=yuv420p[vout]')
    parts.append('[araw]aresample=48000,alimiter=limit=0.95[aout]')
    return ';'.join(parts)

def build(source=INPUT,output=OUTPUT):
    source,output=Path(source),Path(output)
    if not source.is_file():raise FileNotFoundError(source)
    output.parent.mkdir(parents=True,exist_ok=True)
    cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(source),
         '-filter_complex',filter_graph(),'-map','[vout]','-map','[aout]',
         '-t','15.6','-r','30','-c:v','libx264','-preset','veryfast','-crf','17',
         '-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-ar','48000',
         '-movflags','+faststart',str(output)]
    r=subprocess.run(cmd,capture_output=True,text=True)
    if r.returncode:raise RuntimeError(r.stderr[-4000:])
    return output

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--source',type=Path,default=INPUT)
    p.add_argument('--output',type=Path,default=OUTPUT)
    args=p.parse_args();print(build(args.source,args.output))
