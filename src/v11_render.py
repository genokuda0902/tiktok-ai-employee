#!/usr/bin/env python3
from PIL import Image,ImageEnhance,ImageFilter
from pathlib import Path
import subprocess,wave,math,shutil
W,H,FPS=1080,1920,30
O=Path('output');O.mkdir(exist_ok=True)
board=Path('assets/v10/storyboard.jpg');voice=O/'narration.wav';op=O/'v9_operation.mp4';final=O/'AI時短ラボ_01_v11.mp4'
for p in (board,voice,op):
    if not p.exists(): raise SystemExit(f'missing {p}')
with wave.open(str(voice),'rb') as w: dur=w.getnframes()/w.getframerate()
im=Image.open(board).convert('RGB')
# remove footer, split exact 4x4 scene artwork
usable_h=int(im.height*.955);cw=im.width//4;ch=usable_h//4
panels=[im.crop((c*cw,r*ch,(c+1)*cw,(r+1)*ch)) for r in range(4) for c in range(4)]
# Explicit 33-second-style timeline; normalized to narration so there can never be a grey/blank tail.
weights=[2.0,2.0,2.0,2.0,2.0,2.0,2.0,2.0,4.0,4.0,4.0,2.0,2.0,2.0,1.0,1.0]
s=sum(weights);bounds=[0.0]
for x in weights:bounds.append(bounds[-1]+dur*x/s)
frames=O/'v11_frames';shutil.rmtree(frames,ignore_errors=True);frames.mkdir()
def cover(src,zoom,cx=.5,cy=.5):
 sw,sh=src.size;scale=max(W/sw,H/sh)*zoom
 rs=src.resize((round(sw*scale),round(sh*scale)),Image.Resampling.LANCZOS)
 maxx=max(0,rs.width-W);maxy=max(0,rs.height-H)
 l=int(maxx*cx);top=int(maxy*cy)
 return rs.crop((l,top,l+W,top+H))
N=math.ceil(dur*FPS)
for n in range(N):
 t=min(n/FPS,dur-1e-4)
 idx=next((i for i in range(16) if bounds[i]<=t<bounds[i+1]),15)
 u=(t-bounds[idx])/max(.001,bounds[idx+1]-bounds[idx])
 # upscale once with Lanczos, gentle sharpening/contrast, no repeated JPEG scaling chain
 z=1.035+.055*(u if idx%2==0 else 1-u)
 cx=.5+.025*math.sin(u*math.pi*2 + idx*.7)
 fr=cover(panels[idx],z,cx,.5)
 fr=ImageEnhance.Sharpness(fr).enhance(1.12)
 fr=ImageEnhance.Contrast(fr).enhance(1.035)
 fr.save(frames/f'{n:05d}.png',compress_level=2)
scene=O/'v11_scenes.mp4'
subprocess.run(['ffmpeg','-y','-framerate',str(FPS),'-i',str(frames/'%05d.png'),'-c:v','libx264','-preset','slow','-crf','14','-pix_fmt','yuv420p','-t',f'{dur:.3f}',str(scene)],check=True)
# Proof starts at its own zero when inserted; v10 incorrectly showed the proof stream at global timestamp.
start=bounds[3];end=bounds[8];proofdur=end-start
fc=(f"[1:v]scale=1080:1920:flags=lanczos,trim=start=0:end={proofdur:.3f},setpts=PTS-STARTPTS+{start:.3f}/TB[proof];"
    f"[0:v][proof]overlay=0:0:enable='between(t,{start:.3f},{end:.3f})':eof_action=pass[v]")
subprocess.run(['ffmpeg','-y','-i',str(scene),'-i',str(op),'-i',str(voice),'-filter_complex',fc,'-map','[v]','-map','2:a','-t',f'{dur:.3f}','-c:v','libx264','-preset','slow','-crf','14','-maxrate','12M','-bufsize','24M','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart',str(final)],check=True)
# hard technical QA: resolution, duration and no missing tail
subprocess.run(['ffprobe','-v','error','-show_entries','stream=width,height,codec_name','-show_entries','format=duration','-of','default=nw=1',str(final)],check=True)
print(final)
