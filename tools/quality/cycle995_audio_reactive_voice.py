#!/usr/bin/env python3
"""Audio-energy-reactive VOICE meter for portrait image-slide shorts.

Changes only a small, pre-reviewed top UI rectangle. Audio stream is copied
without modification; baked subtitles and central images are left untouched.
No ASR, speech recognition, copyright verification or publication approval.
"""
from __future__ import annotations
import argparse
from array import array
from pathlib import Path
import math
import subprocess
import tempfile
from PIL import Image, ImageDraw

FPS = 30
METER = (570, 75, 145, 40)
COLORS = {
    'ai_work': (38, 232, 220), 'business': (54, 202, 238),
    'finance': (76, 220, 170), 'education': (89, 187, 255),
    'health': (83, 221, 183), 'travel': (252, 187, 101),
    'cooking': (255, 169, 116), 'lifestyle': (230, 165, 240),
    'technology': (83, 225, 245), 'entertainment': (255, 160, 193),
}

def decode_energy(path: Path, fps: int = FPS, rate: int = 8000) -> list[float]:
    if fps <= 0 or rate < fps * 20:
        raise ValueError('invalid fps/rate')
    proc = subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-i',str(path),
        '-vn','-ac','1','-ar',str(rate),'-f','s16le','-acodec','pcm_s16le','-'],
        check=True,capture_output=True)
    samples = array('h'); samples.frombytes(proc.stdout)
    if not samples:
        raise ValueError('audio missing')
    n = math.ceil(len(samples)*fps/rate)
    out = []
    for i in range(n):
        a = round(i*rate/fps); b = min(len(samples),round((i+1)*rate/fps))
        segment = samples[a:b]
        rms = math.sqrt(sum(float(x)*x for x in segment)/max(1,len(segment)))/32768
        out.append(rms)
    return out

def smooth_levels(energies: list[float]) -> list[float]:
    if not energies:
        raise ValueError('no energy frames')
    p90 = sorted(energies)[min(len(energies)-1,int(.90*(len(energies)-1)))]
    scale = max(.055, p90)
    out=[]; state=0.
    for e in energies:
        target = min(1., max(0., e/scale)) if e >= .005 else 0.
        alpha = .48 if target > state else .19
        state += alpha*(target-state)
        out.append(state)
    return out

def meter_frame(level: float, index: int, rgb=(38,232,220)) -> Image.Image:
    if not 0 <= level <= 1 or index < 0:
        raise ValueError('bad meter level/index')
    w,h=METER[2:]
    im=Image.new('RGBA',(w,h),(0,0,0,0)); d=ImageDraw.Draw(im)
    d.rounded_rectangle((0,0,w-1,h-1),radius=7,fill=(3,10,28,246))
    d.line((7,h-6,w-8,h-6),fill=(*rgb,32),width=1)
    for k in range(8):
        variation=.75+.25*math.sin(index*.17+k*.87)**2
        height=3+int(26*level*variation)
        x=10+k*17
        y=h-8-height
        d.rounded_rectangle((x,y,x+7,h-8),radius=3,fill=(*rgb,235))
        if height>=12:
            d.line((x+2,y+2,x+5,y+2),fill=(232,255,255,200),width=1)
    return im

def render(src: Path, dst: Path, *, genre='ai_work', seconds: float | None=None) -> dict:
    if genre not in COLORS: raise ValueError('unknown genre')
    if not src.is_file(): raise FileNotFoundError(src)
    energies=decode_energy(src)
    levels=smooth_levels(energies)
    # AAC can end before the final video frame; pad to preserve full picture.
    probe=subprocess.run(['ffprobe','-v','error','-select_streams','v:0',
        '-show_entries','stream=nb_frames','-of','default=noprint_wrappers=1:nokey=1',
        str(src)],capture_output=True,text=True,check=True)
    n_video=int(probe.stdout.strip())
    if n_video > len(levels): levels.extend([levels[-1]]*(n_video-len(levels)))
    else: levels=levels[:n_video]
    dst.parent.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='voice_meter_') as tmp:
        folder=Path(tmp)
        for i,level in enumerate(levels):
            meter_frame(level,i,COLORS[genre]).save(folder/f'{i:04d}.png')
        cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(src),
             '-framerate',str(FPS),'-start_number','0','-i',str(folder/'%04d.png'),
             '-filter_complex',f'[0:v][1:v]overlay={METER[0]}:{METER[1]}:shortest=1:format=auto,format=yuv420p[v]',
             '-map','[v]','-map','0:a:0','-c:v','libx264','-preset','veryfast','-crf','19',
             '-pix_fmt','yuv420p','-c:a','copy','-movflags','+faststart']
        if seconds is not None: cmd+=['-t',str(seconds)]
        cmd += [str(dst)]
        subprocess.run(cmd,check=True)
    return {'frames_meter':len(levels),'level_min':round(min(levels),4),
            'level_max':round(max(levels),4),'genre':genre,'meter_roi':METER}

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--input',required=True,type=Path)
    p.add_argument('--output',required=True,type=Path)
    p.add_argument('--genre',default='ai_work',choices=COLORS)
    p.add_argument('--seconds',type=float)
    args=p.parse_args()
    print(render(args.input,args.output,genre=args.genre,seconds=args.seconds))
if __name__=='__main__': main()
