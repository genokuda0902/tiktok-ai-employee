"""Review-only Before/After arithmetic verification ribbon for a pre-approved local preview.

New reimplementation; not v33 original. Does not assert productivity gains, voice transcription,
source data accuracy, publication rights or TikTok approval. Input SHA is mandatory.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import subprocess
import tempfile
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

GENRES = ('ai_work','money','career','business','health','study','lifestyle','technology','travel','mindset')
PALETTES = {
 'ai_work':'#26d2c3','money':'#52d7a4','career':'#6fc9ff','business':'#2fcac8',
 'health':'#70d6b0','study':'#6dd3e5','lifestyle':'#65d4c5','technology':'#5bc9ff',
 'travel':'#70d4c7','mindset':'#93c9f7'}
RIBBON = (52,1065,1028,1210)
CAPTION_START_Y = 1280
START, REVEAL, END = 14.3, 15.35, 17.333333
FONT = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'

def sha(path):
 h=hashlib.sha256()
 with open(path,'rb') as f:
  for b in iter(lambda:f.read(1<<20),b''): h.update(b)
 return h.hexdigest()

def run(cmd):
 p=subprocess.run(cmd,capture_output=True,text=True)
 if p.returncode: raise RuntimeError('command failed: '+str(cmd[:4])+'\n'+p.stderr[-3000:])
 return p.stdout

def probe(path):
 return json.loads(run(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(path)]))

def audio_sha(path):
 with tempfile.TemporaryDirectory() as td:
  f=Path(td)/'a.aac'
  run(['ffmpeg','-v','error','-y','-i',str(path),'-map','0:a:0','-c:a','copy','-f','adts',str(f)])
  return sha(f)

def validate(m):
 if set(m) != {'genre','synthetic_scenario','review_only','rights_status','contains_private_data','proof','labels'}:
  raise ValueError('manifest strict keys required')
 if m['genre'] not in GENRES: raise ValueError('unsupported genre')
 if m['synthetic_scenario'] is not True or m['review_only'] is not True: raise ValueError('review-only synthetic gate')
 if m['rights_status']!='unverified' or m['contains_private_data'] is not False: raise ValueError('privacy and rights gate')
 p=m['proof']
 if set(p)!={'operands','total'} or type(p['total'])!=int or not isinstance(p['operands'],list) or len(p['operands'])!=2:
  raise ValueError('invalid proof schema')
 if any(type(v)!=int or v<0 or v>9999 for v in p['operands']) or sum(p['operands'])!=p['total']:
  raise ValueError('incorrect arithmetic')
 labels=m['labels']
 if set(labels)!={'before','after','pending','note'} or any(not isinstance(v,str) or not 1<=len(v)<=45 for v in labels.values()):
  raise ValueError('invalid labels')
 if RIBBON[3]>=CAPTION_START_Y: raise ValueError('caption safe area collision')
 return p

def make_overlay(m,verified,out):
 p=validate(m); accent=PALETTES[m['genre']]
 im=Image.new('RGBA',(1080,1920),(0,0,0,0));d=ImageDraw.Draw(im)
 try:
  f32=ImageFont.truetype(FONT,32);f28=ImageFont.truetype(FONT,28);f23=ImageFont.truetype(FONT,23)
 except OSError:
  f32=ImageFont.load_default();f28=f32;f23=f32
 d.rounded_rectangle(RIBBON,radius=22,fill='#092b3b',outline='#407083',width=3)
 d.rounded_rectangle((70,1080,490,1167),radius=13,fill='#164052' if not verified else '#10313e',outline=accent if not verified else '#355a6a',width=3)
 d.rounded_rectangle((538,1080,1010,1167),radius=13,fill='#104d4d' if verified else '#10313e',outline=accent if verified else '#355a6a',width=3)
 l=m['labels']; before=l['before']; after=l['after']; pending=l['pending']
 d.text((88,1087),before,font=f23,fill=accent if not verified else '#a7bdc8')
 d.text((88,1122),pending,font=f32,fill='#ffffff' if not verified else '#b7cbd2')
 d.text((555,1087),after,font=f23,fill=accent if verified else '#a7bdc8')
 val=f"{p['operands'][0]} + {p['operands'][1]} = {p['total']}" if verified else '照合待ち'
 d.text((555,1122),val,font=f32,fill='#ffffff' if verified else '#9eb6c0')
 d.text((500,1112),'→',font=f28,fill=accent)
 d.text((74,1177),l['note'],font=f23,fill='#a9c5cf')
 im.save(out)
 return out

def render(source,out,expected_sha,manifest,start=START,reveal=REVEAL,end=END):
 validate(manifest)
 if sha(source)!=expected_sha: raise ValueError('input SHA256 mismatch')
 q=probe(source)
 v=next((s for s in q['streams'] if s['codec_type']=='video'),None)
 a=next((s for s in q['streams'] if s['codec_type']=='audio'),None)
 if not v or (v['codec_name'],v['width'],v['height'],v['r_frame_rate'])!=('h264',1080,1920,'30/1'):
  raise ValueError('requires H264 1080x1920 30fps')
 if not a or (a['codec_name'],a['sample_rate'])!=('aac','48000'):
  raise ValueError('requires AAC 48kHz')
 if not 14.25<=start<reveal<end<=17.35 or end>float(q['format']['duration']):
  raise ValueError('invalid scene06 time window')
 out=Path(out);out.parent.mkdir(parents=True,exist_ok=True)
 with tempfile.TemporaryDirectory() as td:
  before=make_overlay(manifest,False,Path(td)/'before.png')
  after=make_overlay(manifest,True,Path(td)/'after.png')
  fc=(f"[0:v][1:v]overlay=0:0:enable='gte(t,{start})*lt(t,{reveal})':eof_action=pass[tmp];"
      f"[tmp][2:v]overlay=0:0:enable='gte(t,{reveal})*lt(t,{end})':eof_action=pass[v]")
  run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(source),'-loop','1','-i',str(before),'-loop','1','-i',str(after),
       '-filter_complex',fc,'-map','[v]','-map','0:a:0','-c:v','libx264','-preset','veryfast','-crf','18',
       '-pix_fmt','yuv420p','-c:a','copy','-frames:v',str(int(v.get('nb_frames','691'))),'-movflags','+faststart',str(out)])
 result=probe(out);vout=next(s for s in result['streams'] if s['codec_type']=='video')
 old_a=audio_sha(source);new_a=audio_sha(out)
 return {'input_sha256':expected_sha,'output_sha256':sha(out),'duration':float(result['format']['duration']),
         'frames':int(vout.get('nb_frames',0)),'audio_bitstream_identical':old_a==new_a,
         'audio_adts_sha256':new_a,'changed_scene_seconds':[start,end],
         'comparison':'before=unverified total; after=arithmetic verified only',
         'arithmetic':f"{manifest['proof']['operands'][0]}+{manifest['proof']['operands'][1]}={manifest['proof']['total']}",
         'speech_transcription':'NOT_VERIFIED','source_data_accuracy':'NOT_VERIFIED',
         'rights':'UNVERIFIED','phone_playback':'NOT_VERIFIED','publication':'NOT_APPROVED'}

def main():
 p=argparse.ArgumentParser();p.add_argument('--source',required=True);p.add_argument('--source-sha',required=True)
 p.add_argument('--manifest',required=True);p.add_argument('--out',required=True);p.add_argument('--report')
 a=p.parse_args();m=json.loads(Path(a.manifest).read_text(encoding='utf-8'))
 result=render(a.source,a.out,a.source_sha,m)
 if a.report: Path(a.report).write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
 print(json.dumps(result,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
