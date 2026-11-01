#!/usr/bin/env python3
"""Cycle1199: offline, narration-safe subtle parallax on the central visual panel.

Only the visual-content ROI is transformed. Header, Japanese burned-in subtitles,
voice meter and compliance footer are preserved. Uses FFmpeg, Pillow and numpy.
No posting, cloud service or network calls.
"""
from __future__ import annotations
import argparse, json, subprocess, tempfile
from pathlib import Path
import numpy as np
from PIL import Image

FPS = 30
GENRE_CONFIG = {
    'ai': {'accent':'#4DE3D2'}, 'business':{'accent':'#8EC5FF'},
    'money':{'accent':'#63E5B8'}, 'learning':{'accent':'#A7C4FF'},
    'health':{'accent':'#74E4C4'}, 'food':{'accent':'#A9E69B'},
    'travel':{'accent':'#78D6F0'}, 'beauty':{'accent':'#D5B6F7'},
    'career':{'accent':'#82C4F8'}, 'life':{'accent':'#98E0C5'},
}
DEFAULT_ROI=(60,430,820,735)

def probe(path):
    result=subprocess.run(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(path)],
                          check=True,capture_output=True,text=True)
    return json.loads(result.stdout)

def check_video(meta):
    video=next(s for s in meta['streams'] if s['codec_type']=='video')
    audio=next(s for s in meta['streams'] if s['codec_type']=='audio')
    if (int(video['width']),int(video['height'])) != (1080,1920):
        raise ValueError('Input must be 1080x1920; no implicit resizing')
    if video['r_frame_rate']!='30/1':
        raise ValueError('Input must be exactly 30fps')
    if audio['codec_name']!='aac':
        raise ValueError('Input must have AAC audio for bitstream-copy preservation')
    frames=int(video.get('nb_frames') or round(float(meta['format']['duration'])*FPS))
    return frames

def validate_roi(roi, feather=36):
    x,y,w,h=roi
    if not (0<=x<1080 and 0<=y<1920 and w>=200 and h>=200 and x+w<=1080 and y+h<=1920):
        raise ValueError('ROI outside portrait frame')
    if not (0<feather<min(w,h)//4):
        raise ValueError('Invalid feather')
    if y<400 or y+h>1180 or x+w>930:
        raise ValueError('ROI overlaps header, narration/subtitles, footer or UI edge')

def make_mask(path, roi=DEFAULT_ROI, feather=36):
    validate_roi(roi,feather)
    _,_,w,h=roi
    xx=np.arange(w,dtype=np.float32)
    yy=np.arange(h,dtype=np.float32)
    dx=np.minimum(xx,w-1-xx)
    dy=np.minimum(yy,h-1-yy)
    edge=np.minimum(dy[:,None],dx[None,:])
    t=np.clip(edge/feather,0,1)
    alpha=np.rint(255*t*t*(3-2*t)).astype(np.uint8)
    Image.fromarray(alpha,'L').save(path)
    return alpha

def filter_graph(roi,frames,max_zoom=1.018):
    validate_roi(roi)
    if not (1.0<=max_zoom<=1.025):
        raise ValueError('Zoom must be within [1.0,1.025] for text legibility')
    x,y,w,h=roi
    den=max(1,frames-1)
    z=f'1+{max_zoom-1:.6f}*on/{den}'
    xp=f'(iw-iw/zoom)/2+min(2,(iw-iw/zoom)/4)*sin(on*PI/{den})'
    yp='(ih-ih/zoom)/2'
    return (f'[0:v]split=2[base][src];'
            f'[src]crop={w}:{h}:{x}:{y},'
            f"zoompan=z='{z}':x='{xp}':y='{yp}':d=1:s={w}x{h}:fps={FPS},"
            f'format=rgb24[push];'
            f'[1:v]format=gray[alpha];'
            f'[push][alpha]alphamerge[layer];'
            f'[base][layer]overlay={x}:{y}:shortest=1:format=auto[v]')

def render(src,dst,genre='ai',roi=DEFAULT_ROI,max_zoom=1.018,crf=17,limit=None):
    if genre not in GENRE_CONFIG: raise ValueError(f'Unknown genre: {genre}')
    frames=check_video(probe(src))
    if limit is not None:
        frames=min(frames,round(limit*FPS))
    dst=Path(dst);dst.parent.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory() as td:
        mask=Path(td)/'alpha.png'; make_mask(mask,roi)
        graph=filter_graph(roi,frames,max_zoom)
        cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(src),
             '-loop','1','-framerate',str(FPS),'-i',str(mask),
             '-filter_complex',graph,'-map','[v]','-map','0:a:0',
             '-c:v','libx264','-preset','veryfast','-crf',str(crf),
             '-pix_fmt','yuv420p','-r',str(FPS),'-fps_mode','cfr',
             '-c:a','copy','-frames:v',str(frames),'-movflags','+faststart',
             '-metadata:s:a:0','language=jpn',str(dst)]
        proc=subprocess.run(cmd,capture_output=True,text=True)
        if proc.returncode:
            raise RuntimeError('ffmpeg failed: '+proc.stderr[-2500:])
    return {'frames_expected':frames,'output':str(dst),'genre':genre,'roi':list(roi),'max_zoom':max_zoom}

def main():
    p=argparse.ArgumentParser()
    p.add_argument('source');p.add_argument('output')
    p.add_argument('--genre',choices=list(GENRE_CONFIG),default='ai')
    p.add_argument('--max-zoom',type=float,default=1.018)
    p.add_argument('--limit',type=float,default=None)
    a=p.parse_args()
    print(json.dumps(render(a.source,a.output,a.genre,max_zoom=a.max_zoom,limit=a.limit),ensure_ascii=False))

if __name__=='__main__': main()
