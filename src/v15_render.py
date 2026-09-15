#!/usr/bin/env python3
from PIL import Image,ImageEnhance,ImageStat,ImageFilter
from pathlib import Path
import base64,subprocess,wave,math,shutil,json
W,H,FPS=1080,1920,30
O=Path('output'); O.mkdir(exist_ok=True)
voice=O/'narration.wav'; proof=O/'v9_operation.mp4'; out=O/'AI時短ラボ_01_v15.mp4'
raw=base64.b64decode(Path('assets/v10/storyboard.b64').read_text().strip())
master=O/'v15_master.jpg'; master.write_bytes(raw)
im=Image.open(master).convert('RGB'); sw,sh=im.size; cw,ch=sw/4,sh/4
panels=[]
for i in range(16):
 r,c=divmod(i,4); p=im.crop((round(c*cw),round(r*ch),round((c+1)*cw),round((r+1)*ch)))
 ratio=max(W/p.width,H/p.height); p=p.resize((round(p.width*ratio),round(p.height*ratio)),Image.Resampling.LANCZOS)
 x=(p.width-W)//2; y=(p.height-H)//2; p=p.crop((x,y,x+W,y+H))
 p=ImageEnhance.Contrast(p).enhance(1.08); p=ImageEnhance.Sharpness(p).enhance(1.20); panels.append(p)
with wave.open(str(voice),'rb') as w: D=w.getnframes()/w.getframerate()
weights=[1.35,1.25,1.2,1.05,1,1,1,1.05,1.55,1.35,1.25,1.0,.9,.9,.8,.85]
S=sum(weights); bounds=[0.0]
for q in weights: bounds.append(bounds[-1]+D*q/S)
fd=O/'v15_frames'; shutil.rmtree(fd,ignore_errors=True); fd.mkdir()
for n in range(math.ceil(D*FPS)):
 t=min(n/FPS,D-.001); idx=next((i for i in range(16) if bounds[i]<=t<bounds[i+1]),15)
 u=(t-bounds[idx])/max(.01,bounds[idx+1]-bounds[idx]); p=panels[idx]
 z=1.07+0.10*(u if idx%2==0 else 1-u); rw,rh=round(W*z),round(H*z); q=p.resize((rw,rh),Image.Resampling.LANCZOS)
 mx,my=rw-W,rh-H; x=round(mx*(.15+.7*u)) if idx%3==0 else round(mx*(.85-.7*u)) if idx%3==1 else mx//2
 y=round(my*(.2+.55*u)) if idx%2==0 else round(my*(.75-.55*u)); frame=q.crop((x,y,x+W,y+H))
 frame.save(fd/f'{n:05d}.jpg',quality=96,subsampling=0)
base=O/'v15_visual.mp4'
subprocess.run(['ffmpeg','-y','-framerate',str(FPS),'-i',str(fd/'%05d.jpg'),'-c:v','libx264','-preset','slow','-crf','13','-pix_fmt','yuv420p','-t',f'{D:.3f}',str(base)],check=True)
start,end=bounds[3],bounds[8]; pd=end-start
fc=f"[1:v]scale=1080:1920:flags=lanczos,trim=start=0:end={pd:.3f},setpts=PTS-STARTPTS,tpad=stop_mode=clone:stop_duration=1[pr];[pr]setpts=PTS+{start:.3f}/TB[proof];[0:v][proof]overlay=0:0:enable='between(t,{start:.3f},{end:.3f})':eof_action=pass[v]"
subprocess.run(['ffmpeg','-y','-i',str(base),'-i',str(proof),'-i',str(voice),'-filter_complex',fc,'-map','[v]','-map','2:a','-t',f'{D:.3f}','-c:v','libx264','-preset','slow','-crf','13','-maxrate','16M','-bufsize','32M','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart',str(out)],check=True)
probe=subprocess.check_output(['ffprobe','-v','error','-show_entries','stream=width,height,codec_name','-show_entries','format=duration,size','-of','json',str(out)],text=True)
meta=json.loads(probe); st=meta['streams'][0]; dur=float(meta['format']['duration'])
assert st['width']==1080 and st['height']==1920 and dur>=D-.15
# Tail QA: reject actual black/empty output, but allow intentional low-contrast cinematic artwork.
qa=O/'v15_tailqa'; shutil.rmtree(qa,ignore_errors=True); qa.mkdir()
subprocess.run(['ffmpeg','-y','-sseof','-8','-i',str(out),'-vf','fps=1,scale=270:480','-q:v','2',str(qa/'%02d.jpg')],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
stats=[]
for f in sorted(qa.glob('*.jpg')):
 a=Image.open(f).convert('L')
 mean=ImageStat.Stat(a).mean[0]; std=ImageStat.Stat(a).stddev[0]
 edge=ImageStat.Stat(a.filter(ImageFilter.FIND_EDGES)).mean[0]
 stats.append({'mean':round(mean,1),'std':round(std,1),'edge':round(edge,1)})
if len(stats)<5: raise SystemExit('QA FAIL: insufficient tail frames')
# True failure means several nearly-black frames with almost no spatial detail.
blank=sum(1 for s in stats if s['mean']<8 and s['std']<3 and s['edge']<3)
if blank>=3: raise SystemExit('QA FAIL: genuinely blank/black tail')
print(json.dumps({'output':str(out),'duration':dur,'tail_stats':stats,'blank_frames':blank},ensure_ascii=False))
