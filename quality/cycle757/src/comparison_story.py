#!/usr/bin/env python3
"""Cycle757: genre-agnostic evidence comparison beat for review-only TikTok videos.

Creates an original comparison composition from an authorized synthetic Calc screenshot
and verified synthetic values; preserves inherited Japanese AAC audio verbatim.
Not a demonstration of live AI automation, no performance/time-savings claims.
"""
from __future__ import annotations
import argparse, hashlib, json, math, subprocess, tempfile
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W,H,FPS=540,960,30
START_FRAME,END_FRAME=493,604  # [16.43333,20.13333), 111 frames
FRAMES=END_FRAME-START_FRAME
COLORS={
 'ai_work':'#4EF4DD','romance':'#FF86C0','beauty':'#CBA6FF',
 'money':'#84E9A9','trivia':'#FFCB73','gadgets':'#7CB8FF',
 'health':'#9BE4D1','sales':'#F7B37A','travel':'#75D9EF','mystery':'#BEA5FA'
}
SAFETY=(30,45,438,790)
MONTHS={'1月':120000,'2月':150000,'3月':200000,'4月':180000}
FONT='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
REG='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'

def font(size,bold=True):return ImageFont.truetype(FONT if bold else REG,size)
def ease(x):
    x=max(0,min(1,x));return x*x*(3-2*x)
