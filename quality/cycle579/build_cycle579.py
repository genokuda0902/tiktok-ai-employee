"""Offline cycle579 Japanese footer / CG provenance overlay. HUMAN_REVIEW only."""
import argparse, json, subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
ROOT=Path(__file__).resolve().parent
W,H,S=1080,1920,2
FONT='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
SOURCE=ROOT/'assets/cycle578.mp4'
OUTPUT=ROOT/'output/cycle579_JA_TRUST_FOOTER_HUMAN_REVIEW.mp4'
def genre_themes():
    return json.loads((ROOT/'config/genres.json').read_text(encoding='utf-8'))['genres']
def rgb(v): return tuple(int(v[i:i+2],16) for i in (1,3,5))
def make_overlay(genre='雑学・科学',provenance='cg'):
    genres=genre_themes()
    if genre not in genres: raise ValueError('unknown genre')
    if provenance not in ('cg','unknown'): raise ValueError('unknown provenance')
    value=genres[genre]
    color=rgb(value['theme'] if isinstance(value,dict) else value)
    bg=(5,15,30,255)
    im=Image.new('RGBA',(W*S,H*S),(0,0,0,0));d=ImageDraw.Draw(im)
    def box(rect,fill,r=0,outline=None,width=1):
        rect=tuple(x*S for x in rect)
        if r:d.rounded_rectangle(rect,radius=r*S,fill=fill,outline=outline,width=width*S)
        else:d.rectangle(rect,fill=fill)
    def label(x,y,value,size,fill):
        d.text((x*S,y*S),value,font=ImageFont.truetype(FONT,size*S),fill=fill)
    box((66,1708,310,1787),bg)
    box((78,1722,299,1775),(11,51,59,255),24,(*color,255),2)
    label(99,1728,'学びメモ',32,(247,253,255,255))
    box((334,1716,626,1784),bg)
    if provenance=='cg':
        box((342,1725,609,1773),(12,35,50,255),20,(*color,255),2)
        label(366,1731,'CGイメージ',29,(207,246,239,255))
    box((66,1861,970,1919),bg)
    note='※図解・CGによるイメージ映像です' if provenance=='cg' else '※素材の出典・権利は確認中です'
    label(78,1864,note,29,(181,206,216,255))
    return im.resize((W,H),Image.Resampling.LANCZOS)
def build(source=SOURCE,output=OUTPUT,genre='雑学・科学',provenance='cg'):
    source,output=Path(source),Path(output)
    if not source.is_file():raise FileNotFoundError(source)
    output.parent.mkdir(parents=True,exist_ok=True)
    overlay=ROOT/'work/footer_overlay.png';overlay.parent.mkdir(parents=True,exist_ok=True)
    make_overlay(genre,provenance).save(overlay)
    cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(source),
         '-loop','1','-framerate','30','-i',str(overlay),
         '-filter_complex','[0:v][1:v]overlay=0:0:format=auto:shortest=1,format=yuv420p[v]',
         '-map','[v]','-map','0:a:0','-c:v','libx264','-preset','medium',
         '-crf','19','-r','30','-pix_fmt','yuv420p','-c:a','copy',
         '-t','15.6','-movflags','+faststart',str(output)]
    p=subprocess.run(cmd,text=True,capture_output=True)
    if p.returncode:raise RuntimeError(p.stderr[-2500:])
    return output
if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--source',type=Path,default=SOURCE)
    p.add_argument('--output',type=Path,default=OUTPUT)
    p.add_argument('--genre',default='雑学・科学')
    p.add_argument('--provenance',default='cg',choices=['cg','unknown'])
    a=p.parse_args();print(build(a.source,a.output,a.genre,a.provenance))
