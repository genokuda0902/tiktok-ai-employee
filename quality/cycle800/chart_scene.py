"""Original, rights-safe animated chart segment. Review only; NOT Excel footage."""
import argparse, json, subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
W,H,FPS,FRAMES=1080,1920,30,96
START,END=420,516
FONT='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
BOLD='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'

def validate(c):
    if c.get('mode')!='review_only' or any(c.get(k) is not False for k in ('rights_reviewed','employee_approved','publication_approved')):
        raise ValueError('unapproved media must remain review-only')
    if len(c.get('genres',[]))!=10 or len(set(c['genres']))!=10: raise ValueError('10 unique genres required')
    chart=c['chart']; v=chart['values']; lab=chart['labels']
    if not (2<=len(v)<=8 and len(v)==len(lab)):raise ValueError('2–8 matched bars')
    if any(type(x) is not int or x<0 for x in v) or max(v)<=0:raise ValueError('nonnegative nonzero integer data required')
    if sum(v)!=chart['total']:raise ValueError('sum mismatch')
    if any(not isinstance(s,str) or not 1<=len(s)<=8 for s in lab):raise ValueError('invalid category label')
    if not all(isinstance(chart.get(k),str) and chart[k] for k in ('title','unit','claim')):raise ValueError('missing chart label')
    if not c.get('disclaimer'):raise ValueError('disclaimer required')
    return True

def easing(x):
    x=max(0,min(1,x));return x*x*(3-2*x)

def safe_boxes():
    return {'title':(94,255,986,390),'chart':(94,440,986,1265),'callout':(94,1335,986,1545),'disclosure':(94,1570,986,1645)}

def font(sz,bold=False):return ImageFont.truetype(BOLD if bold else FONT,sz)

def draw_frame(i,c):
    validate(c)
    if not 0<=i<FRAMES:raise ValueError('frame index outside segment')
    im=Image.new('RGB',(W,H),'#061522');d=ImageDraw.Draw(im)
    for k in range(40):
        x=round(900-20*k);y=round(250+18*k)
        d.ellipse((x-400,y-330,x+400,y+330),outline=(7+k//5,24+k//2,39+k),width=2)
    d.rounded_rectangle((80,170,1000,1690),radius=44,fill='#0d2b3d',outline='#255a6c',width=4)
    d.rounded_rectangle((96,185,984,232),radius=16,fill='#155b5b')
    d.text((123,191),'AI時短ラボ  /  DEMO',font=font(27,True),fill='#d5fff4')
    d.text((106,271),'月別データが、グラフに。',font=font(52,True),fill='white')
    d.text((109,350),'数字の変化を一目で確認',font=font(33),fill='#9ed2db')
    d.rounded_rectangle((102,440,978,1280),radius=32,fill='#f4f9fc',outline='#74d7d0',width=4)
    d.rounded_rectangle((125,461,955,532),radius=17,fill='#126b63')
    d.text((148,472),c['chart']['title'],font=font(35,True),fill='white')
    left,right,top,bottom=214,917,608,1115
    values=c['chart']['values'];labels=c['chart']['labels'];n=len(values)
    ymax=max(values)*1.15
    for step in range(5):
        yy=round(bottom-(bottom-top)*step/4)
        d.line((left,yy,right,yy),fill='#d2e2e8',width=2)
        d.text((142,yy-18),f'{round(ymax*step/4/10000)}万',font=font(22),fill='#667e89')
    spacing=(right-left)/n; bw=min(100,spacing*.54)
    for j,(lab,v) in enumerate(zip(labels,values)):
        progress=easing((i-5-j*10)/30)
        bh=round((bottom-top)*v/ymax*progress)
        x=round(left+spacing*(j+.5)); y=bottom-bh
        if bh>0:
            d.rounded_rectangle((round(x-bw/2),y,round(x+bw/2),bottom),radius=10,fill='#1572dd',outline='#0b54b0',width=2)
        d.text((x,bottom+19),lab,font=font(28,True),fill='#27485d',anchor='mt')
        if progress>.97:d.text((x,y-16),f'{v//10000}万円',font=font(25,True),fill='#164b7b',anchor='mb')
    d.text((150,1200),'※ 実際の表計算操作ではありません',font=font(25),fill='#718b99')
    d.rounded_rectangle((103,1330,978,1546),radius=32,fill='#104b57',outline='#28d8be',width=4)
    callout=easing((i-64)/18)
    d.text((142,1360),c['chart']['claim'],font=font(38,True),fill='#e7fffb')
    d.text((142,1442),f'4か月合計  {c["chart"]["total"]:,}{c["chart"]["unit"]}' if callout>.85 else '4か月の数値を表示中…',font=font(39,True),fill='#ffdf65')
    d.text((105,1580),c['disclaimer'],font=font(25),fill='#bdd0d8')
    return im

def render(c,out):
    validate(c)
    cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','pipe:0','-an','-c:v','libx264','-preset','ultrafast','-crf','20','-pix_fmt','yuv420p','-movflags','+faststart',str(out)]
    p=subprocess.Popen(cmd,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
    try:
        for i in range(FRAMES):p.stdin.write(draw_frame(i,c).tobytes())
        p.stdin.close();err=p.stderr.read();rc=p.wait()
        if rc:raise RuntimeError(err.decode(errors='replace'))
    finally:
        if p.poll() is None:p.kill()

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--config',required=True);ap.add_argument('--segment',required=True)
    a=ap.parse_args();render(json.loads(Path(a.config).read_text()),a.segment)
if __name__=='__main__':main()
