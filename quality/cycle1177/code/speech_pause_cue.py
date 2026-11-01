#!/usr/bin/env python3
"""Review-only acoustic-pause cue; no ASR, posting, or paid media."""
from __future__ import annotations
import argparse, json, math, re, subprocess, tempfile
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter

GENRES={'ai':'#57e0d3','business':'#79d9ce','money':'#a0e6b0',
'learning':'#70caff','health':'#75e3bb','food':'#f0cc86',
'travel':'#85caff','beauty':'#e7aadf','career':'#78e1d1','life':'#a5dba9'}
SIZE=96; FPS=30; DEFAULT_CUE_XY=(26,1510)
SILENCE_RE=re.compile(r'silence_(start|end):\s*([0-9.]+)')

def command(args,**kwargs):
    return subprocess.run(args,check=True,**kwargs)

def probe(path):
    p=command(['ffprobe','-v','error','-show_streams','-show_chapters',
               '-show_format','-of','json',str(path)],capture_output=True,text=True)
    return json.loads(p.stdout)

def parse_silences(log):
    intervals=[];start=None
    for kind,value in SILENCE_RE.findall(log):
        t=float(value)
        if kind=='start':start=t
        elif start is not None and t>start:
            intervals.append((start,t));start=None
    return intervals

def find_silences(path,noise='-36dB',minimum=.28):
    p=command(['ffmpeg','-nostdin','-hide_banner','-i',str(path),
               '-vn','-af',f'silencedetect=noise={noise}:d={minimum}',
               '-f','null','-'],capture_output=True,text=True)
    return parse_silences(p.stderr)

def get_chapters(meta):
    chapters=[(float(x['start_time']),float(x['end_time']))
              for x in meta.get('chapters',[])]
    return chapters or [(0.,float(meta['format']['duration']))]

def select_cues(chapters,silences,min_silence=.28,offset=.025):
    result=[]
    for start,end in chapters:
        options=[(a,b) for a,b in silences if b-a>=min_silence
                 and a>=start+.25 and b<=end-.24]
        if options:
            a,b=min(options,key=lambda x:abs((x[0]+x[1])/2-(start+end)/2))
            result.append(round(b+offset,3))
    return result

def pulse_alpha(t,onset,duration=.36):
    if duration<=0:raise ValueError('duration must be positive')
    u=(t-onset)/duration
    return math.sin(math.pi*u)**1.4 if 0<u<1 else 0.

def rgba_color(color,alpha):
    return tuple(bytes.fromhex(color.lstrip('#')))+(max(0,min(255,alpha)),)

def cue_frame(color,strength):
    if not 0<=strength<=1:raise ValueError('invalid strength')
    base=Image.new('RGBA',(SIZE,SIZE),(0,0,0,0))
    if strength<.002:return base
    halo=Image.new('RGBA',(SIZE,SIZE),(0,0,0,0))
    d=ImageDraw.Draw(halo)
    d.ellipse((18,18,78,78),fill=rgba_color(color,int(80*strength)))
    base=Image.alpha_composite(base,halo.filter(ImageFilter.GaussianBlur(13)))
    d=ImageDraw.Draw(base)
    d.ellipse((29,29,67,67),outline=rgba_color(color,int(220*strength)),width=4)
    d.ellipse((41,41,55,55),fill=rgba_color('#ffffff',int(190*strength)))
    return base

def validate_source(meta,genre,xy=DEFAULT_CUE_XY):
    if genre not in GENRES:raise ValueError('unknown genre')
    videos=[s for s in meta['streams'] if s['codec_type']=='video']
    audios=[s for s in meta['streams'] if s['codec_type']=='audio']
    if len(videos)!=1 or not audios or audios[0]['codec_name']!='aac':
        raise ValueError('one video and AAC audio required')
    v=videos[0]
    if (int(v['width']),int(v['height']))!=(1080,1920):
        raise ValueError('requires 1080x1920')
    x,y=xy
    if not (0<=x<=120 and 1400<=y<=1530 and x+SIZE<=125 and y+SIZE<=1640):
        raise ValueError('cue outside protected left margin')
    return int(v['nb_frames'])

def make_overlay(path,frames,cues,color,fps=FPS):
    cmd=['ffmpeg','-nostdin','-y','-hide_banner','-loglevel','error',
         '-f','rawvideo','-pixel_format','rgba','-video_size',f'{SIZE}x{SIZE}',
         '-framerate',str(fps),'-i','pipe:0','-vf','format=argb',
         '-c:v','qtrle','-pix_fmt','argb',str(path)]
    proc=subprocess.Popen(cmd,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
    try:
        for f in range(frames):
            t=f/fps
            strength=max((pulse_alpha(t,c) for c in cues),default=0.)
            proc.stdin.write(cue_frame(color,strength).tobytes())
        proc.stdin.close()
        error=proc.stderr.read()
        if proc.wait()!=0:raise RuntimeError(error.decode(errors='replace')[-2000:])
    finally:
        if proc.poll() is None:proc.kill()

def render(src,dst,*,genre='ai',xy=DEFAULT_CUE_XY,
           silence_override=None,chapters_override=None):
    if src.resolve()==dst.resolve():raise ValueError('source overwrite refused')
    meta=probe(src);n=validate_source(meta,genre,xy)
    chapters=chapters_override if chapters_override is not None else get_chapters(meta)
    silences=silence_override if silence_override is not None else find_silences(src)
    cues=select_cues(chapters,silences)
    if not cues:raise RuntimeError('no speech pause; refusing unsynced cue')
    dst.parent.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory() as td:
        overlay=Path(td)/'pause_overlay.mov'
        make_overlay(overlay,n,cues,GENRES[genre])
        x,y=xy
        command(['ffmpeg','-nostdin','-hide_banner','-loglevel','error','-y',
                 '-i',str(src),'-i',str(overlay),
                 '-filter_complex',f'[0:v][1:v]overlay=x={x}:y={y}:shortest=1:format=auto,format=yuv420p[v]',
                 '-map','[v]','-map','0:a:0','-map_metadata','0','-map_chapters','0',
                 '-c:v','libx264','-preset','veryfast','-crf','17','-pix_fmt','yuv420p',
                 '-c:a','copy','-movflags','+faststart','-frames:v',str(n),str(dst)])
    return {'genre':genre,'chapters':chapters,'silences':silences,'cues':cues,
            'frames':n,'cue_position':xy,'independent_japanese_asr':False,
            'publication':'HUMAN_REVIEW / PUBLICATION_NOT_APPROVED'}

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('source',type=Path);p.add_argument('output',type=Path)
    p.add_argument('--genre',choices=tuple(GENRES),default='ai')
    p.add_argument('--report',type=Path)
    a=p.parse_args()
    result=render(a.source,a.output,genre=a.genre)
    if a.report:
        a.report.parent.mkdir(parents=True,exist_ok=True)
        a.report.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(result,ensure_ascii=False))
