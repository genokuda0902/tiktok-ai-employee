"""Cycle1019: free caption-safe BEFORE/AFTER attention guide for 10 genres.

Input is an existing 1080x1920 H264/AAC MP4 with scene06 BEFORE/AFTER cards.
Only the borders of existing cards are animated. No narration, subtitles,
facts, or upload/posting logic is generated or modified.
"""
from __future__ import annotations
import argparse
import json
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter

PALETTES = {
    'ai_work': ('#FF737B', '#20D8D3'),
    'business': ('#F07780', '#28D4D4'),
    'education': ('#FFB36B', '#6CD7C7'),
    'career': ('#FF8E83', '#6AD9D2'),
    'finance': ('#ECA56B', '#5DD4AD'),
    'wellness': ('#F398AA', '#74CBAE'),
    'science': ('#EE7A9B', '#60C9EF'),
    'history': ('#E8B574', '#8EC9C5'),
    'productivity': ('#F68E76', '#35D1CF'),
    'daily_tips': ('#FF9A78', '#6FD8C0'),
}
SIZE = (1080, 1920)
BEFORE = (73, 692, 1007, 929)
AFTER = (73, 942, 1007, 1261)

def validate(rect):
    x0,y0,x1,y1=rect
    if not (0 <= x0 < x1 <= SIZE[0] and 0 <= y0 < y1 <= int(SIZE[1]*.68)):
        raise ValueError('Focus must not cover subtitle-safe lower area')

def overlay(path, rect, color):
    validate(rect)
    mask=Image.new('L',SIZE,0)
    ImageDraw.Draw(mask).rounded_rectangle(rect,radius=16,outline=255,width=5)
    glow=mask.filter(ImageFilter.GaussianBlur(19))
    rgb=tuple(bytes.fromhex(color.lstrip('#')))
    result=Image.new('RGBA',SIZE,(0,0,0,0))
    for m,strength in [(glow,.57),(mask,.84)]:
        layer=Image.new('RGBA',SIZE,(*rgb,0))
        layer.putalpha(m.point(lambda x:round(x*strength)))
        result.alpha_composite(layer)
    path.parent.mkdir(parents=True,exist_ok=True)
    result.save(path)

def timings(start=14.1,end=16.767):
    if end-start < 1: raise ValueError('Scene must be >=1s')
    d=end-start
    return ((start+.06*d,start+.37*d),(start+.39*d,end-.04*d),min(.20,d*.09))

def filtergraph(start=14.1,end=16.767):
    before,after,fade=timings(start,end)
    def layer(n,span):
        s,e=span
        return (f'[{n}:v]format=rgba,'
                f'fade=t=in:st={s:.3f}:d={fade:.3f}:alpha=1,'
                f'fade=t=out:st={e-fade:.3f}:d={fade:.3f}:alpha=1[{n}f]')
    return ';'.join([layer(1,before),layer(2,after),
        '[0:v][1f]overlay=shortest=1:format=auto[tmp]',
        '[tmp][2f]overlay=shortest=1:format=auto,format=yuv420p[v]'])

def probe(path):
    return json.loads(subprocess.check_output(['ffprobe','-v','error',
        '-show_entries','format=duration:stream=codec_type,width,height',
        '-of','json',str(path)],text=True))

def render(src,dst,genre='ai_work',start=14.1,end=16.767):
    if genre not in PALETTES: raise ValueError('Unknown genre')
    p=probe(src)
    v=next(x for x in p['streams'] if x['codec_type']=='video')
    if (v['width'],v['height']) != SIZE: raise ValueError('Expected 1080x1920')
    if start<0 or end>float(p['format']['duration']): raise ValueError('Invalid scene time')
    dst.parent.mkdir(parents=True,exist_ok=True)
    colors=PALETTES[genre]
    b=dst.parent/'focus_before.png';a=dst.parent/'focus_after.png'
    overlay(b,BEFORE,colors[0]);overlay(a,AFTER,colors[1])
    subprocess.run(['ffmpeg','-y','-hide_banner','-loglevel','error',
        '-i',str(src),'-loop','1','-framerate','30','-i',str(b),
        '-loop','1','-framerate','30','-i',str(a),
        '-filter_complex',filtergraph(start,end),'-map','[v]','-map','0:a:0',
        '-map_metadata','0','-map_chapters','0','-c:v','libx264',
        '-preset','veryfast','-crf','18','-pix_fmt','yuv420p','-r','30',
        '-c:a','copy','-t',str(p['format']['duration']),
        '-movflags','+faststart',str(dst)],check=True)
    return dst

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('source',type=Path);p.add_argument('output',type=Path)
    p.add_argument('--genre',choices=PALETTES,default='ai_work')
    p.add_argument('--start',type=float,default=14.1)
    p.add_argument('--end',type=float,default=16.767)
    a=p.parse_args()
    print(render(a.source,a.output,a.genre,a.start,a.end))
