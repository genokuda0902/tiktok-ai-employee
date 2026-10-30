#!/usr/bin/env python3
"""Three-stage visual CTA focus for vertical Japanese slide videos.

Review-only. Does not modify the audio, burnt subtitles, upload, or publish.
Requires the shared three-card CTA template or explicit safe coordinates.
"""
import argparse
import json
import subprocess
from pathlib import Path

GENRES = ('ai_work','trivia','cooking','beauty','money','health','travel','product','story','work_skills')
COLORS = {
 'ai_work':'0x2BE4D2','trivia':'0xF0C76B','cooking':'0xF9A96C',
 'beauty':'0xF6B3C9','money':'0x7DDB99','health':'0x73D5B4',
 'travel':'0x75C9F2','product':'0xA4BBFF','story':'0xD8A9F2','work_skills':'0x6CD8D6'
}
# Coordinates from the original 1080x1920 CTA 3-card template. No captions in this ROI.
DEFAULT_BOXES = ((145,947,250,174),(404,947,254,174),(665,947,253,174))
SAFE_REGION = (70, 380, 950, 1170)  # x_min, y_min, x_max, y_max

def validate_boxes(boxes):
    if len(boxes)!=3: raise ValueError('Exactly 3 card boxes required')
    x0,y0,x1,y1=SAFE_REGION
    for x,y,w,h in boxes:
        if not all(isinstance(z,int) for z in (x,y,w,h)):
            raise ValueError('Box coordinates must be integers')
        if w<=20 or h<=20 or x<x0 or y<y0 or x+w>x1 or y+h>y1:
            raise ValueError('Box outside caption/header-safe CTA area')
    for i in range(3):
        for j in range(i+1,3):
            ax,ay,aw,ah=boxes[i]; bx,by,bw,bh=boxes[j]
            if max(ax,bx)<min(ax+aw,bx+bw) and max(ay,by)<min(ay+ah,by+bh):
                raise ValueError('Stage boxes must not overlap')
    return boxes

def stage_windows(start,end):
    if end-start<1.5: raise ValueError('CTA must be at least 1.5 seconds')
    width=(end-start)/3
    return [(round(start+i*width,6),round(start+(i+1)*width,6)) for i in range(3)]

def filtergraph(genre='ai_work',start=19.767,end=22.5,boxes=DEFAULT_BOXES):
    if genre not in COLORS: raise ValueError('Unknown genre')
    validate_boxes(boxes)
    filters=[]
    for (x,y,w,h),(s,e) in zip(boxes,stage_windows(start,end)):
        enable=f"gte(t,{s})*lt(t,{e})"
        # Subtle glow + clean 4px border; no fill, preserving Japanese glyphs.
        filters.append(f"drawbox=x={x-5}:y={y-5}:w={w+10}:h={h+10}:color={COLORS[genre]}@0.20:t=10:enable='{enable}'")
        filters.append(f"drawbox=x={x}:y={y}:w={w}:h={h}:color={COLORS[genre]}@0.94:t=4:enable='{enable}'")
    return ','.join(filters)+',format=yuv420p'

def render(src,dst,genre='ai_work',start=19.767,end=22.5,boxes=DEFAULT_BOXES,preset='veryfast'):
    if not Path(src).is_file(): raise FileNotFoundError(src)
    Path(dst).parent.mkdir(parents=True,exist_ok=True)
    graph=filtergraph(genre,start,end,boxes)
    cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(src),
         '-vf',graph,'-map','0:v:0','-map','0:a:0','-map','0:d?',
         '-map_metadata','0','-map_chapters','0','-c:v','libx264','-preset',preset,
         '-crf','18','-pix_fmt','yuv420p','-c:a','copy','-c:d','copy',
         '-movflags','+faststart',str(dst)]
    subprocess.run(cmd,check=True)

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('source');p.add_argument('destination')
    p.add_argument('--genre',choices=GENRES,default='ai_work')
    p.add_argument('--start',type=float,default=19.767)
    p.add_argument('--end',type=float,default=22.5)
    p.add_argument('--boxes-json',help='JSON array of three [x,y,width,height] safe card boxes')
    p.add_argument('--preset',default='veryfast')
    a=p.parse_args()
    boxes=tuple(tuple(z) for z in json.loads(a.boxes_json)) if a.boxes_json else DEFAULT_BOXES
    render(a.source,a.destination,a.genre,a.start,a.end,boxes,a.preset)
