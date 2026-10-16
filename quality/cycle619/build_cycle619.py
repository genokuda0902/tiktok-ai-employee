#!/usr/bin/env python3
"""Cycle 619: remove two ghosted transitions without altering Japanese audio.

Input is a locally supplied licensed MP4; no video or private material is committed.
Reusable for 10 genres. No publishing, paid APIs, or automatic merging.
"""
from __future__ import annotations
import argparse, hashlib, json, subprocess, tempfile
from pathlib import Path

ROOT=Path(__file__).resolve().parent
SOURCE=ROOT/'assets/cycle617_baseline.mp4'
OUTPUT=ROOT/'output/cycle619_DEGHOSTED_CUTS_HUMAN_REVIEW.mp4'
PATCHES=((215,216,219),(223,220,222),(279,280,286),(290,287,289))
FPS=30; FRAMES=468; WIDTH=1080; HEIGHT=1920

def run(cmd,timeout=300):
    p=subprocess.run(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,timeout=timeout)
    if p.returncode:raise RuntimeError(f'command failed: {cmd[:4]} / {p.stderr[-2500:]}')
    return p.stdout

def sha256(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for chunk in iter(lambda:f.read(1<<20),b''):h.update(chunk)
    return h.hexdigest()

def check_patches(patches=PATCHES):
    used=set()
    for still,a,b in patches:
        if not 0<=still<FRAMES or not 0<=a<=b<FRAMES: raise ValueError('invalid frame index')
        if a<=still<=b: raise ValueError('reference frame must be outside its patched interval')
        for i in range(a,b+1):
            if i in used:raise ValueError('overlapping patches')
            used.add(i)
    return len(used)

def replacement_frame(n,patches=PATCHES):
    if not 0<=n<FRAMES:raise ValueError('frame outside video')
    for still,a,b in patches:
        if a<=n<=b:return still
    return n

def render(source=SOURCE,output=OUTPUT):
    source=Path(source);output=Path(output)
    if not source.exists():raise FileNotFoundError(source)
    check_patches()
    output.parent.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='cycle619_') as d:
        d=Path(d)
        for i,(still,_,_) in enumerate(PATCHES):
            run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(source),
                 '-vf',f'select=eq(n\\,{still})','-vsync','0','-frames:v','1',str(d/f'stable{i}.png')],120)
        args=['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(source)]
        for i in range(len(PATCHES)):
            args+=['-loop','1','-framerate',str(FPS),'-i',str(d/f'stable{i}.png')]
        graph=[];prev='[0:v]'
        for i,(_,start,end) in enumerate(PATCHES):
            name=f'[v{i}]'
            graph.append(f'{prev}[{i+1}:v]overlay=0:0:enable=between(n\\,{start}\\,{end}):shortest=1:format=auto{name}')
            prev=name
        graph.append(f'{prev}format=yuv420p[outv]')
        silent=d/'silent.mp4'
        args+=['-filter_complex',';'.join(graph),'-map','[outv]','-an',
               '-c:v','libx264','-preset','veryfast','-crf','17','-threads','2',
               '-r',str(FPS),'-frames:v',str(FRAMES),'-movflags','+faststart',str(silent)]
        run(args,300)
        # Separate remux retains the final AAC packet (otherwise -frames:v truncates it).
        run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(silent),'-i',str(source),
             '-map','0:v:0','-map','1:a:0','-c','copy','-movflags','+faststart',str(output)],120)
    manifest={'cycle':619,'previous_cycle':617,'change':'Replace ghosted crossfade frames at chapter 04->05 and 05->06 with nearest clean source stills.','patches':PATCHES,'frames_replaced':check_patches(), 'genres_supported':10, 'source_sha256':sha256(source),'output_sha256':sha256(output),'status':'HUMAN_REVIEW','publication':'NOT_APPROVED','cost_jpy':0}
    (output.parent/'render_manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
    return manifest

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--input',type=Path,default=SOURCE);p.add_argument('--output',type=Path,default=OUTPUT)
    a=p.parse_args();print(json.dumps(render(a.input,a.output),ensure_ascii=False,indent=2))
