#!/usr/bin/env python3
"""Review-only, 10-genre-capable story bridge. Reimplementation, not v33 source.
Uses only procedural graphics and an allowlisted synthetic-data prior MP4.
No TTS is claimed; prior instrumental is retained. No auto posting.
"""
import argparse, hashlib, json, subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

W,H,FPS=1080,1920,30
BASE_SHA='a791205610df6bbd0bbab97148bc4a034cdb9e399f995b63a4f062971f772573'
BOLD='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
REG='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
VALUES=[120,150,200,250]

def font(size,bold=True):return ImageFont.truetype(BOLD if bold else REG,size)
def run(cmd):return subprocess.run(cmd,check=True,capture_output=True,text=True)
def ease(x):
    x=max(0,min(1,x));return x*x*(3-2*x)
def rounded(d,box,fill,outline=None,r=26,width=3):
    d.rounded_rectangle(box,radius=r,fill=fill,outline=outline,width=width)
def text(d,s,x,y,size,fill,bold=True):d.text((x,y),s,font=font(size,bold),fill=fill)
def center(d,s,y,size,fill,bold=True):
    f=font(size,bold); b=d.textbbox((0,0),s,font=f)
    d.text(((W-(b[2]-b[0]))/2,y),s,font=f,fill=fill)
def validate_story(values=VALUES):
    if len(values)!=4 or any(type(x)!=int or x<0 for x in values):raise ValueError('invalid synthetic dataset')
    if sum(values)!=720:raise ValueError('numeric proof mismatch')
    scenes=[(2,4,'before'),(4,6,'after')]
    assert all(b>a for a,b,_ in scenes)
    return scenes

def make_bg():
    # Bright, high-contrast editorial look instead of previous uniformly dark UI.
    im=Image.new('RGB',(W,H)); px=im.load()
    for y in range(H):
        q=y/H
        c=(int(10+12*q),int(27+20*q),int(48+33*q))
        for x in range(W):px[x,y]=c
    return im

def frame(t,bg):
    before=t<4; phase=ease((t-(2 if before else 4))/.65)
    im=bg.copy();d=ImageDraw.Draw(im)
    accent='#FFBD75' if before else '#42F3C3'
    rounded(d,(54,155,1026,247),'#15394B',outline=accent,r=28,width=3)
    center(d,'AI時短ラボ  /  架空データの再現',171,41,'#F4FCFF')
    center(d,'BEFORE' if before else 'AFTER',323,69,accent)
    center(d,'手入力で集計' if before else 'AIで整理 → 人が検算',443,72,'#FFFFFF')
    center(d,'転記と計算に確認が必要' if before else '元データとの一致を確認',554,42,'#B6D8E6',False)
    rounded(d,(75,700,1005,1325),'#F4FAFF',outline='#A9C7D5',r=48,width=4)
    # Scene motion is genuine frame-by-frame rendering, not a static caption swap.
    if before:
        # Animate a pile of loose paper cards and an incomplete calculation.
        for i,(v,dx,dy) in enumerate(zip(VALUES,[-18,28,-28,24],[0,18,43,63])):
            x=160+dx;y=740+i*107+dy
            off=int((1-phase)*(140 if i%2==0 else -140))
            rounded(d,(x+off,y,x+735+off,y+105),'#FFFFFF',outline='#D2DBE4',r=18,width=3)
            text(d,f'{i+1}月',x+35+off,y+20,39,'#243E53')
            text(d,str(v),x+480+off,y+11,56,'#27384A')
        rounded(d,(210,1210,875,1290),'#FFE8D6',r=18)
        center(d,'合計 ？　手で確認',1217,43,'#AE4D26')
    else:
        for i,v in enumerate(VALUES):
            y=746+i*99
            rounded(d,(154,y,930,y+80),'#E5F7F2',outline='#A7E6D6',r=14,width=2)
            text(d,f'{i+1}月',188,y+9,38,'#2D5660')
            if phase>(i+1)*.14:
                text(d,str(v),686,y+2,49,'#113C42')
                text(d,'✓',844,y+2,47,'#118E73')
        rounded(d,(180,1165,900,1285),'#075E58',r=20)
        center(d,f'検算合計  {sum(VALUES) if phase>.7 else "…"}',1180,56,'#FFFFFF')
    # A continuous progress indicator and action cue guide the eye.
    rounded(d,(90,1400,990,1510),'#103D50',outline=accent,r=22,width=3)
    center(d,'確認前' if before else '120 + 150 + 200 + 250 = 720',1420,43,'#FFFFFF')
    rounded(d,(95,1595,985,1614),'#315367',r=9)
    rounded(d,(95,1595,95+int(890*((t-2)/4)),1614),accent,r=9)
    center(d,'課題を見せる  →  解決の流れを見せる',1670,36,'#B5D7E6')
    center(d,'※架空データ／操作の再現映像／公開未承認',1815,25,'#A2BBC9',False)
    return im

