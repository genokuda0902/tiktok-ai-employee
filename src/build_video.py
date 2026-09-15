#!/usr/bin/env python3
from pathlib import Path
import subprocess,wave,json,math,struct
O=Path('output'); A=O/'narration.wav'; T=O/'narration_timing.json'; V=O/'AI時短ラボ_01_完成版.mp4'; S=O/'ui_sfx.wav'; CAP=O/'operation_demo.mp4'; ROB=Path('assets/robot/presenter.png')
F='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
for p in (A,T,CAP,ROB):
 if not p.exists(): raise SystemExit(f'V8 missing required asset: {p}')
with wave.open(str(A),'rb') as w:D=w.getnframes()/w.getframerate()
sr=44100; buf=bytearray(int(sr*(D+.5))*2)
for c,hz in [(0.1,1180),(2.2,760),(5.8,980),(9,1250),(14,820),(21,1050),(27,760)]:
 for j in range(int(.07*sr)):
  x=j/sr; v=math.sin(2*math.pi*hz*x)*math.exp(-44*x)*.12; i=(int(c*sr)+j)*2
  if i+1<len(buf): struct.pack_into('<h',buf,i,int(v*32767))
with wave.open(str(S),'wb') as w:w.setparams((1,2,sr,len(buf)//2,'NONE',''));w.writeframes(buf)
timing=json.loads(T.read_text(encoding='utf-8')); subs=[]
for i,x in enumerate(timing):
 a,b=x['start'],x['end']; txt=x['text'].replace("'","’").replace(':','\\:').replace(',','，'); size=45 if len(txt)>20 else 57; col='0xffe45e' if i in (0,4,len(timing)-1) else 'white'
 subs += [f"drawbox=x=55:y=1450:w=970:h=190:color=black@0.78:t=fill:enable='between(t,{a},{b})'",f"drawtext=fontfile={F}:text='{txt}':fontcolor={col}:fontsize={size}:x=(w-text_w)/2:y=1505:enable='between(t,{a},{b})'"]
subs += [f"drawtext=fontfile={F}:text='AI時短ラボ':fontcolor=0x67e8f9:fontsize=30:x=50:y=58",f"drawbox=x=0:y=1880:w='min(1080,1080*t/{D:.3f})':h=9:color=0x38d9ff:t=fill"]
fc=f"[0:v]scale=1080:1920,trim=duration={D:.3f},setpts=PTS-STARTPTS[bg];[1:v]scale=940:-2,trim=duration=10,setpts=PTS-STARTPTS[demo];[2:v]scale=430:-2,format=rgba[p];[bg][demo]overlay=x=70:y=180:enable='between(t,5.5,18.5)'[b1];[b1][p]overlay=x='40+8*sin(t*3)':y='280+8*cos(t*3.5)':enable='between(t,0,5.5)+between(t,18.5,21.5)+gte(t,27)'[b2];[b2]{','.join(subs)}[v];[3:a]volume=1[voice];[4:a]volume=.28[fx];[voice][fx]amix=inputs=2:duration=first:normalize=0[a]"
cmd=['ffmpeg','-y','-f','lavfi','-i',f'color=c=0x050914:s=1080x1920:r=30:d={D+.2:.3f}','-stream_loop','-1','-i',str(CAP),'-loop','1','-i',str(ROB),'-i',str(A),'-i',str(S),'-filter_complex',fc,'-map','[v]','-map','[a]','-t',f'{D:.3f}','-c:v','libx264','-preset','ultrafast','-crf','19','-pix_fmt','yuv420p','-c:a','aac','-b:a','160k','-movflags','+faststart',str(V)]
subprocess.run(cmd,check=True)
print(V)
