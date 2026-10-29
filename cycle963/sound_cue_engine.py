"""cycle963: original, quiet, event-synchronized UI sound cues for private review.

Reimplementation, not the v33 generator. The existing Japanese narration and
burned subtitles are inherited, not independently speech-transcribed. No posting.
No third-party sounds: waveforms are generated mathematically.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import math
import subprocess
import tempfile
import wave
from pathlib import Path
import numpy as np

SOURCE_SHA = '4257fccc11a1e8880eb208a5a50f53a9fb815c35f53069048409da021084344d'
RATE = 48000
DURATION = 691 / 30
MAX_CUE_PEAK = 10 ** (-23 / 20)  # -23 dBFS, deliberately quiet under narration
EVENTS = (
    ('proof_reveal', 1.39, 560, 830, 0.20),
    ('report_ready', 8.02, 660, 880, 0.12),
    ('prompt_ready', 11.05, 610, 920, 0.13),
    ('source_check', 16.25, 490, 730, 0.16),
    ('closing_action', 21.15, 620, 940, 0.19),
)
GENRE_CUE_POLICIES = {
    'ai_work': 'UI demonstration: evidence and action beats',
    'finance': 'verified chart transitions only',
    'history': 'dated archival source transitions only',
    'science': 'experiment/result transitions only',
    'health': 'approved factual illustration transitions only',
    'travel': 'verified itinerary step transitions only',
    'food': 'original cooking step transitions only',
    'career': 'approved workflow step transitions only',
    'education': 'worked-example transitions only',
    'lifestyle': 'approved before/after transitions only',
}
REVIEWED = frozenset({'ai_work'})


def sha256(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for chunk in iter(lambda:f.read(1024*1024),b''):
            h.update(chunk)
    return h.hexdigest()


def validate(source, genre='ai_work', review_only=True, publication_approved=False):
    if genre not in GENRE_CUE_POLICIES:
        raise ValueError('unknown genre')
    if genre not in REVIEWED:
        raise ValueError('genre cue mapping and asset rights not independently reviewed')
    if review_only is not True or publication_approved is not False:
        raise ValueError('publication requires employee approval and rights review')
    if not Path(source).is_file() or sha256(source)!=SOURCE_SHA:
        raise ValueError('missing private source or SHA mismatch')
    for name,sec,f1,f2,dur in EVENTS:
        if not (0.0<sec< DURATION-dur-0.05 and 0.05<=dur<=0.25 and 200<=f1<f2<=1500):
            raise ValueError(f'unsafe cue timing/frequency: {name}')
    if any(EVENTS[i+1][1] - (EVENTS[i][1]+EVENTS[i][4]) < 0.7 for i in range(len(EVENTS)-1)):
        raise ValueError('cue overlap')


def cue_waveform(f1,f2,duration, rate=RATE):
    n=int(round(duration*rate))
    t=np.arange(n,dtype=np.float64)/rate
    # Soft two-note percussive UI cue; Hann window removes discontinuities.
    phase=2*np.pi*(f1*t + (f2-f1)*t*t/(2*duration))
    env=np.sin(np.pi*np.arange(n)/(n-1))**2
    out=(0.78*np.sin(phase)+0.22*np.sin(phase*1.5))*env
    return out.astype(np.float32)


def synthesize(rate=RATE):
    out=np.zeros(int(math.ceil(DURATION*rate)),dtype=np.float32)
    for _,sec,f1,f2,dur in EVENTS:
        pulse=cue_waveform(f1,f2,dur,rate)
        start=int(round(sec*rate))
        out[start:start+len(pulse)] += pulse
    peak=float(np.max(np.abs(out)))
    if peak <= 0:
        raise ValueError('silent cues')
    out*=MAX_CUE_PEAK/peak
    return out


def write_wav(path, samples, rate=RATE):
    if len(samples)==0 or np.max(np.abs(samples))>MAX_CUE_PEAK+1e-5:
        raise ValueError('sound effect amplitude exceeds safety limit')
    pcm=np.clip(np.round(samples*32767),-32768,32767).astype('<i2')
    with wave.open(str(path),'wb') as f:
        f.setnchannels(2);f.setsampwidth(2);f.setframerate(rate)
        f.writeframes(np.column_stack((pcm,pcm)).ravel().tobytes())


def render(source,output,genre='ai_work'):
    validate(source,genre)
    source=Path(source);output=Path(output)
    output.parent.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='cycle963_') as td:
        wav=Path(td)/'original_cues.wav'
        write_wav(wav,synthesize())
        # Stream-copy video, preserve all 691 frames and burned subtitles.
        # Deliberately do not alter loudness globally: separate cycle962 handles that.
        cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(source),'-i',str(wav),
             '-filter_complex','[0:a:0][1:a:0]amix=inputs=2:duration=first:normalize=0:dropout_transition=0[a]',
             '-map','0:v:0','-map','[a]','-c:v','copy','-c:a','aac','-b:a','192k',
             '-ar','48000','-ac','2','-metadata:s:a:0','language=jpn',
             '-movflags','+faststart',str(output)]
        subprocess.run(cmd,check=True,timeout=180)
    return {'source_sha256':sha256(source),'output_sha256':sha256(output),
            'cue_events':[{'name':e[0],'at_seconds':e[1],'duration':e[4]} for e in EVENTS],
            'cue_peak_limit_dbfs':-23,'audio':'existing Japanese-tagged narration + original quiet cues',
            'video':'H.264 stream copied unchanged; burned captions preserved',
            'genre':genre,'publication':'HUMAN_REVIEW / PUBLICATION_NOT_APPROVED'}


if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--source',required=True)
    ap.add_argument('--output',required=True);ap.add_argument('--qa',required=True)
    ap.add_argument('--genre',default='ai_work');a=ap.parse_args()
    result=render(a.source,a.output,a.genre)
    Path(a.qa).write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(result,ensure_ascii=False))
