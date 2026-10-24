"""Review-only sequential visual focus on a two-column task scene.

Preserves original audio bitstream and captions. Does not add claims,
source assets, identities, or publishing functionality.
"""
from __future__ import annotations
import argparse
import json
import subprocess
from pathlib import Path

PALETTES = {
 'ai_work':'31B7DA','beauty':'E978A4','love_psychology':'A98DE7',
 'money_saving':'E8A548','sales_business':'16A996','career':'4D88DB',
 'health_life':'75B46D','science':'3A9CCB','travel_food':'E58C5B',
 'product_life':'A480CC'
}
# Borders are strictly above the preexisting lower-third subtitle region.
FOCUS_A = (142, 728, 381, 300)
FOCUS_B = (557, 728, 381, 300)
SAFE_CAPTION_TOP = 1150

def focus_filter(genre: str, start: float, duration: float) -> str:
    if genre not in PALETTES:
        raise ValueError(f'unknown genre: {genre}')
    if start < 0 or duration < 1.5:
        raise ValueError('invalid focus timing')
    for x,y,w,h in (FOCUS_A, FOCUS_B):
        if x<0 or y<0 or x+w>1080 or y+h>SAFE_CAPTION_TOP:
            raise ValueError('focus outside safe visual region')
    color=PALETTES[genre]
    middle=start+duration*0.5
    windows=((FOCUS_A,start+0.14,middle),(FOCUS_B,middle,start+duration-0.12))
    stages=[]
    for (x,y,w,h),a,b in windows:
        enable=f"between(t,{a:.3f},{b:.3f})"
        stages.append(f"drawbox=x={x}:y={y}:w={w}:h={h}:color=0x{color}@0.88:t=9:enable='{enable}'")
        stages.append(f"drawbox=x={x+11}:y={y+11}:w={w-22}:h={h-22}:color=white@0.43:t=2:enable='{enable}'")
    return ','.join(stages)

def run(source:Path, output:Path, genre:str, start:float, duration:float) -> dict:
    if not source.is_file():
        raise FileNotFoundError(source)
    output.parent.mkdir(parents=True,exist_ok=True)
    filt=focus_filter(genre,start,duration)
    cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(source),
         '-map','0:v:0','-map','0:a:0','-vf',filt,
         '-c:v','libx264','-preset','veryfast','-crf','21','-pix_fmt','yuv420p',
         '-c:a','copy','-movflags','+faststart',str(output)]
    subprocess.run(cmd,check=True)
    return {'genre':genre,'start':start,'duration':duration,'focus_regions':[FOCUS_A,FOCUS_B],
            'source':str(source),'output':str(output),'audio_codec':'copy',
            'caption_area_modified':False,'publication_approved':False,'auto_post':False}

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--source',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True)
    p.add_argument('--genre',choices=sorted(PALETTES),required=True)
    p.add_argument('--start',type=float,default=16.0)
    p.add_argument('--duration',type=float,default=3.3)
    args=p.parse_args()
    print(json.dumps(run(args.source,args.output,args.genre,args.start,args.duration),ensure_ascii=False,indent=2))
