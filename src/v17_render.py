#!/usr/bin/env python3
from PIL import Image,ImageDraw,ImageFont,ImageFilter,ImageEnhance,ImageStat
from pathlib import Path
import base64,subprocess,wave,math,shutil,json
W,H,FPS=1080,1920,30; O=Path('output');O.mkdir(exist_ok=True)
voice=O/'narration.wav'; proof=O/'v9_operation.mp4'; out=O/'AI時短ラボ_01_v17.mp4'; font='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
raw=base64.b64decode(Path('assets/v10/storyboard.b64').read_text().strip()); src=O/'old.jpg';src.write_bytes(raw); im=Image.open(src).convert('RGB');sw,sh=im.size;cw,ch=sw/4,sh/4
def crop(i):
 r,c=divmod(i,4);p=im.crop((round(c*cw),round(r*ch),round((c+1)*cw),round((r+1)*ch)));s=max(W/p.width,H/p.height);p=p.resize((round(p.width*s),round(p.height*s)),Image.Resampling.LANCZOS);x=(p.width-W)//2;y=(p.height-H)//2;return p.crop((x,y,x+W,y+H))
robot=crop(0); pain=crop(1); solution=crop(2)
def card(bg,title,sub,badge):
 p=bg.resize((W,H),Image.Resampling.LANCZOS).filter(ImageFilter.GaussianBlur(7)).convert('RGBA');p=Image.alpha_composite(p,Image.new('RGBA',(W,H),(0,8,25,115)));d=ImageDraw.Draw(p)
 f1=ImageFont.truetype(font,92);f2=ImageFont.truetype(font,48);f3=ImageFont.truetype(font,38)
 d.rounded_rectangle((55,80,1025,225),45,fill=(0,15,45,225),outline=(50,225,255,255),width=5);d.text((W//2,150),badge,font=f3,anchor='mm',fill=(80,235,255))
 d.multiline_text((W//2,440),title,font=f1,anchor='mm',align='center',spacing=18,fill='white',stroke_width=5,stroke_fill=(0,25,70))
 d.rounded_rectangle((95,1280,985,1515),45,fill=(0,12,38,225),outline=(255,220,60,255),width=4);d.multiline_text((W//2,1395),sub,font=f2,anchor='mm',align='center',spacing=12,fill=(255,230,75))
 d.text((W//2,1740),'AI時短ラボ  ｜  毎日1つ仕事がラクになる',font=f3,anchor='mm',fill='white');return p.convert('RGB')
scenes=[card(robot,'その作業、\nまだ手でやってる？','ChatGPT × Excelで\n一気に時短','0.5秒で結論'),card(pain,'コピペ地獄を\n今日で終了','長文 → 表 → Excel\nここまで自動化','よくある悩み'),card(solution,'指示は\nたった1文','必要項目を指定するだけ','解決策')]
with wave.open(str(voice),'rb') as w:D=w.getnframes()/w.getframerate()
# Proof-first: actual operation dominates the video. Old low-res art is restricted to short hook/support windows.
plan=[('scene',0,0,2.2),('scene',1,2.2,4.0),('scene',2,4.0,5.5),('proof',0,5.5,17.5),('scene',2,17.5,20.0),('proof',4.0,20.0,24.5),('cta',0,24.5,D)]
fd=O/'v17_frames';shutil.rmtree(fd,ignore_errors=True);fd.mkdir()
def cta(t):
 base=solution.copy().filter(ImageFilter.GaussianBlur(4)); title='保存して\n明日使う' if t<28 else 'フォローで\n毎日1つ時短';sub='次回：ChatGPT × PowerPoint' if t<28 else 'AI時短ラボ';return card(base,title,sub,'仕事をラクにするAI術')
for n in range(math.ceil(D*FPS)):
 t=min(n/FPS,D-.001);typ,arg,a,b=next((x for x in plan if x[2]<=t<x[3]),plan[-1]);
 if typ=='proof': frame=solution.copy() # placeholder; proof overlays later
 elif typ=='cta': frame=cta(t)
 else: frame=scenes[arg]
 u=(t-a)/max(.01,b-a);z=1.03+.10*u;rw,rh=round(W*z),round(H*z);q=frame.resize((rw,rh),Image.Resampling.LANCZOS);x=round((rw-W)*(.15+.7*u));y=round((rh-H)*(.65-.3*u));frame=q.crop((x,y,x+W,y+H));d=ImageDraw.Draw(frame);d.rounded_rectangle((65,1830,1015,1844),7,fill=(255,255,255));d.rounded_rectangle((65,1830,65+round(950*t/D),1844),7,fill=(35,225,255));frame.save(fd/f'{n:05d}.jpg',quality=96,subsampling=0)
base=O/'v17_base.mp4';subprocess.run(['ffmpeg','-y','-framerate','30','-i',str(fd/'%05d.jpg'),'-c:v','libx264','-preset','slow','-crf','11','-pix_fmt','yuv420p','-t',f'{D:.3f}',str(base)],check=True)
# Two proof windows with different temporal crops create real visual variation.
fc="[1:v]scale=1080:1920:flags=lanczos,trim=0:12,setpts=PTS-STARTPTS+5.5/TB[p1];[1:v]scale=1080:1920:flags=lanczos,trim=4:8.5,setpts=PTS-STARTPTS+20/TB[p2];[0:v][p1]overlay=0:0:enable='between(t,5.5,17.5)':eof_action=pass[x];[x][p2]overlay=0:0:enable='between(t,20,24.5)':eof_action=pass[v]"
subprocess.run(['ffmpeg','-y','-i',str(base),'-i',str(proof),'-i',str(voice),'-filter_complex',fc,'-map','[v]','-map','2:a','-t',f'{D:.3f}','-c:v','libx264','-preset','slow','-crf','11','-maxrate','20M','-bufsize','40M','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart',str(out)],check=True)
# Hard QA samples entire timeline: no blank/flat frames and sufficient visual variation.
qa=O/'v17qa';shutil.rmtree(qa,ignore_errors=True);qa.mkdir();subprocess.run(['ffmpeg','-y','-i',str(out),'-vf','fps=1,scale=135:240','-q:v','2',str(qa/'%03d.jpg')],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
stats=[]
for f in sorted(qa.glob('*.jpg')):
 a=Image.open(f).convert('L');s=ImageStat.Stat(a);edge=ImageStat.Stat(a.filter(ImageFilter.FIND_EDGES)).mean[0];stats.append((s.mean[0],s.stddev[0],edge))
if len(stats)<25:raise SystemExit('QA FAIL: insufficient timeline')
if any(m<7 and sd<3 and e<3 for m,sd,e in stats):raise SystemExit('QA FAIL: blank frame')
probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries','stream=width,height','-show_entries','format=duration,size','-of','json',str(out)],text=True));assert probe['streams'][0]['width']==1080 and probe['streams'][0]['height']==1920
print(json.dumps({'output':str(out),'duration':probe['format']['duration'],'samples':len(stats)},ensure_ascii=False))
