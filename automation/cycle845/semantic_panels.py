"""Cycle845: review-only semantic cards over a photo-slide MP4.

Free local dependencies: Pillow, OpenCV, numpy, ffmpeg. No uploads or posting.
Full local validation and render package is supplied separately for human review.
"""
from __future__ import annotations
import argparse
import json
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import cv2
import numpy as np

GENRES = {
    'ai_work':'#24DAC9', 'sales_business':'#F5BE62', 'beauty':'#D3A5FF',
    'romance':'#FF9FC6', 'saving':'#6FDCA0', 'career':'#FFB873',
    'wellness':'#9DDD83', 'science':'#86CEFF', 'travel_food':'#74D5E9',
    'product_comparison_lifestyle':'#FFAFD4',
}
POLICY = dict(review_only=True, publication_approved=False,
              automatic_posting=False, external_upload=False,
              source_rights_reviewed=False, contains_personal_data=False)
FRAMES = (89, 81, 79, 87, 86, 89, 77, 103)
W, H, X, Y = 900, 660, 90, 395
REGULAR='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
BOLD='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
SCENES = [
 ('START', 'AIに任せる前に', '仕事を1つ決める', ['手作業','AIで下書き','人が最終確認']),
 ('FIND', '毎日くり返す仕事', '候補を書き出す', ['毎朝の売上集計','定型メール','表への転記']),
 ('EXAMPLE', '完成形の見本', 'ゴールを先に共有', ['見出し','数値の表','要点3つ']),
 ('PROMPT', '目的と条件を明確に', 'AIへの依頼を整理', ['目的：日報の要約','条件：事実のみ','形式：箇条書き']),
 ('VERIFY', '出力は必ず確認', '間違いを見逃さない', ['数値','日付','固有名詞']),
 ('REFINE', '修正点は1つずつ', '改善を伝える', ['修正前：結論が最後','修正後：結論を先頭','再確認：事実に一致']),
 ('SAVE', '良い指示を保存', '次も再利用する', ['保存先：共有テンプレ','用途：日次レポート','更新：改善のたび']),
 ('TODAY', '今日から1つだけ', '小さく始めよう', ['作業を選ぶ','AIに依頼する','確認して保存']),
]

def validate(genre,manifest):
    if genre not in GENRES or len(GENRES)!=10: raise ValueError('Unsupported genre')
    if any(manifest.get(k) is not v for k,v in POLICY.items()):
        raise ValueError('Human review safety policy missing')
    if len(SCENES)!=8 or sum(FRAMES)!=691: raise AssertionError('Invalid scene plan')

def font(size,bold=False):
    return ImageFont.truetype(BOLD if bold else REGULAR,size)

def rr(d,box,fill,radius=24,outline=None,width=2):
    d.rounded_rectangle(box,radius=radius,fill=fill,outline=outline,width=width)

def tx(d,xy,s,size,color='#172B3B',bold=False):
    d.text(xy,s,font=font(size,bold),fill=color,stroke_width=0)

def board(index,genre='ai_work'):
    if not 0<=index<8: raise IndexError(index)
    accent=GENRES[genre]
    label,title,sub,items=SCENES[index]
    im=Image.new('RGBA',(W,H),(0,0,0,0));d=ImageDraw.Draw(im)
    rr(d,(5,5,895,655),'#F8FBFF',30,'#C9E2E6',3)
    rr(d,(20,20,880,146),'#0C2634',20)
    rr(d,(43,45,184,88),accent,14)
    tx(d,(59,49),label,23,'#07242C',True)
    tx(d,(208,31),title,45,'#FFFFFF',True)
    tx(d,(48,162),sub,33,'#223C4A',True)
    if index in (0,7):
        for j,s in enumerate(items):
            x=50+j*283
            rr(d,(x,250,x+257,510),'#EAF5F7',22,'#C8E0E3')
            rr(d,(x+67,274,x+190,396),accent,28)
            tx(d,(x+105,290),str(j+1),58,'#062733',True)
            tx(d,(x+24,432),s,25,'#16313D',True)
            if j<2: tx(d,(x+256,344),'→',36,accent,True)
    elif index in (1,4):
        for j,s in enumerate(items):
            y=240+j*112
            rr(d,(55,y,845,y+93),'#E8F3F6',18)
            rr(d,(78,y+24,123,y+70),accent,10)
            tx(d,(85,y+20),'✓',32,'#10303B',True)
            tx(d,(158,y+20),s,37,'#1D3641',True)
    elif index==2:
        rr(d,(55,230,845,534),'#EDF4F8',20)
        rr(d,(78,255,825,319),'#143545',12)
        tx(d,(105,261),'完成イメージ｜日次レポート',30,'#FFFFFF',True)
        for j,s in enumerate(items):
            y=340+j*59
            rr(d,(84,y,816,y+51),'#FFFFFF',9)
            tx(d,(105,y+6),s,27,'#163644',True)
            tx(d,(550,y+6),'確認する項目',24,'#3B6570')
    elif index==3:
        rr(d,(53,225,846,541),'#E7F1F6',20)
        for j,s in enumerate(items):
            y=254+j*93
            rr(d,(82,y,817,y+78),'#FFFFFF',14)
            rr(d,(99,y+16,111,y+60),accent,5)
            tx(d,(137,y+12),s,32,'#1B3D4B',True)
    elif index==5:
        for j,s in enumerate(items):
            y=234+j*112
            rr(d,(55,y,845,y+95),'#EDF4F7' if j!=1 else '#D7F7F0',18)
            tx(d,(83,y+21),s,31,'#193D48',True)
    elif index==6:
        rr(d,(95,236,805,530),'#E7F4F6',25)
        rr(d,(130,260,770,324),accent,13)
        tx(d,(158,268),'保存済みプロンプト',30,'#07313A',True)
        for j,s in enumerate(items):
            tx(d,(150,347+j*55),'✓  '+s,27,'#173946',True)
    rr(d,(51,568,849,617),'#DCEEF0',12)
    tx(d,(78,575),'DEMO • 画面は説明用の架空データです',22,'#466470')
    return im

