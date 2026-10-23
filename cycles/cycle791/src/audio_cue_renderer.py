"""Cycle791: estimate Japanese caption boundaries from 20ms audio RMS.
Technical heuristic only: NOT forced alignment or pronunciation verification.
Inherited media is human-review only; no paid APIs or automatic posting.
"""
from __future__ import annotations
import argparse, json, re, subprocess, wave
from pathlib import Path
import numpy as np

FPS=30
FRAMES=(60,60,60,64,39,48,48,50)
WORDS=(('この','基板、'),('実は','パソコン。'),('手のひら','サイズ、'),
 ('でも','本格派。'),('画面に','つなげば、'),('操作','できる。'),
 ('必要','なのは、'),('三つの','接続。'),('LED','も'),('光らせ','られる。'),
 ('入力、','処理、'),('出力。',),('最初','は、'),('たった','一行。'),
 ('保存','して、'),('あとで','試そう。'))
SPLITS=(1.00,3.23,5.10,7.03,8.73,10.33,11.63,13.17)
PALETTES={'ai_work':'35E8D2','beauty':'F0A5D8','relationships':'FF98B9',
 'saving':'79D7FF','sales_business':'FFD176','career':'77E2C4',
 'health':'77DBBD','science':'35E8D2','travel_food':'FFA877',
 'product_lifestyle':'A8CFFF'}

def run(cmd):
 subprocess.run(cmd,check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)

def wav_rms(wav,hop=.02):
 with wave.open(str(wav),'rb') as w:
  assert w.getnchannels()==1 and w.getsampwidth()==2
  sr=w.getframerate()
  a=np.frombuffer(w.readframes(w.getnframes()),dtype=np.int16).astype(np.float32)/32768
 n=round(sr*hop)
 a=np.pad(a,(0,(-len(a))%n))
 rms=np.sqrt(np.mean(a.reshape(-1,n)**2,axis=1))
 return np.convolve(rms,np.ones(3)/3,mode='same'),hop

def align(energy,hop):
 starts=np.cumsum([0]+list(FRAMES[:-1]))/FPS
 ends=np.cumsum(FRAMES)/FPS
 threshold=max(.012,min(.035,float(np.percentile(energy,90))*.095))
 cues=[]
 for i,(ss,se) in enumerate(zip(starts,ends)):
  lo=int((ss+.03)/hop);hi=min(len(energy),int((se-.04)/hop))
  speech=np.where(energy[lo:hi]>threshold)[0]
  if not len(speech):raise ValueError('No speech detected in scene '+str(i+1))
  onset=max(ss,(lo+int(speech[0]))*hop-.02)
  offset=min(se,(lo+int(speech[-1])+1)*hop+.04)
  old=SPLITS[i]
  l=max(onset+.2,old-.13);r=min(offset-.2,old+.13)
  if r<=l:split=old
  else:
   a=max(0,int(l/hop));b=min(len(energy),int(r/hop)+1)
   split=(a+int(np.argmin(energy[a:b])))*hop
  split=max(onset+.12,min(offset-.12,split))
  for j,(st,en) in enumerate(((onset,split),(split,offset))):
   if en<=st:raise ValueError('Invalid caption interval')
   cues.append((round(float(st),3),round(float(en),3),WORDS[i*2+j]))
 return cues

def clock(t):
 cs=round(t*100);h,cs=divmod(cs,360000);m,cs=divmod(cs,6000);s,cs=divmod(cs,100)
 return f'{h}:{m:02}:{s:02}.{cs:02}'

def write_ass(path,cues,genre='science'):
 if genre not in PALETTES:raise ValueError('Unknown genre')
 rgb=PALETTES[genre];color='&H00'+rgb[4:6]+rgb[2:4]+rgb[0:2]
 lines=['[Script Info]','Title: cycle791 RMS approximate captions','ScriptType: v4.00+',
  'PlayResX: 1080','PlayResY: 1920','WrapStyle: 2','ScaledBorderAndShadow: yes',
  '[V4+ Styles]',
  'Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding',
  'Style: JP,Noto Sans CJK JP,72,'+color+',&H00FFFFFF,&H00222616,&H00000000,-1,0,0,0,100,100,0,0,1,3,1,2,90,170,425,1',
  '[Events]','Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text']
 for st,en,words in cues:
  duration=max(2,round((en-st)*100))
  lengths=[max(1,len(w)) for w in words]
  spans=[round(duration*n/sum(lengths)) for n in lengths]
  spans[-1]+=duration-sum(spans)
  karaoke=''.join(r'{\kf'+str(n)+'}'+re.sub(r'[{}\\]','',w) for n,w in zip(spans,words))
  lines.append(f'Dialogue: 0,{clock(st)},{clock(en)},JP,,0,0,0,,{karaoke}')
 path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
 path.write_text('\n'.join(lines)+'\n',encoding='utf-8')

def render(source,strip,output,work,genre='science'):
 source=Path(source);strip=Path(strip);output=Path(output);work=Path(work)
 if not source.is_file() or not strip.is_file():raise FileNotFoundError('Missing review input')
 if source.resolve()==output.resolve():raise ValueError('Input must differ from output')
 work.mkdir(parents=True,exist_ok=True);output.parent.mkdir(parents=True,exist_ok=True)
 wav=work/'mono.wav'
 run(['ffmpeg','-v','error','-nostdin','-y','-i',str(source),'-vn','-ac','1','-ar','16000','-c:a','pcm_s16le',str(wav)])
 rms,hop=wav_rms(wav);cues=align(rms,hop)
 ass=work/'cues.ass';write_ass(ass,cues,genre)
 video=work/'video_only.mp4'
 graph=f'[0:v][1:v]overlay=x=0:y=1390:shortest=1,ass={ass}[v]'
 run(['ffmpeg','-v','error','-nostdin','-y','-i',str(source),'-loop','1','-i',str(strip),
  '-filter_complex',graph,'-map','[v]','-an','-c:v','libx264','-preset','veryfast',
  '-crf','18','-pix_fmt','yuv420p','-r','30','-frames:v',str(sum(FRAMES)),str(video)])
 run(['ffmpeg','-v','error','-nostdin','-y','-i',str(video),'-i',str(source),
  '-map','0:v:0','-map','1:a:0','-c','copy','-movflags','+faststart',str(output)])
 (work/'cues.json').write_text(json.dumps(cues,ensure_ascii=False,indent=2))
 return cues

if __name__=='__main__':
 p=argparse.ArgumentParser()
 for x in ('input','strip','output','work'):p.add_argument('--'+x,required=True)
 p.add_argument('--genre',default='science',choices=sorted(PALETTES))
 a=p.parse_args();render(a.input,a.strip,a.output,a.work,a.genre)
