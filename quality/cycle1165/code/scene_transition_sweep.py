"""Copyright-safe, zero-cost chapter-divider light sweep for portrait slide videos.

The transparent overlay affects only the horizontal divider immediately under
scene titles, never the Japanese captions, diagrams, faces, or narration.
Source media is not bundled with the source code or uploaded to GitHub.
"""
from __future__ import annotations
import argparse
import json
import math
import os
import subprocess
from pathlib import Path

import numpy as np
from PIL import Image

FPS = 30
CUTS = (42, 94, 168, 250, 330, 412, 499)
TOTAL_FRAMES = 675
ROI = (70, 354, 820, 28)  # x,y,w,h; title divider, outside captions
SWEEP_FRAMES = 13
GENRES = {
    'ai-work': (73, 228, 211), 'finance': (243, 205, 125),
    'career': (129, 231, 162), 'health': (105, 226, 200),
    'learning': (121, 192, 252), 'travel': (252, 171, 123),
    'technology': (126, 173, 254), 'business': (95, 225, 203),
    'life': (242, 156, 197), 'history': (237, 198, 133),
}

def validate_timing(cuts=CUTS, total_frames=TOTAL_FRAMES, fps=FPS):
    assert fps > 0 and total_frames > 0
    assert all(isinstance(c, int) for c in cuts)
    assert all(0 < c and c + SWEEP_FRAMES <= total_frames for c in cuts)
    assert list(cuts) == sorted(set(cuts))
    assert all(b - a >= SWEEP_FRAMES for a, b in zip(cuts, cuts[1:]))
    x, y, w, h = ROI
    assert x >= 0 and y >= 0 and x+w <= 1080 and y+h < 500
    assert len(GENRES) == 10
    return True

def make_frame(progress: float, rgb: tuple[int,int,int]) -> Image.Image:
    """RGBA streak: glow + white-hot core, confined to a 28px header strip."""
    assert 0 <= progress <= 1
    w, h = ROI[2:]
    head = -110 + (w+220)*progress
    x = np.arange(w, dtype=np.float32)
    y = np.arange(h, dtype=np.float32)
    trail = np.exp(-np.maximum(0, head-x)/125.0) * (x <= head)
    core = np.exp(-0.5*((x-head)/13.0)**2)
    glow = np.exp(-0.5*((x-head)/58.0)**2)
    vertical = np.exp(-0.5*((y-(h-1)/2)/5.5)**2)
    alpha = np.minimum(215, (trail*72 + glow*80 + core*102)[None,:]*vertical[:,None])
    envelope = min(1., progress/.18, (1.-progress)/.20)
    alpha *= max(0., envelope)
    rgba = np.zeros((h,w,4), dtype=np.uint8)
    for ch in range(3):
        rgba[:,:,ch] = np.clip(rgb[ch] + (255-rgb[ch])*core[None,:]*.6,0,255).astype('uint8')
    rgba[:,:,3] = np.clip(alpha,0,255).astype('uint8')
    return Image.fromarray(rgba,'RGBA')

def generate_overlay_sequence(folder: Path, cuts=CUTS, total_frames=TOTAL_FRAMES, genre='ai-work'):
    validate_timing(cuts,total_frames)
    if genre not in GENRES: raise ValueError('Unsupported genre')
    folder=Path(folder);folder.mkdir(parents=True,exist_ok=True)
    empty=folder/'empty.png'
    Image.new('RGBA', ROI[2:], (0,0,0,0)).save(empty)
    for n in range(total_frames):
        os.link(empty,folder/f'overlay_{n:05d}.png')
    modified=[]
    for cut in cuts:
        for k in range(SWEEP_FRAMES):
            n=cut+k
            p=k/(SWEEP_FRAMES-1)
            path=folder/f'overlay_{n:05d}.png'
            path.unlink()
            make_frame(p,GENRES[genre]).save(path)
            modified.append(n)
    return modified

def probe(source):
    r=subprocess.run(['ffprobe','-v','error','-show_streams','-of','json',str(source)],check=True,capture_output=True,text=True)
    streams=json.loads(r.stdout)['streams']
    video=next(s for s in streams if s['codec_type']=='video')
    audios=[s for s in streams if s['codec_type']=='audio']
    if (video['width'],video['height']) != (1080,1920): raise ValueError('Expected 1080x1920 input')
    if video.get('avg_frame_rate') != '30/1': raise ValueError('Expected 30fps input')
    if not audios or audios[0].get('codec_name')!='aac': raise ValueError('Expected AAC Japanese narration')
    return {'video':video,'audio':audios[0]}

def render(source,output,workdir,genre='ai-work',cuts=CUTS,total_frames=TOTAL_FRAMES,preset='veryfast'):
    source=Path(source);output=Path(output);workdir=Path(workdir)
    probe(source)
    modified=generate_overlay_sequence(workdir/'overlays',cuts,total_frames,genre)
    output.parent.mkdir(parents=True,exist_ok=True)
    x,y,_,_=ROI
    cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(source),
         '-framerate',str(FPS),'-i',str(workdir/'overlays'/'overlay_%05d.png'),
         '-filter_complex',f'[0:v][1:v]overlay={x}:{y}:shortest=1:format=auto,format=yuv420p[v]',
         '-map','[v]','-map','0:a:0','-map_metadata','0',
         '-c:v','libx264','-crf','18','-preset',preset,'-pix_fmt','yuv420p',
         '-c:a','copy','-frames:v',str(total_frames),'-t',str(total_frames/FPS),
         '-movflags','+faststart',str(output)]
    subprocess.run(cmd,check=True)
    return {'genre':genre,'cuts':list(cuts),'modified_frames':len(modified),
            'affected_region':list(ROI),'audio_stream_copy':True,
            'ten_genre_presets':len(GENRES),'independent_japanese_asr':False,
            'publication_approved':False}

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--source',required=True)
    p.add_argument('--output',required=True)
    p.add_argument('--workdir',required=True)
    p.add_argument('--genre',default='ai-work',choices=list(GENRES))
    p.add_argument('--preset',default='veryfast')
    a=p.parse_args()
    print(json.dumps(render(a.source,a.output,a.workdir,a.genre,preset=a.preset),ensure_ascii=False))
