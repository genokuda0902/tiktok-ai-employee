"""cycle879: review-only genre-neutral audio-activity/caption timing QA.

RMS activity is NOT speech recognition, word alignment, or rights verification.
Only the final cue may be shortened to remove verified low-energy trailing audio.
Source video/audio stays private and is never uploaded to GitHub.
"""
from __future__ import annotations
import argparse
from array import array
import hashlib
import json
import math
from pathlib import Path
import subprocess
import tempfile
from PIL import Image, ImageDraw

FPS = 30
W, H = 1080, 1920
SAMPLE_RATE = 16000
THRESHOLD_DBFS = -32.0
CUES = ((.27,2.93),(3.31,5.60),(5.90,8.23),(8.52,11.10),
        (11.41,13.97),(14.28,16.93),(17.26,19.50),(19.86,23.03))
POLICY = dict(review_only=True, publication_approved=False, external_upload=False,
              automatic_posting=False, source_rights_reviewed=False)


def digest(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''): h.update(b)
    return h.hexdigest()


def validate_cues(cues, duration):
    prev=0.0
    if not 1<=len(cues)<=16: raise ValueError('1..16 cues required')
    for s,e in cues:
        if not 0<=s<e<=duration+.01 or s<prev: raise ValueError('invalid cue')
        if e-s<.35: raise ValueError('unreadably short cue')
        prev=e
    return True


def read_energy(video, fps=FPS):
    cmd=['ffmpeg','-v','error','-nostdin','-i',str(video),'-vn',
         '-ac','1','-ar',str(SAMPLE_RATE),'-f','s16le','-']
    pcm=subprocess.run(cmd,check=True,capture_output=True,timeout=90).stdout
    samples=array('h');samples.frombytes(pcm)
    block=round(SAMPLE_RATE/fps)
    out=[]
    for start in range(0,len(samples),block):
        chunk=samples[start:start+block]
        if not chunk: break
        mean_sq=sum(v*v for v in chunk)/len(chunk)
        out.append(20*math.log10(max(math.sqrt(mean_sq)/32768.0,1e-7)))
    return out


def analyze(energy,cues,threshold=THRESHOLD_DBFS,fps=FPS):
    validate_cues(cues,len(energy)/fps+.05)
    rows=[]
    for i,(start,end) in enumerate(cues):
        first=max(0,round(start*fps));last=min(len(energy),round(end*fps))
        active=[j for j in range(first,last) if energy[j]>=threshold]
        if not active: raise ValueError('no audible activity in cue '+str(i+1))
        rows.append({'cue':i+1,'start':start,'end':end,
                     'activity_ratio':round(len(active)/max(last-first,1),3),
                     'first_activity':round(active[0]/fps,3),
                     'last_activity_end':round((active[-1]+1)/fps,3),
                     'trailing_low_energy_s':round(end-(active[-1]+1)/fps,3)})
    return rows


def trim_last_cue(cues,rows,postroll=.12,min_tail=.35):
    out=list(cues)
    r=rows[-1]
    if r['trailing_low_energy_s']>min_tail:
        new_end=min(out[-1][1],round(r['last_activity_end']+postroll,2))
        if new_end-out[-1][0]>=.35: out[-1]=(out[-1][0],new_end)
    return tuple(out)


def meter_png(path,energy,frame,cues,threshold=THRESHOLD_DBFS):
    t=frame/FPS
    visible=any(s<=t<e for s,e in cues)
    im=Image.new('RGBA',(410,62),(0,0,0,0))
    if visible:
        d=ImageDraw.Draw(im)
        d.rounded_rectangle((0,0,409,61),radius=16,fill=(7,26,42,225),outline=(38,99,111,220),width=2)
        for j in range(18):
            idx=max(0,frame-(17-j)*2)
            db=energy[min(idx,len(energy)-1)]
            height=5 if db<threshold else min(42,max(8,int((db+35)*2.2)))
            x=18+j*20
            d.rounded_rectangle((x,31-height//2,x+11,31+height//2),radius=5,
                                fill=(61,215,222,235) if db>=threshold else (55,103,113,180))
    im.save(path)


def render(source,output,manifest,cues=CUES):
    source,output=Path(source),Path(output)
    if not source.is_file() or output.exists(): raise ValueError('missing source or output already exists')
    if manifest!={**POLICY,'source_sha256':digest(source)}:
        raise ValueError('fail closed: source review manifest invalid')
    energy=read_energy(source)
    original=analyze(energy,cues)
    updated=trim_last_cue(cues,original)
    adjusted=analyze(energy,updated)
    # No transcript exists: do not label this semantic or word-level alignment.
    with tempfile.TemporaryDirectory(prefix='cycle879_meter_') as td:
        folder=Path(td)
        for f in range(691): meter_png(folder/f'meter_{f:04d}.png',energy,f,updated)
        end=updated[-1][1]
        # Hide last caption during confirmed quiet tail; leave progress indicator intact.
        graph=(f"[0:v]drawbox=x=0:y=1495:w=1080:h=265:color=0x071326:t=fill:"
               f"enable='gte(t,{end})'[base];"
               "[base][1:v]overlay=x=95:y=1708:format=auto:shortest=1[v]")
        cmd=['ffmpeg','-hide_banner','-loglevel','error','-nostdin','-i',str(source),
             '-framerate',str(FPS),'-i',str(folder/'meter_%04d.png'),
             '-filter_complex',graph,'-map','[v]','-map','0:a:0',
             '-c:v','libx264','-preset','veryfast','-crf','19','-pix_fmt','yuv420p',
             '-r',str(FPS),'-frames:v','691','-c:a','copy',
             '-movflags','+faststart',str(output)]
        subprocess.run(cmd,check=True,timeout=240)
    return {'source_sha256':digest(source),'output_sha256':digest(output),
            'original_cues':original,'adjusted_cues':adjusted,
            'final_cue_end_before':cues[-1][1], 'final_cue_end_after':updated[-1][1],
            'threshold_dbfs':THRESHOLD_DBFS,
            'method':'RMS audio activity at 30 fps; NOT ASR or semantic synchronization',
            'voice_semantics_verified':False,'word_alignment_verified':False,
            'source_rights_verified':False,'policy':POLICY}


if __name__=='__main__':
    p=argparse.ArgumentParser()
    for n in ('source','output','manifest','report'):p.add_argument('--'+n,required=True)
    a=p.parse_args()
    m=json.loads(Path(a.manifest).read_text(encoding='utf-8'))
    result=render(a.source,a.output,m)
    Path(a.report).write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({'output':a.output,'final_cue_end':result['final_cue_end_after'],
                      'sha256':result['output_sha256']},ensure_ascii=False))
