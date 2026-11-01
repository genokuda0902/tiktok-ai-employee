"""Review-only real Calc UI continuity and truthful reconciliation, ten-genre palettes.

The UI comes from an explicitly SHA-pinned *private* review MP4. Do not commit
source videos, extracted UI, frames or audio to public GitHub. Not v33 source.
"""
from __future__ import annotations
import argparse, hashlib, json, subprocess, tempfile
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

W, H, FPS, START, END, SAFE_Y = 1080, 1920, 30, 429, 520, 1260
UI_TIME = 7.75
UI_CROP = (71, 294, 824, 820)
PALETTES = {
 'ai_work':'#20d4c5','money':'#f5be5c','career':'#78c2ff',
 'business':'#72dfb5','health':'#ff9d9b','study':'#b6a1ff',
 'lifestyle':'#f4a4d5','technology':'#56d4ef','travel':'#ffd18b',
 'mindset':'#9ce5b7'
}
FONT = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'

def sha(path):
 h=hashlib.sha256()
 with open(path,'rb') as f:
  for chunk in iter(lambda:f.read(1<<20),b''):h.update(chunk)
 return h.hexdigest()

def check_hash(path,expected):
 if not expected or len(expected)!=64 or sha(path)!=expected:raise ValueError('SHA-256 mismatch / source not approved: fail closed')

def run(cmd):subprocess.run(cmd,check=True,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)

def probe(path):
 r=subprocess.run(['ffprobe','-v','error','-show_entries','stream=codec_name,width,height,r_frame_rate,sample_rate','-show_entries','format=duration','-of','json',str(path)],capture_output=True,text=True,check=True)
 d=json.loads(r.stdout);vs=[s for s in d['streams'] if s['codec_name']=='h264'];aud=[s for s in d['streams'] if s['codec_name']=='aac']
 if len(vs)!=1 or len(aud)!=1:raise ValueError('H264 + AAC required')
 v=vs[0]
 if (v['width'],v['height'],v['r_frame_rate'],int(aud[0]['sample_rate']))!=(W,H,'30/1',48000):raise ValueError('unexpected media format')
 return float(d['format']['duration'])

def validate(data):
 if set(data)!={'categories','series','note'} or len(data['series'])!=2:raise ValueError('two explicit series required')
 if not 1<=len(data['categories'])<=12:raise ValueError('invalid categories')
 totals=[]
 for s in data['series']:
  if not isinstance(s['name'],str) or len(s['name'])>8 or len(s['values'])!=len(data['categories']):raise ValueError('bad series')
  if any(type(v) is not int or v<0 or v>999 for v in s['values']):raise ValueError('invalid number')
  totals.append(sum(s['values']))
 if sum(totals)>9999:raise ValueError('total too large')
 return totals

def extract_ui(video,path):
 run(['ffmpeg','-v','error','-y','-ss',str(UI_TIME),'-i',str(video),'-frames:v','1','-update','1',str(path)])
 with Image.open(path) as im:
  return im.convert('RGB').crop(UI_CROP).resize((908,484),Image.Resampling.LANCZOS)

def font(size):return ImageFont.truetype(FONT,size)

def paint(draw,xy,msg,size=32,color='#ffffff'):
 draw.text(xy,str(msg),font=font(size),fill=color,stroke_width=0)

def ease(x):
 x=max(0,min(1,x));return x*x*(3-2*x)

