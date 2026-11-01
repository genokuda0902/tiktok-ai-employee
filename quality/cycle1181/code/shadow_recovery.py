#!/usr/bin/env python3
"""Panel-local shadow visibility recovery for review-only 1080x1920 slides.

The narration, subtitles, header and footer are protected by geometry.
This does not verify Japanese speech, rights or publication readiness.
"""
from __future__ import annotations
import argparse
import json
import subprocess
from pathlib import Path

GENRE_GAMMA = {
    'ai': 1.15, 'business': 1.13, 'money': 1.12,
    'learning': 1.15, 'health': 1.10, 'food': 1.09,
    'travel': 1.09, 'beauty': 1.08, 'career': 1.12,
    'life': 1.10,
}
DEFAULT_ROI = (60, 390, 960, 930)

def probe(path):
    r = subprocess.run(['ffprobe','-v','error','-show_streams','-show_format',
                        '-show_chapters','-of','json',str(path)],check=True,
                       capture_output=True,text=True)
    return json.loads(r.stdout)

def validate(meta, genre, roi):
    if genre not in GENRE_GAMMA:
        raise ValueError('unsupported genre')
    if len(roi) != 4 or any(type(v) is not int for v in roi):
        raise ValueError('ROI must be four integers')
    x,y,w,h=roi
    if x<40 or y<350 or w<=0 or h<=0 or x+w>1040 or y+h>1330 or any(v%2 for v in roi):
        raise ValueError('ROI overlaps protected header, subtitle, footer or frame boundary')
    vids=[s for s in meta['streams'] if s.get('codec_type')=='video']
    auds=[s for s in meta['streams'] if s.get('codec_type')=='audio']
    if len(vids)!=1 or not auds or auds[0].get('codec_name')!='aac':
        raise ValueError('requires single video and AAC audio')
    v=vids[0]
    if (int(v['width']),int(v['height']))!=(1080,1920) or v.get('r_frame_rate')!='30/1':
        raise ValueError('requires 1080x1920 at 30 fps')
    return int(v['nb_frames'])

def graph(genre, roi):
    x,y,w,h=roi
    gamma=GENRE_GAMMA[genre]
    return (f'[0:v]split[base][region];'
            f'[region]crop={w}:{h}:{x}:{y},'
            f'eq=gamma={gamma:.3f}:contrast=1.000:brightness=0.000:saturation=1.020[lift];'
            f'[base][lift]overlay={x}:{y}:shortest=1,format=yuv420p[v]')

def render(source, output, genre='ai', roi=DEFAULT_ROI):
    source,output=Path(source),Path(output)
    if source.resolve()==output.resolve():
        raise ValueError('source overwrite forbidden')
    n=validate(probe(source),genre,roi)
    output.parent.mkdir(parents=True,exist_ok=True)
    cmd=['ffmpeg','-nostdin','-hide_banner','-loglevel','error','-y','-i',str(source),
         '-filter_complex',graph(genre,roi),'-map','[v]','-map','0:a:0',
         '-map_metadata','0','-map_chapters','0','-c:v','libx264',
         '-preset','veryfast','-crf','17','-pix_fmt','yuv420p',
         '-c:a','copy','-frames:v',str(n),'-movflags','+faststart',str(output)]
    subprocess.run(cmd,check=True)
    actual=probe(output)
    v=next(s for s in actual['streams'] if s['codec_type']=='video')
    if int(v['nb_frames'])!=n:
        raise RuntimeError(f'frame count mismatch: {v["nb_frames"]} != {n}')
    return {'genre':genre,'gamma':GENRE_GAMMA[genre],'roi':roi,'frames':n,
            'semantic_asr_verified':False,'publication_approved':False}

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('source');p.add_argument('output')
    p.add_argument('--genre',default='ai',choices=GENRE_GAMMA)
    args=p.parse_args()
    print(json.dumps(render(args.source,args.output,args.genre),ensure_ascii=False,indent=2))
