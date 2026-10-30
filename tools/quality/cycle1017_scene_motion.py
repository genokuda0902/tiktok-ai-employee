"""Cycle1017: masked chapter-aware push-in for 10-genre vertical image slides.
No speech, subtitle, chapter or publication action is generated here.
"""
from __future__ import annotations
import argparse, json, subprocess
from pathlib import Path
from PIL import Image
import numpy as np

GENRES=('ai_work','business','education','career','finance','wellness','science','history','productivity','daily_tips')
FPS=30
X,Y,W,H=40,240,1000,1000
ZOOM_MAX=1.026

def chapters_frames(source:Path):
    obj=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_chapters','-of','json',str(source)]))
    chapters=obj['chapters']
    if not chapters: raise ValueError('Source lacks scene chapter boundaries')
    b=[round(float(c['start_time'])*FPS) for c in chapters]+[round(float(chapters[-1]['end_time'])*FPS)]
    if b[0]!=0 or any(y<=x for x,y in zip(b,b[1:])): raise ValueError('Invalid chapter boundaries')
    return b

def make_mask(path:Path):
    xx=np.minimum(np.arange(W),W-1-np.arange(W))
    yy=np.minimum(np.arange(H),H-1-np.arange(H))
    ax=.5-.5*np.cos(np.pi*np.clip(xx/52,0,1))
    ay=.5-.5*np.cos(np.pi*np.clip(yy/62,0,1))
    mask=np.uint8(np.rint(255*np.minimum(ay[:,None],ax[None,:])))
    path.parent.mkdir(parents=True,exist_ok=True)
    Image.fromarray(mask,'L').save(path)

def progress_expr(bounds):
    e='0'
    for a,b in reversed(list(zip(bounds[:-1],bounds[1:]))):
        e=f'if(lt(on,{b}),(on-{a})/{b-a},{e})'
    return e

def build_filter(bounds,zoom=ZOOM_MAX):
    if not (1.001<=zoom<=1.035): raise ValueError('Zoom exceeds safe range')
    z=f'1+{zoom-1:.5f}*pow(sin(PI*({progress_expr(bounds)})),2)'
    return (f'[0:v]split=2[base][region];'
            f'[region]crop={W}:{H}:{X}:{Y},'
            f"zoompan=z='{z}':x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2':d=1:s={W}x{H}:fps={FPS},"
            f'format=yuv420p[zoomed];'
            f'[1:v]format=gray[alpha];'
            f'[zoomed][alpha]alphamerge[feathered];'
            f'[base][feathered]overlay={X}:{Y}:shortest=1:format=auto,format=yuv420p[v]')

def render(src:Path,dst:Path,genre='ai_work',zoom=ZOOM_MAX):
    if genre not in GENRES: raise ValueError('Unknown genre')
    dst.parent.mkdir(parents=True,exist_ok=True)
    bounds=chapters_frames(src)
    mask=dst.parent/'feather_mask.png'
    make_mask(mask)
    cmd=['ffmpeg','-hide_banner','-y','-loglevel','error','-i',str(src),
         '-loop','1','-framerate',str(FPS),'-i',str(mask),
         '-filter_complex',build_filter(bounds,zoom),'-map','[v]','-map','0:a:0',
         '-map_metadata','0','-map_chapters','0','-c:v','libx264','-preset','veryfast',
         '-crf','18','-pix_fmt','yuv420p','-r',str(FPS),'-c:a','copy',
         '-movflags','+faststart',str(dst)]
    subprocess.run(cmd,check=True)
    return bounds

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('src',type=Path);p.add_argument('dst',type=Path)
    p.add_argument('--genre',choices=GENRES,default='ai_work')
    p.add_argument('--zoom',type=float,default=ZOOM_MAX)
    a=p.parse_args();print(render(a.src,a.dst,a.genre,a.zoom))
