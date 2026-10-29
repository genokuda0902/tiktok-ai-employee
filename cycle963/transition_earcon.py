"""Original non-musical transition cues for Japanese image-slide MP4 (review only)."""
from __future__ import annotations
import argparse, hashlib, json, math, subprocess, wave
from pathlib import Path
import numpy as np

GENRE_PRESETS = {
    'ai_work': (620, -27), 'business': (520, -29),
    'finance': (490, -30), 'education': (660, -28),
    'career': (550, -29), 'wellness': (450, -31),
    'lifestyle': (610, -30), 'technology': (700, -28),
    'travel': (580, -30), 'trivia': (740, -28),
}
REVIEWED_GENRES = {'ai_work'}
SR = 48000

def run(args, *, stdout=False):
    p = subprocess.run(args, stdout=subprocess.PIPE if stdout else subprocess.DEVNULL,
                       stderr=subprocess.PIPE, check=False, timeout=240)
    if p.returncode:
        raise RuntimeError(f"command failed {p.returncode}: {p.stderr.decode(errors='replace')[-1400:]}")
    return p.stdout if stdout else None

def digest(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for block in iter(lambda:f.read(1<<20), b''):h.update(block)
    return h.hexdigest()

def probe(path):
    return json.loads(run(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(path)],stdout=True))

def decode_audio(path):
    data=run(['ffmpeg','-v','error','-i',str(path),'-map','0:a:0','-vn',
              '-ar',str(SR),'-ac','1','-f','f32le','-'],stdout=True)
    return np.frombuffer(data,dtype='<f4').astype(np.float64)

def detect_scene_cuts(path, count=8, sample_fps=10):
    meta=probe(path)
    duration=float(meta['format']['duration'])
    w,h=54,96
    raw=run(['ffmpeg','-v','error','-i',str(path),'-map','0:v:0','-vf',
             f'fps={sample_fps},scale={w}:{h}','-f','rawvideo','-pix_fmt','rgb24','-'],stdout=True)
    frame_size=w*h*3
    frames=np.frombuffer(raw[:len(raw)//frame_size*frame_size],dtype=np.uint8).reshape(-1,h,w,3)
    if len(frames)<count*2: raise ValueError('insufficient frames')
    diffs=np.abs(np.diff(frames.astype(np.int16),axis=0)).mean(axis=(1,2,3))
    events=[]
    for k in range(1,count):
        center=duration*k/count
        lo=max(1,round((center-.34)*sample_fps))
        hi=min(len(diffs),round((center+.34)*sample_fps))
        if lo>=hi: raise ValueError('scene detection window empty')
        idx=lo+int(np.argmax(diffs[lo-1:hi]))
        score=float(diffs[idx-1])
        if score<9: raise ValueError(f'no reliable scene change near {center:.2f}s: {score:.2f}')
        events.append({'scene':k+1,'time_s':round(idx/sample_fps,3),'visual_change_score':round(score,2)})
    return events

def earcon(f0=620, peak_db=-27, sample_rate=SR):
    """Original non-musical ~140ms two-layer page-swish UI cue."""
    n=int(.14*sample_rate)
    t=np.arange(n)/sample_rate
    sweep=f0+240*(t/.14)**.75
    phase=2*np.pi*np.cumsum(sweep)/sample_rate
    rng=np.random.default_rng(20261029)
    noise=rng.standard_normal(n)
    hp=np.r_[0,np.diff(noise)]
    hp/=max(1e-12,np.max(np.abs(hp)))
    envelope=(1-np.exp(-t/.006))*np.exp(-t/.039)
    sig=(.84*np.sin(phase)+.16*hp)*envelope
    sig*=10**(peak_db/20)/max(1e-12,np.max(np.abs(sig)))
    return sig

def add_earcons(audio, events, genre='ai_work'):
    if genre not in GENRE_PRESETS: raise ValueError('unknown genre')
    if genre not in REVIEWED_GENRES: raise PermissionError('genre not reviewed; no render')
    pitch,level=GENRE_PRESETS[genre]
    out=audio.copy()
    metrics=[]
    for e in events:
        start=round(e['time_s']*SR)
        if start>=len(out): raise ValueError('event after audio')
        cue=earcon(pitch,level)
        before=audio[max(0,start-int(.08*SR)):min(len(audio),start+int(.08*SR))]
        rms=float(np.sqrt(np.mean(before**2))) if len(before) else 0.
        gain_db=-9.0 if rms>10**(-26/20) else -2.0
        cue=cue*10**(gain_db/20)
        end=min(len(out),start+len(cue))
        out[start:end]+=cue[:end-start]
        metrics.append({**e,'voice_rms_dbfs':round(20*math.log10(max(rms,1e-10)),2),
                        'cue_gain_db':gain_db,'cue_peak_dbfs':round(20*math.log10(np.max(np.abs(cue))),2)})
    peak=float(np.max(np.abs(out)))
    if peak>.86:
        raise ValueError(f'unsafe PCM peak {peak:.4f}')
    out *= 10**(-.2/20)
    return out,metrics

def write_wav(path,audio):
    a=np.clip(audio,-1,1)
    with wave.open(str(path),'wb') as w:
        w.setnchannels(1);w.setsampwidth(2);w.setframerate(SR)
        w.writeframes((a*32767).astype('<i2').tobytes())

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--input',required=True)
    ap.add_argument('--output',required=True)
    ap.add_argument('--report',required=True)
    ap.add_argument('--genre',default='ai_work')
    args=ap.parse_args()
    src=Path(args.input);out=Path(args.output);report=Path(args.report)
    out.parent.mkdir(parents=True,exist_ok=True)
    events=detect_scene_cuts(src)
    audio=decode_audio(src)
    mixed,metrics=add_earcons(audio,events,args.genre)
    wav=out.with_suffix('.temporary.wav')
    try:
        write_wav(wav,mixed)
        run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(src),'-i',str(wav),
             '-map','0:v:0','-map','1:a:0','-c:v','copy','-c:a','aac','-b:a','160k',
             '-ar',str(SR),'-metadata:s:a:0','language=jpn',
             '-movflags','+faststart','-t','23.033333',str(out)])
    finally:
        wav.unlink(missing_ok=True)
    result={'source_sha256':digest(src),'output_sha256':digest(out),
            'genre':args.genre,'source_audio_samples':len(audio),
            'original_sound_synthesis':True,'no_third_party_sfx':True,
            'events':metrics,'review_only':True,'publish_approved':False}
    report.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(result,ensure_ascii=False))

if __name__=='__main__':main()
