"""Cycle1108 review-only Japanese hook legibility renderer, NOT v33 original.

Creates two legible hook stages over an existing local preview. Strict source SHA,
private-data and publication gates. No external asset download, upload or posting.
"""
from __future__ import annotations
import argparse, hashlib, json, subprocess, tempfile
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

GENRES=('ai_work','money','career','business','health','study','lifestyle','technology','travel','mindset')
ACCENTS=dict(zip(GENRES,('#43ded0','#6bd6ad','#82cfff','#54d7c7','#89d8b5','#7bd8ef','#75d6cc','#69d5ff','#87dcc9','#a0caff')))
FONT='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
SAFE=(66,146,1014,550)
CAPTION_START_Y=1280
START,SECOND,END=0.0,0.70,1.45

def sha(path):
 h=hashlib.sha256()
 with open(path,'rb') as f:
  for chunk in iter(lambda:f.read(1<<20),b''):h.update(chunk)
 return h.hexdigest()

def cmd(args):
 p=subprocess.run(args,capture_output=True,text=True)
 if p.returncode:raise RuntimeError('ffmpeg/ffprobe failed: '+p.stderr[-2500:])
 return p.stdout

def probe(path):
 return json.loads(cmd(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(path)]))

def audio_hash(path):
 with tempfile.TemporaryDirectory() as td:
  p=Path(td)/'audio.aac'
  cmd(['ffmpeg','-v','error','-y','-i',str(path),'-map','0:a:0','-c:a','copy','-f','adts',str(p)])
  return sha(p)

def validate(m):
 if set(m)!={'genre','review_only','rights_status','contains_private_data','synthetic_scenario','headline','next_step'}:
  raise ValueError('strict manifest keys required')
 if m['genre'] not in GENRES:raise ValueError('unsupported genre')
 if m['review_only'] is not True or m['synthetic_scenario'] is not True:
  raise ValueError('review-only gate')
 if m['rights_status']!='unverified' or m['contains_private_data'] is not False:
  raise ValueError('rights/privacy gate')
 if not isinstance(m['headline'],list) or len(m['headline'])!=2 or any(not isinstance(x,str) or not 1<=len(x)<=14 for x in m['headline']):
  raise ValueError('headline schema')
 if not isinstance(m['next_step'],str) or not 1<=len(m['next_step'])<=24:raise ValueError('next step schema')
 if SAFE[3]>=CAPTION_START_Y:raise ValueError('caption collision')
 return m

def make_overlay(m,second,out):
 validate(m)
 accent=ACCENTS[m['genre']]
 im=Image.new('RGBA',(1080,1920),(0,0,0,0));d=ImageDraw.Draw(im)
 d.rounded_rectangle(SAFE,radius=31,fill=(4,17,35,255),outline=accent,width=5)
 f1=ImageFont.truetype(FONT,82);f2=ImageFont.truetype(FONT,94);f3=ImageFont.truetype(FONT,37)
 for text,font,y,fill in ((m['headline'][0],f1,192,'#f8fafc'),(m['headline'][1],f2,303,'#ffe477')):
  bb=d.textbbox((0,0),text,font=font)
  x=(1080-(bb[2]-bb[0]))//2
  d.text((x,y),text,font=font,fill=fill,stroke_width=2,stroke_fill='#03101e')
 d.rounded_rectangle((276,434,804,446),radius=6,fill=accent)
 if second:
  d.rounded_rectangle((112,467,968,528),radius=16,fill=(15,75,83,255),outline=accent,width=2)
  txt=m['next_step'];bb=d.textbbox((0,0),txt,font=f3)
  d.text(((1080-(bb[2]-bb[0]))//2,473),txt,font=f3,fill='white')
 im.save(out)
 return out

def render(source,out,source_sha,manifest,second=SECOND,end=END):
 validate(manifest)
 if sha(source)!=source_sha:raise ValueError('source SHA mismatch')
 info=probe(source)
 v=next((x for x in info['streams'] if x['codec_type']=='video'),None)
 a=next((x for x in info['streams'] if x['codec_type']=='audio'),None)
 if not v or (v['codec_name'],v['width'],v['height'],v['r_frame_rate'])!=('h264',1080,1920,'30/1'):
  raise ValueError('requires H264 1080x1920 30fps')
 if not a or (a['codec_name'],a['sample_rate'])!=('aac','48000'):
  raise ValueError('requires AAC 48kHz')
 if not .5<second<end<=1.46 or end>float(info['format']['duration']):
  raise ValueError('invalid hook window')
 out=Path(out);out.parent.mkdir(parents=True,exist_ok=True)
 with tempfile.TemporaryDirectory() as td:
  first=make_overlay(manifest,False,Path(td)/'first.png')
  second_png=make_overlay(manifest,True,Path(td)/'second.png')
  fc=(f"[0:v][1:v]overlay=0:0:enable='lt(t,{second})':eof_action=pass[x];"
      f"[x][2:v]overlay=0:0:enable='gte(t,{second})*lt(t,{end})':eof_action=pass[v]")
  cmd(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(source),'-loop','1','-i',str(first),'-loop','1','-i',str(second_png),
       '-filter_complex',fc,'-map','[v]','-map','0:a:0','-c:v','libx264','-preset','veryfast','-crf','18',
       '-pix_fmt','yuv420p','-c:a','copy','-frames:v',str(int(v.get('nb_frames','691'))),'-movflags','+faststart',str(out)])
 q=probe(out);v2=next(x for x in q['streams'] if x['codec_type']=='video')
 return {'source_sha256':source_sha,'output_sha256':sha(out),'duration':float(q['format']['duration']),
         'frames':int(v2.get('nb_frames',0)),'video_codec':v2['codec_name'],'size':[v2['width'],v2['height']],
         'audio_bitstream_identical':audio_hash(source)==audio_hash(out),'audio_sample_rate':a['sample_rate'],
         'changed_seconds':[0,end],'review_only':True,'semantic_voice_caption_alignment':'UNVERIFIED',
         'source_rights':'UNVERIFIED','publication':'NOT_APPROVED'}

def main():
 p=argparse.ArgumentParser()
 for x in ('source','source-sha','manifest','out','report'):p.add_argument('--'+x,required=True)
 args=p.parse_args();m=json.loads(Path(args.manifest).read_text(encoding='utf8'))
 result=render(args.source,args.out,args.source_sha,m)
 Path(args.report).write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf8')
 print(json.dumps(result,ensure_ascii=False))
if __name__=='__main__':main()
