#!/usr/bin/env python3
"""Rights-isolated 10-genre editorial TikTok renderer, review-only.

Requires a locally supplied, rights-reviewed narration file and an accompanying
voice_timing.json. Does NOT retrieve or commit inherited/private footage.
The text shown as subtitles is exactly the text in the narration manifest.
"""
import argparse
import hashlib
import json
import math
import os
from pathlib import Path
import subprocess
import tempfile
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W,H,FPS=1080,1920,30
SAFE=(120,155,120,315) # left, top, right, bottom in output pixels
GENRES=('ai_work','beauty','love_psychology','money_saving','sales_business',
        'career','health_life','science','travel_food','product_life')
THEMES={
 'ai_work':('#42CFF5','#B1E6FF'), 'beauty':('#F39ECF','#FFD9EA'),
 'love_psychology':('#F08BA4','#FFE2E8'), 'money_saving':('#F4C36E','#FFE9B6'),
 'sales_business':('#65E0CE','#F6D488'), 'career':('#80BCF4','#D1E8FF'),
 'health_life':('#93E2A9','#D7F8E0'), 'science':('#9CA8F8','#D8DEFF'),
 'travel_food':('#F8BA80','#FCE4C6'), 'product_life':('#89D9DA','#C8F5F1')}
TITLES=(('仕事ができる人は','質問が違う。'),('ゴールを','言葉にする。'),
        ('現在地を','数字で見る。'),('差は、まず','ひとつだけ。'),
        ('「なぜ？」を','3回重ねる。'),('今日の行動に','落とし込む。'),
        ('数字を見て','また直す。'),('小さな改善が','強いチームをつくる。'))
TAGS=('THE QUESTION','GOAL','CURRENT KPI','PRIORITY','ROOT CAUSE','TODAY ACTION','FEEDBACK','BETTER TEAM')
FONT_CANDIDATES=('/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc',
                 '/usr/share/fonts/truetype/noto/NotoSansCJK-Bold.ttc',
                 '/usr/share/fonts/truetype/noto/NotoSansCJKjp-Bold.otf')

def font(size,bold=True):
    path=os.environ.get('CYCLE805_FONT')
    if not path:
        path=next((p for p in FONT_CANDIDATES if Path(p).exists()),None)
    if not path or not Path(path).is_file():
        raise RuntimeError('Japanese Noto font missing; set CYCLE805_FONT')
    return ImageFont.truetype(path,size)

def rgb(s):return tuple(int(s[i:i+2],16) for i in (1,3,5))
def lerp(a,b,t):return tuple(round(a[i]*(1-t)+b[i]*t) for i in range(3))
def center(draw,text,y,f,fill,*,min_x=SAFE[0],max_x=W-SAFE[2]):
    box=draw.textbbox((0,0),text,font=f)
    tw=box[2]-box[0]
    x=(W-tw)//2
    if x<min_x or x+tw>max_x:
        raise ValueError(f'Text outside safe area: {text!r} ({x},{x+tw})')
    draw.text((x,y),text,font=f,fill=fill,stroke_width=0)
    return x,x+tw

def card(d,xy,fill,outline=None,r=26,width=2):
    d.rounded_rectangle(xy,radius=r,fill=fill,outline=outline,width=width)

def background(accent):
    # Original graphics: no stock images, third-party logos, or personal data.
    top=(10,21,37);bottom=(17,44,62)
    row=Image.new('RGB',(1,H));p=row.load()
    for y in range(H):
        t=y/H;p[0,y]=lerp(top,bottom,t)
    im=row.resize((W,H))
    d=ImageDraw.Draw(im,'RGBA')
    for x in range(0,W,90):d.line((x,0,x,H),fill=(175,235,255,10),width=1)
    for y in range(0,H,90):d.line((0,y,W,y),fill=(175,235,255,10),width=1)
    for cx,cy,r in ((870,360,390),(130,1100,450),(950,1570,320)):
        for rad in (r,int(r*.72),int(r*.42)):
            d.ellipse((cx-rad,cy-rad,cx+rad,cy+rad),outline=(*rgb(accent),14),width=3)
    return im

