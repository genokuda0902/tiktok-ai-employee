"""Zero-cost 10-genre scene-progress rail for portrait Japanese slide videos.

Scene progress is time-based, NOT speech-to-text or word-level subtitle sync.
Private MP4 files are never included in this repository.
"""
from __future__ import annotations
import argparse
import json
import subprocess
from pathlib import Path

import numpy as np
from PIL import Image

FPS = 30
TOTAL_FRAMES = 675
SCENE_STARTS = (0, 42, 94, 168, 250, 330, 412, 499)
SCENE_ENDS = SCENE_STARTS[1:] + (TOTAL_FRAMES,)
ROI = (130, 1600, 620, 18)
GENRE_COLORS = {
    'ai-work': (74, 223, 207), 'finance': (244, 203, 126),
    'career': (125, 222, 168), 'health': (103, 213, 192),
    'learning': (122, 187, 247), 'travel': (244, 170, 130),
    'technology': (129, 171, 250), 'business': (95, 215, 201),
    'life': (235, 160, 204), 'history': (232, 194, 139),
}

def validate(starts=SCENE_STARTS, total=TOTAL_FRAMES, fps=FPS, roi=ROI):
    if not isinstance(total, int) or total <= 0 or fps <= 0:
        raise ValueError('Invalid video length or frame rate')
    if not starts or starts[0] != 0 or sorted(set(starts)) != list(starts):
        raise ValueError('Scene starts must be unique, sorted and begin at zero')
    if not all(isinstance(n,int) and 0 <= n < total for n in starts):
        raise ValueError('Scene start out of range')
    x,y,w,h=roi
    if not (0 <= x and 0 <= y and w>0 and h>0 and x+w<=1080 and y+h<=1920):
        raise ValueError('ROI out of portrait canvas')
    if y < 1560 or y+h > 1640:
        raise ValueError('Rail must remain in caption-card safe strip')
    if len(GENRE_COLORS) != 10:
        raise ValueError('Exactly ten genres required')
    return True

def scene_for_frame(frame, starts=SCENE_STARTS, total=TOTAL_FRAMES):
    if not 0 <= frame < total:
        raise ValueError('Frame out of range')
    idx=int(np.searchsorted(starts,frame,side='right')-1)
    end=starts[idx+1] if idx+1<len(starts) else total
    progress=(frame-starts[idx])/max(1,end-starts[idx]-1)
    return idx, min(1.,max(0.,progress))

def draw_rail(progress, rgb, roi=ROI):
    if not 0 <= progress <= 1: raise ValueError('Progress out of range')
    w,h=roi[2:]
    canvas=np.zeros((h,w,4),dtype=np.uint8)
    margin=5
    y0=7
    canvas[y0:y0+3,margin:w-margin,:3]=(54,90,107)
    canvas[y0:y0+3,margin:w-margin,3]=110
    fill=int(round((w-2*margin)*progress))
    if fill:
        canvas[y0:y0+3,margin:margin+fill,:3]=rgb
        canvas[y0:y0+3,margin:margin+fill,3]=205
        head=margin+fill-1
        for dx,alpha in ((-4,32),(-2,65),(0,105),(2,45)):
            x=head+dx
            if 0<=x<w:
                canvas[4:7,x,:3]=rgb
                canvas[4:7,x,3]=alpha
    return Image.fromarray(canvas,'RGBA')

def write_overlays(folder, genre='ai-work', starts=SCENE_STARTS,total=TOTAL_FRAMES):
    validate(starts,total)
    if genre not in GENRE_COLORS: raise ValueError('Unsupported genre')
    folder=Path(folder);folder.mkdir(parents=True,exist_ok=True)
    for n in range(total):
        _,p=scene_for_frame(n,starts,total)
        draw_rail(p,GENRE_COLORS[genre]).save(folder/f'rail_{n:05d}.png',compress_level=1)
    return total

def probe(source):
    r=subprocess.run(['ffprobe','-v','error','-show_streams','-of','json',str(source)],check=True,capture_output=True,text=True)
    streams=json.loads(r.stdout)['streams']
    v=next(s for s in streams if s['codec_type']=='video')
    a=next((s for s in streams if s['codec_type']=='audio'),None)
    if (v['width'],v['height'])!=(1080,1920) or v.get('avg_frame_rate')!='30/1':
        raise ValueError('Expected 1080x1920/30fps source')
    if a is None or a.get('codec_name')!='aac':
        raise ValueError('Expected AAC narration')
    return {'video':v,'audio':a}

def render(source, output, workdir, genre='ai-work',starts=SCENE_STARTS,total=TOTAL_FRAMES,preset='veryfast'):
    probe(source)
    source,output,workdir=Path(source),Path(output),Path(workdir)
    write_overlays(workdir/'rails',genre,starts,total)
    output.parent.mkdir(parents=True,exist_ok=True)
    x,y,_,_=ROI
    cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(source),
         '-framerate',str(FPS),'-i',str(workdir/'rails'/'rail_%05d.png'),
         '-filter_complex',f'[0:v][1:v]overlay={x}:{y}:shortest=1:format=auto,format=yuv420p[v]',
         '-map','[v]','-map','0:a:0','-map_metadata','0',
         '-c:v','libx264','-crf','18','-preset',preset,'-pix_fmt','yuv420p',
         '-c:a','copy','-frames:v',str(total),'-t',str(total/FPS),
         '-movflags','+faststart',str(output)]
    subprocess.run(cmd,check=True)
    return {'genre':genre,'scene_starts':list(starts),'total_frames':total,
            'roi':list(ROI),'ten_genre_presets':True,
            'audio_stream_copy':True,'word_level_asr_verified':False}

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--input',required=True)
    p.add_argument('--output',required=True)
    p.add_argument('--workdir',required=True)
    p.add_argument('--genre',default='ai-work',choices=tuple(GENRE_COLORS))
    p.add_argument('--preset',default='veryfast')
    a=p.parse_args()
    print(json.dumps(render(a.input,a.output,a.workdir,a.genre,preset=a.preset),ensure_ascii=False))
if __name__=='__main__': main()
