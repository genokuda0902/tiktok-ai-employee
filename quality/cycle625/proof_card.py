#!/usr/bin/env python3
"""Cycle625: reusable four-row proof card. Procedural art only; no voice/real app capture."""
import argparse
import subprocess
from PIL import Image, ImageDraw, ImageFont

W, H, FPS, DURATION = 540, 960, 30, 3.5
FONT = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
BOLD = '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
ALLOWED = ('ai_work','beauty','relationships','money','sales_business','career',
           'health_lifestyle','science_trivia','travel_food','product_lifestyle')

def validate(values, labels, genre):
    if genre not in ALLOWED: raise ValueError('unapproved genre')
    if len(values) != 4 or len(labels) != 4: raise ValueError('four labels and values required')
    if any(not isinstance(v, int) or isinstance(v,bool) or v < 0 for v in values):
        raise ValueError('nonnegative integers required')
    if any(not isinstance(s,str) or not s or len(s)>12 for s in labels):
        raise ValueError('invalid label')
    return sum(values)

def layout():
    return {'row_y':[270,360,450,540], 'row_height':74,
            'formula_box':(32,680,508,796), 'safe':(30,100,510,855)}

def frame(t, values=(120,150,200,250), labels=('1月','2月','3月','4月'), genre='ai_work'):
    total=validate(values,labels,genre)
    im=Image.new('RGB',(W,H),(5,19,35)); d=ImageDraw.Draw(im)
    f=lambda n,b=False: ImageFont.truetype(BOLD if b else FONT,n)
    d.rounded_rectangle((28,55,512,120),radius=14,fill=(10,51,67),outline=(34,211,238),width=2)
    d.text((44,71),'AI時短ラボ  /  数字で検証',font=f(24,True),fill=(233,252,255))
    d.text((34,151),'4つの数値を、全部見せる',font=f(32,True),fill='white')
    d.text((35,204),'1月〜4月のサンプル売上',font=f(22),fill=(143,189,205))
    rows=layout()['row_y']; m=max(values) or 1
    for i,(v,label,y) in enumerate(zip(values,labels,rows)):
        appear=max(0.,min(1.,(t-i*0.34)/0.28))
        if appear==0:continue
        d.rounded_rectangle((32,y,508,y+74),radius=13,fill=(18,45,63),outline=(31,77,94),width=2)
        d.text((48,y+15),label,font=f(25,True),fill='white')
        d.rounded_rectangle((127,y+26,350,y+48),radius=7,fill=(32,69,85))
        bar_width=int(220*v/m*appear)
        if bar_width>0:d.rounded_rectangle((127,y+26,127+bar_width,y+48),radius=7,fill=(46,216,202) if i<3 else (255,205,79))
        d.text((375,y+14),str(v),font=f(31,True),fill=(255,220,127) if i==3 else 'white')
    if t>=1.95:
        d.rounded_rectangle((32,680,508,796),radius=20,fill=(207,250,240),outline=(42,212,173),width=3)
        d.text((55,691),'=SUM(B2:B5)',font=f(33,True),fill=(5,71,73))
        if t>=2.45:
            d.text((55,742),f'合計  {total}',font=f(36,True),fill=(5,87,71))
        else:d.text((55,742),'4つの数値を検算',font=f(26),fill=(5,87,71))
    d.text((35,824),'※ 架空データ／Excel操作の再現',font=f(18),fill=(166,193,203))
    return im

def render(path,values=(120,150,200,250),labels=('1月','2月','3月','4月'),genre='ai_work'):
    validate(values,labels,genre)
    cmd=['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s','540x960',
         '-r',str(FPS),'-i','pipe:0','-c:v','libx264','-preset','ultrafast','-crf','19',
         '-pix_fmt','yuv420p','-movflags','+faststart',str(path)]
    p=subprocess.Popen(cmd,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
    try:
        for n in range(round(FPS*DURATION)):
            p.stdin.write(frame(n/FPS,values,labels,genre).tobytes())
        p.stdin.close(); err=p.stderr.read(); rc=p.wait()
    except Exception:
        p.kill();p.wait();raise
    if rc: raise RuntimeError(err.decode(errors='replace'))
    return path

if __name__=='__main__':
    a=argparse.ArgumentParser();a.add_argument('--output',required=True);a.add_argument('--genre',default='ai_work')
    args=a.parse_args();render(args.output,genre=args.genre)