def diagram(d,idx,accent):
    fg='#F4F9FF'; muted='#A8C3D3'; a=accent
    if idx==0:
        card(d,(140,800,940,1245),(22,56,76,255),outline=(*rgb(a),150))
        center(d,'WHAT  →  WHY  →  HOW',845,font(44),a)
        for i,(txt,num) in enumerate((('目的','01'),('原因','02'),('行動','03'))):
            x=195+i*260
            d.ellipse((x,980,x+170,1150),fill=(37,91,106),outline=a,width=4)
            d.text((x+36,998),num,font=font(39),fill=a)
            d.text((x+28,1057),txt,font=font(44),fill=fg)
    elif idx==1:
        card(d,(140,805,940,1250),(23,57,76,255),outline=(92,168,175,160))
        center(d,'GOAL',845,font(46),a)
        center(d,'月間の目標を明確に',950,font(56),fg)
        d.line((220,1110,850,1110),fill='#526D83',width=13)
        d.ellipse((785,1080,845,1140),fill=a)
        center(d,'数字と期限で定義する',1170,font(34),muted)
    elif idx==2:
        card(d,(150,800,930,1270),(24,54,74,255),outline=(90,165,190,130))
        center(d,'TODAY / KPI',845,font(42),a)
        for j,(lab,score) in enumerate((('接続率',0.52),('成約率',0.74),('継続率',0.64))):
            y=955+j*95
            d.text((205,y),lab,font=font(38),fill=fg)
            d.rounded_rectangle((440,y+10,850,y+48),radius=16,fill='#2C4659')
            d.rounded_rectangle((440,y+10,440+int(410*score),y+48),radius=16,fill=a)
        center(d,'※図は架空の例',1235,font(25),muted)
    elif idx==3:
        card(d,(155,820,925,1245),(25,57,75,255),outline=(90,165,190,130))
        for j,(txt,col) in enumerate((('課題 A','#667D8B'),('課題 B',a),('課題 C','#667D8B'))):
            y=875+j*105
            card(d,(220,y,860,y+80),(39,72,86,255),outline=col,width=5 if j==1 else 2)
            d.text((270,y+12),txt,font=font(42),fill=fg)
            if j==1:d.text((720,y+15),'✓',font=font(40),fill=a)
    elif idx==4:
        card(d,(145,820,935,1280),(24,56,76,255),outline=(95,175,190,130))
        for j in range(3):
            y=865+j*125
            d.ellipse((210,y,300,y+90),fill=a if j==2 else '#34556C')
            d.text((242,y+15),str(j+1),font=font(40),fill='#0E2432' if j==2 else fg)
            d.text((350,y+8),'なぜ？',font=font(58),fill=fg)
            if j<2:d.line((255,y+90,255,y+122),fill=a,width=7)
    elif idx==5:
        card(d,(150,810,930,1270),(25,59,77,255),outline=(90,165,190,130))
        center(d,'TODAY  /  ACTION',850,font(43),a)
        for j,txt in enumerate(('誰が','何を','いつまでに')):
            y=960+j*95
            d.rounded_rectangle((225,y,285,y+60),radius=10,outline=a,width=4)
            d.text((330,y-5),txt,font=font(51),fill=fg)
    elif idx==6:
        card(d,(150,820,930,1270),(24,55,75,255),outline=(90,165,190,130))
        points=[(220,1150),(350,1060),(480,1095),(610,940),(750,900),(845,870)]
        for j in range(len(points)-1):d.line((*points[j],*points[j+1]),fill=a,width=12)
        for x,y in points:d.ellipse((x-14,y-14,x+14,y+14),fill='#F3FAFF')
        center(d,'PLAN  →  DO  →  CHECK',1190,font(40),fg)
    else:
        card(d,(150,820,930,1280),(24,58,78,255),outline=(90,165,190,130))
        center(d,'SMALL IMPROVEMENTS',860,font(40),a)
        for j,h in enumerate((95,160,230,315)):
            x=260+j*155
            d.rounded_rectangle((x,1175-h,x+100,1175),radius=14,fill=a if j==3 else '#3D8293')
        center(d,'KEEP IMPROVING',1200,font(38),fg)

def render_slide(idx,caption,genre='sales_business'):
    if genre not in GENRES:raise ValueError('unsupported genre')
    accent,soft=THEMES[genre]
    im=background(accent);d=ImageDraw.Draw(im,'RGBA')
    d.rounded_rectangle((120,160,960,220),radius=22,fill=(42,80,102,170))
    d.text((148,169),'BUSINESS / FIELD NOTES',font=font(28),fill='#D5EAF3')
    d.text((850,169),f'{idx+1:02d}/08',font=font(28),fill=accent)
    for j in range(8):
        x=120+j*108
        d.rounded_rectangle((x,245,x+85,253),radius=3,fill=accent if j<=idx else '#36566B')
    center(d,TAGS[idx],320,font(37),accent)
    headline=TITLES[idx]
    for j,line in enumerate(headline):
        sz=75 if len(line)<=11 else 61
        center(d,line,435+j*104,font(sz),'#FFFFFF')
    d.rounded_rectangle((180,675,900,685),radius=4,fill=accent)
    diagram(d,idx,accent)
    # Captions placed well above TikTok bottom UI, text equals narration manifest.
    card(d,(120,1355,960,1535),(9,27,41,245),outline=(110,172,189,170),r=28)
    csize=49 if len(caption)<=18 else 43
    center(d,caption,1412,font(csize),'#FFFFFF')
    d.text((124,1585),'VOICE & CAPTION: SAME SOURCE',font=font(26),fill='#8FADBF')
    d.text((124,1640),'REVIEW ONLY  •  NO AUTO POST',font=font(25),fill=accent)
    return im