def overlay(i,ui,data,genre):
 totals=validate(data)
 if genre not in PALETTES:raise ValueError('unsupported genre')
 if not 0<=i<END-START:raise ValueError('invalid frame index')
 a=PALETTES[genre];im=Image.new('RGBA',(W,SAFE_Y));d=ImageDraw.Draw(im)
 d.rounded_rectangle((28,116,1052,1246),radius=34,fill='#071c2b',outline='#456779',width=3)
 d.rounded_rectangle((58,146,1022,267),radius=23,fill='#12374a')
 paint(d,(82,163),'実画面の数字を、検算でつなぐ',42)
 paint(d,(83,223),'4〜6月の架空データ / Calcの操作画面から確認',24,'#b6d5e3')
 d.rounded_rectangle((67,290,1013,804),radius=22,fill='#eaf5f6',outline='#6d91a0',width=3)
 im.paste(ui,(85,307))
 # Animate two evidence highlights over real screenshot values 46 and 29.
 for k,(cx,cy) in enumerate(((395,712),(596,712))):
  if i>=8+k*18:
   d.rounded_rectangle((cx-72,cy-47,cx+72,cy+40),radius=13,outline=a,width=5)
 # Distinct lower proof cards; math comes only from supplied JSON.
 labels=[data['series'][0]['name'],data['series'][1]['name'],'合計']
 values=[totals[0],totals[1],sum(totals)]
 for k,(label,value) in enumerate(zip(labels,values)):
  x=74+330*k
  d.rounded_rectangle((x,835,x+280,1044),radius=20,fill=('#144354' if k<2 else '#105354'),outline=(a if k==2 else '#648a98'),width=3)
  paint(d,(x+18,854),label,30,'#d7edf1')
  prog=ease((i-(k*17+4))/15)
  if prog>0:paint(d,(x+42,908),round(value*prog),72,a if k==2 else '#ffffff')
  if k<2:paint(d,(x+287,911),'+' if k==0 else '=',45,a)
 d.rounded_rectangle((78,1064,1002,1174),radius=18,fill='#143648')
 if i>=62:
  paint(d,(99,1073),f'{labels[0]} {values[0]} ＋ {labels[1]} {values[1]} ＝ 合計 {values[2]}',37)
  paint(d,(101,1127),'架空データの照合例。AIによる修正効果の証明ではありません。',22,'#c7dce7')
 else:
  paint(d,(100,1091),'元データの内訳から合計を確認',30,'#c7dce7')
 assert im.getbbox() is not None
 return im

def render(source,ui_video,out,source_sha,ui_sha,data,genre='ai_work',smoke=False):
 validate(data)
 if genre not in PALETTES:raise ValueError('unsupported genre')
 check_hash(source,source_sha);check_hash(ui_video,ui_sha)
 duration=probe(source);probe(ui_video)
 if duration<END/FPS or (not smoke and abs(duration-23.033333)>0.08):raise ValueError('unexpected duration')
 out=Path(out);out.parent.mkdir(parents=True,exist_ok=True)
 with tempfile.TemporaryDirectory() as temp:
  t=Path(temp);ui=extract_ui(ui_video,t/'ui.png')
  for i in range(END-START):overlay(i,ui,data,genre).save(t/f'ov_{i:03d}.png',compress_level=1)
  flt=(f'[1:v]format=rgba,setpts=PTS-STARTPTS+{START/FPS}/TB[ov];'
       f"[0:v][ov]overlay=0:0:eof_action=pass:repeatlast=0:enable='between(n,{START},{END-1})'[v]")
  run(['ffmpeg','-v','error','-y','-i',str(source),'-framerate',str(FPS),'-i',str(t/'ov_%03d.png'),'-filter_complex',flt,
       '-map','[v]','-map','0:a:0','-c:v','libx264','-preset','veryfast','-crf','19','-pix_fmt','yuv420p',
       '-r',str(FPS),'-c:a','copy','-movflags','+faststart',str(out)])
 return {'duration':probe(out),'source_sha256':source_sha,'ui_sha256':ui_sha,'output_sha256':sha(out),'genre':genre,'changed_frames':[START,END-1],'caption_area':'unchanged via transparent overlay below y=1260'}

def smoke():
 with tempfile.TemporaryDirectory() as temp:
  t=Path(temp);src=t/'synthetic.mp4';out=t/'out.mp4'
  run(['ffmpeg','-v','error','-y','-f','lavfi','-i','testsrc2=size=1080x1920:rate=30:duration=18',
       '-f','lavfi','-i','sine=frequency=440:sample_rate=48000:duration=18','-c:v','libx264','-preset','ultrafast',
       '-pix_fmt','yuv420p','-c:a','aac','-shortest',str(src)])
  data={'categories':['4月','5月','6月'],'series':[{'name':'営業A','values':[12,16,18]},{'name':'営業B','values':[8,9,12]}],'note':'架空データ'}
  print(json.dumps(render(src,src,out,sha(src),sha(src),data,smoke=True)))
  run(['ffmpeg','-v','error','-xerror','-i',str(out),'-f','null','-'])
  print('PASS synthetic 18s A/V full decode')

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--source');p.add_argument('--ui-video');p.add_argument('--source-sha');p.add_argument('--ui-sha');p.add_argument('--data-json');p.add_argument('--out');p.add_argument('--genre',default='ai_work',choices=PALETTES);p.add_argument('--smoke',action='store_true');a=p.parse_args()
 if a.smoke:smoke()
 else:
  if not a.data_json:raise SystemExit('explicit data JSON required')
  data=json.loads(Path(a.data_json).read_text(encoding='utf-8'))
  print(json.dumps(render(a.source,a.ui_video,a.out,a.source_sha,a.ui_sha,data,a.genre),ensure_ascii=False,indent=2))
