#!/usr/bin/env python3
"""cycle756: original, mobile-legible result-first title card; review only.

Reimplementation: no v33 source/assets, confidential imagery, or scraped artwork.
Narration is inherited unchanged from an already review-only local source MP4.
"""
from __future__ import annotations
import argparse, hashlib, json, math, subprocess, tempfile
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W,H,FPS = 1080,1920,30
DURATION=3.2
FONT='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
FONT_REG='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
GENRE_COLORS={
 'ai_work':'#48F4E2', 'romance':'#FF8CC3','beauty':'#DCA7FF',
 'money':'#83E6AA','trivia':'#FFD27C','gadgets':'#84B8FF',
 'health':'#94E5D3','sales':'#F7B27B','travel':'#7CE0F1','mystery':'#C4A4FF'
}
# All content important for comprehension must stay inside this conservative
# mobile preview-safe rectangle; TikTok app chrome is not reproduced/verified.
SAFE=(62,90,880,1580)
NUMBERS=(120000,150000,200000,180000)


def sha256(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for part in iter(lambda:f.read(1<<20),b''): h.update(part)
    return h.hexdigest()


def sum_sales(values=NUMBERS):
    if not 1 <= len(values) <= 12 or any(type(v) is not int or v<0 or v>10**9 for v in values):
        raise ValueError('invalid synthetic sales data')
    return sum(values)


def verify_important_bounds(boxes, safe=SAFE):
    x0,y0,x1,y1=safe
    for name,(a,b,c,d) in boxes.items():
        if not(x0<=a<c<=x1 and y0<=b<d<=y1):
            raise ValueError(f'{name} outside safe region: {(a,b,c,d)}')
    return True


def smooth(x):
    x=max(0.,min(1.,x)); return x*x*(3-2*x)


def fonts():
    return {n:ImageFont.truetype(FONT,size) for n,size in
            [('label',31),('headline',71),('number',155),('unit',74),('caption',40),('small',27)]}


def _hex_rgb(value): return tuple(bytes.fromhex(value[1:]))


def compose_static(screenshot:Image.Image, genre='ai_work'):
    if genre not in GENRE_COLORS: raise ValueError('unknown genre')
    if screenshot.width < 400 or screenshot.height < 200: raise ValueError('screenshot too small')
    accent=GENRE_COLORS[genre];f=fonts()
    im=Image.new('RGB',(W,H));p=im.load()
    # Original gradient with no third-party textures.
    for y in range(H):
        t=y/H
        c=(int(7+7*t),int(19+9*t),int(36+13*t))
        for x in range(W):p[x,y]=c
    glow=Image.new('RGBA',(W,H),(0,0,0,0));g=ImageDraw.Draw(glow)
    g.ellipse((-180,260,1040,1160),fill=(*_hex_rgb(accent),32))
    g.ellipse((280,990,1480,1870),fill=(22,132,174,26))
    glow=glow.filter(ImageFilter.GaussianBlur(105))
    im=Image.alpha_composite(im.convert('RGBA'),glow)
    d=ImageDraw.Draw(im)
    for i in range(7):
        x=35+i*160
        d.line((x,0,x-250,1900),fill=(27,57,75,110),width=2)
    # Vertical safe-area strip is intentionally free of critical text at x>880.
    d.rounded_rectangle((65,112,836,180),radius=21,fill=(15,51,69,240),outline=accent,width=2)
    d.text((92,126),'AI時短ラボ  /  EXCEL',font=f['label'],fill='#F3FAFD')
    d.text((69,268),'Excel集計、',font=f['headline'],fill='#FFFFFF',stroke_width=1,stroke_fill='#FFFFFF')
    d.text((69,365),'まだ手作業？',font=f['headline'],fill='#FFFFFF',stroke_width=1,stroke_fill='#FFFFFF')
    d.rounded_rectangle((68,618,854,924),radius=27,fill=(12,41,58,250),outline=accent,width=3)
    d.text((95,641),'4か月の売上合計',font=f['caption'],fill='#D5EFF3')
    # Keep the proof screenshot readable and framed. Its content is synthetic.
    frame=(70,965,855,1480)
    d.rounded_rectangle(frame,radius=26,fill=(12,40,52,255),outline=accent,width=3)
    pic=screenshot.convert('RGB')
    # Compose two faithful crops from the same Calc screenshot: formula bar and
    # selected cells. Exclude application warning banners, not data or values.
    if pic.width>=510 and pic.height>=430:
        formula=pic.crop((55,146,510,188)).resize((742,69),Image.Resampling.LANCZOS)
        cells=pic.crop((55,260,380,425)).resize((742,306),Image.Resampling.LANCZOS)
        proof=Image.new('RGB',(742,460),'#F8FAFB')
        proof.paste(formula,(0,12))
        proof.paste(cells,(0,100))
    else:
        proof=pic.resize((742,460),Image.Resampling.LANCZOS)
    d.rounded_rectangle((88,991,836,1462),radius=14,fill=(246,249,250,255))
    im.paste(proof,(91,997))
    d.text((84,1492),'実際の表計算画面の抜粋',font=f['small'],fill='#DAF5F5')
    d.text((84,1530),'※架空データ / AI操作はイメージ',font=f['small'],fill='#AFCAD4')
    return im


def important_boxes():
    return {
       'headline':(69,268,810,462),
       'numeric_result':(92,696,834,900),
       'screenshot':(70,965,855,1480),
       'disclaimer':(84,1492,845,1570),
    }


def frame_image(i:int, base:Image.Image, genre='ai_work', total_frames=96):
    if genre not in GENRE_COLORS: raise ValueError('unknown genre')
    if not 0<=i<total_frames:raise ValueError('frame index out of range')
    verify_important_bounds(important_boxes())
    f=fonts();accent=GENRE_COLORS[genre]
    im=base.copy();d=ImageDraw.Draw(im)
    # Number appears by 0.4s and remains large. No animated per-character jitter.
    reveal=smooth((i/FPS-.10)/.30)
    y=691+int((1-reveal)*22)
    if reveal>0:
        fill=(*_hex_rgb(accent),int(255*reveal))
        d.text((101,y),'65',font=f['number'],fill=fill)
        d.text((405,y+47),'万円',font=f['unit'],fill='#FFFFFF')
    # A small leading line makes the motion perceptible even after number reveal.
    d.rounded_rectangle((96,895,830,903),radius=4,fill=(30,80,94,220))
    d.rounded_rectangle((96,895,96+round(734*smooth(i/(total_frames-1))),903),radius=4,fill=accent)
    # Fade into existing shot for continuity, without changing original audio.
    fade=max(0.,min(1.,(total_frames-i-1)/8))
    im.putalpha(round(255*fade))
    return im


def render(source:Path,screenshot:Path,output:Path,genre='ai_work'):
    if genre not in GENRE_COLORS:raise ValueError('unknown genre')
    if not source.is_file() or not screenshot.is_file():raise FileNotFoundError('missing approved local input')
    base=compose_static(Image.open(screenshot),genre)
    count=round(DURATION*FPS)
    output.parent.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='cycle756_') as tmp:
        p=Path(tmp)
        for i in range(count):
            frame_image(i,base,genre,count).save(p/f'{i:04d}.png')
        cmd=['ffmpeg','-hide_banner','-nostdin','-y','-loglevel','error','-threads','2',
             '-i',str(source),'-framerate',str(FPS),'-i',str(p/'%04d.png'),
             '-filter_complex','[1:v]format=rgba[hero];[0:v][hero]overlay=0:0:eof_action=pass:shortest=0:format=auto,format=yuv420p[v]',
             '-map','[v]','-map','0:a:0','-c:v','libx264','-preset','veryfast','-crf','20',
             '-pix_fmt','yuv420p','-r',str(FPS),'-c:a','copy','-movflags','+faststart',str(output)]
        subprocess.run(cmd,check=True,timeout=240)
    return {'source_sha256':sha256(source),'output_sha256':sha256(output),'genre':genre,
            'changed_interval_s':[0,DURATION],'total_frames_overlay':count,
            'data':list(NUMBERS),'total_yen':sum_sales(),'safe_rect':SAFE,
            'approval':'HUMAN_REVIEW / PUBLICATION_NOT_APPROVED'}


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--source',required=True,type=Path)
    p.add_argument('--screenshot',required=True,type=Path)
    p.add_argument('--output',required=True,type=Path)
    p.add_argument('--genre',choices=list(GENRE_COLORS),default='ai_work')
    a=p.parse_args()
    print(json.dumps(render(a.source,a.screenshot,a.output,a.genre),ensure_ascii=False,indent=2))

if __name__=='__main__':main()