def get_timing(timing_path):
    m=json.loads(Path(timing_path).read_text(encoding='utf-8'))
    if m.get('genre')!='sales_business' or len(m.get('sentences',[]))!=8:
        raise ValueError('Expected exactly 8 business sentences from verified TTS artifact')
    if m.get('voice_engine')!='Open JTalk':raise ValueError('unexpected voice provenance')
    times=[float(x['seconds']) for x in m['sentences']]
    if not all(1.0<t<7.0 for t in times):raise ValueError('invalid sentence duration')
    if not all(x['text'].strip() and '@' not in x['text'] for x in m['sentences']):
        raise ValueError('invalid or potentially private subtitle')
    return m,times

def frame_counts(times):
    result=[];last=0;total=0.
    for t in times:
        total+=t;now=round(total*FPS);result.append(now-last);last=now
    return result

def run(cmd):
    subprocess.run(cmd,check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)

def render(audio,timing,output,slides_dir,genre='sales_business',fast=False):
    m,times=get_timing(timing)
    slides_dir=Path(slides_dir);slides_dir.mkdir(parents=True,exist_ok=True)
    paths=[]
    for i,s in enumerate(m['sentences']):
        p=slides_dir/f'scene_{i+1:02d}.png';render_slide(i,s['text'],genre).save(p)
        paths.append(p)
    counts=frame_counts(times)
    filters=[];inputs=[]
    for i,(p,n) in enumerate(zip(paths,counts)):
        inputs.extend(['-loop','1','-framerate','1','-t','1','-i',str(p)])
        filters.append(f'[{i}:v]zoompan=z=\'min(zoom+0.00035,1.025)\':x=\'iw/2-(iw/zoom/2)\':y=\'ih/2-(ih/zoom/2)\':d={n}:s={W}x{H}:fps={FPS},setsar=1,format=yuv420p[v{i}]')
    filters.append(''.join(f'[v{i}]' for i in range(8))+'concat=n=8:v=1:a=0[v]')
    output=Path(output);output.parent.mkdir(parents=True,exist_ok=True)
    cmd=['ffmpeg','-hide_banner','-loglevel','error','-y',*inputs,'-i',str(audio),
         '-filter_complex',';'.join(filters),'-map','[v]','-map','8:a:0',
         '-c:v','libx264','-preset','ultrafast' if fast else 'veryfast','-crf','23',
         '-pix_fmt','yuv420p','-r',str(FPS),'-c:a','aac','-b:a','128k','-ar','48000',
         '-movflags','+faststart','-shortest',str(output)]
    run(cmd)
    qa={'genre':genre,'status':'HUMAN_REVIEW / PUBLICATION_NOT_APPROVED',
        'captions_source':'exact narration script from voice_timing.json',
        'alignment':'segment-level durations from Open JTalk WAV; not phoneme/ASR verified',
        'seconds_manifest':sum(times),'scene_frames':counts,
        'frame_count_expected':sum(counts),'safe_area':SAFE,
        'no_external_image_assets':True,'voice_license_review_required':True,
        'audio_sha256':hashlib.sha256(Path(audio).read_bytes()).hexdigest(),
        'output_sha256':hashlib.sha256(output.read_bytes()).hexdigest()}
    (output.parent/'qa.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2),encoding='utf-8')
    return qa

if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('--audio',required=True);ap.add_argument('--timing',required=True)
    ap.add_argument('--output',required=True);ap.add_argument('--slides-dir',required=True)
    ap.add_argument('--genre',choices=GENRES,default='sales_business')
    ap.add_argument('--fast',action='store_true')
    a=ap.parse_args()
    print(json.dumps(render(a.audio,a.timing,a.output,a.slides_dir,a.genre,a.fast),ensure_ascii=False,indent=2))
