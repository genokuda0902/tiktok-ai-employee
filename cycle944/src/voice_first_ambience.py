"""Review-only original ambient bed. No external media, uploads, or publishing."""
from __future__ import annotations
import argparse
import hashlib
import json
import subprocess
from pathlib import Path
import numpy as np

SAMPLE_RATE = 48000
GENRES = ('ai_work', 'business', 'finance', 'health', 'education', 'lifestyle', 'technology', 'career', 'productivity', 'travel')
SCENE_CUTS = (2.9, 5.8, 8.7, 11.6, 14.5, 17.4, 20.3)

def command(*args):
    subprocess.run(args, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)

def read_audio(path):
    p = subprocess.run(['ffmpeg','-v','error','-i',str(path),'-vn','-f','f32le','-ac','2','-ar',str(SAMPLE_RATE),'-'],capture_output=True,check=True)
    return np.frombuffer(p.stdout,dtype='<f4').copy().reshape(-1,2)

def generate_bed(n, genre='ai_work'):
    """Deterministic, non-melodic synthesized soundscape; no sampled music."""
    if genre not in GENRES: raise ValueError('unsupported genre')
    t = np.arange(n, dtype=np.float64)/SAMPLE_RATE
    idx = GENRES.index(genre)
    fundamental = 92.0 + 3.0 * idx
    slow = np.sin(2*np.pi*0.12*t)
    # Three inharmonic soft tones, subtle movement, no recognizable melody.
    pad = (0.48*np.sin(2*np.pi*fundamental*t + .08*slow)
           +0.29*np.sin(2*np.pi*(fundamental*1.503)*t + .19*slow)
           +0.23*np.sin(2*np.pi*(fundamental*2.017)*t - .11*slow))
    pad *= .75 + .25*np.sin(2*np.pi*.19*t)**2
    # Smooth, very soft original scene transition air swells.
    for cut in SCENE_CUTS:
        z=(t-cut)/.22
        pad += .12*np.exp(-.5*z*z)*np.sin(2*np.pi*(fundamental*.65)*t)
    fade = np.minimum(1.0, np.minimum(t/0.7, (n/SAMPLE_RATE-t)/0.8)).clip(0,1)
    pad *= fade
    return np.column_stack([pad, .985*pad]).astype(np.float32)

def duck_envelope(voice, hop=960):
    """Speech-preserving gain control from short-term RMS; no ASR claim."""
    mono = np.mean(voice,axis=1)
    blocks = (len(mono)+hop-1)//hop
    levels = np.array([np.sqrt(np.mean(mono[i*hop:min((i+1)*hop,len(mono))]**2)+1e-12) for i in range(blocks)])
    # Audio in this project is predominantly narration; gate avoids ambient masking.
    active = levels > 10**(-35/20)
    # Hold attenuation around syllables; attack/release 120ms/240ms.
    mask = np.convolve(active.astype(np.float32), np.ones(19,dtype=np.float32), mode='same')>0
    target = np.where(mask, 10**(-43/20), 10**(-31/20))
    smooth = np.convolve(target, np.ones(11)/11, mode='same')
    env = np.interp(np.arange(len(mono)), np.minimum(np.arange(blocks)*hop+hop//2,len(mono)-1),smooth)
    return env.astype(np.float32), active

def mix(voice, genre='ai_work'):
    bed = generate_bed(len(voice), genre)
    env, active = duck_envelope(voice)
    ambience = bed*env[:,None]
    result = voice + ambience
    peak = float(np.max(np.abs(result)))
    if peak>0.95: result *= .95/peak
    return result.astype(np.float32), {'voice_peak':float(np.max(np.abs(voice))), 'mixed_peak':float(np.max(np.abs(result))), 'active_blocks':int(active.sum()), 'total_blocks':len(active), 'ambient_rms':float(np.sqrt(np.mean(ambience**2))), 'genre':genre}

def render(source,output,genre='ai_work'):
    source,output=Path(source),Path(output)
    if not source.is_file():raise FileNotFoundError(source)
    output.parent.mkdir(parents=True,exist_ok=True)
    voice=read_audio(source)
    mixed,qa=mix(voice,genre)
    pcm=output.with_suffix('.review-temp.f32')
    wav=output.with_suffix('.review-temp.m4a')
    try:
        pcm.write_bytes(mixed.astype('<f4').tobytes())
        command('ffmpeg','-y','-v','error','-f','f32le','-ar',str(SAMPLE_RATE),'-ac','2','-i',str(pcm),'-c:a','aac','-b:a','192k',str(wav))
        command('ffmpeg','-y','-v','error','-i',str(source),'-i',str(wav),'-map','0:v:0','-map','1:a:0','-c:v','copy','-c:a','copy','-movflags','+faststart',str(output))
    finally:
        pcm.unlink(missing_ok=True);wav.unlink(missing_ok=True)
    qa.update({'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'output_sha256':hashlib.sha256(output.read_bytes()).hexdigest(),'sample_rate':SAMPLE_RATE,'approval':'HUMAN_REVIEW / PUBLICATION_NOT_APPROVED','independent_japanese_asr':False})
    return qa

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--source',required=True);p.add_argument('--output',required=True);p.add_argument('--genre',choices=GENRES,default='ai_work');a=p.parse_args()
    print(json.dumps(render(a.source,a.output,a.genre),ensure_ascii=False,indent=2))
