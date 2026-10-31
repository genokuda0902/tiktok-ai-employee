#!/usr/bin/env python3
"""Original deterministic transition SFX. Review only; no external audio samples."""
import argparse, hashlib, json, subprocess
from pathlib import Path
import numpy as np

GENRE_INTENSITY={
'ai_work':1.0,'business':0.85,'money':0.82,'learning':0.82,
'health':0.70,'lifestyle':0.85,'psychology':0.75,'science':1.0,
'history':0.70,'travel':0.92}
BOUNDARIES=(2.900,5.800,8.520,11.400,14.280,17.340,20.300)
SAMPLE_RATE=48000
SFX_LENGTH=0.24
SFX_PEAK_CEILING=0.065

def sfx_wave(sample_rate=SAMPLE_RATE,seed=0,intensity=1.0):
    if sample_rate<8000 or not 0<intensity<=1.2:raise ValueError('unsupported intensity/rate')
    n=round(SFX_LENGTH*sample_rate)
    t=np.arange(n,dtype=np.float64)/sample_rate
    window=np.sin(np.pi*np.arange(n)/(n-1))**2
    noise=np.random.default_rng(20261031+seed).standard_normal(n)
    noise=np.convolve(noise,np.ones(12)/12,mode='same')
    chirp=np.sin(2*np.pi*(460*t+0.5*1000/SFX_LENGTH*t*t))
    ping=np.sin(2*np.pi*1080*t)*np.exp(-28*t)
    mono=(0.065*noise+0.032*chirp+0.025*ping)*window*intensity
    peak=np.max(np.abs(mono))
    if peak>SFX_PEAK_CEILING:mono*=SFX_PEAK_CEILING/peak
    pan=-0.12 if seed%2 else 0.12
    return np.stack((mono*(1-pan),mono*(1+pan)),axis=1).astype(np.float32)

def make_overlay(n_samples,boundaries=BOUNDARIES,genre='ai_work',sample_rate=SAMPLE_RATE):
    if genre not in GENRE_INTENSITY:raise ValueError('unknown genre; fail closed')
    if any(b<=0 or b>=n_samples/sample_rate for b in boundaries) or any(a>=b for a,b in zip(boundaries,boundaries[1:])):
        raise ValueError('boundaries must be increasing and inside audio')
    overlay=np.zeros((n_samples,2),dtype=np.float32)
    events=[]
    for i,b in enumerate(boundaries):
        # 20.3s had no adjacent acoustic pause in prior audit; duck this cue.
        intensity=GENRE_INTENSITY[genre]*(0.32 if abs(b-20.3)<0.001 else 1.0)
        cue=sfx_wave(sample_rate,i,intensity)
        start=round((b-0.12)*sample_rate)
        end=min(start+len(cue),n_samples)
        overlay[start:end]+=cue[:end-start]
        events.append({'boundary_s':b,'start_s':start/sample_rate,'end_s':end/sample_rate,'intensity':round(intensity,3)})
    return overlay,events

def run(cmd,input_bytes=None):
    p=subprocess.run(cmd,input=input_bytes,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    if p.returncode:raise RuntimeError(' '.join(cmd)+'\n'+p.stderr.decode(errors='replace')[-2000:])
    return p.stdout

def mix_file(source,output,genre='ai_work',report=None,boundaries=BOUNDARIES):
    source,output=Path(source),Path(output)
    if not source.is_file():raise FileNotFoundError(source)
    output.parent.mkdir(parents=True,exist_ok=True)
    decoded=run(['ffmpeg','-v','error','-i',str(source),'-map','0:a:0',
                 '-f','f32le','-acodec','pcm_f32le','-ac','2','-ar',str(SAMPLE_RATE),'-'])
    audio=np.frombuffer(decoded,dtype='<f4').reshape(-1,2).copy()
    overlay,events=make_overlay(len(audio),boundaries,genre)
    combined=audio+overlay
    peak=float(np.max(np.abs(combined)))
    if peak>=0.985:raise ValueError('clipping risk; no automatic speech gain change')
    raw=output.parent/'mix_temp.f32le'
    raw.write_bytes(combined.astype('<f4').tobytes())
    try:
        run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(source),
             '-f','f32le','-ar',str(SAMPLE_RATE),'-ac','2','-i',str(raw),
             '-map','0:v:0','-map','1:a:0','-c:v','copy','-c:a','aac',
             '-b:a','192k','-ar',str(SAMPLE_RATE),'-movflags','+faststart',str(output)])
    finally:raw.unlink(missing_ok=True)
    touched=np.any(overlay!=0,axis=1)
    unchanged=float(np.max(np.abs(combined[~touched]-audio[~touched]))) if np.any(~touched) else None
    data={'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
          'output_sha256':hashlib.sha256(output.read_bytes()).hexdigest(),
          'genre':genre,'events':events,'mixed_pcm_peak':peak,
          'pre_aac_narration_correlation':float(np.corrcoef(audio.ravel(),combined.ravel())[0,1]),
          'outside_sfx_pcm_max_delta':unchanged,
          'sfx_origin':'original seeded mathematical synthesis, no samples',
          'video':'stream copy; verify with independent hash',
          'japanese_asr':'NOT_VERIFIED','semantic_caption_sync':'NOT_VERIFIED',
          'status':'HUMAN_REVIEW / PUBLICATION_NOT_APPROVED'}
    if report:Path(report).write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
    return data

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('source');p.add_argument('output')
    p.add_argument('--genre',default='ai_work',choices=list(GENRE_INTENSITY))
    p.add_argument('--report')
    p.add_argument('--boundaries',help='comma-separated seconds for custom/synthetic scenes')
    p.add_argument('--publish',action='store_true')
    a=p.parse_args()
    if a.publish:p.error('publication disabled until employee, rights, and quality approval')
    bounds=tuple(float(x) for x in a.boundaries.split(',')) if a.boundaries else BOUNDARIES
    print(json.dumps(mix_file(a.source,a.output,a.genre,a.report,bounds),ensure_ascii=False,indent=2))
