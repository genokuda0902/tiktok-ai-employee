#!/usr/bin/env python3
"""Conservative, independent *acoustic pause* review aid; not Japanese ASR.

Silence is not a proof of word boundaries. This script never marks semantic
alignment PASS, even when a cue happens near an acoustic pause.
"""
from __future__ import annotations
import argparse, json, re, subprocess
from pathlib import Path

STAMP=re.compile(r'(?:(\d+):)?(\d+):(\d+),(\d+)')
SILENCE_START=re.compile(r'silence_start:\s*([0-9.]+)')
SILENCE_END=re.compile(r'silence_end:\s*([0-9.]+)')

def seconds(s):
    m=STAMP.fullmatch(s.strip())
    if not m: raise ValueError('bad SRT timestamp: '+s)
    h,mm,ss,ms=m.groups()
    return int(h or 0)*3600+int(mm)*60+int(ss)+int(ms)/1000

def cues_from_srt(s):
    chunks=re.split(r'\n\s*\n',s.strip())
    cues=[]
    for chunk in chunks:
        lines=chunk.splitlines()
        time_line=next((line for line in lines if ' --> ' in line),None)
        if time_line is None: raise ValueError('missing cue timing')
        start,end=map(seconds,time_line.split(' --> '))
        if end<=start: raise ValueError('invalid cue interval')
        cues.append((start,end))
    if any(a[1]>b[0]+.002 for a,b in zip(cues,cues[1:])):
        raise ValueError('overlapping SRT cues')
    return cues

def pauses_from_log(log, duration):
    starts=[];pauses=[]
    for line in log.splitlines():
        a=SILENCE_START.search(line)
        b=SILENCE_END.search(line)
        if a: starts.append(float(a.group(1)))
        if b and starts:
            start=starts.pop(0);end=float(b.group(1))
            if 0<=start<end<=duration+.02:pauses.append((start,end))
    return pauses

def audit(cues, pauses, tolerance=.25):
    result=[]
    for i in range(len(cues)-1):
        boundary=cues[i][1]
        if abs(boundary-cues[i+1][0])>.005:raise ValueError('cue gap detected')
        nearby=sorted(pauses,key=lambda p:min(abs(boundary-p[0]),abs(boundary-p[1]),abs(boundary-(p[0]+p[1])/2)))
        if nearby:
            p=nearby[0]
            distance=0 if p[0]<=boundary<=p[1] else min(abs(boundary-p[0]),abs(boundary-p[1]))
        else:p=None;distance=None
        result.append({'boundary_index':i+1,'subtitle_boundary_s':round(boundary,3),
                       'nearest_pause_s':[round(x,3) for x in p] if p else None,
                       'distance_to_pause_s':round(distance,3) if distance is not None else None,
                       'acoustic_pause_proximity':'NEEDS_REVIEW' if distance is None or distance>tolerance else 'NEAR_PAUSE_NOT_SEMANTIC_PROOF'})
    return result

def main(mp4,srt,report):
    mp4,srt,report=map(Path,(mp4,srt,report))
    if not mp4.exists():raise FileNotFoundError(mp4)
    p=subprocess.run(['ffmpeg','-hide_banner','-i',str(mp4),'-af',
                      'silencedetect=noise=-32dB:d=0.18','-f','null','-'],
                     capture_output=True,text=True)
    if p.returncode:raise RuntimeError(p.stderr[-1000:])
    cues=cues_from_srt(srt.read_text(encoding='utf-8'))
    pauses=pauses_from_log(p.stderr,23.033333)
    boundaries=audit(cues,pauses)
    data={'audio_check':'PAUSE_PROXIMITY_ONLY','threshold':'-32 dB, min 0.18 s',
          'subtitle_cues':len(cues),'detected_silence_intervals':len(pauses),
          'boundaries':boundaries,'needs_review':sum(b['acoustic_pause_proximity']=='NEEDS_REVIEW' for b in boundaries),
          'japanese_transcription':'NOT_VERIFIED','pronunciation':'NOT_VERIFIED',
          'semantic_caption_alignment':'NOT_VERIFIED','human_listening':'REQUIRED'}
    report.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
    return data
if __name__=='__main__':
    a=argparse.ArgumentParser()
    for n in ('mp4','srt','report'):a.add_argument('--'+n,required=True)
    x=a.parse_args();print(json.dumps(main(x.mp4,x.srt,x.report),ensure_ascii=False))
