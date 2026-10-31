"""cycle1080: 10-genre proof-based before/after illustration (REVIEW ONLY).

Reimplementation, not original v33. Requires SHA-pinned private source MP4;
extracts a fictional Calc evidence still locally; never commits media.
Does not assert narration/caption semantic alignment or publication rights.
"""
from __future__ import annotations
import argparse, hashlib, json, subprocess, tempfile
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

FPS=30; W=1080; H=1920; START=429; END=520; SAFE_Y=1280
PALETTES={
 'ai_work':'#19c8bd','finance':'#f2c36a','education':'#75a8fc',
 'health':'#78e0ac','travel':'#f8a9bb','beauty':'#d5a6fb',
 'food':'#ffa673','career':'#70ceef','productivity':'#b8e271',
 'lifestyle':'#f6c97e'}
FONT='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'

def sha256(path):
 h=hashlib.sha256()
 with open(path,'rb') as f:
  for b in iter(lambda:f.read(1<<20),b''):h.update(b)
 return h.hexdigest()

def probe(path):
 j=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(path)]))
 v=next(x for x in j['streams'] if x['codec_type']=='video')
 a=next((x for x in j['streams'] if x['codec_type']=='audio'),None)
 return {'width':v['width'],'height':v['height'],'fps':v['r_frame_rate'],'codec':v['codec_name'],
  'frames':int(v.get('nb_frames') or 0),'duration':float(j['format']['duration']),
  'audio':a['codec_name'] if a else None,'sample_rate':int(a['sample_rate']) if a else None}

def text(d,xy,s,size,color='#edf8ff'):
 d.text(xy,s,font=ImageFont.truetype(FONT,size),fill=color,stroke_width=0)

def still(source,path):
 subprocess.run(['ffmpeg','-v','error','-y','-ss','8.49','-i',str(source),'-frames:v','1',str(path)],check=True)
 with Image.open(path) as im:
  # Actual Calc cell result 75 in a fictional, local demonstration.
  return im.convert('RGB').crop((65,355,900,820)).resize((836,345),Image.Resampling.LANCZOS)

def frame(i,proof,genre='ai_work'):
 if genre not in PALETTES:raise ValueError('unsupported genre')
 accent=PALETTES[genre]; t=i/FPS
 im=Image.new('RGBA',(W,H),(0,0,0,0));d=ImageDraw.Draw(im)
 # Content stays strictly above the inherited subtitle/progress safe island.
 d.rectangle((37,150,1038,226),fill='#061e30')
 d.rounded_rectangle((43,211,1037,1235),radius=38,fill='#061e30',outline='#3b647b',width=3)
 d.rounded_rectangle((71,242,1009,352),radius=18,fill='#0a2d40')
 text(d,(94,257),'数字の違いを、1つずつ修正',43)
 text(d,(94,319),'架空データによる確認例',22,'#a4c0d2')
 d.rounded_rectangle((83,394,505,649),radius=26,fill='#30242f',outline='#ff8595',width=4)
 text(d,(110,418),'確認前｜B列だけ',29,'#ffc7d0')
 text(d,(129,473),'46',107,'#ff9bad')
 text(d,(285,536),'合計不足',30,'#ffd3db')
 if t>=0.40:
  d.rounded_rectangle((574,394,997,649),radius=26,fill='#143b3d',outline=accent,width=4)
  text(d,(600,418),'確認後｜B列＋C列',28,'#d6fdf8')
  if t>=0.85:
   text(d,(627,473),'75',107,'#b1fff2')
   text(d,(781,536),'検算済',30,'#d4fff9')
 if t>=0.65:
  d.polygon([(523,505),(562,505),(562,487),(587,523),(562,559),(562,541),(523,541)],fill='#ffdb78')
 if t>=1.20:
  d.rounded_rectangle((81,680,999,1093),radius=24,fill='#0d3244',outline='#2c7b86',width=3)
  text(d,(108,695),'実アプリの数式結果で照合',30,'#c5eff0')
  im.paste(proof,(122,744))
 if t>=2.05:
  d.rounded_rectangle((83,1110,996,1195),radius=19,fill='#0e5153')
  text(d,(106,1125),'修正例：合計にC列を追加  ✓',30,'#ffffff')
  text(d,(713,1198),'FICTIONAL DATA / REVIEW ONLY',17,'#b1cad6')
 return im

def render(source,out,source_sha,genre='ai_work',smoke=False):
 if genre not in PALETTES:raise ValueError('unsupported genre')
 if sha256(source)!=source_sha:raise ValueError('source SHA mismatch (fail closed)')
 p=probe(source)
 if (p['codec'],p['width'],p['height'],p['fps'],p['audio'],p['sample_rate']) != ('h264',W,H,'30/1','aac',48000):
  raise ValueError('unsupported source A/V')
 if p['duration']<END/FPS or (not smoke and abs(p['duration']-23.033333)>0.08):
  raise ValueError('unexpected source duration')
 Path(out).parent.mkdir(parents=True,exist_ok=True)
 with tempfile.TemporaryDirectory() as td:
  td=Path(td);proof=still(source,td/'calc.png')
  for i in range(END-START):
   frame(i,proof,genre).save(td/f'frame_{i:03d}.png',compress_level=1)
  graph=(f'[1:v]format=rgba,setpts=PTS-STARTPTS+{START/FPS}/TB[ov];'
    f'[0:v][ov]overlay=0:0:shortest=0:eof_action=pass:repeatlast=0:'
    f"enable='between(n,{START},{END-1})'[v]")
  cmd=['ffmpeg','-v','error','-y','-i',str(source),'-framerate',str(FPS),'-i',str(td/'frame_%03d.png'),
   '-filter_complex',graph,'-map','[v]','-map','0:a:0','-c:v','libx264','-preset','veryfast',
   '-crf','19','-pix_fmt','yuv420p','-r',str(FPS),'-c:a','copy','-movflags','+faststart',str(out)]
  subprocess.run(cmd,check=True)
 return probe(out)

def smoke_test():
 with tempfile.TemporaryDirectory() as td:
  td=Path(td);s=td/'source.mp4';o=td/'out.mp4'
  subprocess.run(['ffmpeg','-v','error','-y','-f','lavfi','-i','testsrc2=size=1080x1920:rate=30:duration=18',
    '-f','lavfi','-i','sine=frequency=440:sample_rate=48000:duration=18',
    '-c:v','libx264','-preset','ultrafast','-pix_fmt','yuv420p','-c:a','aac','-shortest',str(s)],check=True)
  p=render(s,o,sha256(s),smoke=True)
  subprocess.run(['ffmpeg','-v','error','-i',str(o),'-f','null','-'],check=True)
  assert p['audio']=='aac' and p['width']==1080
  print('PASS synthetic 18s full A/V decode; no private source in CI')

if __name__=='__main__':
 a=argparse.ArgumentParser()
 a.add_argument('--source');a.add_argument('--out');a.add_argument('--source-sha')
 a.add_argument('--genre',default='ai_work',choices=PALETTES.keys());a.add_argument('--smoke',action='store_true')
 x=a.parse_args()
 if x.smoke:smoke_test()
 else:print(json.dumps(render(x.source,x.out,x.source_sha,x.genre),ensure_ascii=False,indent=2))
