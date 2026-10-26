"""Audio-energy coverage gate for timed subtitles (not ASR or semantic alignment).

An independent, conservative check that almost all audible narration falls inside
caption intervals. Does NOT verify spoken Japanese words match caption text.
"""
from array import array
from pathlib import Path
import json,math,subprocess


def rms_20ms_from_audio(media, sample_rate=16000, window_ms=20):
    if sample_rate<=0 or window_ms<=0:
        raise ValueError('invalid sample rate/window')
    data=subprocess.check_output(['ffmpeg','-v','error','-i',str(media),'-vn','-f','f32le','-ac','1','-ar',str(sample_rate),'-'])
    values=array('f');values.frombytes(data)
    width=sample_rate*window_ms//1000
    if width<1:raise ValueError('window too small')
    return [math.sqrt(sum(float(v)*float(v) for v in values[i:i+width])/len(values[i:i+width]))
            for i in range(0,len(values),width) if len(values[i:i+width])==width]


def coverage_from_rms(rms,beats,threshold=.01,window_ms=20):
    if threshold<=0 or window_ms<=0:raise ValueError('invalid threshold/window')
    if not rms or not beats:raise ValueError('missing audio/captions')
    mask=[False]*len(rms)
    for b in beats:
        s=float(b['start']);e=float(b['end'])
        if s<0 or e<=s:raise ValueError('invalid caption interval')
        lo=max(0,round(s*1000/window_ms));hi=min(len(mask),round(e*1000/window_ms))
        for i in range(lo,hi):mask[i]=True
    voiced=[i for i,r in enumerate(rms) if r>threshold]
    if not voiced:raise ValueError('no detectable speech energy')
    return sum(mask[i] for i in voiced)/len(voiced)


def audit_media(media,caption_beats_json):
    beats=json.loads(Path(caption_beats_json).read_text())
    return coverage_from_rms(rms_20ms_from_audio(media),beats)
