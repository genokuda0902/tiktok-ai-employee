"""Review-only chart-to-proof animation. Reimplementation, not original v33 source.
Private input MP4/audio must not be committed. SHA pinning does not grant publication rights.
"""
from __future__ import annotations
import argparse, hashlib, json, subprocess, tempfile
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

W,H,FPS,START,END,SAFE_Y = 1080,1920,30,380,429,1260
PALETTES={
 'ai_work':'#20d4c5','money':'#f5be5c','career':'#78c2ff',
 'business':'#72dfb5','health':'#ff9d9b','study':'#b6a1ff',
 'lifestyle':'#f4a4d5','technology':'#56d4ef','travel':'#ffd18b',
 'mindset':'#9ce5b7'}
FONT='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'

def sha(path):
 h=hashlib.sha256()
 with open(path,'rb') as f:
  for chunk in iter(lambda:f.read(1<<20),b''):h.update(chunk)
 return h.hexdigest()

def check_source(path,expected):
 if not expected or len(expected)!=64 or sha(path)!=expected:
  raise ValueError('Unpinned or mismatched source: fail closed')

def run(cmd):
 r=subprocess.run(cmd,capture_output=True,text=True)
 if r.returncode:raise RuntimeError(' '.join(cmd[:5])+' : '+r.stderr[-1800:])
 return r.stdout

def probe(path):
 d=json.loads(run(['ffprobe','-v','error','-show_entries','stream=codec_name,width,height,r_frame_rate,sample_rate','-show_entries','format=duration','-of','json',str(path)]))
 v=[s for s in d['streams'] if s['codec_name']=='h264']
 a=[s for s in d['streams'] if s['codec_name']=='aac']
 if len(v)!=1 or len(a)!=1 or (v[0]['width'],v[0]['height'],v[0]['r_frame_rate'],int(a[0]['sample_rate']))!=(W,H,'30/1',48000):
  raise ValueError('expected H264 1080x1920 30fps + AAC 48kHz')
 return float(d['format']['duration'])

def totals(data):
 if set(data)!={'categories','series','note'} or len(data['series'])!=2 or not 1<=len(data['categories'])<=12:
  raise ValueError('expected two series and 1..12 categories')
 values=[]
 for s in data['series']:
  if not isinstance(s['name'],str) or not 1<=len(s['name'])<=8 or len(s['values'])!=len(data['categories']):
   raise ValueError('bad series')
  if any(type(v) is not int or not 0<=v<=999 for v in s['values']):
   raise ValueError('invalid value')
  values.append(sum(s['values']))
 if any(x>9999 for x in values+[sum(values)]):raise ValueError('values too large for display')
 if '架空' not in data['note'] and 'synthetic' not in data['note'].lower():
  raise ValueError('only explicitly synthetic demonstration data supported')
 return values+[sum(values)]

def easing(x):
 x=max(0.,min(1.,x));return x*x*(3-2*x)

def frame(i,data,genre='ai_work'):
 if not 0<=i<END-START:raise ValueError('bad frame index')
 if genre not in PALETTES:raise ValueError('unknown genre')
 vals=totals(data);names=[data['series'][0]['name'],data['series'][1]['name'],'合計']
 im=Image.new('RGBA',(W,SAFE_Y),(0,0,0,0));d=ImageDraw.Draw(im)
 # Replace the old static summary at y=1044, never stack over chart labels.
 d.rounded_rectangle((89,1038,991,1170),radius=18,fill='#092d3e',outline=PALETTES[genre],width=3)
 for j,(label,value) in enumerate(zip(names,vals)):
  x=101+j*294;y=1048;right=x+276;bottom=1158
  d.rounded_rectangle((x,y,right,bottom),radius=12,fill='#12394b',outline='#4c7586',width=2)
  d.rounded_rectangle((x+8,y+11,x+15,bottom-11),radius=3,fill=PALETTES[genre])
  f=ImageFont.truetype(FONT,24);vf=ImageFont.truetype(FONT,48)
  d.text((x+30,y+5),label,font=f,fill='#dceef6')
  if i>=5+j*13:
   alpha=round(255*easing((i-(5+j*13))/7))
   d.text((x+30,y+43),str(value),font=vf,fill=(255,255,255,alpha))
 return im

def render(source,out,expected_sha,data,genre='ai_work',smoke=False):
 check_source(source,expected_sha);totals(data)
 if genre not in PALETTES:raise ValueError('unknown genre')
 duration=probe(source)
 if duration<END/FPS or (not smoke and abs(duration-23.033333)>0.08):raise ValueError('unexpected duration')
 out=Path(out);out.parent.mkdir(parents=True,exist_ok=True)
 with tempfile.TemporaryDirectory() as td:
  for i in range(END-START):frame(i,data,genre).save(Path(td)/f'ov_{i:03d}.png',compress_level=1)
  flt=(f'[1:v]format=rgba,setpts=PTS-STARTPTS+{START/FPS}/TB[ov];'
       f"[0:v][ov]overlay=0:0:eof_action=pass:repeatlast=0:enable='between(n,{START},{END-1})'[v]")
  run(['ffmpeg','-v','error','-y','-i',str(source),'-framerate',str(FPS),'-i',str(Path(td)/'ov_%03d.png'),
       '-filter_complex',flt,'-map','[v]','-map','0:a:0','-c:v','libx264','-preset','veryfast','-crf','19',
       '-pix_fmt','yuv420p','-r',str(FPS),'-c:a','copy','-movflags','+faststart',str(out)])
 return {'input_sha256':expected_sha,'output_sha256':sha(out),'genre':genre,'frames_changed':[START,END-1],
         'duration':probe(out),'totals':totals(data),'protected':'no drawn pixels y>=1170; original subtitle y>=1280'}

DEMO={'categories':['4月','5月','6月'], 'series':[{'name':'営業A','values':[12,16,18]},
      {'name':'営業B','values':[8,9,12]}],'note':'架空データ'}

def smoke():
 with tempfile.TemporaryDirectory() as td:
  p=Path(td);src=p/'source.mp4';out=p/'out.mp4'
  run(['ffmpeg','-v','error','-y','-f','lavfi','-i','color=c=0x102c41:s=1080x1920:r=30:d=15',
       '-f','lavfi','-i','sine=frequency=440:sample_rate=48000:duration=15',
       '-c:v','libx264','-preset','ultrafast','-pix_fmt','yuv420p','-c:a','aac','-shortest',str(src)])
  print(json.dumps(render(src,out,sha(src),DEMO,smoke=True)))
  run(['ffmpeg','-v','error','-xerror','-i',str(out),'-f','null','-'])
  print('PASS synthetic A/V full decode')

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--source');p.add_argument('--source-sha');p.add_argument('--out');
 p.add_argument('--data-json');p.add_argument('--genre',default='ai_work',choices=PALETTES);p.add_argument('--smoke',action='store_true');a=p.parse_args()
 if a.smoke:smoke()
 else:
  if not a.data_json:raise SystemExit('explicit JSON required')
  data=json.loads(Path(a.data_json).read_text(encoding='utf-8'))
  print(json.dumps(render(a.source,a.out,a.source_sha,data,a.genre),ensure_ascii=False,indent=2))
