"""Review-only audio-energy-synced camera punches for ten genres.

Source must be a locally approved private MP4; never uploads, posts, merges,
or invokes paid services. This is NOT independent Japanese ASR.
"""
from __future__ import annotations
import argparse
from array import array
import json
import math
from pathlib import Path
import subprocess

FPS = 30
W, H = 1080, 1920
TOP_H = 1380  # y>=1380 remains source video; caption band begins near 1490
SCENE_BOUNDS = (0, 87, 174, 261, 348, 435, 522, 588, 691)
GENRES = ('ai_work','business','learning','health','beauty','travel',
          'money','cooking','pets','entertainment')
STATUS = 'HUMAN_REVIEW / PUBLICATION_NOT_APPROVED'

def run(*args):
    return subprocess.run(args, check=True, capture_output=True)

def audio_rms_windows(src: Path, sample_rate: int = 16000, hop: int = 1600):
    raw = run('ffmpeg','-v','error','-i',str(src),'-map','0:a:0',
              '-ac','1','-ar',str(sample_rate),'-f','s16le','-').stdout
    samples = array('h')
    samples.frombytes(raw[:len(raw)//2*2])
    rms = []
    for i in range(0, len(samples), hop):
        chunk = samples[i:i+hop]
        if len(chunk) < hop//2:
            break
        rms.append(math.sqrt(sum(x*x for x in chunk)/len(chunk))/32768.0)
    return rms

def choose_punches(rms):
    """Select a speech-energy peak in the middle of each scene, not words."""
    punches = []
    for index, (start, stop) in enumerate(zip(SCENE_BOUNDS, SCENE_BOUNDS[1:])):
        lo = start + max(16, round((stop-start)*.34))
        hi = stop - max(19, round((stop-start)*.32))
        if hi <= lo:
            raise ValueError('scene too short')
        candidates = [(rms[min(len(rms)-1, round(f/FPS*10))], f)
                      for f in range(lo, hi+1, 3)]
        level, center = max(candidates, key=lambda x: x[0])
        if level < .012:
            continue
        a, b = center-12, center+18
        if not (start <= a < center < b < stop):
            raise ValueError('pulse outside scene')
        punches.append(dict(scene=index+1, start=a, peak=center,
                            end=b, audio_rms=round(level, 5)))
    return punches

def zoom_expression(punches):
    pulses = []
    for p in punches:
        a, b = p['start'], p['end']
        pulses.append(f'if(between(on,{a},{b}),max(0,min(1,min((on-{a})/8,({b}-on)/10))),0)')
    expression = '0'
    for p in pulses:
        expression = f'max({expression},{p})'
    return f'1+0.055*({expression})'

def make_filter(punches):
    zoom = zoom_expression(punches)
    return ("[0:v]split=2[base][t];"
            f"[t]crop={W}:{TOP_H}:0:0,"
            f"zoompan=z='{zoom}':x='(iw-iw/zoom)/2':"
            f"y='(ih-ih/zoom)*0.45':d=1:s={W}x{TOP_H}:fps={FPS}[focus];"
            "[base][focus]overlay=0:0:shortest=1[v]")

def render(src: Path, dst: Path, manifest: Path, genre: str):
    if genre not in GENRES:
        raise ValueError('unknown genre')
    if src.resolve() == dst.resolve():
        raise ValueError('never overwrite source')
    dst.parent.mkdir(parents=True, exist_ok=True)
    rms = audio_rms_windows(src)
    punches = choose_punches(rms)
    if len(punches) < 4:
        raise ValueError('insufficient audio activity; fail closed')
    filtergraph = make_filter(punches)
    cmd = ['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(src),
           '-filter_complex',filtergraph,'-map','[v]','-map','0:a:0',
           '-c:v','libx264','-preset','veryfast','-crf','19',
           '-pix_fmt','yuv420p','-r',str(FPS),'-frames:v','691',
           '-c:a','copy','-movflags','+faststart',str(dst)]
    run(*cmd)
    manifest.write_text(json.dumps({'cycle':920,'genre':genre,'status':STATUS,
        'scene_bounds':SCENE_BOUNDS,'punches':punches,'max_zoom':1.055,
        'preserved_lower_region_y':TOP_H,'audio_semantic_check':'NOT_DONE',
        'source':str(src),'output':str(dst)},ensure_ascii=False,indent=2),encoding='utf-8')
    return punches

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--source',required=True,type=Path)
    p.add_argument('--output',required=True,type=Path)
    p.add_argument('--manifest',required=True,type=Path)
    p.add_argument('--genre',default='ai_work',choices=GENRES)
    a = p.parse_args()
    punches = render(a.source,a.output,a.manifest,a.genre)
    print('Review-only rendered:',len(punches),'camera accents')

if __name__ == '__main__':
    main()
