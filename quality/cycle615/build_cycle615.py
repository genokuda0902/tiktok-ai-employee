#!/usr/bin/env python3
"""Cycle615: 0-yen synthetic transition SFX. No downloaded music or paid APIs.
Source media rights remain unverified. Human approval required; no posting.
"""
from __future__ import annotations
import argparse, hashlib, json, math, subprocess, tempfile
from pathlib import Path
import numpy as np
import soundfile as sf

ROOT=Path(__file__).resolve().parent
BASE=ROOT/'assets/cycle614_baseline.mp4'
OUT=ROOT/'output/cycle615_SCENE_EARCONS_HUMAN_REVIEW.mp4'
GENRES=ROOT/'assets/genres.json'
SR=48000
FPS=30
CUT_FRAMES=(70,178,219,246,352,415)
EARCON_SECONDS=.185
PEAK_DBFS=-34.0

def sha256(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for block in iter(lambda:f.read(1<<20),b''):h.update(block)
    return h.hexdigest()

def genre_settings(genre):
    genres=json.loads(GENRES.read_text(encoding='utf-8'))['genres']
    if len(genres)!=10 or genre not in genres:
        raise ValueError('Exactly ten configured genres required')
    return {'genre':genre,'pitch_hz':600+list(genres).index(genre)*24,
            'peak_dbfs':PEAK_DBFS,'genre_count':10}

def earcon(sr=SR,pitch_hz=600,peak_dbfs=PEAK_DBFS):
    if sr<8000 or not 250<=pitch_hz<=1600 or not -50<=peak_dbfs<=-25:
        raise ValueError('Unsafe earcon configuration')
    n=round(sr*EARCON_SECONDS)
    t=np.arange(n,dtype=np.float64)/sr
    rng=np.random.default_rng(615)
    noise=rng.standard_normal(n)
    high=noise-np.convolve(noise,np.ones(65)/65,mode='same')
    high/=max(np.max(np.abs(high)),1e-8)
    freq=pitch_hz*(1.18-.36*(t/EARCON_SECONDS))
    phase=2*np.pi*np.cumsum(freq)/sr
    tonal=np.sin(phase)+.22*np.sin(2*phase)
    env=np.sin(np.pi*np.linspace(0,1,n))**2
    wave=(.76*tonal+.24*high)*env
    wave-=np.mean(wave)
    wave*=10**(peak_dbfs/20)/max(np.max(np.abs(wave)),1e-9)
    return wave.astype(np.float32)

def mix_earcons(audio,genre='雑学・科学',sr=SR):
    if audio.ndim!=2 or audio.shape[1]!=2:raise ValueError('Stereo required')
    if sr!=SR:raise ValueError('48kHz required')
    cfg=genre_settings(genre)
    accent=earcon(sr,cfg['pitch_hz'],cfg['peak_dbfs'])
    out=audio.astype(np.float64).copy()
    events=[]
    for frame in CUT_FRAMES:
        start=round(frame*sr/FPS)
        if start+len(accent)>len(out):raise ValueError('Audio too short')
        local=audio[max(0,start-round(.08*sr)):min(len(audio),start+round(.08*sr))]
        rms=float(np.sqrt(np.mean(local.astype(np.float64)**2)))
        gain=.50 if rms>10**(-26/20) else .78
        effect=accent*gain
        out[start:start+len(effect),:]+=effect[:,None]
        events.append({'frame':frame,'seconds':round(frame/FPS,3),'gain':gain})
    peak=float(np.max(np.abs(out)))
    if peak>.94:out*=.94/peak
    return out.astype(np.float32),events

def render(source=BASE,output=OUT,genre='雑学・科学'):
    source=Path(source);output=Path(output)
    if not source.is_file():raise FileNotFoundError(source)
    output.parent.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='cycle615_') as tmp:
        raw=Path(tmp)/'input.wav'
        mixed=Path(tmp)/'mixed.wav'
        subprocess.run(['ffmpeg','-v','error','-y','-i',str(source),'-vn',
                        '-ac','2','-ar','48000','-c:a','pcm_f32le',str(raw)],
                       check=True,timeout=180)
        audio,sr=sf.read(raw,dtype='float32',always_2d=True)
        processed,events=mix_earcons(audio,genre,sr)
        sf.write(mixed,processed,sr,subtype='FLOAT')
        subprocess.run(['ffmpeg','-v','error','-y','-i',str(source),
                        '-i',str(mixed),'-map','0:v:0','-map','1:a:0',
                        '-c:v','copy','-c:a','aac','-b:a','192k',
                        '-ar','48000','-ac','2','-t','15.616',
                        '-movflags','+faststart',str(output)],check=True,timeout=180)
    return {'mp4_sha256':sha256(output),'genre':genre,'events':events,
            'quality':'HUMAN_REVIEW','publication':'NOT_APPROVED'}

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--input',type=Path,default=BASE)
    p.add_argument('--output',type=Path,default=OUT)
    p.add_argument('--genre',default='雑学・科学')
    a=p.parse_args()
    print(json.dumps(render(a.input,a.output,a.genre),ensure_ascii=False))
