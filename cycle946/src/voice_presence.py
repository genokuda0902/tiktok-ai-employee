"""Offline voice-presence enhancement and acoustic QA; review-only, no ASR or posting.

Changes only the soundtrack. Source video and burned captions are bitstream copied.
This does NOT certify Japanese transcription, caption meaning, licensing or approval.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import subprocess
from pathlib import Path
import numpy as np

GENRES = ('ai_work','business','finance','health','education','lifestyle','technology','career','productivity','travel')
SAMPLE_RATE = 16000
SCENE_CUTS = (2.9,5.8,8.7,11.6,14.5,17.4,20.3)


def run(*args):
    return subprocess.run(args, check=True, capture_output=True, text=True)


def filter_chain(genre: str) -> str:
    if genre not in GENRES:
        raise ValueError('unsupported genre')
    # One conservative, genre-independent chain for spoken narration.
    # A 95Hz high-pass suppresses low rumble/ambient pad, a mild presence boost
    # helps small-device speech audibility, and a low-pass avoids ultrasonic hiss.
    return 'highpass=f=95,equalizer=f=2600:t=q:w=1.2:g=1.8,lowpass=f=12000'


def read_audio(path: Path, rate: int = SAMPLE_RATE) -> np.ndarray:
    p = subprocess.run(['ffmpeg','-v','error','-i',str(path),'-vn','-ac','1','-ar',str(rate),'-f','f32le','-'],check=True,capture_output=True)
    return np.frombuffer(p.stdout,dtype='<f4').copy()


def band_energy_ratio(audio: np.ndarray, rate: int = SAMPLE_RATE) -> float:
    """Presence-band (1.5–4 kHz) / bass (100–400 Hz) energy, dB; NOT intelligibility."""
    if audio.ndim != 1 or len(audio) < rate // 10 or not np.isfinite(audio).all():
        raise ValueError('invalid audio')
    # Stable 100ms windows; mean power avoids treating phase changes as improvement.
    n = rate // 10
    chunks = audio[:len(audio)//n*n].reshape(-1,n).astype(np.float64)
    window = np.hanning(n)
    spectrum = np.abs(np.fft.rfft(chunks*window,axis=1))**2
    freqs = np.fft.rfftfreq(n,1/rate)
    low = spectrum[:,(freqs>=100)&(freqs<400)].sum()
    presence = spectrum[:,(freqs>=1500)&(freqs<4000)].sum()
    return float(10*np.log10((presence+1e-12)/(low+1e-12)))


def speech_activity(audio: np.ndarray, rate: int = SAMPLE_RATE, hop_ms: int = 20) -> np.ndarray:
    """Broadband speech-energy *candidate*, not VAD/ASR. Ambient sound can trigger it."""
    hop = round(rate*hop_ms/1000)
    blocks = len(audio)//hop
    if blocks < 1: raise ValueError('empty audio')
    rms = np.sqrt(np.mean(audio[:blocks*hop].reshape(blocks,hop).astype(np.float64)**2,axis=1))
    floor = np.percentile(rms,20)
    threshold = max(0.009,float(floor*2.4))
    return rms > threshold


def boundary_audit(audio: np.ndarray, cuts=SCENE_CUTS, rate: int = SAMPLE_RATE):
    activity = speech_activity(audio,rate)
    records=[]
    for cut in cuts:
        center=round(cut*50)
        lo=max(0,center-8);hi=min(len(activity),center+9)
        records.append({'cut_seconds':cut,'energy_active_fraction_near_cut':round(float(np.mean(activity[lo:hi])),3),
                        'human_timing_review':bool(np.mean(activity[lo:hi])>.55)})
    return records


def video_hash(path: Path) -> str:
    p=subprocess.Popen(['ffmpeg','-v','error','-i',str(path),'-map','0:v:0','-c:v','copy','-f','h264','-'],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    h=hashlib.sha256()
    while True:
        b=p.stdout.read(1024*1024)
        if not b:break
        h.update(b)
    _,err=p.communicate()
    if p.returncode:raise RuntimeError(err.decode(errors='replace'))
    return h.hexdigest()


def render(source: Path, output: Path, genre='ai_work'):
    source=Path(source);output=Path(output)
    if not source.is_file():raise FileNotFoundError(source)
    if source.resolve()==output.resolve():raise ValueError('cannot overwrite source')
    output.parent.mkdir(parents=True,exist_ok=True)
    run('ffmpeg','-y','-v','error','-i',str(source),'-map','0:v:0','-map','0:a:0',
        '-c:v','copy','-af',filter_chain(genre),'-c:a','aac','-b:a','192k',
        '-ar','48000','-ac','2','-movflags','+faststart',str(output))
    original=read_audio(source);processed=read_audio(output)
    before=band_energy_ratio(original);after=band_energy_ratio(processed)
    src_v=video_hash(source);out_v=video_hash(output)
    if src_v!=out_v:raise RuntimeError('video stream unexpectedly changed')
    if abs(len(original)-len(processed))>SAMPLE_RATE*.08:raise RuntimeError('audio duration drift')
    run('ffmpeg','-v','error','-i',str(output),'-f','null','-')
    return {'genre':genre,'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
        'output_sha256':hashlib.sha256(output.read_bytes()).hexdigest(),
        'video_bitstream_sha256':out_v,'video_unchanged':True,
        'presence_to_bass_db_before':round(before,3),
        'presence_to_bass_db_after':round(after,3),
        'presence_to_bass_db_delta':round(after-before,3),
        'scene_cut_energy_audit':boundary_audit(processed),
        'japanese_asr_verified':False,'caption_semantics_verified':False,
        'approval':'HUMAN_REVIEW / PUBLICATION_NOT_APPROVED'}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--source',required=True);p.add_argument('--output',required=True)
    p.add_argument('--genre',choices=GENRES,default='ai_work');a=p.parse_args()
    print(json.dumps(render(Path(a.source),Path(a.output),a.genre),ensure_ascii=False,indent=2))
