"""Cycle846: photo-first semantic lower thirds. Local review-only renderer."""
from __future__ import annotations
import argparse
import json
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import cv2

W,H,FPS=1080,1920,30
SCENE_FRAMES=(89,81,79,87,86,89,77,103)
GENRES={
 'ai_work':'#26D9C9','sales_business':'#F4C15D','beauty':'#D7A6FF',
 'romance':'#FF91C6','saving':'#64D69C','career':'#FFB36E',
 'wellness':'#A0D977','science':'#7ECFFF','travel_food':'#6FD7DF',
 'product_comparison_lifestyle':'#F9A7CF'}
POLICY={'review_only':True,'publication_approved':False,'automatic_posting':False,
 'external_upload':False,'source_rights_reviewed':False,'contains_personal_data':False}
SCENES=[
 ('まず1つ選ぶ','毎日くり返す作業から'),
 ('候補を探す','集計・転記・定型文'),
 ('完成例を見せる','出力のゴールを共有'),
 ('条件をそろえる','目的・形式・禁止事項'),
 ('事実を照合','数字と日付は人が確認'),
 ('一度に1点直す','修正内容を具体的に'),
 ('良い指示を保存','再利用できる型にする'),
 ('今日1つ試す','最終確認してから使う')]
FONT='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
FONT_R='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
PANEL_X,PANEL_Y,PANEL_W,PANEL_H=110,1090,860,132
PREVIOUS_PANEL_AREA=900*660

def validate(genre,manifest):
    if genre not in GENRES or len(GENRES)!=10: raise ValueError('Unsupported genre')
    if any(manifest.get(k) is not v for k,v in POLICY.items()): raise ValueError('Unsafe manifest')
    if len(SCENES)!=8 or sum(SCENE_FRAMES)!=691: raise AssertionError('Scene timing changed')
    if not (PANEL_Y>=1080 and PANEL_Y+PANEL_H<=1230): raise AssertionError('Panel leaves existing example banner')
    if PANEL_W*PANEL_H>=PREVIOUS_PANEL_AREA*.3: raise AssertionError('Photo visibility regressed')

def make_panel(i,genre='ai_work'):
    if not 0<=i<8: raise IndexError(i)
    accent=GENRES[genre]
    im=Image.new('RGBA',(PANEL_W,PANEL_H),(0,0,0,0))
    d=ImageDraw.Draw(im)
    d.rounded_rectangle((2,3,PANEL_W-3,PANEL_H-4),radius=25,
                        fill=(8,27,38,250),outline=(58,94,106,250),width=3)
    d.rounded_rectangle((0,4,12,PANEL_H-5),radius=5,fill=accent)
    d.rounded_rectangle((28,21,104,62),radius=15,fill=accent)
    d.text((44,22),f'{i+1:02}',font=ImageFont.truetype(FONT,25),fill='#0C2934')
    d.text((126,13),SCENES[i][0],font=ImageFont.truetype(FONT,43),fill='#FFFFFF')
    d.text((128,77),SCENES[i][1],font=ImageFont.truetype(FONT_R,26),fill='#C7E1E7')
    return np.array(im)

def render(src,dst,genre,manifest):
    validate(genre,manifest)
    cap=cv2.VideoCapture(str(src))
    if not cap.isOpened(): raise RuntimeError('Source video cannot be opened')
    if (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))!=(W,H):
        raise RuntimeError('Source resolution mismatch')
    patches=[make_panel(i,genre) for i in range(8)]
    cmd=['ffmpeg','-hide_banner','-loglevel','error','-y',
         '-f','rawvideo','-pix_fmt','bgr24','-s',f'{W}x{H}','-r',str(FPS),'-i','pipe:0',
         '-i',str(src),'-map','0:v:0','-map','1:a:0',
         '-c:v','libx264','-preset','ultrafast','-crf','19','-pix_fmt','yuv420p',
         '-c:a','copy','-movflags','+faststart',str(dst)]
    proc=subprocess.Popen(cmd,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
    bounds=np.cumsum((0,*SCENE_FRAMES))
    n=0
    try:
        while True:
            ok,frame=cap.read()
            if not ok: break
            if n>=691: raise RuntimeError('Unexpected extra frames')
            scene=int(np.searchsorted(bounds[1:],n,side='right'))
            within=n-int(bounds[scene]);remain=SCENE_FRAMES[scene]-within
            strength=min(1.,(within+1)/10.,remain/9.)
            patch=patches[scene]
            a=(patch[:,:,3:4].astype(np.float32)/255.)*strength
            roi=frame[PANEL_Y:PANEL_Y+PANEL_H,PANEL_X:PANEL_X+PANEL_W]
            frame[PANEL_Y:PANEL_Y+PANEL_H,PANEL_X:PANEL_X+PANEL_W]=(
                roi.astype(np.float32)*(1-a)+patch[:,:,:3][:,:,::-1]*a).astype(np.uint8)
            proc.stdin.write(frame.tobytes())
            n+=1
        proc.stdin.close()
        err=proc.stderr.read().decode('utf8','replace')
        if proc.wait(): raise RuntimeError('FFmpeg failed: '+err[-1000:])
        if n!=691: raise RuntimeError(f'Unexpected frame count {n}')
        return {'frames':n,'photo_footprint_reduction':round(1-PANEL_W*PANEL_H/PREVIOUS_PANEL_AREA,4)}
    finally:
        cap.release()
        if proc.poll() is None: proc.kill()

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--src',required=True);p.add_argument('--out',required=True)
    p.add_argument('--genre',default='ai_work');p.add_argument('--manifest',required=True)
    a=p.parse_args()
    print(json.dumps(render(Path(a.src),Path(a.out),a.genre,json.loads(Path(a.manifest).read_text())),ensure_ascii=False))
