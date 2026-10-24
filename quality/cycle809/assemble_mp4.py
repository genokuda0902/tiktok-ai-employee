#!/usr/bin/env python3
"""Free local review-only 10-genre-neutral image slide assembler.
Requires 8 pre-rendered 1080x1920 slides, timing JSON, and a source MP4 with
Japanese AAC audio. Does not synthesize or publish assets.
"""
import argparse,json,subprocess
from pathlib import Path
from PIL import Image
FPS=30

def command(args):
    p=subprocess.run(args,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
    if p.returncode:raise RuntimeError(p.stderr[-1800:])
    return p.stdout

def frame_counts(timing,expected):
    secs=[float(x['seconds']) for x in timing['sentences']]
    if len(secs)!=8 or min(secs)<=0:raise ValueError('Need eight positive scenes')
    frames=[round(t*FPS) for t in secs]
    frames[-1]+=expected-sum(frames)
    if min(frames)<=0 or sum(frames)!=expected:raise ValueError('Invalid frame allocation')
    return frames

def assemble(slides,source,timing,out):
    slides,source,out=Path(slides),Path(source),Path(out)
    if 'HUMAN_REVIEW' not in out.name:raise ValueError('Only human-review output allowed')
    meta=json.loads(Path(timing).read_text())
    info=json.loads(command(['ffprobe','-v','error','-select_streams','v:0','-show_entries','stream=nb_frames','-of','json',str(source)]))
    total=int(info['streams'][0]['nb_frames']);counts=frame_counts(meta,total)
    tmp=out.parent/'_assemble_work';tmp.mkdir(parents=True,exist_ok=True)
    clips=[]
    for i,n in enumerate(counts):
        options=[slides/f'scene_{i+1:02d}.{ext}' for ext in ('jpg','png')]
        matches=[p for p in options if p.exists()]
        if len(matches)!=1:raise FileNotFoundError(f'Expected exactly one scene {i+1} image')
        with Image.open(matches[0]) as im:
            if im.size!=(1080,1920):raise ValueError('Slide is not 1080x1920')
        clip=tmp/f'part_{i+1:02d}.mp4'
        command(['ffmpeg','-y','-v','error','-loop','1','-framerate','30','-i',str(matches[0]),'-frames:v',str(n),'-vf','format=yuv420p','-c:v','libx264','-preset','veryfast','-crf','20',str(clip)])
        clips.append(clip)
    listfile=tmp/'parts.txt';listfile.write_text(''.join("file '"+str(p.resolve())+"'\n" for p in clips))
    silent=tmp/'silent.mp4'
    command(['ffmpeg','-y','-v','error','-f','concat','-safe','0','-i',str(listfile),'-c','copy',str(silent)])
    command(['ffmpeg','-y','-v','error','-i',str(silent),'-i',str(source),'-map','0:v:0','-map','1:a:0','-c:v','copy','-c:a','copy','-movflags','+faststart',str(out)])
    command(['ffmpeg','-v','error','-xerror','-i',str(out),'-f','null','-'])
    return out

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--slides',required=True);p.add_argument('--source',required=True)
    p.add_argument('--timing',required=True);p.add_argument('--out',required=True)
    a=p.parse_args()
    print(assemble(a.slides,a.source,a.timing,a.out))