def sha(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for chunk in iter(lambda:f.read(1048576),b''):h.update(chunk)
    return h.hexdigest()
def verify_data(data=MONTHS):
    if list(data.keys())!=['1月','2月','3月','4月'] or any(type(v)!=int or v<0 for v in data.values()):raise ValueError('invalid synthetic data')
    if data['3月']!=200000 or data['4月']!=180000 or sum(data.values())!=650000:raise ValueError('narration/visual value mismatch')
    return True

def verify_bounds(boxes, safe=SAFETY):
    l,t,r,b=safe
    for name,(x0,y0,x1,y1) in boxes.items():
        if not(l<=x0<x1<=r and t<=y0<y1<=b):raise ValueError(f'unsafe {name}: {(x0,y0,x1,y1)}')
    return True

def boxes():return {'title':(38,98,415,174),'before':(38,223,227,656),'after':(238,223,427,656),'result':(38,685,427,758)}

def frame(index:int,screenshot:Image.Image,genre='ai_work'):
    if genre not in COLORS:raise ValueError('unsupported genre')
    if not 0<=index<FRAMES:raise ValueError('invalid frame index')
    verify_data();verify_bounds(boxes())
    accent=COLORS[genre];s=index/FPS
    im=Image.new('RGB',(W,H),'#081729');d=ImageDraw.Draw(im)
    for y in range(H):
        u=y/H
        d.line((0,y,W,y),fill=(int(7+7*u),int(19+10*u),int(37+12*u)))
    # Soft original glow, no third-party images.
    glow=Image.new('RGBA',(W,H),(0,0,0,0));g=ImageDraw.Draw(glow)
    g.ellipse((175,170,610,720),fill=(26,170,180,45))
    g.ellipse((-180,370,220,950),fill=(28,92,194,42))
    im=Image.alpha_composite(im.convert('RGBA'),glow.filter(ImageFilter.GaussianBlur(48)))
    d=ImageDraw.Draw(im)
    for k in range(7):
        x=25+k*92;d.line((x,0,x-140,H),fill=(48,78,103,60),width=1)
    d.rounded_rectangle((34,53,430,84),radius=10,fill='#12344A',outline=accent,width=1)
    d.text((45,58),'AI時短ラボ  /  比較で理解',font=font(14),fill='#E8F8FC')
    d.text((37,107),'数字の違いが',font=font(34),fill='#FFFFFF')
    d.text((37,149),'一目でわかる',font=font(34),fill=accent)
    # Cards have a consistent soft shadow / bevel for all genres.
    for x0,x1 in ((38,227),(238,427)):
        d.rounded_rectangle((x0+3,231,x1+4,662),radius=19,fill=(0,0,0,130))
        d.rounded_rectangle((x0,223,x1,656),radius=18,fill='#0C2B3D',outline='#406176',width=2)
        d.rounded_rectangle((x0+2,226,x1-2,271),radius=16,fill='#153E54')
    d.text((52,233),'BEFORE',font=font(19),fill='#C9D7E3')
    d.text((250,233),'AFTER',font=font(19),fill=accent)
    d.text((52,278),'表の数字を読む',font=font(17),fill='#F6FCFF')
    d.text((250,278),'グラフで比較',font=font(17),fill='#F6FCFF')
    # Genuine local screenshot, cropped only from cells with synthetic data.
    pic=screenshot.convert('RGB').crop((55,264,250,386)).resize((162,182),Image.Resampling.LANCZOS)
    d.rounded_rectangle((51,322,215,507),radius=8,fill='#F4F7FA')
    im.paste(pic,(52,323))
    d.rounded_rectangle((53,520,212,615),radius=10,fill='#152F40')
    d.text((64,532),'3月  200,000円',font=font(15),fill='#FFFFFF')
    d.text((64,568),'4月  180,000円',font=font(15),fill='#FFFFFF')
    # Animated comparison: the two values and heights always share data.
    d.line((259,532,410,532),fill='#526E7F',width=2)
    vals=[MONTHS['3月'],MONTHS['4月']]
    for j,(value,x) in enumerate(zip(vals,(270,344))):
        progress=ease((s-.22-j*.38)/.80)
        barh=round(183*value/max(vals)*progress)
        y=532-barh
        if barh>0:
            col=accent if j==0 else '#4A9CC7'
            d.rounded_rectangle((x,y,x+49,532),radius=7,fill=col)
        d.text((x+6,545),('3月','4月')[j],font=font(16),fill='#F5FBFF')
        if progress>.94:
            d.text((x-1,322),('20万','18万')[j],font=font(16),fill='#FFFFFF')
    d.text((252,588),'差：2万円',font=font(18),fill=accent)
    d.rounded_rectangle((38,684,427,758),radius=16,fill='#0E354A',outline=accent,width=2)
    # Match inherited spoken line: 3月20万円、4月18万円.
    d.text((52,696),'3月 20万円',font=font(25),fill='#FFFFFF')
    d.text((247,696),'4月 18万円',font=font(25),fill=accent)
    d.text((52,732),'※架空データ / 実際のAI操作録画ではありません',font=font(12,False),fill='#BCD5DD')
    # Minimal progress strip; no text in platform UI exclusion zone.
    d.rounded_rectangle((38,773,427,778),radius=2,fill='#315166')
    d.rounded_rectangle((38,773,38+round(389*index/(FRAMES-1)),778),radius=2,fill=accent)
    return im.convert('RGB')

def render(source:Path,screenshot:Path,output:Path,genre='ai_work'):
    if not source.is_file() or not screenshot.is_file():raise FileNotFoundError('source/screenshot missing')
    verify_data();verify_bounds(boxes())
    output.parent.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='cycle757_') as tmp:
        tmp=Path(tmp)
        pic=Image.open(screenshot)
        for i in range(FRAMES):frame(i,pic,genre).save(tmp/f'{i:04d}.png',compress_level=2)
        cmd=['ffmpeg','-hide_banner','-nostdin','-y','-loglevel','error',
            '-threads','2','-i',str(source),'-framerate','30','-i',str(tmp/'%04d.png'),
            '-filter_complex',f'[1:v]scale=1080:1920,format=rgba,setpts=PTS-STARTPTS+{START_FRAME}/30/TB[beat];[0:v][beat]overlay=0:0:eof_action=pass:format=auto,format=yuv420p[v]',
            '-map','[v]','-map','0:a:0','-c:v','libx264','-preset','veryfast','-crf','20',
            '-pix_fmt','yuv420p','-r','30','-c:a','copy','-movflags','+faststart',str(output)]
        subprocess.run(cmd,check=True,timeout=240)
    return {'cycle':757,'source_sha256':sha(source),'output_sha256':sha(output),
            'interval_frames':[START_FRAME,END_FRAME],'frames':FRAMES,'genre':genre,
            'values':MONTHS,'approval':'HUMAN_REVIEW / PUBLICATION_NOT_APPROVED'}

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--source',type=Path,required=True)
    p.add_argument('--screenshot',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True)
    p.add_argument('--genre',choices=list(COLORS),default='ai_work')
    a=p.parse_args();print(json.dumps(render(a.source,a.screenshot,a.output,a.genre),ensure_ascii=False,indent=2))
if __name__=='__main__':main()
