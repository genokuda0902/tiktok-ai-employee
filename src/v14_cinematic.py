#!/usr/bin/env python3
from PIL import Image,ImageEnhance,ImageFilter
from pathlib import Path
import base64,subprocess,wave,math,shutil
W,H,FPS=1080,1920,30; O=Path('output');O.mkdir(exist_ok=True)
voice=O/'narration.wav'; proof=O/'v9_operation.mp4'; out=O/'AI時短ラボ_01_v14.mp4'
# v14 intentionally removes all programmatically drawn mascot/UI. Every non-proof shot comes from the approved cinematic storyboard asset.
src=Path('assets/v10/storyboard.b64')
raw=base64.b64decode(src.read_text().strip()); master=O/'v14_master.jpg'; master.write_bytes(raw)
im=Image.open(master).convert('RGB'); sw,sh=im.size; cw,ch=sw/4,sh/4
panels=[]
for i in range(16):
 r,c=divmod(i,4); p=im.crop((round(c*cw),round(r*ch),round((c+1)*cw),round((r+1)*ch)))
 # cinematic cover + mild cleanup; no synthetic mascot redraw
 ratio=max(W/p.width,H/p.height); p=p.resize((round(p.width*ratio),round(p.height*ratio)),Image.Resampling.LANCZOS); x=(p.width-W)//2;y=(p.height-H)//2;p=p.crop((x,y,x+W,y+H));p=ImageEnhance.Contrast(p).enhance(1.04);p=ImageEnhance.Sharpness(p).enhance(1.15);panels.append(p)
with wave.open(str(voice),'rb') as w:D=w.getnframes()/w.getframerate()
# visual rhythm modeled after reference: fast hook/proof, longer before-after/use cases, short CTA
weights=[1.5,1.5,1.4,1.1,1.0,1.0,1.0,1.1,2.0,1.6,1.5,1.1,1.0,1.0,.8,.9]; S=sum(weights); bounds=[0]
for q in weights:bounds.append(bounds[-1]+D*q/S)
fd=O/'v14_frames';shutil.rmtree(fd,ignore_errors=True);fd.mkdir()
for n in range(math.ceil(D*FPS)):
 t=min(n/FPS,D-.001); idx=next((i for i in range(16) if bounds[i]<=t<bounds[i+1]),15);u=(t-bounds[idx])/max(.01,bounds[idx+1]-bounds[idx]);p=panels[idx]
 # alternating push-in/pull-out/side drift so every shot has camera motion
 z=1.04+(.07*u if idx%3!=1 else .07*(1-u)); rw,rh=round(W*z),round(H*z);q=p.resize((rw,rh),Image.Resampling.LANCZOS); maxx=rw-W;maxy=rh-H
 if idx%3==0:x=round(maxx*u)
 elif idx%3==1:x=round(maxx*(1-u))
 else:x=maxx//2
 y=round(maxy*(.25+.5*u)) if idx%2==0 else round(maxy*(.75-.5*u));q.crop((x,y,x+W,y+H)).save(fd/f'{n:05d}.jpg',quality=94,subsampling=0)
base=O/'v14_visual.mp4';subprocess.run(['ffmpeg','-y','-framerate','30','-i',str(fd/'%05d.jpg'),'-c:v','libx264','-preset','slow','-crf','14','-pix_fmt','yuv420p','-t',f'{D:.3f}',str(base)],check=True)
# Real operation proof replaces storyboard demo panels while retaining cinematic cuts before/after.
start,end=bounds[3],bounds[8];pd=end-start
fc=f"[1:v]scale=1080:1920:flags=lanczos,trim=0:{pd:.3f},setpts=PTS-STARTPTS+{start:.3f}/TB[proof];[0:v][proof]overlay=0:0:enable='between(t,{start:.3f},{end:.3f})':eof_action=pass[v]"
subprocess.run(['ffmpeg','-y','-i',str(base),'-i',str(proof),'-i',str(voice),'-filter_complex',fc,'-map','[v]','-map','2:a','-t',f'{D:.3f}','-c:v','libx264','-preset','slow','-crf','14','-maxrate','14M','-bufsize','28M','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart',str(out)],check=True)
print(out)
