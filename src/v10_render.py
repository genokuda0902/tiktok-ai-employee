#!/usr/bin/env python3
from PIL import Image,ImageDraw,ImageFont,ImageEnhance
from pathlib import Path
import subprocess,wave,math
W,H,FPS=1080,1920,30
O=Path('output'); O.mkdir(exist_ok=True)
board=Path('assets/v10/storyboard.jpg'); voice=O/'narration.wav'; op=O/'v9_operation.mp4'; final=O/'AI時短ラボ_01_v10.mp4'
for p in (board,voice,op):
    if not p.exists(): raise SystemExit(f'missing {p}')
with wave.open(str(voice),'rb') as w: dur=w.getnframes()/w.getframerate()
im=Image.open(board).convert('RGB')
# generated reference is a 4x4 storyboard plus a small footer; crop only the 16 scene cells
usable_h=int(im.height*0.955); cw=im.width//4; ch=usable_h//4
panels=[]
for r in range(4):
    for c in range(4):
        x0=c*cw; y0=r*ch
        panels.append(im.crop((x0,y0,x0+cw,y0+ch)))
# 16 scene timing: strong hook then fast visual changes, matched to narration duration
weights=[2,2,2,2,2,2,2,2,4,4,4,2,2,2,1,1]
s=sum(weights); bounds=[0]
for wgt in weights: bounds.append(bounds[-1]+dur*wgt/s)
frames=O/'v10_frames'; frames.mkdir(exist_ok=True)
def cover(src,zoom=1.0):
    sw,sh=src.size; scale=max(W/sw,H/sh)*zoom
    x=src.resize((int(sw*scale),int(sh*scale)),Image.Resampling.LANCZOS)
    l=(x.width-W)//2; t=(x.height-H)//2
    return x.crop((l,t,l+W,t+H))
for n in range(int(dur*FPS)):
    t=n/FPS
    idx=max(0,min(15,next((i for i in range(16) if bounds[i]<=t<bounds[i+1]),15)))
    local=(t-bounds[idx])/max(.01,bounds[idx+1]-bounds[idx])
    # cinematic push/pull and slight horizontal drift; every scene is a designed visual, never a blank slide
    z=1.02+0.075*(local if idx%2==0 else 1-local)
    fr=cover(panels[idx],z)
    # subtle motion crop
    shift=int(14*math.sin(local*math.pi*2))
    if shift:
        canvas=Image.new('RGB',(W,H),'black'); canvas.paste(fr,(shift,0)); fr=canvas.crop((0,0,W,H))
    fr.save(frames/f'{n:05d}.jpg',quality=91)
# render designed scenes
scene=O/'v10_scenes.mp4'
subprocess.run(['ffmpeg','-y','-framerate',str(FPS),'-i',str(frames/'%05d.jpg'),'-c:v','libx264','-crf','17','-pix_fmt','yuv420p',str(scene)],check=True)
# During the central demonstration, blend in the real animated operation proof at full screen for credibility.
# Keep designed visual intro/outro, use operation motion in the middle, and preserve narration.
start=bounds[3]; end=bounds[8]
fc=(f"[0:v]setsar=1[design];[1:v]scale=1080:1920,setsar=1[proof];"
    f"[design][proof]overlay=0:0:enable='between(t,{start:.3f},{end:.3f})'[v]")
subprocess.run(['ffmpeg','-y','-i',str(scene),'-i',str(op),'-i',str(voice),'-filter_complex',fc,'-map','[v]','-map','2:a','-t',f'{dur:.3f}','-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p','-c:a','aac','-b:a','160k','-movflags','+faststart',str(final)],check=True)
print(final)
