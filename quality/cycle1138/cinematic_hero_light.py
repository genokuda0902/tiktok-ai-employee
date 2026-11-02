#!/usr/bin/env python3
"""Free/offline, fail-closed, review-only soft directional key-light sweep.

A generic overlay for an APPROVED/AUDITED subject ROI in any of ten genres.
It is not AI image generation or a substitute for human review. Private media
and approval manifests must never be committed.
"""
import argparse
import hashlib
import json
import math
import subprocess
import tempfile
from pathlib import Path
import numpy as np
from PIL import Image

POLICY = 'HUMAN_REVIEW/PUBLICATION_NOT_APPROVED'
GENRES = ('ai','business','money','learning','health','food','travel','beauty','career','life')
FPS = 30

def cmd(args):
    p=subprocess.run(args,capture_output=True,text=True)
    if p.returncode:
        raise RuntimeError(f'{args[0]} failed: {p.stderr[-2000:]}')
    return p.stdout

def sha256(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for block in iter(lambda:f.read(1048576),b''):h.update(block)
    return h.hexdigest()

def probe(path):
    d=json.loads(cmd(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(path)]))
    v=[s for s in d['streams'] if s['codec_type']=='video']
    a=[s for s in d['streams'] if s['codec_type']=='audio']
    if len(v)!=1 or len(a)!=1 or any(s['codec_type']=='subtitle' for s in d['streams']):
        raise ValueError('one video + one audio + no soft subtitles required')
    if v[0]['codec_name']!='h264' or a[0]['codec_name']!='aac' or a[0]['sample_rate']!='48000' or a[0].get('tags',{}).get('language')!='jpn':
        raise ValueError('H264 and AAC jpn 48kHz required')
    if (v[0]['width'],v[0]['height'],v[0]['avg_frame_rate'])!=(1080,1920,'30/1'):
        raise ValueError('1080x1920 30fps required')
    return {'frames':int(v[0]['nb_frames']),'duration':float(d['format']['duration'])}

def validate(m,actual_sha,spec):
    keys={'policy','asset_approval','source_sha256','genre','roi','start_frame','sweep_frames','color_rgb','max_alpha'}
    if set(m)!=keys:raise ValueError('unexpected/missing manifest fields')
    if m['policy']!=POLICY or m['asset_approval']!='private_review_only' or m['source_sha256']!=actual_sha:
        raise ValueError('source approval or SHA mismatch')
    if m['genre'] not in GENRES:raise ValueError('unsupported genre')
    roi=m['roi']
    if not isinstance(roi,dict) or set(roi)!={'x','y','width','height'} or any(type(v)!=int for v in roi.values()):raise ValueError('invalid ROI')
    x,y,w,h=(roi[k] for k in ('x','y','width','height'))
    # Conservative protected UI: header above y475, chapter and captions below y1000.
    if not (x>=50 and y>=475 and w>=300 and h>=250 and x+w<=1030 and y+h<=1000):
        raise ValueError('ROI outside audited subject-safe area')
    st,n=m['start_frame'],m['sweep_frames']
    if type(st)!=int or type(n)!=int or not (0<=st<=20 and 20<=n<=32 and st+n+1<min(35,spec['frames'])):
        raise ValueError('light sweep must fit audited robot-only opening beat')
    if not isinstance(m['color_rgb'],list) or len(m['color_rgb'])!=3 or any(type(v)!=int or v<0 or v>255 for v in m['color_rgb']):
        raise ValueError('invalid light color')
    if type(m['max_alpha']) not in (float,int) or not (0.05<=m['max_alpha']<=0.22):
        raise ValueError('unsafe light intensity')
    return x,y,w,h,st,n

def light_rgba(w,h,progress,color,max_alpha):
    """A diagonal Gaussian highlight with gentle temporal ramp and no hard seam."""
    if not 0<=progress<=1:raise ValueError('progress out of range')
    xx=np.arange(w,dtype=np.float32)[None,:]
    yy=np.arange(h,dtype=np.float32)[:,None]
    center=(-0.25+1.5*progress)*w
    diagonal=0.16*(yy-h/2)
    width=max(42,w*.18)
    spatial=np.exp(-0.5*((xx-center-diagonal)/width)**2)
    # Slowly fade in and out, no abrupt changes.
    temporal=math.sin(math.pi*progress)**1.2
    alpha=np.clip(spatial*temporal*max_alpha*255,0,255).astype(np.uint8)
    arr=np.empty((h,w,4),dtype=np.uint8)
    arr[:,:,:3]=color
    arr[:,:,3]=alpha
    return Image.fromarray(arr,'RGBA')

def render(source,output,manifest,report):
    source=Path(source);output=Path(output)
    spec=probe(source)
    x,y,w,h,st,n=validate(manifest,sha256(source),spec)
    output.parent.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='hero_light_') as temp:
        folder=Path(temp)
        blank=Image.new('RGBA',(w,h),(0,0,0,0))
        for i in range(st):blank.save(folder/f'light_{i:03d}.png',compress_level=1)
        for j in range(n):
            light_rgba(w,h,(j+1)/(n+1),tuple(manifest['color_rgb']),manifest['max_alpha']).save(folder/f'light_{st+j:03d}.png',compress_level=1)
        blank.save(folder/f'light_{st+n:03d}.png',compress_level=1)
        cmd(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(source),'-framerate','30','-i',str(folder/'light_%03d.png'),
             '-filter_complex',f'[0:v][1:v]overlay=x={x}:y={y}:eof_action=pass:repeatlast=0:format=auto[v]',
             '-map','[v]','-map','0:a:0','-frames:v',str(spec['frames']),'-c:v','libx264','-preset','veryfast','-crf','17',
             '-pix_fmt','yuv420p','-c:a','copy','-metadata:s:a:0','language=jpn','-movflags','+faststart',str(output)])
    dest=probe(output)
    if dest['frames']!=spec['frames'] or abs(dest['duration']-spec['duration'])>.04:raise RuntimeError('frame/duration mismatch')
    cmd(['ffmpeg','-v','error','-i',str(output),'-f','null','-'])
    r={'policy':POLICY,'source_sha256':sha256(source),'output_sha256':sha256(output),'frames':dest['frames'],
       'duration':dest['duration'],'resolution':[1080,1920],'fps':FPS,'roi':[x,y,w,h],
       'sweep_frames':n,'start_frame':st,'max_alpha':manifest['max_alpha'],
       'technique':'subtle animated cyan key-light sweep on audited opening subject ROI only',
       'audio':'AAC jpn 48kHz stream copy','subtitle_semantics':'NOT_VERIFIED','real_phone':'NOT_VERIFIED'}
    Path(report).write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf-8')
    return r

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--source',required=True);p.add_argument('--output',required=True)
    p.add_argument('--manifest',required=True);p.add_argument('--report',required=True)
    a=p.parse_args();print(json.dumps(render(a.source,a.output,json.loads(Path(a.manifest).read_text()),a.report),ensure_ascii=False,indent=2))
