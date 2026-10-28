"""cycle940: conservative Japanese narration scene-level matching for private review MP4.

Uses local FFmpeg and NumPy. Never uploads, publishes, merges or posts media.
Keeps the original H.264 bitstream and therefore all burned Japanese subtitles.
No ASR is performed: scene loudness is not proof of subtitle semantic alignment.
"""
from __future__ import annotations
import argparse
import json
import math
import subprocess
import tempfile
from pathlib import Path

SCENE_EDGES = (0., 2.9, 5.8, 8.7, 11.6, 14.5, 17.4, 20.3, 23.04)
GENRE_PROFILES = {
    'ai_productivity': {'max_adjust_db': 1.2, 'transition_ms': 240},
    'business': {'max_adjust_db': 1.2, 'transition_ms': 240},
    'finance': {'max_adjust_db': 1.0, 'transition_ms': 260},
    'education': {'max_adjust_db': 1.0, 'transition_ms': 280},
    'health': {'max_adjust_db': 0.9, 'transition_ms': 300},
    'beauty': {'max_adjust_db': 1.1, 'transition_ms': 260},
    'food': {'max_adjust_db': 1.1, 'transition_ms': 240},
    'travel': {'max_adjust_db': 1.2, 'transition_ms': 240},
    'lifestyle': {'max_adjust_db': 1.0, 'transition_ms': 280},
    'technology': {'max_adjust_db': 1.2, 'transition_ms': 240},
}
SAMPLE_RATE = 48000
ACTIVE_RMS_THRESHOLD = .025


def db(value: float) -> float:
    return 20. * math.log10(max(value, 1e-12))


def db_to_gain(db_value: float) -> float:
    return 10. ** (db_value / 20.)


