"""Objective inherited-audio pause diagnostic; not ASR or speech/caption verification."""
from __future__ import annotations
import re
import subprocess
from pathlib import Path
from cycle833.focal_layout import FRAMES

START=re.compile(r'silence_start:\s*([\d.]+)')
END=re.compile(r'silence_end:\s*([\d.]+)')

def parse_intervals(log:str)->list[tuple[float,float]]:
    intervals=[]
    start=None
    for line in log.splitlines():
        a=START.search(line)
        b=END.search(line)
        if a:start=float(a.group(1))
        if b and start is not None:
            end=float(b.group(1))
            if end>start:intervals.append((start,end))
            start=None
    return intervals

def audit(path:Path,noise_db:int=-32,min_pause:float=.18)->dict:
    p=subprocess.run(['ffmpeg','-hide_banner','-nostats','-i',str(path),
        '-af',f'silencedetect=noise={noise_db}dB:d={min_pause}',
        '-f','null','-'],capture_output=True,text=True,check=True)
    intervals=parse_intervals(p.stderr)
    boundaries=[sum(FRAMES[:i])/30 for i in range(1,len(FRAMES))]
    long_gaps=[{'start_s':round(s,3),'end_s':round(e,3),'duration_s':round(e-s,3)}
               for s,e in intervals if e-s>=.7]
    return {'method':'FFmpeg silencedetect; NOT ASR, not transcript verification',
        'threshold_db':noise_db,'min_pause_s':min_pause,
        'long_gaps_ge_0_7s':long_gaps,
        'scene_cuts_with_nearby_long_pause':sum(
            any(s-.3<=cut<=e+.3 for s,e in intervals if e-s>=.7) for cut in boundaries),
        'scene_cuts':len(boundaries)}
