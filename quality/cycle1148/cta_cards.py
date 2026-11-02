#!/usr/bin/env python3
"""Review-only ten-genre final CTA card cleanup. Never publishes media."""
import argparse,hashlib,json,subprocess
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont

GENRES={'ai':'#27d9d1','business':'#51c7f4','money':'#eac56c','learning':'#8fc4ff',
'health':'#79d7ab','food':'#f3bd79','travel':'#80c8e8','beauty':'#efafd2',
'career':'#93a5ff','life':'#a7dfb0'}
POLICY='HUMAN_REVIEW/PUBLICATION_NOT_APPROVED'
WIDTH,HEIGHT,FPS=1080,1920,30
ROI=(84,970,912,116)
CAPTION_START=1280
FONT='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
LABELS=('01  数字を確認','02  保存する','03  次回も再利用')

def sha256(path):
 h=hashlib.sha256()
 with open(path,'rb') as f:
  for block in iter(lambda:f.read(1024*1024),b''):h.update(block)
 return h.hexdigest()

def probe(path):
 obj=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(path)]))
 v=next(s for s in obj['streams'] if s['codec_type']=='video')
 a=next(s for s in obj['streams'] if s['codec_type']=='audio')
 if (v['codec_name'],int(v['width']),int(v['height']),v['r_frame_rate'])!=('h264',WIDTH,HEIGHT,'30/1'):
  raise ValueError('H264 1080x1920 30fps required')
 if a['codec_name']!='aac' or int(a['sample_rate'])!=48000:
  raise ValueError('AAC 48kHz required')
 return float(obj['format']['duration']),int(v.get('nb_frames') or 0)

def check(manifest,source,duration):
 if manifest.get('policy')!=POLICY or manifest.get('genre') not in GENRES:raise ValueError('Unapproved policy or genre')
 if manifest.get('source_sha256')!=sha256(source):raise ValueError('Source SHA mismatch')
 if manifest.get('asset_approval')!='review_only_original_graphics':raise ValueError('Asset approval metadata missing')
 times=manifest.get('steps')
 if not isinstance(times,list) or len(times)!=4 or any(not isinstance(t,(int,float)) for t in times):
  raise ValueError('Invalid step intervals')
 if not (20.3<=times[0]<times[1]<times[2]<times[3]<=duration+0.04):
  raise ValueError('Unsafe time window')
 if min(times[i+1]-times[i] for i in range(3))<0.25:raise ValueError('Steps too short')
 x,y,w,h=ROI
 if x<0 or y<0 or x+w>WIDTH or y+h>=CAPTION_START:raise ValueError('Caption ROI overlap')
 return times

def make_card_strip(genre,focus,path):
 x,y,w,h=ROI
 im=Image.new('RGBA',(w,h),(3,18,32,255))
 d=ImageDraw.Draw(im);accent=GENRES[genre];font=ImageFont.truetype(FONT,25)
 for i,label in enumerate(LABELS):
  left=6+i*303;right=left+291;active=(i==focus)
  d.rounded_rectangle((left,7,right,h-7),radius=15,
   fill=(5,62,72,255) if active else (5,34,52,255),
   outline=accent if active else '#3b6574',width=4 if active else 2)
  bb=d.textbbox((0,0),label,font=font);tw=bb[2]-bb[0]
  if tw>right-left-20:raise ValueError('Card text overflow')
  d.text((left+(right-left-tw)//2,41),label,font=font,
   fill=(247,253,255,255) if active else (191,215,226,255))
  if active:d.ellipse((right-21,14,right-10,25),fill=accent)
 im.save(path)
 return path

def render(source,output,manifest_path,workdir=None):
 source,output=Path(source),Path(output)
 duration,frames=probe(source)
 data=json.loads(Path(manifest_path).read_text(encoding='utf-8'))
 times=check(data,source,duration)
 workdir=Path(workdir) if workdir else output.parent
 workdir.mkdir(parents=True,exist_ok=True)
 paths=[make_card_strip(data['genre'],i,workdir/f'cta_state{i+1}.png') for i in range(3)]
 inputs=[]
 for path in paths:inputs+=['-loop','1','-framerate',str(FPS),'-i',str(path)]
 x,y,_,_=ROI;filters=[];prev='0:v'
 for i in range(3):
  nxt='v' if i==2 else f'tmp{i}'
  a,b=times[i],times[i+1]
  filters.append(f"[{prev}][{i+1}:v]overlay={x}:{y}:format=auto:enable='gte(t,{a:.3f})*lt(t,{b:.3f})'[{nxt}]")
  prev=nxt
 cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(source),*inputs,
  '-filter_complex',';'.join(filters),'-map','[v]','-map','0:a:0',
  '-c:v','libx264','-preset','veryfast','-crf','18','-threads','2',
  '-pix_fmt','yuv420p','-frames:v',str(frames or round(duration*FPS)),
  '-c:a','copy','-movflags','+faststart',str(output)]
 subprocess.run(cmd,check=True)
 outduration,outframes=probe(output)
 if frames and outframes!=frames:raise RuntimeError('Frame count changed')
 if abs(outduration-duration)>.06:raise RuntimeError('Duration changed')
 return {'source_sha256':sha256(source),'output_sha256':sha256(output),
  'frames':outframes,'duration':outduration,'steps':times,'genre':data['genre'],
  'policy':POLICY,'source_media_uploaded':False}

if __name__=='__main__':
 p=argparse.ArgumentParser()
 for field in ('source','output','manifest','report'):p.add_argument('--'+field,required=True)
 args=p.parse_args()
 result=render(args.source,args.output,args.manifest)
 Path(args.report).write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
 print(json.dumps(result,ensure_ascii=False))
