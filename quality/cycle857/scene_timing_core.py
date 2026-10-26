"""Reusable, narration-aligned scene timing and native-photo gates (10 genres)."""
from dataclasses import dataclass
from pathlib import Path
from PIL import Image
import hashlib

FPS=30
TOTAL_FRAMES=691
# Boundary times chosen in the silences between each 3-beat narration group.
BOUNDARIES=(0,93,174,252,339,423,513,591,691)
GENRES=('ai_work','sales_business','beauty','romance','saving','career','wellness','science','travel_food','product_comparison_lifestyle')
PHOTO_BOX=(90,260,990,1510) # 900x1250 pixels, larger than cycle856 630x630


def frame_counts(boundaries=BOUNDARIES):
    if len(boundaries)!=9 or boundaries[0]!=0 or boundaries[-1]!=TOTAL_FRAMES or any(b<=a for a,b in zip(boundaries,boundaries[1:])):
        raise ValueError('invalid scene boundaries')
    return [b-a for a,b in zip(boundaries,boundaries[1:])]


def native_crop_scale(source_size, box=PHOTO_BOX):
    w,h=source_size; x1,y1,x2,y2=box
    if min(w,h,x2-x1,y2-y1)<=0: raise ValueError('invalid geometry')
    scale=max((x2-x1)/w,(y2-y1)/h)
    if scale>1.0:raise ValueError('photo would be enlarged')
    return scale


def audit_sources(paths):
    if len(paths)!=8:raise ValueError('8 independent images required')
    shas=[];rows=[]
    for p in paths:
        with Image.open(p) as im:
            sz=im.size
        if sz[0]<900 or sz[1]<1500:raise ValueError(f'source below high-resolution floor: {p} {sz}')
        scale=native_crop_scale(sz)
        digest=hashlib.sha256(Path(p).read_bytes()).hexdigest()
        shas.append(digest);rows.append({'path':str(p),'dimensions':list(sz),'scale':round(scale,5),'sha256':digest})
    if len(set(shas))!=8:raise ValueError('duplicate source image')
    return rows


def validate_beats(beats,boundaries=BOUNDARIES):
    if len(beats)!=24:raise ValueError('24 beats required')
    for i in range(8):
        start=boundaries[i]/FPS;end=boundaries[i+1]/FPS
        group=beats[3*i:3*i+3]
        if float(group[0]['start'])<start or float(group[-1]['end'])>end+0.035:
            raise ValueError(f'scene {i+1} does not align with narration')
    return True
