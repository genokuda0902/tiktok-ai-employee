"""Cycle1151: reusable, source-data-driven chart reveal for image-slide videos.

Overlay only a selected diagram region in an already reviewed source MP4.
All artwork is generated from code and synthetic numeric data; no external assets.
No ASR claims, auto-publishing, or network access. 10 genre palettes supported.
"""
from __future__ import annotations
import argparse, json, math, shutil, subprocess, tempfile
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

FPS=30
SCENE_START=5.6
SCENE_END=8.233
POS=(610,746)
SIZE=(352,400)
VALUES=(9,14,21)
LABELS=('1週','2週','3週')
PALETTES={
 'ai-work':'#49E3D6','finance':'#E0BD72','career':'#98CAFF',
 'health':'#82DDB7','learning':'#ADAAFF','travel':'#FFC398',
 'technology':'#7FE2FF','business':'#6FE2C7','life':'#F5A9C9',
 'history':'#E7C58C',
}
FONT='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
FONT_BOLD='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'

def ease(x):
    x=max(0.,min(1.,x)); return x*x*(3-2*x)

def reveal_fraction(t,i):
    # Independent staggered proof reveals, each with a meaningful data label.
    return ease((t-(.24+i*.43))/.52)

def font(size,bold=False):
    path=FONT_BOLD if bold else FONT
    if not Path(path).exists():
        from subprocess import check_output
        path=check_output(['fc-match','-f','%{file}','Noto Sans CJK JP'],text=True).strip()
    return ImageFont.truetype(path,size)

def draw_frame(t,genre='ai-work',values=VALUES,labels=LABELS):
    if genre not in PALETTES:raise ValueError('Unknown genre')
    if len(values)!=3 or len(labels)!=3 or any(not 0<=v<=1000 for v in values):
        raise ValueError('Three nonnegative bounded values required')
    im=Image.new('RGBA',SIZE,(0,0,0,0)); d=ImageDraw.Draw(im,'RGBA')
    # Intentional inset card hides the original static graph, preserving its panel header/footer.
    d.rounded_rectangle((0,0,351,399),radius=16,fill=(4,31,46,255),outline=(57,130,143,245),width=2)
    d.text((20,13),'完了件数の推移',font=font(22,True),fill=(226,250,249,255))
    d.text((20,46),'数値が伸びる過程を可視化',font=font(14),fill=(142,204,209,255))
    # Light guide lines, shared between genres.
    for y in (115,167,219,271):
        d.line((24,y,327,y),fill=(64,113,128,90),width=1)
    maxv=max(max(values),1)
    accent=tuple(bytes.fromhex(PALETTES[genre][1:]))
    bar_centers=(73,176,279)
    for i,(v,cx,lab) in enumerate(zip(values,bar_centers,labels)):
        f=reveal_fraction(t,i)
        full=int(156*v/maxv)
        h=round(full*f)
        x0=cx-26; x1=cx+26; bottom=271
        if h>=3:
            for j in range(h):
                y=bottom-j
                glow=0.70+0.30*j/max(1,h)
                rgb=tuple(round(c*glow) for c in accent)
                d.line((x0,y,x1,y),fill=(*rgb,255),width=1)
            d.rounded_rectangle((x0,bottom-h,x1,bottom-h+7),radius=3,fill=(*accent,255))
        d.text((cx,292),lab,font=font(19,True),anchor='mt',fill=(218,239,242,255))
        if f>.80:
            d.text((cx,bottom-h-7),str(v),font=font(23,True),anchor='mb',fill=(243,255,255,255))
    d.line((22,340,329,340),fill=(66,118,132,155),width=1)
    d.text((24,351),'※ 架空の数値・実績ではありません',font=font(14),fill=(151,190,200,255))
    return im

def make_frames(folder,genre,values=VALUES,labels=LABELS):
    folder=Path(folder);folder.mkdir(parents=True,exist_ok=True)
    n=round((SCENE_END-SCENE_START)*FPS)
    for i in range(n):
        draw_frame(i/FPS,genre,values,labels).save(folder/f'frame_{i:04d}.png')
    return n

def run(source,output,genre='ai-work',report=None,preset='veryfast'):
    source=Path(source);output=Path(output);output.parent.mkdir(parents=True,exist_ok=True)
    if not source.is_file():raise FileNotFoundError(source)
    with tempfile.TemporaryDirectory(prefix='cycle1151_') as td:
        n=make_frames(td,genre)
        cmd=['ffmpeg','-hide_banner','-loglevel','error','-y',
            '-i',str(source),'-itsoffset',str(SCENE_START),'-framerate',str(FPS),
            '-i',str(Path(td)/'frame_%04d.png'),
            '-filter_complex',f"[0:v]drawbox=x=555:y=1105:w=407:h=45:color=0x0a2d40:t=fill:enable='between(t,5.6,8.233)'[base];[base][1:v]overlay=x={POS[0]}:y={POS[1]}:eof_action=pass:repeatlast=0:format=auto,format=yuv420p[v]",
            '-map','[v]','-map','0:a:0','-map_metadata','0',
            '-c:v','libx264','-preset',preset,'-crf','18','-pix_fmt','yuv420p',
            '-c:a','copy','-movflags','+faststart',str(output)]
        subprocess.run(cmd,check=True)
    data={'change':'scene03 animated proof chart (9,14,21) replacing static chart area',
          'source':str(source),'output':str(output),'genre':genre,'overlay_position':POS,
          'overlay_size':SIZE,'scene_window_s':[SCENE_START,SCENE_END],
          'overlay_frames':n,'values':VALUES,'labels':LABELS,'palette_count':len(PALETTES),
          'meaning_or_asr_verified':False,'human_review_required':True,
          'publication_approved':False,'external_media_used':False}
    if report:Path(report).write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
    return data

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('source');p.add_argument('output')
    p.add_argument('--genre',default='ai-work');p.add_argument('--report');p.add_argument('--preset',default='veryfast')
    a=p.parse_args();print(json.dumps(run(a.source,a.output,a.genre,a.report,a.preset),ensure_ascii=False))
