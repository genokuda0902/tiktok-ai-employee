"""Cycle1163: repair double-rendered scene05 status-strip text.

Uses only original, factual-on-screen copy; does not add claims or change
Japanese narration, main captions, or the other seven scenes. The renderer
accepts ten style presets, with source footage kept outside the repository.
"""
from __future__ import annotations
import argparse
import json
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

FPS=30
FIRST=282  # 9.4 s
LAST=329   # 10.9667 s; scene06 begins at 11.0 s
X,Y,W,H=90,1255,900,39
FONT='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
COPY='目的 → 条件 → 形式  |  架空の入力例'
GENRES={
 'ai-work':'#bcefea','finance':'#f6e1ac','career':'#d0f5d6',
 'health':'#c1f0e2','learning':'#d3ebfc','travel':'#f9d7b6',
 'technology':'#c9dfff','business':'#b7f4e8','life':'#f6d3e8',
 'history':'#f4dfbd',
}

def check_bounds():
    assert FIRST>=0 and LAST>=FIRST and LAST<675
    assert X>=0 and Y>1150 and X+W<=1080 and Y+H<1340
    assert len(GENRES)==10
    return True

def make_patch(path:Path,genre='ai-work',font=FONT):
    check_bounds()
    if genre not in GENRES: raise ValueError('Unsupported genre')
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    im=Image.new('RGBA',(W,H),(0,0,0,0))
    d=ImageDraw.Draw(im)
    for i in range(H):
        c=(7+round(i/H*2),43+round(i/H*2),57+round(i/H*2),255)
        d.line((8,i,W-9,i),fill=c,width=1)
    d.rounded_rectangle((0,0,W-1,H-1),radius=9,fill=(8,44,58,255))
    f=ImageFont.truetype(font,26)
    d.text((18,3),COPY,font=f,fill=GENRES[genre],stroke_width=0)
    im.save(path)
    return path

def run(cmd):
    return subprocess.run(cmd,check=True,capture_output=True,text=True)

def render(source,output,patch,genre='ai-work',font=FONT,preset='veryfast'):
    source=Path(source);output=Path(output);patch=Path(patch)
    info=json.loads(run(['ffprobe','-v','error','-show_streams','-of','json',str(source)]).stdout)
    v=next(x for x in info['streams'] if x['codec_type']=='video')
    if (v['width'],v['height'],v['avg_frame_rate'])!=(1080,1920,'30/1'):
        raise ValueError('Requires 1080x1920 30fps source')
    if not any(x['codec_type']=='audio' for x in info['streams']):
        raise ValueError('Source Japanese narration audio missing')
    make_patch(patch,genre,font)
    output.parent.mkdir(parents=True,exist_ok=True)
    filt=f"[0:v][1:v]overlay={X}:{Y}:enable='between(n,{FIRST},{LAST})':shortest=1:format=auto,format=yuv420p[v]"
    run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(source),'-loop','1',
         '-framerate',str(FPS),'-i',str(patch),'-filter_complex',filt,'-map','[v]',
         '-map','0:a:0','-map_metadata','0','-c:v','libx264','-crf','18','-preset',preset,
         '-pix_fmt','yuv420p','-c:a','copy','-frames:v','675','-t','22.5','-movflags','+faststart',str(output)])
    return {'modified_frames':LAST-FIRST+1,'start_frame':FIRST,'last_frame':LAST,
            'genres':len(GENRES),'audio_stream_copy':True,'asr_verified':False,
            'publication_approved':False}

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--source',required=True);p.add_argument('--output',required=True)
    p.add_argument('--patch',required=True);p.add_argument('--genre',default='ai-work',choices=list(GENRES))
    p.add_argument('--font',default=FONT);p.add_argument('--preset',default='veryfast')
    a=p.parse_args()
    print(json.dumps(render(a.source,a.output,a.patch,a.genre,a.font,a.preset),ensure_ascii=False))
