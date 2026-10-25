"""Offline, review-only, 10-genre sound accents over existing Japanese narration.

No downloads, commercial libraries, licensed samples, voice synthesis, or posting.
Source is SHA-pinned and fictional; video bitstream is copied unchanged.
This is a reimplementation and NOT the original v33 source.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import subprocess
import tempfile
import wave
from pathlib import Path
import numpy as np

SAMPLE_RATE = 48000
FPS = 30
GENRES = ('ai_work','sales_business','beauty','romance','saving','career',
          'wellness','science','travel_food','product_comparison_lifestyle')
# Frame-exact boundaries of eight scenes in the reviewed 691-frame video.
CUT_FRAMES = (96,170,249,332,420,511,587)
GATE = {'data_classification':'fictional','contains_personal_data':False,
        'contains_confidential_media':False,'review_only':True,
        'publication_approved':False,'external_upload':False,
        'automatic_posting':False,'source_rights_reviewed':False}


def sha256(path: Path) -> str:
    h=hashlib.sha256()
    with Path(path).open('rb') as f:
        for b in iter(lambda:f.read(1<<20),b''):h.update(b)
    return h.hexdigest()


def validate(manifest: dict, genre: str, source: Path, output: Path) -> None:
    if genre not in GENRES:raise ValueError('Unrecognized genre')
    if any(manifest.get(k)!=v for k,v in GATE.items()):
        raise ValueError('Fail-closed rights/privacy/publication policy')
    if not source.is_file() or source.resolve()==output.resolve():
        raise ValueError('Missing source or source/output collision')
    if manifest.get('source_sha256')!=sha256(source):
        raise ValueError('Source checksum mismatch')


def probe(path: Path, strict: bool=True) -> dict:
    data=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams',
                         '-show_format','-of','json',str(path)],text=True))
    v=next((s for s in data['streams'] if s['codec_type']=='video'),None)
    a=next((s for s in data['streams'] if s['codec_type']=='audio'),None)
    if not v or not a or v['codec_name']!='h264' or a['codec_name']!='aac':
        raise ValueError('H264 and AAC required')
    if int(a['sample_rate'])!=SAMPLE_RATE:raise ValueError('48kHz audio required')
    frames=int(v.get('nb_frames') or 0)
    duration=float(data['format']['duration'])
    if strict and (int(v['width']),int(v['height']),v['r_frame_rate'],frames)!=(1080,1920,'30/1',691):
        raise ValueError('Review video must be 1080x1920/30/691')
    if strict and abs(duration-691/FPS)>.1:raise ValueError('Incorrect duration')
    return {'width':int(v['width']),'height':int(v['height']),
            'fps':v['r_frame_rate'],'frames':frames,'duration':duration,
            'audio_codec':a['codec_name'],'sample_rate':int(a['sample_rate'])}


def decode_audio(path: Path) -> np.ndarray:
    raw=subprocess.check_output(['ffmpeg','-v','error','-i',str(path),'-map','0:a:0',
           '-f','f32le','-acodec','pcm_f32le','-ar',str(SAMPLE_RATE),'-ac','2','-'])
    return np.frombuffer(raw,dtype='<f4').reshape(-1,2).copy()


def sound_cue(length: int=int(.19*SAMPLE_RATE),peak: float=.018,
              seed: int=20261025,pan: float=0.) -> np.ndarray:
    """Deterministic gentle stereo brush sound; no external/licensed audio.

    Windowed band-limited-ish noise + low sine sweep. Peak <= peak per channel.
    """
    if not (0<length<=SAMPLE_RATE and 0<peak<=.025 and -1<=pan<=1):
        raise ValueError('Unsafe cue configuration')
    rng=np.random.default_rng(seed)
    n=rng.standard_normal(length)
    # Lowpass + highpass difference to remove harsh extremes and rumble.
    smooth=np.convolve(n,np.ones(31)/31,mode='same')
    wide=np.convolve(n,np.ones(5)/5,mode='same')
    brush=wide-smooth
    t=np.arange(length,dtype=np.float64)/SAMPLE_RATE
    chirp=np.sin(2*np.pi*(900*t+480*t*t))
    attack=np.clip(t/.026,0,1)**2
    release=np.clip((length/SAMPLE_RATE-t)/.11,0,1)**2
    envelope=attack*release
    mono=(.76*brush/(max(np.max(np.abs(brush)),1e-9))+.24*chirp)*envelope
    mono=mono/max(float(np.max(np.abs(mono))),1e-9)*peak
    # Constant-power-ish mild panning; never louder than mono peak.
    return np.column_stack((mono*(1-.2*pan),mono*(1+.2*pan))).astype('<f4')


def overlay_cues(original: np.ndarray,cut_frames: tuple[int,...]=CUT_FRAMES,
                 fps: int=FPS,peak: float=.018) -> tuple[np.ndarray,list[tuple[int,int]]]:
    if original.ndim!=2 or original.shape[1]!=2 or not np.isfinite(original).all():
        raise ValueError('Stereo finite PCM required')
    if len(set(cut_frames))!=len(cut_frames) or tuple(sorted(cut_frames))!=cut_frames:
        raise ValueError('Cut boundaries must be sorted and unique')
    out=original.copy()
    spans=[]
    for i,frame in enumerate(cut_frames):
        at=round(frame*SAMPLE_RATE/fps)
        if at<0 or at>=len(out):raise ValueError('Cue outside audio')
        cue=sound_cue(peak=peak,seed=20261025+i,pan=(-.5 if i%2==0 else .5))
        end=min(len(out),at+len(cue))
        out[at:end]+=cue[:end-at]
        spans.append((at,end))
    if np.max(np.abs(out))>=.8913:  # <= -1.0 dBFS, no hard clipping
        raise ValueError('Peak safety ceiling exceeded; lower cue level')
    return out,spans


def write_wav(path: Path, audio: np.ndarray) -> None:
    pcm=np.round(np.clip(audio,-1,1)*32767).astype('<i2')
    with wave.open(str(path),'wb') as f:
        f.setnchannels(2);f.setsampwidth(2);f.setframerate(SAMPLE_RATE)
        f.writeframes(pcm.tobytes())


def video_stream_sha(path: Path) -> str:
    raw=subprocess.check_output(['ffmpeg','-v','error','-i',str(path),'-map','0:v:0',
        '-c:v','copy','-f','h264','-'])
    return hashlib.sha256(raw).hexdigest()


def render(source: Path,output: Path,manifest: dict,genre: str='ai_work',
           cuts: tuple[int,...]=CUT_FRAMES,strict: bool=True) -> dict:
    source,output=Path(source),Path(output)
    validate(manifest,genre,source,output)
    before=probe(source,strict)
    original=decode_audio(source)
    enhanced,spans=overlay_cues(original,cuts)
    output.parent.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='cycle845_') as tmp:
        wav=Path(tmp)/'mixed.wav'
        write_wav(wav,enhanced)
        subprocess.run(['ffmpeg','-v','error','-y','-i',str(source),'-i',str(wav),
           '-map','0:v:0','-map','1:a:0','-c:v','copy','-c:a','aac','-b:a','192k',
           '-movflags','+faststart',str(output)],check=True,timeout=180)
    after=probe(output,strict)
    subprocess.run(['ffmpeg','-v','error','-xerror','-i',str(output),'-f','null','-'],check=True,timeout=120)
    v0,v1=video_stream_sha(source),video_stream_sha(output)
    if v0!=v1:raise ValueError('Video stream unexpectedly changed')
    decoded=decode_audio(output)
    n=min(len(original),len(decoded))
    if abs(len(decoded)-len(original))>2048:raise ValueError('Audio length changed unexpectedly')
    # Source voice is still present. Correlation does NOT prove semantics or naturalness.
    correlation=float(np.corrcoef(original[:n].reshape(-1),decoded[:n].reshape(-1))[0,1])
    if correlation<.997:raise ValueError('Voice waveform correlation too low')
    peak=float(np.max(np.abs(decoded)))
    if peak>=.92:raise ValueError('Decoded output exceeds peak guard')
    return {'source_sha256':sha256(source),'output_sha256':sha256(output),
            'before':before,'after':after,'video_stream_sha256_unchanged':v0==v1,
            'voice_waveform_correlation':correlation,'decoded_peak':peak,
            'cue_frames':list(cuts),'cue_count':len(spans),'ten_genres':len(GENRES),
            'full_av_decode':True,'asr_semantic_verified':False,
            'subtitle_word_sync_verified':False,'original_v33_compared':False,
            'rights_approved':False,'phone_playback_verified':False,
            'publication_approved':False,'status':'HUMAN_REVIEW / PUBLICATION_NOT_APPROVED'}


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--source',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True)
    p.add_argument('--manifest',type=Path,required=True)
    p.add_argument('--genre',default='ai_work')
    a=p.parse_args()
    print(json.dumps(render(a.source,a.output,json.loads(a.manifest.read_text()),a.genre),ensure_ascii=False,indent=2))
if __name__=='__main__':main()
