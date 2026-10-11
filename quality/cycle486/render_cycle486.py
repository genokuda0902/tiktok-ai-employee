#!/usr/bin/env python3
"""Review-only synthetic-data UI demonstration; does not synthesize speech.
Uses self-rendered graphics and a user-owned review MP4 as the audio baseline.
Audio is copied, not independently verified as Japanese speech.
"""
from __future__ import annotations
import argparse, hashlib, json, subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

W,H,FPS=1080,1920,30
REG='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
BOLD='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
VALUES=(120,150,200,250)
MONTHS=('1月','2月','3月','4月')
TOTAL=sum(VALUES)
SCENES=(('problem',1.5,3.5),('source',3.5,5.5),('typing',5.5,7.5),
        ('check',7.5,9.5),('output',9.5,12.0),('compare',14.0,17.0),('cta',17.0,20.166667))
COLORS={'navy':'#08172B','panel':'#122E48','line':'#295878','cyan':'#4CE1FF',
        'mint':'#42E8B1','yellow':'#FFE27D','white':'#F7FBFF','gray':'#ABC6D8'}

def font(size,bold=False): return ImageFont.truetype(BOLD if bold else REG,size)
def command(cmd):
    p=subprocess.run(cmd,capture_output=True,text=True)
    if p.returncode: raise RuntimeError(' '.join(cmd)+'\n'+p.stderr[-3000:])
    return p.stdout

