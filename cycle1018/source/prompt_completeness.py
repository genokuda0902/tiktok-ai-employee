#!/usr/bin/env python3
"""Review-only illustrated prompt-entry insert. Never claims real ChatGPT capture or ASR.

Renders an original 3-line prompt card over the existing *mock UI* at 8.94–11.31s.
Real media must be a SHA-pinned locally reviewed source; CI accepts only short synthetic A/V.
"""
import argparse, hashlib, json, subprocess, tempfile
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

SOURCE_SHA = 'ba2b8937fd6343a12f5dd09fcfcef590d800fef73347b52662792ea72e5fa163'
GENRES = ('ai_work','business','money','learning','health','life','travel','food','tech','history')
LINES = ('この売上データを月別に集計して', '4〜6月の営業AとBを比較し', '表とグラフで要点をまとめて')
FONT = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
BOLD = '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
W,H,FPS=1080,1920,30
X,Y,OW,OH=52,444,860,550
START,END=8.94,11.31

def digest(path):
 h=hashlib.sha256()
 with open(path,'rb') as f:
  for b in iter(lambda:f.read(1<<20),b''):h.update(b)
 return h.hexdigest()

def command(args, binary=False):
 p=subprocess.run([str(x) for x in args],capture_output=True)
 if p.returncode:raise RuntimeError('command failed: '+' '.join(map(str,args))+'\n'+p.stderr.decode(errors='replace')[-1200:])
 return p.stdout if binary else p.stdout.decode(errors='replace')

def probe(path):return json.loads(command(['ffprobe','-v','error','-show_streams','-show_format','-of','json',path]))

def validate(source, output, genre, review_only, synthetic):
 source=Path(source).resolve();output=Path(output).resolve()
 if not review_only or genre not in GENRES or not source.is_file() or output.exists() or source==output:raise ValueError('review-only/genre/input/output gate')
 info=probe(source);streams=info['streams']
 if len(streams)!=2:raise ValueError('one video and one audio stream required')
 v=next((s for s in streams if s['codec_type']=='video'),{});a=next((s for s in streams if s['codec_type']=='audio'),{})
 if (v.get('codec_name'),v.get('width'),v.get('height'),v.get('r_frame_rate'))!=('h264',W,H,'30/1'):raise ValueError('wrong video format')
 if (a.get('codec_name'),a.get('sample_rate'),a.get('tags',{}).get('language'))!=('aac','48000','jpn'):raise ValueError('wrong Japanese-tagged audio')
 if synthetic:
  if source.name!='synthetic_input.mp4' or float(info['format']['duration'])>3.1:raise ValueError('CI synthetic fixture gate')
 elif genre!='ai_work' or digest(source)!=SOURCE_SHA:raise ValueError('real input not allowlisted')
 return info

def text_fits(draw, text, font, max_width):
 box=draw.textbbox((0,0),text,font=font)
 return box[2]-box[0]<=max_width

def frame(progress, lines=LINES):
 if len(lines)!=3 or not all(isinstance(s,str) and 1<=len(s)<=42 for s in lines):raise ValueError('three nonempty prompt lines required')
 p=max(0,min(1,progress));alpha=int(255*min(1,p/.075,(1-p)/.075))
 image=Image.new('RGBA',(OW,OH),(0,0,0,0));d=ImageDraw.Draw(image)
 reg=ImageFont.truetype(FONT,32);bold=ImageFont.truetype(BOLD,40)
 for s in lines:
  if not text_fits(d,s,bold,746):raise ValueError('prompt text would be clipped')
 # Original illustrative mock UI, not actual software screen recording.
 d.rounded_rectangle((10,8,850,540),radius=34,fill=(235,246,249,alpha),outline=(28,160,158,alpha),width=4)
 d.rounded_rectangle((30,25,830,100),radius=18,fill=(8,45,63,alpha))
 d.text((55,39),'PROMPT  /  INPUT',font=ImageFont.truetype(BOLD,31),fill=(157,239,231,alpha))
 d.text((510,43),'再現画面・説明用',font=ImageFont.truetype(FONT,26),fill=(200,221,227,alpha))
 d.text((53,123),'入力する指示（完成例）',font=bold,fill=(10,39,52,alpha))
 for i,s in enumerate(lines):
  y=190+i*105
  d.rounded_rectangle((42,y,818,y+90),radius=16,fill=(255,255,255,alpha),outline=(157,184,196,alpha),width=2)
  # Character reveal is illustrative, not word-level speech alignment.
  q=max(0,min(1,(p-.09-i*.245)/.235))
  n=round(len(s)*q)
  if n:
   d.text((66,y+24),s[:n],font=bold,fill=(13,45,58,alpha))
  if 0<q<1 and alpha>0:
   w=d.textbbox((0,0),s[:n],font=bold)[2]
   d.rounded_rectangle((68+w,y+26,72+w,y+76),radius=2,fill=(15,178,168,alpha))
 d.rounded_rectangle((55,518,805,524),radius=3,fill=(164,198,205,alpha))
 d.rounded_rectangle((55,518,55+round(750*p),524),radius=3,fill=(11,158,153,alpha))
 return image

