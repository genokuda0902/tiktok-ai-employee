"""Review-only source-to-chart bridge; never uploads or posts private media.

The dataset is explicit, locally supplied and labelled illustrative; this is not
an actual AI-generated result or a measured productivity improvement.
"""
from __future__ import annotations
import argparse, hashlib, json, subprocess, tempfile
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

W,H,FPS,START,END,SAFE_Y=1080,1920,30,380,429,1280
ACCENTS={'ai_work':'#1fd5c5','finance':'#f2c36a','education':'#7ca8fa',
'health':'#78e0ac','travel':'#f8a9bb','beauty':'#d5a6fb',
'food':'#ffa673','career':'#70ceef','productivity':'#b8e271','lifestyle':'#f6c97e'}
FONT='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
SAMPLE={'categories':['4月','5月','6月'],'series':[{'name':'営業A','values':[12,16,18]},
{'name':'営業B','values':[8,9,12]}],'note':'架空の営業データ（説明用）'}

def sha256(path):
 h=hashlib.sha256()
 with open(path,'rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 return h.hexdigest()

def validate(data):
 if not isinstance(data,dict) or set(data)!={'categories','series','note'}:raise ValueError('dataset schema')
 if len(data['categories'])!=3 or len(data['series'])!=2:raise ValueError('requires 3 categories and 2 series')
 if not all(isinstance(x,str) and 0<len(x)<=12 for x in data['categories']):raise ValueError('category labels')
 if not isinstance(data['note'],str) or not (1<=len(data['note'])<=32):raise ValueError('illustrative note required')
 for s in data['series']:
  if set(s)!={'name','values'} or not isinstance(s['name'],str) or not 1<=len(s['name'])<=12:raise ValueError('series schema')
  if len(s['values'])!=3 or any(type(v) is not int or not 0<=v<=999 for v in s['values']):raise ValueError('numeric values')
 return [sum(s['values']) for s in data['series']]

def probe(path):
 j=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(path)]))
 v=next(x for x in j['streams'] if x['codec_type']=='video')
 a=next((x for x in j['streams'] if x['codec_type']=='audio'),None)
 return {'codec':v['codec_name'],'width':v['width'],'height':v['height'],'fps':v['r_frame_rate'],
 'frames':int(v.get('nb_frames') or 0),'duration':float(j['format']['duration']),
 'audio':a['codec_name'] if a else None,'sample_rate':int(a['sample_rate']) if a else None}

def label(d,xy,s,size=36,color='#eef8ff'):
 d.text(xy,str(s),font=ImageFont.truetype(FONT,size),fill=color)

def frame(i,data=SAMPLE,genre='ai_work'):
 totals=validate(data)
 if genre not in ACCENTS:raise ValueError('unsupported genre')
 accent=ACCENTS[genre]
 im=Image.new('RGBA',(W,H),(0,0,0,0));d=ImageDraw.Draw(im)
 d.rounded_rectangle((45,175,1035,1230),radius=34,fill='#061e30',outline='#2c6277',width=3)
 d.rounded_rectangle((70,201,1010,318),radius=21,fill='#0e3549')
 label(d,(94,217),'表の数値から、グラフで検算',43)
 label(d,(94,273),data['note'],23,'#b4cbd6')
 d.rounded_rectangle((92,341,988,1017),radius=22,fill='#0a2839')
 d.rectangle((148,435,945,438),fill='#36596c')
 for tick in (0,5,10,15,20):
  y=920-tick*23
  d.line((166,y,950,y),fill='#2b5264',width=2)
  label(d,(102,y-19),tick,23,'#a7c3d2')
 colors=(accent,'#f6b865')
 for k,s in enumerate(data['series']):
  x=340+k*265
  d.rounded_rectangle((x,361,x+24,386),radius=6,fill=colors[k])
  label(d,(x+32,355),s['name'],30)
 t=i/FPS
 for col,cat in enumerate(data['categories']):
  x0=246+col*243
  label(d,(x0+44,940),cat,29)
  for k,s in enumerate(data['series']):
   v=s['values'][col];x=x0+k*75
   phase=max(0.0,min(1.0,(t-0.08-col*0.27)/0.36))
   eased=1-(1-phase)**3
   hh=int(v*23*eased)
   if hh:d.rounded_rectangle((x,920-hh,x+57,920),radius=9,fill=colors[k])
   if phase>=0.93:label(d,(x+4,882-v*23),v,25)
 if t>=1.02:
  d.rounded_rectangle((90,1043,989,1164),radius=21,fill='#0d454d',outline=accent,width=3)
  label(d,(111,1061),f'{data["series"][0]["name"]} {totals[0]}  ＋  {data["series"][1]["name"]} {totals[1]}  ＝  {sum(totals)}',36)
  label(d,(112,1122),'元データと合計を照合',24,'#c2e7e8')
 label(d,(679,1184),'ILLUSTRATIVE / REVIEW ONLY',19,'#a9c5d0')
 assert im.crop((0,SAFE_Y,W,H)).getbbox() is None
 return im

