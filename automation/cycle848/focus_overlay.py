"""Cycle848: offline narration-timed diagram focus. Review-only; no network or posting.

Input: previously approved-for-internal-review MP4 with burned-in captions.
Output: MP4 with 24 visual diagram highlights, original audio stream copied.
Use the same source MP4/beat JSON for local generation and repository CI smoke test.
"""
from __future__ import annotations
import argparse
import json
import subprocess
from pathlib import Path

SIZE = (1080, 1920)
FPS = 30
FRAMES = 691
GENRES = {
    'ai_work':'24E3D1','sales_business':'FFC96D','beauty':'E6A7FF',
    'romance':'FF8BAF','saving':'5EE0A5','career':'FFB67E',
    'wellness':'A7DF77','science':'7BBEFF','travel_food':'70E0E0',
    'product_comparison_lifestyle':'FFC0D0'
}
POLICY = {'review_only':True,'publication_approved':False,
          'automatic_posting':False,'external_upload':False,
          'source_rights_reviewed':False,'contains_personal_data':False}
# Each scene has 3 diagram areas, matched to the 3 voice/caption beats.
# Coordinates are intentionally restricted to illustration stage (y < 1390).
TARGETS = (
    ((395,820,290,240),(418,830,260,220),(420,1010,250,150)),
    ((143,741,795,138),(143,914,795,138),(143,1084,795,138)),
    ((207,676,658,106),(224,824,634,240),(637,1168,230,112)),
    ((145,666,795,166),(145,865,795,166),(145,1064,795,166)),
    ((124,695,404,490),(548,695,404,490),(560,1025,365,150)),
    ((138,683,806,217),(144,984,200,195),(458,984,175,195)),
    ((280,780,567,123),(310,924,550,210),(600,1174,260,114)),
    ((185,826,140,212),(486,826,140,212),(797,826,140,212)),
)

def validate(beats, genre, policy):
    if genre not in GENRES or len(GENRES)!=10:
        raise ValueError('Unsupported genre')
    if policy != POLICY:
        raise ValueError('Review-only policy must match exactly')
    if len(beats)!=24 or len(TARGETS)!=8:
        raise ValueError('Expected 24 subtitle beats and eight diagrams')
    last=-1
    for i,beat in enumerate(beats):
        start,end=float(beat['start']),float(beat['end'])
        if not (0 <= start < end <= 23.04 and start >= last):
            raise ValueError('Invalid or overlapping beat timeline')
        last=end
        x,y,w,h=TARGETS[i//3][i%3]
        if not (0 <= x < x+w <= SIZE[0] and 600 <= y < y+h < 1390):
            raise ValueError('Focus rectangle outside protected illustration area')
    return True

def make_filter(beats, genre='ai_work', policy=POLICY):
    validate(beats,genre,policy)
    accent='0x'+GENRES[genre]
    effects=[]
    for i,beat in enumerate(beats):
        x,y,w,h=TARGETS[i//3][i%3]
        start,end=float(beat['start']),float(beat['end'])
        en=f'between(t,{start:.3f},{end:.3f})'
        # Restrained overlay: low-opacity highlight, crisp frame, no text or caption occlusion.
        effects.append(f'drawbox=x={x}:y={y}:w={w}:h={h}:color={accent}@0.075:t=fill:enable=\'{en}\'')
        effects.append(f'drawbox=x={x}:y={y}:w={w}:h={h}:color={accent}@0.82:t=5:enable=\'{en}\'')
        # Three unobtrusive beat indicators, inside the illustration panel.
        for j in range(3):
            effects.append(f'drawbox=x={474+50*j}:y=1340:w=26:h=8:color={accent}@{0.95 if j==i%3 else 0.24}:t=fill:enable=\'{en}\'')
    return ','.join(effects)

def render(source,beats_path,out,genre='ai_work',policy=POLICY):
    source=Path(source);out=Path(out)
    if not source.is_file():raise FileNotFoundError(source)
    beats=json.loads(Path(beats_path).read_text(encoding='utf-8'))
    vf=make_filter(beats,genre,policy)
    out.parent.mkdir(parents=True,exist_ok=True)
    cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(source),
         '-vf',vf,'-map','0:v:0','-map','0:a:0','-c:v','libx264',
         '-preset','veryfast','-crf','17','-pix_fmt','yuv420p',
         '-c:a','copy','-movflags','+faststart',str(out)]
    subprocess.run(cmd,check=True)
    return out

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--source',required=True)
    p.add_argument('--beats',required=True)
    p.add_argument('--out',required=True)
    p.add_argument('--genre',default='ai_work')
    a=p.parse_args()
    print(render(a.source,a.beats,a.out,a.genre))