def render(source,output):
    validate_story()
    source=Path(source);output=Path(output)
    if not source.is_file():raise FileNotFoundError(source)
    sha=hashlib.sha256(source.read_bytes()).hexdigest()
    if sha!=BASE_SHA:raise ValueError('source SHA mismatch: '+sha)
    output.parent.mkdir(parents=True,exist_ok=True)
    bridge=output.parent/'bridge_2to6.mp4'
    p=subprocess.Popen(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','rawvideo','-pixel_format','rgb24','-video_size',f'{W}x{H}','-framerate',str(FPS),'-i','pipe:0','-c:v','libx264','-preset','ultrafast','-crf','19','-pix_fmt','yuv420p',str(bridge)],stdin=subprocess.PIPE,stderr=subprocess.PIPE)
    bg=make_bg()
    try:
        for n in range(120):p.stdin.write(frame(2+n/FPS,bg).tobytes())
        p.stdin.close();err=p.stderr.read().decode('utf8','replace')
        if p.wait()!=0:raise RuntimeError(err)
    except Exception:
        p.kill();p.wait();raise
    srt=output.parent/'subtitles.srt'
    captions=['4か月の売上を、まず確認','手作業では転記と検算が必要','AIで整理しても、最後は人が検算','集計の指示を入力（再現）','SUMの範囲を確認','表とグラフの数値を照合','計算途中と確定を区別','保存して、後で検算']
    bounds=['00:00:00,000','00:00:02,000','00:00:04,000','00:00:06,000','00:00:09,000','00:00:12,000','00:00:15,500','00:00:18,500','00:00:20,000']
    srt.write_text(''.join(f'{i+1}\n{bounds[i]} --> {bounds[i+1]}\n{v}\n\n' for i,v in enumerate(captions)),encoding='utf8')
    fc='[0:v]trim=0:2,setpts=PTS-STARTPTS[a];[1:v]setpts=PTS-STARTPTS[b];[0:v]trim=6:20,setpts=PTS-STARTPTS[c];[a][b][c]concat=n=3:v=1:a=0[v]'
    run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(source),'-i',str(bridge),'-i',str(srt),'-filter_complex',fc,'-map','[v]','-map','0:a:0','-map','2:0','-c:v','libx264','-preset','veryfast','-crf','20','-pix_fmt','yuv420p','-r','30','-c:a','copy','-c:s','mov_text','-movflags','+faststart',str(output)])
    result={'cycle':569,'previous_cycle':568,'input_sha256':sha,'output_sha256':hashlib.sha256(output.read_bytes()).hexdigest(),'change':'animated 2-6s Before/After bridge; larger contrast and story clarity','video':'original procedural vector graphics, no user private assets','audio':'cycle566 procedural instrumental, no Japanese narration','subtitles':'8 Japanese scene-descriptions; NOT voice transcription','new_japanese_narration':False,'voice_caption_sync_verified':False,'rights_human_verified':False,'employee_approved':False,'publication':'NOT_APPROVED','auto_post':False,'cost_jpy':0}
    (output.parent/'manifest.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf8')
    return result

if __name__=='__main__':
    a=argparse.ArgumentParser();a.add_argument('--source',required=True);a.add_argument('--output',required=True)
    x=a.parse_args();print(json.dumps(render(x.source,x.output),ensure_ascii=False))
