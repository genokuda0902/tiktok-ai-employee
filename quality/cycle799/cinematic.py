#!/usr/bin/env python3
"""cycle799: mobile-first cinematic reframe for 8-scene Japanese image-slide MP4.

Requires an existing 1080x1920 / 30fps / 429-frame MP4. Source audio is
stream-copied. Does not license inherited assets. No network or publishing.
"""
import argparse, bisect, json, subprocess
from pathlib import Path
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

WIDTH, HEIGHT, FPS = 1080, 1920, 30
SCENES = (57, 63, 58, 63, 40, 47, 48, 53)
PANEL = (35, 430, 1010, 1050)
SOURCE_VISUAL = (49, 141, 961, 810)
GENRES = {
 'ai_work':'#9B90FF','beauty':'#E5ACD7','love_psychology':'#C0A2FF',
 'money_saving':'#6BE1B8','sales_business':'#58C5F6','career':'#83C5F9',
 'health_life':'#6EE7BE','science':'#39E7D3','travel_food':'#70D6EA',
 'product_life':'#C6A0F5'
}
TAKEAWAYS = ('小さなコンピューター','手のひらサイズ','HDMIで画面へ','電源・画面・入力',
             'GPIO → 抵抗 → LED → GND','入力 → 処理 → 出力','一行から始める','保存して試してみる')
FONT = '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'

def hex_bgr(color):
    return tuple(int(color[i:i+2],16) for i in (5,3,1))

def scene_at(frame):
    if not 0 <= frame < sum(SCENES): raise ValueError('Frame outside video')
    return bisect.bisect_right(np.cumsum(SCENES),frame)

def make_overlay(idx,genre):
    accent = GENRES[genre]
    im=Image.new('RGBA',(PANEL[2],PANEL[3]),(0,0,0,0))
    d=ImageDraw.Draw(im)
    ft=lambda s: ImageFont.truetype(FONT,s)
    d.rounded_rectangle((22,18,990,1029),radius=27,outline=accent,width=3)
    d.rounded_rectangle((39,28,280,99),radius=18,fill=(6,31,45,235))
    d.text((59,42),f'図解  {idx+1:02d} / 08',font=ft(34),fill='white')
    d.rounded_rectangle((35,903,975,1014),radius=20,fill=(4,21,35,248))
    d.text((62,928),TAKEAWAYS[idx],font=ft(48 if len(TAKEAWAYS[idx])<=15 else 40),fill='white')
    d.rounded_rectangle((310,54,944,66),radius=6,fill=(60,88,98,240))
    d.rounded_rectangle((310,54,310+round(634*(idx+1)/8),66),radius=6,fill=accent)
    return np.asarray(im)

def reframe(panel,idx,local,genre,overlay):
    if panel.shape[:2] != (PANEL[3],PANEL[2]):raise ValueError('Panel size mismatch')
    accent=hex_bgr(GENRES[genre]);out=np.empty_like(panel)
    for y in range(out.shape[0]):
        t=y/out.shape[0]
        out[y,:]=(int(9+5*t),int(22+8*t),int(34+7*t))
    x1,y1,x2,y2=SOURCE_VISUAL
    visual=panel[y1:y2,x1:x2]
    progress=local/max(1,SCENES[idx]-1)
    zoom=1.0+0.015*progress
    cw=int(visual.shape[1]/zoom);ch=int(visual.shape[0]/zoom)
    x=(visual.shape[1]-cw)//2;y=(visual.shape[0]-ch)//2
    visual=visual[y:y+ch,x:x+cw]
    big=cv2.resize(visual,(940,770),interpolation=cv2.INTER_CUBIC)
    out[115:885,35:975]=big
    for j in range(120):
        yy=765+j;a=(j/119)**1.7*0.45
        out[yy,35:975]=cv2.addWeighted(out[yy,35:975],1-a,np.full((940,3),(5,17,28),dtype=np.uint8),a,0)
    cv2.rectangle(out,(35,115),(975,885),accent,2,cv2.LINE_AA)
    bgra=cv2.cvtColor(out,cv2.COLOR_BGR2BGRA)
    alpha=overlay[:,:,3:4].astype(np.float32)/255.0
    bgra[:,:,:3]=(bgra[:,:,:3].astype(np.float32)*(1-alpha)+overlay[:,:,:3][:,:,::-1]*alpha).astype(np.uint8)
    return cv2.cvtColor(bgra,cv2.COLOR_BGRA2BGR)

def render(source,target,genre='science'):
    if genre not in GENRES:raise ValueError('Unsupported genre')
    cap=cv2.VideoCapture(str(source))
    if not cap.isOpened():raise RuntimeError('Source cannot be opened')
    if (round(cap.get(3)),round(cap.get(4)))!=(WIDTH,HEIGHT) or abs(cap.get(5)-FPS)>0.1:
        raise ValueError('Expected 1080x1920 30fps source')
    if int(cap.get(cv2.CAP_PROP_FRAME_COUNT))!=sum(SCENES):
        raise ValueError('Expected 429 frames and 8 scenes')
    overlays=[make_overlay(i,genre) for i in range(8)]
    target=Path(target);target.parent.mkdir(parents=True,exist_ok=True)
    cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-f','rawvideo','-pix_fmt','bgr24',
         '-s',f'{WIDTH}x{HEIGHT}','-r',str(FPS),'-i','pipe:0','-i',str(source),
         '-map','0:v:0','-map','1:a:0','-c:v','libx264','-preset','ultrafast','-crf','19',
         '-pix_fmt','yuv420p','-c:a','copy','-movflags','+faststart',str(target)]
    proc=subprocess.Popen(cmd,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
    count=0;bounds=np.cumsum(SCENES)
    try:
        while True:
            ok,frame=cap.read()
            if not ok:break
            idx=bisect.bisect_right(bounds,count)
            if idx>=8:raise RuntimeError('Extra frame')
            start=0 if idx==0 else bounds[idx-1]
            x,y,w,h=PANEL
            frame[y:y+h,x:x+w]=reframe(frame[y:y+h,x:x+w],idx,count-start,genre,overlays[idx])
            proc.stdin.write(frame.tobytes());count+=1
    except Exception:
        proc.kill();raise
    finally:
        cap.release()
        if proc.stdin:proc.stdin.close()
    err=proc.stderr.read().decode('utf-8','replace');ret=proc.wait()
    if ret:raise RuntimeError(f'FFmpeg failed: {err[-500:]}')
    if count!=429:raise RuntimeError(f'Wrong frame count {count}')
    return {'frames':count,'genre':genre,'output':str(target)}

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--source',type=Path,required=True)
    ap.add_argument('--output',type=Path,required=True)
    ap.add_argument('--genre',choices=list(GENRES),default='science')
    args=ap.parse_args();print(json.dumps(render(args.source,args.output,args.genre),ensure_ascii=False))
