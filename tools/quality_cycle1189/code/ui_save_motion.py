#!/usr/bin/env python3
"""Offline 10-genre reusable UI action cursor for review-only 9:16 slide videos.

Renders a vector-style cursor, eased travel, click ripple, and confirmation check
within a bounded UI demonstration region. Never touches voice, caption or footer
pixels outside the configured overlay rectangle. No external assets, API or upload.
"""
from __future__ import annotations
import argparse
from dataclasses import dataclass
import json
import math
from pathlib import Path
import subprocess
import tempfile
from PIL import Image, ImageDraw

GENRES = ('ai','business','money','learning','health','food','travel','beauty','career','life')
COLORS = {'ai':(69,207,192),'business':(83,164,241),'money':(111,217,146),
          'learning':(247,183,77),'health':(82,207,167),'food':(250,157,100),
          'travel':(104,181,247),'beauty':(237,151,201),'career':(151,172,251),
          'life':(196,182,133)}
FPS=30
WIDTH=1080
HEIGHT=1920

@dataclass(frozen=True)
class Plan:
    start:float=16.633
    duration:float=2.20
    box_x:int=260
    box_y:int=650
    box_w:int=710
    box_h:int=510
    source_xy:tuple[int,int]=(348,925)
    target_xy:tuple[int,int]=(742,905)
    check_xy:tuple[int,int]=(910,768)


def check_plan(p:Plan):
    if p.start<0 or not 0.6<=p.duration<=4.0: raise ValueError('invalid scene timing')
    if min(p.box_x,p.box_y)<0 or p.box_x+p.box_w>WIDTH or p.box_y+p.box_h>1200:
        raise ValueError('overlay must remain in video demonstration safe area, above captions')
    for x,y in (p.source_xy,p.target_xy,p.check_xy):
        if not (p.box_x+50<=x<=p.box_x+p.box_w-50 and p.box_y+50<=y<=p.box_y+p.box_h-50):
            raise ValueError('cursor path or check would clip outside safe region')
    return True


def ease(u):
    u=max(0.,min(1.,u));return u*u*(3-2*u)


def position(t:float,p:Plan):
    q=ease((t-.26)/1.08)
    return (p.source_xy[0]+(p.target_xy[0]-p.source_xy[0])*q,
            p.source_xy[1]+(p.target_xy[1]-p.source_xy[1])*q)


def paint_cursor(d,x,y,color,alpha):
    x=int(x);y=int(y)
    polygon=[(x,y),(x+4,y+43),(x+14,y+32),(x+22,y+48),
             (x+31,y+44),(x+22,y+28),(x+37,y+25)]
    d.polygon([(a+3,b+3) for a,b in polygon],fill=(0,0,0,int(alpha*.5)))
    d.polygon(polygon,fill=(250,253,253,alpha),outline=(13,41,48,alpha),width=3)
    d.line([(x+7,y+13),(x+11,y+30)],fill=(*color,alpha),width=2)


