#!/usr/bin/env python3
"""Review-only CTA step counter/ticks; private source MP4 stays local.
Only ai_work geometry is reviewed; all other real genres fail closed.
"""
import argparse
import hashlib
import json
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

FPS=30
START=609
END=691
SAFE_Y=1440
GENRES=('ai_work','finance','learning','health','travel','food','science','history','business','lifestyle')
CARDS=((73,375,856,516),(73,540,856,682),(73,704,856,849))

def execute(cmd):
    return subprocess.run(cmd,capture_output=True,text=True,check=True)

def sha256(path):
    h=hashlib.sha256()
    with open(path,'rb') as stream:
        for data in iter(lambda:stream.read(1<<20),b''):h.update(data)
    return h.hexdigest()

def probe(path):
    return json.loads(execute(['ffprobe','-v','error','-show_entries',
      'stream=codec_type,codec_name,width,height,r_frame_rate,nb_frames,sample_rate,channels',
      '-show_entries','format=duration','-of','json',str(path)]).stdout)

def validate(genre,synthetic=False):
    if genre not in GENRES:raise ValueError('Unknown genre')
    if genre!='ai_work' and not synthetic:raise ValueError('Unreviewed CTA coordinates; fail closed')

def focus_step(i,count):
    if not 0<=i<count:raise ValueError('Frame index out of range')
    return min(2,3*i//count)

def overlay_frame(i,count):
    """Transparent artwork restricted to y<1440: never paint Japanese captions."""
    active=focus_step(i,count)
    canvas=Image.new('RGBA',(1080,SAFE_Y),(0,0,0,0))
    d=ImageDraw.Draw(canvas,'RGBA')
    # The inherited CTA already highlights the active card. Only add completed
    # ticks and the 1/3,2/3,3/3 counter; do not duplicate its focus border.
    for j,(x0,y0,x1,y1) in enumerate(CARDS):
        if j<active:
            d.ellipse((786,y0+22,839,y0+75),fill=(14,85,79,238),
                      outline=(89,242,210,245),width=3)
            d.line(((798,y0+49),(808,y0+59),(827,y0+36)),
                   fill=(208,255,246,255),width=6,joint='curve')
    d.rounded_rectangle((739,259,859,322),radius=17,
                        fill=(10,48,63,225),outline=(98,235,218,190),width=3)
    font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',33)
    d.text((762,268),f'{active+1}/3',font=font,fill=(217,255,247,255))
    return canvas

def render(source,output,work,genre='ai_work',synthetic=False,start=START,end=END):
    validate(genre,synthetic)
    source,output,work=map(Path,(source,output,work))
    if not source.is_file():raise FileNotFoundError(source)
    meta=probe(source)
    v=[x for x in meta['streams'] if x['codec_type']=='video']
    a=[x for x in meta['streams'] if x['codec_type']=='audio']
    if len(v)!=1 or len(a)!=1 or v[0]['codec_name']!='h264' or a[0]['codec_name']!='aac':
        raise ValueError('Expected H.264 video with AAC audio')
    if (v[0]['width'],v[0]['height'],v[0]['r_frame_rate'])!=(1080,1920,'30/1'):
        raise ValueError('Unreviewed resolution/fps; fail closed')
    n=int(v[0].get('nb_frames') or 0)
    if not 0<=start<end<=n:raise ValueError('Invalid CTA frame range')
    work.mkdir(parents=True,exist_ok=True)
    output.parent.mkdir(parents=True,exist_ok=True)
    frames=work/'overlays'
    frames.mkdir(exist_ok=True)
    for i in range(end-start):
        overlay_frame(i,end-start).save(frames/f'{i:04d}.png',compress_level=3)
    graph=(f'[1:v]format=rgba,setpts=PTS-STARTPTS+{start}/{FPS}/TB[focus];'
           f"[0:v][focus]overlay=x=0:y=0:eof_action=pass:enable='between(n,{start},{end-1})'[v]")
    execute(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(source),
             '-framerate',str(FPS),'-i',str(frames/'%04d.png'),
             '-filter_complex',graph,'-map','[v]','-map','0:a:0',
             '-c:v','libx264','-preset','ultrafast' if synthetic else 'veryfast',
             '-crf','19','-pix_fmt','yuv420p','-r',str(FPS),'-frames:v',str(n),
             '-c:a','copy','-movflags','+faststart',str(output)])
    after=probe(output)
    va=[x for x in after['streams'] if x['codec_type']=='video'][0]
    aa=[x for x in after['streams'] if x['codec_type']=='audio'][0]
    if int(va.get('nb_frames') or 0)!=n or aa['codec_name']!='aac':
        raise RuntimeError('Output stream count/codec failed')
    return dict(source_sha256=sha256(source),output_sha256=sha256(output),
                start_frame=start,end_exclusive=end,frames=n,
                protected_caption_y=SAFE_Y,genre=genre,
                review_only=True,publication_approved=False)

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--source',required=True);p.add_argument('--output',required=True)
    p.add_argument('--work',required=True);p.add_argument('--genre',default='ai_work')
    p.add_argument('--synthetic',action='store_true')
    p.add_argument('--start',type=int,default=START)
    p.add_argument('--end',type=int,default=END)
    a=p.parse_args()
    print(json.dumps(render(a.source,a.output,a.work,a.genre,a.synthetic,a.start,a.end),indent=2))
