"""Cycle1171: 10-genre, portrait-safe numeric proof focus for narrated slides.

Only fictional example numbers 44/54 already visible in source are emphasized.
No user footage, personal data, audio upload, or automatic posting.
"""
from __future__ import annotations
import argparse, json, math, subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

FPS=30
FRAMES=675
FRAME_START=222
FRAME_COUNT=24
XY=(770,1063)
SIZE=(205,85)
COLORS={
 'ai-work':(64,220,203),'finance':(244,199,102),
 'career':(134,222,166),'health':(112,214,179),
 'learning':(139,188,247),'travel':(240,172,129),
 'technology':(132,178,251),'business':(103,222,209),
 'life':(227,157,205),'history':(230,195,136),
}
FONT='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
FONT_REG='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'

def proof_percent(done=44,total=54):
    if not (isinstance(done,int) and isinstance(total,int) and 0<=done<=total and total>0):
        raise ValueError('counts must be nonnegative integers and done <= total')
    return round(100*done/total,1)

def validate():
    x,y=XY;w,h=SIZE
    assert (w,h)==(205,85)
    assert 0<=x<x+w<=1080 and 0<=y<y+h<=1920
    assert 5.6*FPS<=FRAME_START and FRAME_START+FRAME_COUNT<=math.ceil(8.233*FPS)
    assert y+h<1170
    assert len(COLORS)==10
    assert abs(proof_percent()-81.5)<.001
    return True

def alpha_for(i):
    if not 0<=i<FRAME_COUNT: raise ValueError('frame index out of range')
    if i<7: return (i+1)/7
    if i<18: return 1.0
    return max(0.0,(FRAME_COUNT-i)/6)

def overlay(i,genre='ai-work'):
    validate()
    if genre not in COLORS: raise ValueError('unsupported genre')
    w,h=SIZE;scale=2;c=COLORS[genre];a=alpha_for(i)
    im=Image.new('RGBA',(w*scale,h*scale),(0,0,0,0))
    d=ImageDraw.Draw(im)
    d.rounded_rectangle((3*scale,3*scale,(w-3)*scale,(h-3)*scale),
       radius=15*scale,fill=(3,29,39,round(244*a)),
       outline=(*c,round(230*a)),width=2*scale)
    d.text((13*scale,7*scale),'完了率',
       font=ImageFont.truetype(FONT_REG,14*scale),
       fill=(214,243,244,round(238*a)))
    d.text((13*scale,27*scale),f'{proof_percent():.1f}%',
       font=ImageFont.truetype(FONT,34*scale),
       fill=(*c,round(255*a)))
    return im.resize((w,h),Image.Resampling.LANCZOS)

def probe(src):
    d=json.loads(subprocess.check_output(
      ['ffprobe','-v','error','-show_streams','-of','json',str(src)],text=True))
    v=next(s for s in d['streams'] if s['codec_type']=='video')
    a=next((s for s in d['streams'] if s['codec_type']=='audio'),None)
    if (v['width'],v['height'],v['avg_frame_rate'])!=(1080,1920,'30/1'):
        raise ValueError('expected 1080x1920 30fps')
    if not a or a['codec_name']!='aac' or int(a['sample_rate'])!=48000:
        raise ValueError('expected AAC narration')
    return d

def render(src,dst,workdir,genre='ai-work',preset='veryfast'):
    src,dst,workdir=map(Path,(src,dst,workdir));probe(src);validate()
    folder=workdir/'focus_frames';folder.mkdir(parents=True,exist_ok=True)
    for i in range(FRAME_COUNT):
        overlay(i,genre).save(folder/f'focus_{i:04d}.png',compress_level=1)
    dst.parent.mkdir(parents=True,exist_ok=True)
    x,y=XY
    cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(src),
      '-framerate',str(FPS),'-i',str(folder/'focus_%04d.png'),
      '-filter_complex',
      f'[1:v]setpts=PTS+{FRAME_START/FPS:.6f}/TB[ov];'
      f'[0:v][ov]overlay={x}:{y}:eof_action=pass:format=auto,format=yuv420p[v]',
      '-map','[v]','-map','0:a:0','-map_metadata','0',
      '-c:v','libx264','-preset',preset,'-crf','18','-pix_fmt','yuv420p',
      '-c:a','copy','-frames:v',str(FRAMES),'-t',str(FRAMES/FPS),
      '-movflags','+faststart',str(dst)]
    subprocess.run(cmd,check=True)
    return {'change':'scene03_percent_magnification','frame_start':FRAME_START,
       'frame_count':FRAME_COUNT,'percentage':proof_percent(),
       'ten_genre_presets':len(COLORS),'audio_stream_copy':True}

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--input',required=True);p.add_argument('--output',required=True)
    p.add_argument('--workdir',required=True)
    p.add_argument('--genre',default='ai-work',choices=tuple(COLORS))
    p.add_argument('--preset',default='veryfast')
    a=p.parse_args()
    print(json.dumps(render(a.input,a.output,a.workdir,a.genre,a.preset),ensure_ascii=False))
if __name__=='__main__': main()
