#!/usr/bin/env python3
from PIL import Image,ImageEnhance,ImageStat,ImageFilter,ImageDraw,ImageFont
from pathlib import Path
import base64,subprocess,wave,math,shutil,json
W,H,FPS=1080,1920,30
O=Path('output'); O.mkdir(exist_ok=True)
voice=O/'narration.wav'; proof=O/'v9_operation.mp4'; out=O/'AI時短ラボ_01_v16.mp4'
raw=base64.b64decode(Path('assets/v10/storyboard.b64').read_text().strip())
master=O/'v16_master.jpg'; master.write_bytes(raw)
im=Image.open(master).convert('RGB'); sw,sh=im.size; cw,ch=sw/4,sh/4
font='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
def fit_panel(i):
 r,c=divmod(i,4); p=im.crop((round(c*cw),round(r*ch),round((c+1)*cw),round((r+1)*ch)))
 ratio=max(W/p.width,H/p.height); p=p.resize((round(p.width*ratio),round(p.height*ratio)),Image.Resampling.LANCZOS)
 x=(p.width-W)//2; y=(p.height-H)//2
 return ImageEnhance.Contrast(p.crop((x,y,x+W,y+H))).enhance(1.10)
panels=[fit_panel(i) for i in range(12)]
def branded(base,title,sub):
 p=base.copy().filter(ImageFilter.GaussianBlur(2)); ov=Image.new('RGBA',(W,H),(2,10,28,85)); p=Image.alpha_composite(p.convert('RGBA'),ov)
 d=ImageDraw.Draw(p); f1=ImageFont.truetype(font,76); f2=ImageFont.truetype(font,40); f3=ImageFont.truetype(font,52)
 d.rounded_rectangle((70,105,1010,330),radius=42,fill=(3,18,45,220),outline=(34,220,255,255),width=4)
 d.text((W//2,155),title,font=f1,anchor='mm',fill='white',stroke_width=2,stroke_fill=(0,40,90))
 d.text((W//2,270),sub,font=f2,anchor='mm',fill=(90,235,255))
 d.rounded_rectangle((130,1490,950,1690),radius=55,fill=(0,20,55,225),outline=(45,210,255,255),width=5)
 d.text((W//2,1550),'AI時短ラボ',font=f3,anchor='mm',fill='white')
 d.text((W//2,1630),'明日会社で使えるAI仕事術を30秒で',font=f2,anchor='mm',fill=(255,225,70))
 return p.convert('RGB')
# Never use the historically broken final storyboard row. Build final scenes from known-good art + fresh branded overlays.
scenes=panels+[branded(panels[2],'応用は無限','要約・メール・分析・資料作成'),branded(panels[0],'次回予告','ChatGPT × PowerPoint'),branded(panels[2],'役に立ったら保存','毎日1つ、仕事がラクになる'),branded(panels[0],'フォローしてね','AIで仕事をもっと自由に')]
with wave.open(str(voice),'rb') as w: D=w.getnframes()/w.getframerate()
weights=[1.35,1.25,1.2,1.05,1,1,1,1.05,1.55,1.35,1.25,1.0,.9,.9,.85,.9]
S=sum(weights); bounds=[0.0]
for q in weights: bounds.append(bounds[-1]+D*q/S)
fd=O/'v16_frames'; shutil.rmtree(fd,ignore_errors=True); fd.mkdir()
for n in range(math.ceil(D*FPS)):
 t=min(n/FPS,D-.001); idx=next((i for i in range(16) if bounds[i]<=t<bounds[i+1]),15); u=(t-bounds[idx])/max(.01,bounds[idx+1]-bounds[idx]); p=scenes[idx]
 z=1.05+0.13*(u if idx%2==0 else 1-u); rw,rh=round(W*z),round(H*z); q=p.resize((rw,rh),Image.Resampling.LANCZOS)
 mx,my=rw-W,rh-H; x=round(mx*(.1+.8*u)) if idx%3==0 else round(mx*(.9-.8*u)) if idx%3==1 else mx//2; y=round(my*(.15+.7*u)) if idx%2==0 else round(my*(.85-.7*u)); frame=q.crop((x,y,x+W,y+H))
 # subtle progress bar keeps motion visible even on held artwork
 dr=ImageDraw.Draw(frame); dr.rounded_rectangle((70,1815,1010,1830),radius=7,fill=(255,255,255,80)); dr.rounded_rectangle((70,1815,70+round(940*(t/D)),1830),radius=7,fill=(45,220,255))
 frame.save(fd/f'{n:05d}.jpg',quality=96,subsampling=0)
base=O/'v16_visual.mp4'
subprocess.run(['ffmpeg','-y','-framerate',str(FPS),'-i',str(fd/'%05d.jpg'),'-c:v','libx264','-preset','slow','-crf','12','-pix_fmt','yuv420p','-t',f'{D:.3f}',str(base)],check=True)
start,end=bounds[3],bounds[8]; pd=end-start
# Overlay proof only inside its window; base video remains underneath for the entire duration.
fc=f"[1:v]scale=1080:1920:flags=lanczos,trim=start=0:end={pd:.3f},setpts=PTS-STARTPTS[pr];[0:v][pr]overlay=0:0:enable='between(t,{start:.3f},{end:.3f})':eof_action=pass:shortest=0[v]"
# Delay proof input to the intended start without shifting the base timeline.
subprocess.run(['ffmpeg','-y','-i',str(base),'-itsoffset',f'{start:.3f}','-i',str(proof),'-i',str(voice),'-filter_complex',fc,'-map','[v]','-map','2:a','-t',f'{D:.3f}','-c:v','libx264','-preset','slow','-crf','12','-maxrate','18M','-bufsize','36M','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart',str(out)],check=True)
probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries','stream=width,height,codec_name','-show_entries','format=duration,size','-of','json',str(out)],text=True)); st=probe['streams'][0]; dur=float(probe['format']['duration'])
assert st['width']==1080 and st['height']==1920 and dur>=D-.15
qa=O/'v16_tailqa'; shutil.rmtree(qa,ignore_errors=True); qa.mkdir(); subprocess.run(['ffmpeg','-y','-sseof','-8','-i',str(out),'-vf','fps=1,scale=270:480','-q:v','2',str(qa/'%02d.jpg')],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
stats=[]
for f in sorted(qa.glob('*.jpg')):
 a=Image.open(f).convert('L'); s=ImageStat.Stat(a); edge=ImageStat.Stat(a.filter(ImageFilter.FIND_EDGES)).mean[0]; stats.append({'mean':round(s.mean[0],1),'std':round(s.stddev[0],1),'edge':round(edge,1)})
if len(stats)<5: raise SystemExit('QA FAIL: insufficient tail frames')
blank=sum(1 for s in stats if s['mean']<8 and s['std']<3 and s['edge']<3)
if blank: raise SystemExit('QA FAIL: blank tail frame detected')
print(json.dumps({'output':str(out),'duration':dur,'tail_stats':stats,'blank_frames':blank},ensure_ascii=False))