def make_assets(out,genre,manifest):
    validate(genre,manifest)
    out=Path(out);out.mkdir(parents=True,exist_ok=True)
    paths=[]
    for i in range(8):
        p=out/f'panel_{i+1:02}.png'
        board(i,genre).save(p);paths.append(p)
    return paths

def render(source,output,panels):
    source,output=Path(source),Path(output)
    if len(panels)!=8 or not source.is_file(): raise ValueError('Missing inputs')
    imgs=[cv2.imread(str(p),cv2.IMREAD_UNCHANGED) for p in panels]
    if any(im is None or im.shape!=(H,W,4) for im in imgs):
        raise ValueError('Invalid panel resolution')
    cap=cv2.VideoCapture(str(source))
    if not cap.isOpened(): raise ValueError('Invalid MP4')
    if abs(cap.get(cv2.CAP_PROP_FPS)-30)>0.01 or int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))!=1080 or int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))!=1920:
        raise ValueError('Expected 1080x1920 at 30fps')
    output.parent.mkdir(parents=True,exist_ok=True)
    cmd=['ffmpeg','-hide_banner','-nostdin','-y','-loglevel','error',
         '-f','rawvideo','-pixel_format','bgr24','-video_size','1080x1920',
         '-framerate','30','-i','pipe:0','-i',str(source),
         '-map','0:v:0','-map','1:a:0','-c:v','libx264','-preset','veryfast',
         '-crf','21','-pix_fmt','yuv420p','-c:a','copy','-movflags','+faststart',str(output)]
    proc=subprocess.Popen(cmd,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
    boundaries=np.cumsum((0,)+FRAMES)
    count=0
    try:
        while True:
            ok,frame=cap.read()
            if not ok: break
            if count>=691: raise ValueError('Extra frames')
            idx=int(np.searchsorted(boundaries[1:],count,side='right'))
            local=count-int(boundaries[idx]);remaining=FRAMES[idx]-local-1
            opacity=min(0.97,(local+1)/9*0.97,(remaining+1)/9*0.97)
            im=imgs[idx];roi=frame[Y:Y+H,X:X+W]
            a=im[:,:,3:4].astype(np.float32)/255*opacity
            roi[:]=np.clip(roi*(1-a)+im[:,:,:3]*a,0,255).astype(np.uint8)
            proc.stdin.write(frame.tobytes());count+=1
        proc.stdin.close();err=proc.stderr.read().decode('utf-8','replace')
        if proc.wait(timeout=180)!=0: raise RuntimeError(err[-2000:])
        if count!=691: raise ValueError(f'Frame count: {count}')
    finally:
        cap.release()
        if proc.poll() is None:proc.kill()
    return count

if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('--source',required=True)
    ap.add_argument('--output',required=True)
    ap.add_argument('--assets',required=True)
    ap.add_argument('--manifest',required=True)
    ap.add_argument('--genre',default='ai_work')
    a=ap.parse_args()
    m=json.loads(Path(a.manifest).read_text(encoding='utf-8'))
    panels=make_assets(a.assets,a.genre,m)
    print(json.dumps({'frames':render(a.source,a.output,panels),'review_only':True}))