def audio_hash(path):
 return hashlib.sha256(command(['ffmpeg','-v','error','-i',path,'-map','0:a:0','-c:a','copy','-f','adts','-'],True)).hexdigest()

def render(source,output,report,synthetic=False):
 source=Path(source);output=Path(output)
 start,end=(.30,1.50) if synthetic else (START,END)
 count=round((end-start)*FPS)
 with tempfile.TemporaryDirectory(prefix='cycle1018_') as tmp:
  folder=Path(tmp)
  for i in range(count):frame((i+.5)/count).save(folder/f'{i:04d}.png')
  filt=f'[1:v]format=yuva420p,setpts=PTS-STARTPTS+{start}/TB[card];[0:v][card]overlay=x={X}:y={Y}:eof_action=pass:repeatlast=0:format=yuv420[out]'
  command(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',source,'-framerate',FPS,'-i',folder/'%04d.png','-filter_complex',filt,'-map','[out]','-map','0:a:0','-c:v','libx264','-preset','ultrafast','-crf','24','-pix_fmt','yuv420p','-c:a','copy','-metadata:s:a:0','language=jpn','-movflags','+faststart',output])
 command(['ffmpeg','-v','error','-xerror','-i',output,'-map','0:v:0','-f','null','-','-map','0:a:0','-f','null','-'])
 info=probe(output);v=next(s for s in info['streams'] if s['codec_type']=='video');a=next(s for s in info['streams'] if s['codec_type']=='audio')
 before=audio_hash(source);after=audio_hash(output)
 if before!=after:raise AssertionError('AAC payload changed')
 result={'input_sha256':digest(source),'output_sha256':digest(output),'resolution':[v['width'],v['height']],'fps':v['r_frame_rate'],'frames':int(v['nb_frames']),'duration':float(info['format']['duration']),'audio_codec':a['codec_name'],'audio_rate':int(a['sample_rate']),'audio_language':a.get('tags',{}).get('language'),'audio_adts_sha256':after,'audio_unchanged':True,'full_decode':'PASS','overlay_window':[start,end],'new_change':'3-stage complete prompt typing in mock UI; text-fit gate','subtitle':('synthetic fixture has no subtitles' if synthetic else 'inherited burned Japanese 8 segments, no new selectable subtitle'),'japanese_asr':'NOT_VERIFIED','subtitle_semantic_sync':'NOT_VERIFIED','reference_v33':'NOT_ACCESSED','rights':'NOT_VERIFIED','publication':'NOT_APPROVED'}
 Path(report).write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
 return result

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--source',required=True);ap.add_argument('--output',required=True);ap.add_argument('--report',required=True);ap.add_argument('--genre',default='ai_work');ap.add_argument('--review-only',action='store_true');ap.add_argument('--synthetic-ci',action='store_true');a=ap.parse_args()
 info=validate(a.source,a.output,a.genre,a.review_only,a.synthetic_ci)
 if float(info['format']['duration'])<(1.5 if a.synthetic_ci else END):raise ValueError('input shorter than effect')
 print(json.dumps(render(a.source,a.output,a.report,a.synthetic_ci),ensure_ascii=False))
if __name__=='__main__':main()