def bounded_scene_adjustments(levels_db, max_adjust_db=1.2):
    """Return bounded offsets to the median active scene loudness."""
    if not levels_db or not all(math.isfinite(v) for v in levels_db):
        raise ValueError('finite nonempty scene levels required')
    ordered = sorted(levels_db)
    n = len(ordered)
    target = (ordered[(n - 1)//2] + ordered[n//2]) / 2
    return [max(-max_adjust_db, min(max_adjust_db, target - v)) for v in levels_db]


def interpolate_db(t, edges, gains_db, transition_seconds=.24):
    """Smoothstep blend around cuts to avoid instantaneous gain changes."""
    if len(edges) != len(gains_db) + 1:
        raise ValueError('edges mismatch')
    if not all(a < b for a,b in zip(edges, edges[1:])):
        raise ValueError('edges must be strictly increasing')
    if transition_seconds <= 0:
        raise ValueError('transition_seconds must be positive')
    idx = max(0, min(len(gains_db)-1, next((i for i,e in enumerate(edges[1:]) if t < e), len(gains_db)-1)))
    for i in range(1,len(edges)-1):
        edge = edges[i]
        if edge - transition_seconds/2 <= t <= edge + transition_seconds/2:
            u = (t - (edge - transition_seconds/2))/transition_seconds
            u = u*u*(3-2*u)
            return (1-u)*gains_db[i-1]+u*gains_db[i]
    return gains_db[idx]


def analyze_active_levels(audio, sr=SAMPLE_RATE, edges=SCENE_EDGES, window_ms=100):
    import numpy as np
    levels = []
    for a,b in zip(edges[:-1],edges[1:]):
        samples=audio[round(a*sr):min(len(audio),round(b*sr))]
        win=round(sr*window_ms/1000)
        rms=[]
        for pos in range(0,len(samples)-win+1,win):
            segment=samples[pos:pos+win]
            val=float(np.sqrt(np.mean(segment.astype(np.float64)**2)))
            if val >= ACTIVE_RMS_THRESHOLD:
                rms.append(val)
        if not rms:
            raise ValueError(f'no active speech-energy windows in {a}-{b}; no automatic gain applied')
        levels.append(db(math.sqrt(sum(x*x for x in rms)/len(rms))))
    return levels


def make_envelope(count, sr, edges, gains_db, transition_seconds):
    import numpy as np
    times=np.arange(count,dtype=np.float64)/sr
    result=np.full(count,gains_db[0],dtype=np.float64)
    for i in range(1,len(gains_db)):
        boundary=edges[i]
        lo=boundary-transition_seconds/2
        hi=boundary+transition_seconds/2
        u=np.clip((times-lo)/(hi-lo),0.,1.)
        smooth=u*u*(3-2*u)
        result += (gains_db[i]-gains_db[i-1])*smooth
    return np.power(10.,result/20.)


def _run(cmd, **kwargs):
    return subprocess.run(cmd,check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,**kwargs)


def render(source: Path, output: Path, genre: str, report: Path):
    import numpy as np
    import wave
    if genre not in GENRE_PROFILES:
        raise ValueError('unknown genre')
    if not source.exists():
        raise FileNotFoundError(source)
    profile=GENRE_PROFILES[genre]
    with tempfile.TemporaryDirectory(prefix='cycle940_') as tmp:
        raw=Path(tmp)/'voice.f32'
        wav=Path(tmp)/'leveled.wav'
        with raw.open('wb') as f:
            subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(source),'-vn','-ac','1','-ar',str(SAMPLE_RATE),'-f','f32le','-'],check=True,stdout=f)
        audio=np.fromfile(raw,dtype='<f4').astype(np.float64)
        levels_before=analyze_active_levels(audio)
        adjustments=bounded_scene_adjustments(levels_before,profile['max_adjust_db'])
        envelope=make_envelope(len(audio),SAMPLE_RATE,SCENE_EDGES,adjustments,profile['transition_ms']/1000)
        processed=audio*envelope
        peak_before=float(np.max(np.abs(audio)))
        peak_after=float(np.max(np.abs(processed)))
        ceiling=db_to_gain(-1.0)
        safety_gain=min(1.,ceiling/max(peak_after,1e-12))
        processed*=safety_gain
        pcm=(np.clip(processed,-1,1)*32767).astype('<i2')
        with wave.open(str(wav),'wb') as w:
            w.setnchannels(1);w.setsampwidth(2);w.setframerate(SAMPLE_RATE);w.writeframes(pcm.tobytes())
        output.parent.mkdir(parents=True,exist_ok=True)
        _run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(source),'-i',str(wav),'-map','0:v:0','-map','1:a:0','-c:v','copy','-c:a','aac','-b:a','160k','-ar','48000','-movflags','+faststart','-shortest',str(output)])
        levels_after=analyze_active_levels(processed)
        result={
            'genre':genre,'scene_edges_seconds':SCENE_EDGES,
            'active_scene_levels_before_dbfs':[round(v,3) for v in levels_before],
            'active_scene_levels_after_dbfs':[round(v,3) for v in levels_after],
            'scene_gain_offsets_db':[round(v,3) for v in adjustments],
            'active_scene_range_before_db':round(max(levels_before)-min(levels_before),3),
            'active_scene_range_after_db':round(max(levels_after)-min(levels_after),3),
            'peak_before_dbfs':round(db(peak_before),3),
            'peak_after_dbfs':round(db(float(np.max(np.abs(processed)))),3),
            'safety_gain_db':round(db(safety_gain),3),
            'video_codec':'copy','subtitle_treatment':'inherited burned subtitles; H.264 elementary stream unchanged',
            'independent_japanese_asr':'NOT_PERFORMED','publication':'HUMAN_REVIEW / PUBLICATION_NOT_APPROVED'
        }
        report.parent.mkdir(parents=True,exist_ok=True)
        report.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
        return result


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--source',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True)
    p.add_argument('--report',type=Path,required=True)
    p.add_argument('--genre',choices=sorted(GENRE_PROFILES),default='ai_productivity')
    args=p.parse_args()
    print(json.dumps(render(args.source,args.output,args.genre,args.report),ensure_ascii=False,indent=2))

if __name__=='__main__':main()
