#!/usr/bin/env python3
"""Deterministic 8-band audio spectrum meter for 1080x1920 image-first shorts.

Uses actual FFT frequency-band energies instead of synthetic sine bar variation.
Changes only x570..715/y75..115; audio copied, no ASR or release approval.
"""
from __future__ import annotations
import argparse
from pathlib import Path
import subprocess
import tempfile
import math
import numpy as np
from PIL import Image, ImageDraw

FPS = 30
METER = (570, 75, 145, 40)
BANDS_HZ = ((100,180),(180,310),(310,520),(520,850),(850,1350),(1350,2100),(2100,3200),(3200,5400))
COLORS = {
    'ai_work': (38,232,220), 'business': (54,202,238),
    'finance': (76,220,170), 'education': (89,187,255),
    'health': (83,221,183), 'travel': (252,187,101),
    'cooking': (255,169,116), 'lifestyle': (230,165,240),
    'technology': (83,225,245), 'entertainment': (255,160,193),
}

def decode_pcm(path: Path, rate: int = 16000) -> np.ndarray:
    if rate < 12000: raise ValueError('sample rate too low')
    p = subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-i',str(path),'-vn',
        '-ac','1','-ar',str(rate),'-f','f32le','-acodec','pcm_f32le','-'],
        capture_output=True,check=True)
    samples = np.frombuffer(p.stdout,dtype='<f4')
    if samples.size < rate//5: raise ValueError('audio missing/too short')
    return samples

def spectral_envelopes(samples: np.ndarray, fps: int=FPS, rate: int=16000) -> np.ndarray:
    """8 log bands, Hann FFT, percentile normalization and gated smoothing."""
    if fps <= 0 or samples.size < rate//5: raise ValueError('bad signal')
    n = int(math.ceil(len(samples)*fps/rate))
    win_size=2048
    hann=np.hanning(win_size).astype(np.float32)
    freqs=np.fft.rfftfreq(win_size,1/rate)
    masks=[(freqs>=lo)&(freqs<hi) for lo,hi in BANDS_HZ]
    powers=np.zeros((n,8),dtype=np.float32)
    for i in range(n):
        mid=int((i+.5)*rate/fps)
        start=mid-win_size//2
        chunk=np.zeros(win_size,dtype=np.float32)
        left=max(0,start); right=min(len(samples),start+win_size)
        if right>left: chunk[left-start:right-start]=samples[left:right]
        spectrum=np.abs(np.fft.rfft(chunk*hann))
        for j,mask in enumerate(masks):
            powers[i,j]=np.sqrt(np.mean(spectrum[mask]**2)) if mask.any() else 0.
    ref=np.maximum(np.percentile(powers,95,axis=0),0.025)
    targets=np.clip(powers/ref,0,1)
    targets=np.where(targets>=.07,(targets-.07)/.93,0)
    levels=np.zeros_like(targets)
    prev=np.zeros(8,dtype=np.float32)
    for i in range(n):
        alpha=np.where(targets[i]>prev,.32,.13)
        step=np.clip(alpha*(targets[i]-prev),-.095,.17)
        prev=np.clip(prev+step,0,1)
        levels[i]=prev
    return levels

def meter_frame(levels: np.ndarray, rgb=(38,232,220)) -> Image.Image:
    levels=np.asarray(levels,dtype=float)
    if levels.shape!=(8,) or not np.all(np.isfinite(levels)) or np.any(levels<0) or np.any(levels>1):
        raise ValueError('expected 8 normalized bands')
    w,h=METER[2:]
    im=Image.new('RGBA',(w,h),(0,0,0,0)); d=ImageDraw.Draw(im)
    d.rounded_rectangle((0,0,w-1,h-1),radius=7,fill=(3,10,28,246))
    d.line((7,h-6,w-8,h-6),fill=(*rgb,32),width=1)
    for k,level in enumerate(levels):
        height=3+int(round(26*level))
        x=10+k*17; y=h-8-height
        d.rounded_rectangle((x,y,x+7,h-8),radius=3,fill=(*rgb,235))
        if height>=12: d.line((x+2,y+2,x+5,y+2),fill=(232,255,255,200),width=1)
    return im

def video_frames(src: Path) -> int:
    p=subprocess.run(['ffprobe','-v','error','-select_streams','v:0','-show_entries',
        'stream=nb_frames','-of','default=noprint_wrappers=1:nokey=1',str(src)],
        capture_output=True,text=True,check=True)
    return int(p.stdout.strip())

def render(src: Path, dst: Path, genre: str='ai_work', seconds:float|None=None) -> dict:
    if genre not in COLORS: raise ValueError('unknown genre')
    if not src.is_file(): raise FileNotFoundError(src)
    levels=spectral_envelopes(decode_pcm(src))
    frames=video_frames(src)
    if len(levels)<frames:
        levels=np.concatenate([levels,np.repeat(levels[-1:,:],frames-len(levels),axis=0)])
    levels=levels[:frames]
    dst.parent.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='spectral_meter_') as temp:
        folder=Path(temp)
        for i,level in enumerate(levels):
            meter_frame(level,COLORS[genre]).save(folder/f'{i:04d}.png')
        cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(src),
             '-framerate',str(FPS),'-start_number','0','-i',str(folder/'%04d.png'),
             '-filter_complex',f'[0:v][1:v]overlay={METER[0]}:{METER[1]}:shortest=1:format=auto,format=yuv420p[v]',
             '-map','[v]','-map','0:a:0','-c:v','libx264','-preset','veryfast','-crf','19',
             '-pix_fmt','yuv420p','-c:a','copy','-movflags','+faststart']
        if seconds is not None: cmd+=['-t',str(seconds)]
        cmd+=[str(dst)]
        subprocess.run(cmd,check=True)
    return {'frames':len(levels),'genre':genre,'bands_hz':BANDS_HZ,
            'band_mean':[round(float(x),3) for x in levels.mean(axis=0)],
            'meter_roi':METER}

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--input',required=True,type=Path)
    p.add_argument('--output',required=True,type=Path)
    p.add_argument('--genre',default='ai_work',choices=COLORS)
    p.add_argument('--seconds',type=float)
    a=p.parse_args()
    print(render(a.input,a.output,a.genre,a.seconds))
if __name__=='__main__':main()