def render(source,out,source_sha,genre='ai_work',data=SAMPLE,smoke=False):
 validate(data)
 if genre not in ACCENTS:raise ValueError('unsupported genre')
 if sha256(source)!=source_sha:raise ValueError('source SHA mismatch (fail closed)')
 p=probe(source)
 if (p['codec'],p['width'],p['height'],p['fps'],p['audio'],p['sample_rate'])!=('h264',W,H,'30/1','aac',48000):raise ValueError('unexpected A/V source')
 if p['duration']<END/FPS or (not smoke and abs(p['duration']-23.033333)>0.08):raise ValueError('unexpected source duration')
 Path(out).parent.mkdir(parents=True,exist_ok=True)
 with tempfile.TemporaryDirectory() as td:
  td=Path(td)
  for i in range(END-START):frame(i,data,genre).save(td/f'ov_{i:03d}.png',compress_level=1)
  graph=(f'[1:v]format=rgba,setpts=PTS-STARTPTS+{START/FPS}/TB[ov];'
   f'[0:v][ov]overlay=0:0:shortest=0:eof_action=pass:repeatlast=0:'
   f"enable='between(n,{START},{END-1})'[v]")
  subprocess.run(['ffmpeg','-v','error','-y','-i',str(source),'-framerate',str(FPS),'-i',str(td/'ov_%03d.png'),
   '-filter_complex',graph,'-map','[v]','-map','0:a:0','-c:v','libx264','-preset','veryfast',
   '-crf','19','-pix_fmt','yuv420p','-r',str(FPS),'-c:a','copy','-movflags','+faststart',str(out)],check=True)
 return probe(out)

def smoke():
 with tempfile.TemporaryDirectory() as td:
  td=Path(td);s=td/'s.mp4';o=td/'o.mp4'
  subprocess.run(['ffmpeg','-v','error','-y','-f','lavfi','-i','testsrc2=size=1080x1920:rate=30:duration=15',
    '-f','lavfi','-i','sine=frequency=440:sample_rate=48000:duration=15','-c:v','libx264',
    '-preset','ultrafast','-pix_fmt','yuv420p','-c:a','aac','-shortest',str(s)],check=True)
  render(s,o,sha256(s),smoke=True)
  subprocess.run(['ffmpeg','-v','error','-xerror','-i',str(o),'-f','null','-'],check=True)
  print('PASS synthetic 15s A/V smoke; no private media used')

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--source');p.add_argument('--source-sha');p.add_argument('--out')
 p.add_argument('--genre',default='ai_work',choices=ACCENTS);p.add_argument('--data-json');p.add_argument('--smoke',action='store_true')
 a=p.parse_args()
 if a.smoke:smoke()
 else:
  if not a.data_json:raise SystemExit('--data-json required; no implicit production dataset')
  data=json.loads(Path(a.data_json).read_text(encoding='utf-8'))
  print(json.dumps(render(a.source,a.out,a.source_sha,a.genre,data),ensure_ascii=False,indent=2))
