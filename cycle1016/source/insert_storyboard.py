#!/usr/bin/env python3
"""Two original image-first storyboard inserts; REVIEW ONLY, not an ASR/rights approval.

Generic 10-genre insert engine, but real rendering is SHA-gated to one local
AI-work video. Never uploads, merges, posts or approves publication.
"""
import argparse
import hashlib
import json
import math
from pathlib import Path
import subprocess
import tempfile
from PIL import Image, ImageDraw, ImageFont

SOURCE_SHA='b27da279d11e07d3c59a4da32038b51b3a61f25c132fa4ac75ca484efa5d2362'
GENRES=('ai_work','business','money','learning','health','life','travel','food','tech','history')
FONT='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
BOLD='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
W,H,FPS=1080,1920,30
PANEL_W,PANEL_H=860,780
# all content stays in x110..970, y450..1230; caption y>=1490 untouched
INSERTS=(
 {'start':3.90,'end':5.10,'title':'繰り返し作業を見える化','tag':'WORKFLOW  /  EXAMPLE','rows':('毎日の集計','週報への転記','定型レポート'),'kind':'tasks'},
 {'start':18.08,'end':19.28,'title':'使える指示を型に残す','tag':'PROMPT  /  TEMPLATE','rows':('目的：何を達成する？','条件：何を守る？','出力：どんな形で？'),'kind':'template'},
)