def centered(d,txt,y,size,color='white',bold=True):
    ft=font(size,bold); bb=d.textbbox((0,0),txt,font=ft)
    d.text(((W-(bb[2]-bb[0]))//2,y),txt,font=ft,fill=COLORS.get(color,color))
def label(d,txt,x,y,size=38,color='white',bold=False):
    d.text((x,y),txt,font=font(size,bold),fill=COLORS.get(color,color))
def card(d,box,fill='panel',outline='line',radius=30,width=3):
    d.rounded_rectangle(box,radius=radius,fill=COLORS.get(fill,fill),
                        outline=COLORS.get(outline,outline),width=width)
def base(scene,number):
    im=Image.new('RGB',(W,H),COLORS['navy']); d=ImageDraw.Draw(im)
    for i in range(0,14):
        d.line((i*110-300,240,i*110+180,1640),fill='#0E2A45',width=3)
    card(d,(65,75,1015,190),'#0D3554','#0D3554')
    label(d,'AI時短ラボ',98,106,49,'white',True)
    label(d,f'REVIEW DEMO  /  {number:02d}',650,124,27,'cyan',True)
    card(d,(65,1602,1015,1740),'#0D253C','#0D253C')
    label(d,'※ 架空データを使用・実際の操作録画ではありません',100,1644,31,'gray')
    label(d,'VOICE: 既存音声再利用／字幕同期未確認',100,1772,27,'gray')
    return im,d
def spreadsheet(d,focus=None):
    card(d,(95,570,985,1400),'#EAF4FA','#A2C8D9',26,2)
    d.rounded_rectangle((95,570,985,665),radius=26,fill='#156F61')
    label(d,'月別売上  |  デモ用表計算画面',132,596,40,'white',True)
    cols=[(135,320),(320,620),(620,944)]
    for x0,x1 in cols:
        d.rectangle((x0,708,x1,787),fill='#D4E9F2',outline='#A4C1CF',width=2)
    for txt,x in [('月',165),('売上',360),('検算',670)]:
        label(d,txt,x,726,39,'#143B55',True)
    for i,(m,v) in enumerate(zip(MONTHS,VALUES)):
        y0=788+i*105
        for x0,x1 in cols:
            d.rectangle((x0,y0,x1,y0+105),
                fill=('#F6FBFF' if i%2==0 else '#E4F1F8'),
                outline='#B4CDD9',width=2)
        label(d,m,163,y0+28,40,'#143B55')
        label(d,str(v),360,y0+28,43,'#173D59',True)
        label(d,'OK',678,y0+29,36,'#12856D',True)
        if focus==i: d.rectangle((319,y0,621,y0+105),outline='#FFB931',width=8)
    d.rounded_rectangle((135,1265,945,1340),radius=15,fill='#D0F5E9')
    label(d,f'合計   {TOTAL}',360,1274,43,'#0D5C4E',True)
def draw_scene(kind,index):
    im,d=base(kind,index)
    if kind=='problem':
        centered(d,'毎月の集計、',315,87)
        centered(d,'まだ手で確認？',438,94,'yellow')
        for j,(a,b) in enumerate([('120','1月'),('150','2月'),('200','3月'),('250','4月')]):
            x=125+(j%2)*435;y=720+(j//2)*265
            card(d,(x,y,x+380,y+225),'#183E5C','#326A8A')
            label(d,b,x+30,y+22,43,'gray')
            label(d,a,x+78,y+82,100,'white',True)
        centered(d,'数字を転記 → 計算 → グラフ',1395,44,'cyan')
    elif kind=='source':
        centered(d,'まず元データを確認',305,74)
        label(d,'STEP 01  /  SOURCE',105,460,39,'cyan',True)
        spreadsheet(d)
    elif kind=='typing':
        centered(d,'計算式を入力する',300,75)
        label(d,'STEP 02  /  FORMULA',105,460,39,'cyan',True)
        card(d,(95,635,985,1035),'#EFF8FF','#8AC9E3')
        label(d,'B6  fx',140,693,44,'#1B506B',True)
        card(d,(138,805,945,950),'#FFFFFF','#7FB8D4',20)
        label(d,'=SUM(B2:B5)',175,825,63,'#173D59',True)
        card(d,(220,1120,860,1280),'#135D66','#31DCC5')
        centered(d,'4行の売上を合計',1153,51,'white')
        centered(d,'120 + 150 + 200 + 250',1395,43,'gray')
    elif kind=='check':
        centered(d,'元データと照合する',310,75)
        label(d,'STEP 03  /  VERIFY',105,458,39,'cyan',True)
        spreadsheet(d,focus=3)
        centered(d,'120 + 150 + 200 + 250 = 720',1462,44,'mint')
    elif kind=='output':
        centered(d,'結果は「720」',320,86,'yellow')
        label(d,'STEP 04  /  RESULT',105,480,39,'cyan',True)
        card(d,(115,655,965,1430),'#12314C','#43C7E8')
        label(d,'月別売上の推移',175,703,52,'white',True)
        for i,(v,m) in enumerate(zip(VALUES,MONTHS)):
            x=205+i*188; bottom=1280;top=bottom-int(v*1.43)
            d.rounded_rectangle((x,top,x+110,bottom),radius=12,
                                fill='#33B5F2' if i<3 else '#4EE7AE')
            label(d,str(v),x+17,top-58,39,'white',True)
            label(d,m,x+18,bottom+25,36,'white')
        centered(d,'根拠：4件 / 合計720',1470,43,'mint')
    elif kind=='compare':
        centered(d,'Before  →  After',308,88,'yellow')
        for left,title,lines,fill in [
            (100,'Before',('転記','手計算','作図'),'#482A3A'),
            (560,'After',('元データ','SUM関数','検算OK'),'#174D4C')]:
            card(d,(left,625,left+420,1395),fill,fill)
            label(d,title,left+65,672,65,'white',True)
            for i,txt in enumerate(lines):
                card(d,(left+30,790+i*165,left+390,915+i*165),'#143149','#275877')
                label(d,txt,left+65,820+i*165,47,'white',True)
        centered(d,'手順を再現して、数字を確認',1470,43,'cyan')
    elif kind=='cta':
        centered(d,'グラフは「数字」から',370,80,'white')
        centered(d,'確認しよう。',495,94,'yellow')
        card(d,(130,755,950,1190),'#174A65','#55DCEB')
        centered(d,'元データ → 数式 → 検算',820,53,'white')
        centered(d,'4件の合計：720',990,57,'mint')
        centered(d,'あとで試せるように保存',1420,49,'cyan')
    else: raise ValueError(kind)
    return im
def validate_plan(scenes=SCENES,values=VALUES,total=TOTAL,
                  rights='SYNTHETIC_LOCAL',publication='NOT_APPROVED',auto_post=False):
    if rights!='SYNTHETIC_LOCAL' or publication!='NOT_APPROVED' or auto_post:
        raise ValueError('rights/publication gate')
    if not values or any(type(v)!=int or v<0 for v in values) or sum(values)!=total:
        raise ValueError('data integrity gate')
    if len(set(s[0] for s in scenes))!=len(scenes): raise ValueError('duplicate scene')
    if any(not (0<=a<b<=20.17) for _,a,b in scenes): raise ValueError('bad time')
    if any(scenes[i][2]>scenes[i+1][1] for i in range(len(scenes)-1)):
        raise ValueError('overlap')
    return True
def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--source',type=Path,required=True)
    parser.add_argument('--out',type=Path,required=True)
    args=parser.parse_args()
    validate_plan()
    args.out.parent.mkdir(parents=True,exist_ok=True)
    if not args.source.exists(): raise FileNotFoundError(args.source)
    image_paths=[]
    for n,(kind,_,_) in enumerate(SCENES,1):
        p=args.out.parent/f'frame_{n:02d}_{kind}.png'
        draw_scene(kind,n).save(p,optimize=True)
        image_paths.append(p)
    timeline=[('source',0,1.5,None)]
    timeline += [('still',a,b,p) for (_,a,b),p in zip(SCENES[:5],image_paths[:5])]
    timeline += [('source',12,14,None)]
    timeline += [('still',a,b,p) for (_,a,b),p in zip(SCENES[5:],image_paths[5:])]
    segments=[]
    for n,(typ,start,end,p) in enumerate(timeline):
        target=args.out.parent/f'seg_{n:02d}.mp4'
        frames=round((end-start)*FPS)
        if typ=='source':
            c=['ffmpeg','-y','-hide_banner','-loglevel','error',
               '-ss',str(start),'-i',str(args.source)]
        else:
            c=['ffmpeg','-y','-hide_banner','-loglevel','error',
               '-loop','1','-framerate','30','-i',str(p)]
        c+=['-frames:v',str(frames),'-an','-c:v','libx264','-preset','ultrafast',
            '-crf','21','-pix_fmt','yuv420p',str(target)]
        command(c)
        segments.append(target)
    concat=args.out.parent/'segments.txt'
    concat.write_text('\n'.join("file '"+str(p.resolve())+"'" for p in segments),encoding='utf-8')
    video=args.out.parent/'video_only.mp4'
    command(['ffmpeg','-y','-hide_banner','-loglevel','error','-f','concat','-safe','0',
             '-i',str(concat),'-c:v','copy','-an',str(video)])
    command(['ffmpeg','-y','-hide_banner','-loglevel','error','-i',str(video),
             '-i',str(args.source),'-map','0:v:0','-map','1:a:0',
             '-c:v','copy','-c:a','copy','-t','20.166667',
             '-movflags','+faststart',str(args.out)])
    sha=hashlib.sha256(args.out.read_bytes()).hexdigest()
    manifest={'cycle':486,'baseline':'cycle485','source':args.source.name,
      'output':args.out.name,'sha256':sha,'synthetic_values':list(VALUES),
      'synthetic_total':TOTAL,'visual_improvement':'7 new review-only UI scenes',
      'audio':'REUSED_NOT_SEMANTICALLY_VERIFIED','new_japanese_tts':False,
      'captions':'ONSCREEN_SCENE_LABELS_NOT_SPEECH_TRANSCRIPT',
      'semantic_sync':'NOT_VERIFIED','rights':'SYNTHETIC_LOCAL',
      'quality':'HUMAN_REVIEW','publication':'NOT_APPROVED','auto_post':False}
    (args.out.parent/'manifest.json').write_text(
        json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(manifest,ensure_ascii=False,indent=2))
if __name__=='__main__': main()
