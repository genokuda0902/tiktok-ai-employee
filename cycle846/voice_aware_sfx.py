"""Review-only perceptually centered transition accents for ten TikTok genres.

Reuses the cycle845 original synthesized cues; aligns each cue energy centroid
to the picture cut and reduces its level where narration is active. Never posts,
uploads user media, or approves publication.
"""
from __future__ import annotations
import argparse
import json
import subprocess
import tempfile
from pathlib import Path
import numpy as np
from cycle845.transition_audio import (
    SAMPLE_RATE, FPS, CUT_FRAMES, GENRES, GATE, sha256, validate,
    probe, decode_audio, sound_cue, write_wav, video_stream_sha,
)


def adaptive_overlay(original: np.ndarray, cuts=CUT_FRAMES, *, peak=.018,
                     threshold=.012, duck_gain=.25):
    """Center cue energy on the picture cut; duck if its span has loud voice.

    Detection is amplitude-based, not Japanese ASR, so noisy speech may be
    misclassified. Preserve original PCM samples outside the cue windows.
    """
    if original.ndim != 2 or original.shape[1] != 2 or not np.isfinite(original).all():
        raise ValueError('Finite stereo PCM required')
    if not (0 < threshold < .2 and 0 < duck_gain <= 1 and 0 < peak <= .025):
        raise ValueError('Invalid ducking configuration')
    if tuple(sorted(set(cuts))) != tuple(cuts):
        raise ValueError('Cue frames must be sorted and unique')
    out = original.copy()
    details = []
    for i, frame in enumerate(cuts):
        at = round(frame * SAMPLE_RATE / FPS)
        cue = sound_cue(peak=peak, seed=20261025+i, pan=(-.5 if i%2==0 else .5))
        power = np.mean(np.square(cue, dtype=np.float64), axis=1)
        centroid = round(float(np.sum(np.arange(len(cue))*power)/np.sum(power)))
        # Unlike cycle845 (start cue exactly at cut), align the sound's energy
        # center to the actual picture cut. The envelope is front-loaded.
        start = at-centroid
        end = start+len(cue)
        if start < 0 or end > len(original):
            raise ValueError('Cue would extend beyond source audio')
        rms = float(np.sqrt(np.mean(np.square(original[start:end], dtype=np.float64))))
        speech_present = rms >= threshold
        gain = duck_gain if speech_present else 1.0
        out[start:end] += cue * gain
        details.append({'frame':int(frame),'seconds':round(frame/FPS,3),
                        'source_rms':round(rms,6),'speech_proxy_active':bool(speech_present),
                        'cue_gain':gain,'energy_centroid_offset_ms':round(1000*centroid/SAMPLE_RATE,2),
                        'start_sample':start,'end_sample':end})
    if np.max(np.abs(out)) >= .8913:
        raise ValueError('Output would exceed -1dBFS sample-peak safety limit')
    return out, details


def render(source: Path, output: Path, manifest: dict, genre='ai_work',
           cuts=CUT_FRAMES, strict=True):
    source,output = Path(source),Path(output)
    validate(manifest, genre, source, output)
    before=probe(source,strict)
    original=decode_audio(source)
    mixed,details=adaptive_overlay(original,cuts)
    output.parent.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='cycle846_') as tmp:
        wav=Path(tmp)/'adaptive.wav'
        write_wav(wav,mixed)
        subprocess.run(['ffmpeg','-hide_banner','-v','error','-y','-i',str(source),
             '-i',str(wav),'-map','0:v:0','-map','1:a:0','-c:v','copy',
             '-c:a','aac','-b:a','192k','-movflags','+faststart',str(output)],
             check=True,timeout=180)
    after=probe(output,strict)
    subprocess.run(['ffmpeg','-v','error','-xerror','-i',str(output),'-f','null','-'],
                   check=True,timeout=120)
    same_video=video_stream_sha(source)==video_stream_sha(output)
    if not same_video: raise ValueError('Video stream changed')
    decoded=decode_audio(output)
    n=min(len(original),len(decoded))
    if abs(len(original)-len(decoded))>2048: raise ValueError('Audio length drift')
    corr=float(np.corrcoef(original[:n].ravel(),decoded[:n].ravel())[0,1])
    if not np.isfinite(corr) or corr < .997: raise ValueError('Voice retention below threshold')
    decoded_peak=float(np.max(np.abs(decoded)))
    if decoded_peak >= .92: raise ValueError('Decoded peak guard failed')
    return {'source_sha256':sha256(source),'output_sha256':sha256(output),
            'before':before,'after':after,'cut_details':details,
            'speech_ducked_count':sum(d['speech_proxy_active'] for d in details),
            'full_gain_count':sum(not d['speech_proxy_active'] for d in details),
            'video_stream_sha256_unchanged':same_video,
            'voice_waveform_correlation':corr,'decoded_peak':decoded_peak,
            'full_av_decode':True,'ten_genres':len(GENRES),
            'japanese_transcription_verified':False,'caption_semantic_sync_verified':False,
            'reference_v33_compared':False,'rights_approved':False,
            'phone_playback_verified':False,'publication_approved':False,
            'status':'HUMAN_REVIEW / PUBLICATION_NOT_APPROVED'}


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--source',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True)
    p.add_argument('--manifest',type=Path,required=True)
    p.add_argument('--genre',default='ai_work')
    a=p.parse_args()
    print(json.dumps(render(a.source,a.output,json.loads(a.manifest.read_text()),a.genre),
                     ensure_ascii=False,indent=2))
if __name__=='__main__': main()