def sha256(path):
 h=hashlib.sha256()
 with open(path,'rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
 return h.hexdigest()

def run(args):
 p=subprocess.run([str(x) for x in args],capture_output=True,text=True)
 if p.returncode:raise RuntimeError('command failed: '+' '.join(map(str,args))+'\n'+p.stderr[-1400:])
 return p.stdout

def probe(path):return json.loads(run(['ffprobe','-v','error','-show_streams','-show_format','-of','json',path]))

def validate(source,output,genre,review_only,synthetic_ci):
 source=Path(source).resolve();output=Path(output).resolve()
 if not review_only or genre not in GENRES or not source.is_file() or output.exists() or source==output:raise ValueError('review-only/genre/source/output gate failed')
 p=probe(source);v=[s for s in p['streams'] if s['codec_type']=='video'];a=[s for s in p['streams'] if s['codec_type']=='audio']
 if len(p['streams'])!=2 or len(v)!=1 or len(a)!=1:raise ValueError('exactly one video and one audio stream required')
 v,a=v[0],a[0]
 if (v['codec_name'],v['width'],v['height'],v['r_frame_rate'])!=('h264',W,H,'30/1'):raise ValueError('video must be H264 portrait 30fps')
 if (a['codec_name'],a['sample_rate'],a.get('tags',{}).get('language'))!=('aac','48000','jpn'):raise ValueError('audio must be Japanese-tagged AAC 48kHz')
 if synthetic_ci:
  if source.name!='synthetic_input.mp4' or float(p['format']['duration'])>3.1:raise ValueError('synthetic fixture restriction')
 elif genre!='ai_work' or sha256(source)!=SOURCE_SHA:raise ValueError('unapproved real source/genre SHA')
 return p

def font(size,bold=False):return ImageFont.truetype(BOLD if bold else FONT,size)

def smooth(t):
 t=max(0.,min(1.,t));return t*t*(3-2*t)

def make_frame(spec,progress):
 # Progress is local insert time fraction. In/out alpha ramps, plus subtle horizontal motion.
 fade=min(1.,progress/.18,(1-progress)/.18)
 opacity=round(246*smooth(fade))
 im=Image.new('RGBA',(PANEL_W,PANEL_H),(0,0,0,0));d=ImageDraw.Draw(im)
 xshift=round(13*(1-smooth(progress)))
 d.rounded_rectangle((18+xshift,25,838+xshift,748),radius=38,fill=(3,20,36,opacity),outline=(61,214,200,opacity),width=4)
 d.rounded_rectangle((40+xshift,49,820+xshift,114),radius=18,fill=(15,70,83,opacity))
 d.text((68+xshift,60),spec['tag'],font=font(30,True),fill=(133,239,224,opacity))
 d.text((58+xshift,152),spec['title'],font=font(48,True),fill=(246,252,255,opacity))
 d.text((60+xshift,224),'画面イメージ・説明用の例',font=font(25),fill=(169,193,209,opacity))
 for i,row in enumerate(spec['rows']):
  top=298+i*126
  active=progress*3.4>=i+.3
  fill=(15,85,88,opacity) if active else (19,40,60,opacity)
  d.rounded_rectangle((58+xshift,top,803+xshift,top+102),radius=21,fill=fill,outline=(70,204,190,opacity) if active else (51,83,106,opacity),width=3)
  d.rounded_rectangle((77+xshift,top+23,133+xshift,top+79),radius=16,fill=(51,205,183,opacity) if active else (41,75,91,opacity))
  d.text((91+xshift,top+31),str(i+1),font=font(27,True),fill=(4,26,37,opacity) if active else (190,216,221,opacity))
  d.text((157+xshift,top+23),row,font=font(37,True),fill=(240,250,252,opacity))
 d.rounded_rectangle((60+xshift,704,802+xshift,713),radius=5,fill=(36,72,87,opacity))
 d.rounded_rectangle((60+xshift,704,60+xshift+round(742*progress),713),radius=5,fill=(83,227,201,opacity))
 return im

def render(source,output,specs,report):
 with tempfile.TemporaryDirectory(prefix='storyboard_insert_') as tmp:
  inputs=['-i',str(source)];parts=[];overlays=[]
  for k,s in enumerate(specs):
   folder=Path(tmp)/('overlay'+str(k));folder.mkdir()
   n=round((s['end']-s['start'])*FPS)
   for i in range(n):make_frame(s,(i+.5)/n).save(folder/f'{i:03d}.png')
   inputs+=['-framerate',str(FPS),'-start_number','0','-i',str(folder/'%03d.png')]
   parts.append(f'[{k+1}:v]format=yuva420p,setpts=PTS-STARTPTS+{s["start"]}/TB[insert{k}]')
   previous='[0:v]' if k==0 else f'[out{k-1}]'
   overlays.append(f'{previous}[insert{k}]overlay=x=110:y=450:eof_action=pass:repeatlast=0:format=yuv420[out{k}]')
  filt=';'.join(parts+overlays)
  args=['ffmpeg','-hide_banner','-loglevel','error','-y']+inputs+['-filter_complex',filt,'-map',f'[out{len(specs)-1}]','-map','0:a:0','-c:v','libx264','-preset','ultrafast','-crf','24','-pix_fmt','yuv420p','-c:a','copy','-movflags','+faststart','-metadata:s:a:0','language=jpn',str(output)]
  run(args)
  # Full decode, not only stream probing.
  run(['ffmpeg','-v','error','-xerror','-i',output,'-map','0:v:0','-f','null','-','-map','0:a:0','-f','null','-'])
  before=probe(source);after=probe(output)
  v=next(x for x in after['streams'] if x['codec_type']=='video');a=next(x for x in after['streams'] if x['codec_type']=='audio')
  result={'input_sha256':sha256(source),'output_sha256':sha256(output),'resolution':[v['width'],v['height']],'fps':v['r_frame_rate'],'frames':int(v['nb_frames']),'duration':float(after['format']['duration']),'audio_codec':a['codec_name'],'audio_rate':int(a['sample_rate']),'audio_language':a.get('tags',{}).get('language'),'full_decode':'PASS','insert_windows':[{'start':s['start'],'end':s['end'],'kind':s['kind']} for s in specs],'visual_shots_estimate':'8 original scenes + 2 within-scene inserts; not 10 independent scenes','japanese_asr':'NOT_VERIFIED','caption_semantic_sync':'NOT_VERIFIED','rights':'NOT_VERIFIED','publication':'NOT_APPROVED'}
  Path(report).write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
  return result

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--source',required=True);ap.add_argument('--output',required=True);ap.add_argument('--report',required=True);ap.add_argument('--genre',default='ai_work');ap.add_argument('--review-only',action='store_true');ap.add_argument('--synthetic-ci',action='store_true');args=ap.parse_args()
 info=validate(args.source,args.output,args.genre,args.review_only,args.synthetic_ci)
 specs=({'start':.3,'end':1.5,'title':'繰り返し作業を見える化','tag':'SYNTHETIC','rows':('確認','編集','保存'),'kind':'synthetic'},) if args.synthetic_ci else INSERTS
 if float(info['format']['duration'])<max(s['end'] for s in specs):raise ValueError('source shorter than inserts')
 print(json.dumps(render(args.source,args.output,specs,args.report),ensure_ascii=False))
if __name__=='__main__':main()
