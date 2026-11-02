#!/usr/bin/env python3
"""Render original, proportionally accurate micro-bars over approved review-only proof cards.

This deliberately uses no network, external art, fonts, models, music, or paid APIs.
Never publishes. No raw MP4, staff information, or private manifest belongs in Git.
"""
import argparse
import hashlib
import json
import math
import subprocess
import tempfile
from pathlib import Path
from PIL import Image, ImageDraw

POLICY = 'HUMAN_REVIEW/PUBLICATION_NOT_APPROVED'
GENRES = ('ai', 'business', 'money', 'learning', 'health', 'food', 'travel', 'beauty', 'career', 'life')
FPS = 30


def run(cmd):
    p = subprocess.run(cmd, capture_output=True, text=True)
    if p.returncode:
        raise RuntimeError(f"{' '.join(map(str,cmd[:3]))}: {p.stderr[-2000:]}")
    return p.stdout


def sha256(path):
    h = hashlib.sha256()
    with open(path,'rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''):
            h.update(b)
    return h.hexdigest()


def probe(path):
    d = json.loads(run(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(path)]))
    v = [s for s in d['streams'] if s['codec_type']=='video']
    a = [s for s in d['streams'] if s['codec_type']=='audio']
    s = [s for s in d['streams'] if s['codec_type']=='subtitle']
    if len(v)!=1 or len(a)!=1 or s:
        raise ValueError('requires one video, one audio, no soft subtitles')
    if v[0]['codec_name']!='h264' or a[0]['codec_name']!='aac' or a[0]['sample_rate']!='48000':
        raise ValueError('requires H264/AAC 48kHz')
    if v[0]['width']*16!=v[0]['height']*9 or v[0]['avg_frame_rate']!='30/1':
        raise ValueError('requires portrait 9:16 30fps')
    if a[0].get('tags',{}).get('language')!='jpn':
        raise ValueError('requires Japanese audio language tag')
    return {'width':v[0]['width'],'height':v[0]['height'],'frames':int(v[0].get('nb_frames',0)),
            'duration':float(d['format']['duration'])}


def validate_manifest(m, source_sha, spec):
    keys={'policy','asset_approval','source_sha256','genre','scene_start','scene_end','values','monthly_rows','roi'}
    if set(m)!=keys:
        raise ValueError('unexpected manifest fields')
    if m['policy']!=POLICY or m['asset_approval']!='private_review_only' or m['source_sha256']!=source_sha:
        raise ValueError('approval/hash mismatch')
    if m['genre'] not in GENRES:
        raise ValueError('unknown genre')
    vals=m['values']; rows=m['monthly_rows']; roi=m['roi']
    if not isinstance(vals,list) or len(vals)!=3 or any(type(v)!=int or v<=0 for v in vals):
        raise ValueError('positive integer proof values required')
    if vals[0]+vals[1]!=vals[2]:
        raise ValueError('displayed total does not equal source values')
    if not isinstance(rows,list) or len(rows)<1 or any(not isinstance(r,list) or len(r)!=2 or any(type(v)!=int or v<0 for v in r) for r in rows):
        raise ValueError('source row evidence missing')
    if sum(r[0] for r in rows)!=vals[0] or sum(r[1] for r in rows)!=vals[1]:
        raise ValueError('monthly row evidence does not match displayed values')
    if type(m['scene_start']) not in (int,float) or type(m['scene_end']) not in (int,float):
        raise ValueError('invalid scene times')
    start=float(m['scene_start']); end=float(m['scene_end'])
    if not (0<=start<end<=spec['duration']-0.05 and end-start>=2.0):
        raise ValueError('unsafe scene timing')
    if abs(start*FPS-round(start*FPS))>1e-5 or abs(end*FPS-round(end*FPS))>1e-5:
        raise ValueError('times must align to frame boundaries')
    if not isinstance(roi,dict) or set(roi)!={'x','y','width','height'} or any(type(n)!=int for n in roi.values()):
        raise ValueError('invalid ROI')
    if not (0<=roi['x'] and 0<=roi['y'] and roi['width']>=900 and roi['height']>=40 and
            roi['x']+roi['width']<=spec['width'] and roi['y']+roi['height']<=min(1100,spec['height']*0.65)):
        raise ValueError('ROI may overlap subtitles or leave the frame')
    if roi['width']!=960 or roi['height']!=50:
        raise ValueError('this audited card geometry requires an 960x50 ROI')
    return start,end