def generate_frames(folder:Path,genre='ai',p:Plan=Plan()):
    if genre not in GENRES:raise ValueError('unknown genre')
    check_plan(p)
    folder=Path(folder);folder.mkdir(parents=True,exist_ok=True)
    if any(folder.iterdir()):raise ValueError('overlay directory must be empty')
    color=COLORS[genre]
    count=round(p.duration*FPS)
    for i in range(count):
        t=i/FPS
        im=Image.new('RGBA',(p.box_w,p.box_h),(0,0,0,0))
        d=ImageDraw.Draw(im,'RGBA')
        def loc(xy):return (round(xy[0]-p.box_x),round(xy[1]-p.box_y))
        if .32<=t<=1.55:
            trail=[]
            for k in range(12):
                tt=max(.0,t-.045*k)
                trail.append(loc(position(tt,p)))
            for k in range(10,0,-1):
                x,y=trail[k]
                r=max(2,6-k//3)
                d.ellipse((x-r,y-r,x+r,y+r),fill=(*color,max(5,52-k*4)))
        if t<=1.88:
            x,y=loc(position(t,p))
            alpha=round(255*min(1,(1.88-t)/.25)) if t>1.63 else 255
            paint_cursor(d,x,y,color,alpha)
        if 1.37<=t<=1.92:
            u=(t-1.37)/.55
            x,y=loc(p.target_xy)
            r=17+55*u
            d.ellipse((x-r,y-r,x+r,y+r),outline=(*color,round(185*(1-u))),width=5)
            r2=9+30*u
            d.ellipse((x-r2,y-r2,x+r2,y+r2),outline=(240,255,253,round(120*(1-u))),width=3)
        if 1.55<=t<=2.16:
            a=round(220*min(1,(t-1.55)/.15,(2.16-t)/.18))
            x,y=loc(p.check_xy);r=19
            d.ellipse((x-r,y-r,x+r,y+r),fill=(*color,a),outline=(245,255,255,a),width=2)
            d.line([(x-9,y),(x-2,y+7),(x+10,y-8)],fill=(255,255,255,a),width=5,joint='curve')
        im.save(folder/f'{i:04d}.png',optimize=True)
    return count


def cmd(*args):
    return subprocess.run(args,check=True,capture_output=True,text=True).stdout


def probe(path):
    return json.loads(cmd('ffprobe','-v','error','-show_streams','-show_format','-show_chapters','-of','json',str(path)))


def validate_source(path,p):
    check_plan(p)
    path=Path(path)
    if not path.is_file():raise FileNotFoundError(path)
    data=probe(path)
    vs=[s for s in data['streams'] if s['codec_type']=='video']
    aud=[s for s in data['streams'] if s['codec_type']=='audio']
    if len(vs)!=1 or len(aud)!=1:raise ValueError('one video and one narration track required')
    v,a=vs[0],aud[0]
    if (int(v['width']),int(v['height']),v['r_frame_rate'])!=(WIDTH,HEIGHT,'30/1'):
        raise ValueError('source must be 1080x1920/30fps')
    if a['codec_name']!='aac' or int(a['sample_rate'])!=48000:
        raise ValueError('source must contain AAC 48kHz narration')
    if p.start+p.duration>float(data['format']['duration'])-.01:
        raise ValueError('overlay extends beyond source')
    return data


def render(source,output,genre='ai',p:Plan=Plan(),preset='medium',crf=17):
    if genre not in GENRES:raise ValueError('unknown genre')
    src,dst=Path(source),Path(output)
    if src.resolve()==dst.resolve() or dst.exists():raise ValueError('never overwrite source or existing output')
    before=validate_source(src,p)
    dst.parent.mkdir(parents=True,exist_ok=True)
    partial=dst.with_name(dst.stem+'.partial.mp4')
    if partial.exists():raise ValueError('partial output exists')
    with tempfile.TemporaryDirectory(prefix='ui_motion_') as td:
        folder=Path(td)/'frames'
        count=generate_frames(folder,genre,p)
        command=['ffmpeg','-nostdin','-hide_banner','-loglevel','error','-i',str(src),
            '-itsoffset',str(p.start),'-framerate',str(FPS),'-start_number','0',
            '-i',str(folder/'%04d.png'),
            '-filter_complex',f'[0:v][1:v]overlay=x={p.box_x}:y={p.box_y}:format=auto:eof_action=pass:shortest=0,format=yuv420p[v]',
            '-map','[v]','-map','0:a:0','-map_metadata','0','-map_chapters','0',
            '-c:v','libx264','-preset',preset,'-crf',str(crf),'-r','30',
            '-pix_fmt','yuv420p','-c:a','copy','-movflags','+faststart',
            '-metadata:s:a:0','language=jpn',str(partial)]
        try:
            subprocess.run(command,check=True,capture_output=True,text=True)
            after=probe(partial)
            v0=next(s for s in before['streams'] if s['codec_type']=='video')
            v1=next(s for s in after['streams'] if s['codec_type']=='video')
            a1=next(s for s in after['streams'] if s['codec_type']=='audio')
            if v1['nb_frames']!=v0['nb_frames'] or (int(v1['width']),int(v1['height']))!=(WIDTH,HEIGHT):
                raise RuntimeError('frame count or geometry mismatch')
            if a1['codec_name']!='aac' or int(a1['sample_rate'])!=48000:
                raise RuntimeError('audio format changed')
            if abs(float(after['format']['duration'])-float(before['format']['duration']))>.06:
                raise RuntimeError('duration mismatch')
            partial.rename(dst)
        except BaseException:
            if partial.exists():partial.unlink()
            raise
    return {'genre':genre,'frames':int(v1['nb_frames']),'overlay_frames':count,
            'scene_start':p.start,'scene_duration':p.duration,'overlay_box':[p.box_x,p.box_y,p.box_w,p.box_h],
            'caption_region_untouched_by_overlay':True,'narration_stream_copied':True,
            'independent_asr':False,'publication_approved':False}

if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('source');ap.add_argument('output');ap.add_argument('--genre',choices=GENRES,default='ai')
    ap.add_argument('--start',type=float,default=16.633)
    ap.add_argument('--duration',type=float,default=2.20)
    args=ap.parse_args()
    print(json.dumps(render(args.source,args.output,args.genre,Plan(start=args.start,duration=args.duration)),ensure_ascii=False,indent=2))
