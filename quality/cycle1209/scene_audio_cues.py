#!/usr/bin/env python3
"""Zero-cost original scene-change earcons for Japanese narration-first slides.

The H.264 picture stream is copied unchanged; only the AAC sound is remastered.
Review-only. Never posts, merges, purchases, or uses external media.
"""
from __future__ import annotations
import argparse, hashlib, json, subprocess
from pathlib import Path
import numpy as np
from scipy.io import wavfile

FPS=30
SR=48000
SCENE_STARTS=(42,96,171,252,333,414,501,579)
GENRE_TONES={
    'ai':660,'business':590,'money':620,'learning':710,'health':540,
    'food':740,'travel':690,'beauty':780,'career':630,'life':570,
}

def cmd(args,binary=False):
    p=subprocess.run(args,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    if p.returncode:
        raise RuntimeError(p.stderr[-1500:].decode(errors='replace'))
    return p.stdout if binary else p.stdout.decode()

def probe(path):
    return json.loads(cmd(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(path)]))

def source_metadata(src):
    info=probe(src)
    v=next((s for s in info['streams'] if s['codec_type']=='video'),None)
    a=next((s for s in info['streams'] if s['codec_type']=='audio'),None)
    if not v or not a or v.get('codec_name')!='h264' or a.get('codec_name')!='aac':
        raise ValueError('H264/AAC source required')
    if (int(v['width']),int(v['height']),v['r_frame_rate'])!=(1080,1920,'30/1'):
        raise ValueError('1080x1920 30fps required')
    if int(a['sample_rate'])!=SR:raise ValueError('48kHz required')
    return int(v['nb_frames']),info

def decode_audio(src):
    raw=cmd(['ffmpeg','-v','error','-i',str(src),'-map','0:a:0','-vn',
             '-ac','1','-ar',str(SR),'-f','f32le','-'],binary=True)
    return np.frombuffer(raw,dtype='<f4').copy()

def validate_starts(starts,frames):
    if not 2<=len(starts)<=16 or starts[0]<0 or starts[-1]>=frames or tuple(sorted(set(starts)))!=tuple(starts):
        raise ValueError('Scene starts must be sorted unique, 2-16, within video')
    return tuple(starts)

def cue_wave(freq,length=.115,rate=SR):
    n=round(length*rate)
    t=np.arange(n,dtype=np.float64)/rate
    env=np.sin(np.pi*np.arange(n)/(n-1))**2*np.exp(-10*t)
    phase=2*np.pi*(freq*t+.09*freq*t*t/(2*length))
    rng=np.random.default_rng(2409)
    noise=np.convolve(rng.normal(size=n),np.ones(30)/30,mode='same')
    y=(np.sin(phase)+.16*np.sin(phase*2)+.12*noise)*env
    return (y/max(np.max(np.abs(y)),1e-9)).astype(np.float32)

def make_mix(voice,frames,starts,genre='ai',peak=.032):
    if genre not in GENRE_TONES:raise ValueError('Unknown genre')
    if not .005<=peak<=.06:raise ValueError('Unsafe cue level')
    starts=validate_starts(starts,frames)
    total=round(frames/FPS*SR)
    if len(voice)>total+int(.02*SR):raise ValueError('Audio longer than video')
    out=np.zeros(total,dtype=np.float32)
    out[:min(len(voice),total)]=voice[:total]
    original=out.copy()
    base=cue_wave(GENRE_TONES[genre])
    events=[]
    for frame in starts[1:]:
        ix=round(frame/FPS*SR)
        lo=max(0,ix-round(.11*SR));hi=min(total,ix+round(.11*SR))
        rms=float(np.sqrt(np.mean(original[lo:hi].astype(np.float64)**2)))
        gain=peak*(.5 if rms>=.06 else 1.)
        end=min(total,ix+len(base))
        out[ix:end]+=gain*base[:end-ix]
        events.append({'frame':frame,'time_s':round(frame/FPS,3),
                       'voice_rms':round(rms,5),'cue_peak':round(gain,5),
                       'ducked':bool(rms>=.06)})
    if np.max(np.abs(out))>=.94:raise ValueError('Mix would clip')
    return out,original,events

def video_hash(path):
    p=subprocess.Popen(['ffmpeg','-v','error','-i',str(path),'-map','0:v:0',
                        '-c:v','copy','-f','h264','-'],
                       stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    h=hashlib.sha256()
    while True:
        b=p.stdout.read(1024*1024)
        if not b:break
        h.update(b)
    err=p.stderr.read();rc=p.wait()
    if rc:raise RuntimeError(err.decode(errors='replace')[-800:])
    return h.hexdigest()

def render(src,dst,genre='ai',starts=SCENE_STARTS,peak=.032):
    src=Path(src);dst=Path(dst);dst.parent.mkdir(parents=True,exist_ok=True)
    frames,_=source_metadata(src)
    voice=decode_audio(src)
    mix,_,events=make_mix(voice,frames,tuple(starts),genre,peak)
    wav=dst.with_suffix('.mix.wav')
    wavfile.write(wav,SR,mix)
    try:
        cmd(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(src),
             '-i',str(wav),'-map','0:v:0','-map','1:a:0','-c:v','copy',
             '-c:a','aac','-b:a','192k','-ar',str(SR),'-ac','1',
             '-t',str(frames/FPS),'-movflags','+faststart',
             '-metadata:s:a:0','language=jpn',str(dst)])
    finally:
        wav.unlink(missing_ok=True)
    outframes,_=source_metadata(dst)
    if outframes!=frames:raise RuntimeError('Frame count changed')
    vh=video_hash(src)
    if vh!=video_hash(dst):raise RuntimeError('H264 picture stream changed')
    return {'frames':frames,'duration_s':frames/FPS,'genre':genre,
            'video_bitstream_equal':True,'video_sha256':vh,'events':events,
            'peak_mix':float(np.max(np.abs(mix))),'output':str(dst)}

def main():
    p=argparse.ArgumentParser()
    p.add_argument('source');p.add_argument('output')
    p.add_argument('--genre',choices=sorted(GENRE_TONES),default='ai')
    p.add_argument('--starts',default=','.join(map(str,SCENE_STARTS)))
    p.add_argument('--peak',type=float,default=.032)
    a=p.parse_args()
    print(json.dumps(render(a.source,a.output,a.genre,
                            tuple(map(int,a.starts.split(','))),a.peak),
                     ensure_ascii=False,indent=2))
if __name__=='__main__':main()