def eased(x):
    x=max(0.,min(1.,x));return x*x*(3-2*x)


def draw_overlay_frame(m, t):
    vals=m['values']; img=Image.new('RGBA',(960,50),(0,0,0,0)); d=ImageDraw.Draw(img,'RGBA')
    # Three independently timed fills, each proportional to the independently verified total.
    starts=[0.15,0.80,1.50]; duration=0.60
    for i,(v,x,c) in enumerate(zip(vals,[25,365,695],[(65,222,205,255),(99,180,249,255),(255,205,100,255)])):
        d.rounded_rectangle((x,18,x+240,31),radius=6,fill=(8,24,43,190),outline=(160,212,226,120),width=1)
        progress=eased((t-starts[i])/duration)
        w=round(236*(v/vals[2])*progress)
        if w>=2:
            d.rounded_rectangle((x+2,20,x+2+w,29),radius=4,fill=c)
    return img


def render(source,output,manifest,report):
    spec=probe(source); start,end=validate_manifest(manifest,sha256(source),spec)
    output=Path(output);output.parent.mkdir(parents=True,exist_ok=True)
    roi=manifest['roi']; count=round((end-start)*FPS)
    with tempfile.TemporaryDirectory(prefix='proof_bars_') as tmp:
        for n in range(count):
            t=n/FPS
            draw_overlay_frame(manifest,t).save(Path(tmp)/f'overlay_{n:04d}.png',compress_level=1)
        run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(source),'-itsoffset',f'{start:.6f}',
             '-framerate','30','-start_number','0','-i',str(Path(tmp)/'overlay_%04d.png'),
             '-filter_complex',f'[0:v][1:v]overlay=x={roi["x"]}:y={roi["y"]}:eof_action=pass:shortest=0:format=auto[v]',
             '-map','[v]','-map','0:a:0','-c:v','libx264','-preset','veryfast','-crf','17',
             '-pix_fmt','yuv420p','-c:a','copy','-metadata:s:a:0','language=jpn','-movflags','+faststart',str(output)])
    out=probe(output)
    if out['width']!=spec['width'] or out['height']!=spec['height'] or out['frames']!=spec['frames'] or abs(out['duration']-spec['duration'])>0.04:
        raise RuntimeError('render changed duration, dimensions, or frame count')
    run(['ffmpeg','-v','error','-i',str(output),'-f','null','-'])
    result={'source_sha256':sha256(source),'output_sha256':sha256(output),'duration':out['duration'],
            'frames':out['frames'],'resolution':[out['width'],out['height']],'fps':FPS,
            'values':manifest['values'],'row_sums':[sum(r[i] for r in manifest['monthly_rows']) for i in (0,1)],
            'scene':[start,end],'overlay_roi':roi,'rendered_overlay_frames':count,
            'subtitle_streams':0,'audio_codec':'AAC 48kHz Japanese (stream copied)',
            'review_only':True,'asr_semantics':'NOT_VERIFIED','real_phone':'NOT_VERIFIED'}
    Path(report).write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    return result


def main():
    p=argparse.ArgumentParser();p.add_argument('--source',required=True);p.add_argument('--output',required=True)
    p.add_argument('--manifest',required=True);p.add_argument('--report',required=True)
    a=p.parse_args();m=json.loads(Path(a.manifest).read_text(encoding='utf-8'))
    print(json.dumps(render(a.source,a.output,m,a.report),ensure_ascii=False,indent=2))

if __name__=='__main__':main()
