"""Review-only, genre-agnostic numeric evidence card correction.

No transcription, rights approval, public distribution or v33 reconstruction is implied.
Requires a SHA-pinned, synthetic, review-only H264/AAC input. All source media stays local.
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
# This numeric proof component is reusable, but is not appropriate for every scene in every genre.
PALETTES = {
 'ai_work':('#113b4c','#0e4c49','#27c6b5'), 'money':('#173c4a','#174b43','#37cba1'),
 'career':('#233d58','#174953','#53b9e4'), 'business':('#173c50','#144e50','#31c5c0'),
 'health':('#153d4a','#1a4c45','#46cfac'), 'study':('#1b3c58','#174d53','#53c9da'),
 'lifestyle':('#213d4d','#1a4b4e','#47c6c0'), 'technology':('#15374e','#124b55','#3bcde0'),
 'travel':('#1a4052','#1c514a','#5ac9bc'), 'mindset':('#23394e','#214b52','#61bfe0')}
# Source layout: card interiors are entirely above y=1280, well clear of burned-in subtitles.
CARDS=((74,835,355,1046),(404,835,685,1046),(730,835,1021,1046))
SAFE_Y=1280
DEFAULT_START=14.3
DEFAULT_REVEAL=15.35
DEFAULT_END=17.333333
FONT='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'

def sha(path):
 h=hashlib.sha256()
 with open(path,'rb') as f:
  for b in iter(lambda:f.read(1<<20),b''):h.update(b)
 return h.hexdigest()

def call(args):
 p=subprocess.run(args,capture_output=True,text=True)
 if p.returncode:raise RuntimeError('command failed: '+str(args[:3])+'\n'+p.stderr[-2000:])
 return p.stdout

def probe(path):return json.loads(call(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(path)]))

def audio_sha(path):
 with tempfile.TemporaryDirectory() as td:
  p=Path(td)/'audio.aac'
  call(['ffmpeg','-v','error','-y','-i',str(path),'-map','0:a:0','-c:a','copy','-f','adts',str(p)])
  return sha(p)

def validate(manifest):
 if set(manifest)!={'genre','synthetic_scenario','review_only','rights_status','contains_private_data','proof'}:
  raise ValueError('manifest keys do not match strict allowlist')
 if manifest['genre'] not in GENRES or manifest['genre'] not in PALETTES:raise ValueError('unsupported genre')
 if manifest['synthetic_scenario'] is not True or manifest['review_only'] is not True:
  raise ValueError('not synthetic/review-only')
 if manifest['rights_status']!='unverified' or manifest['contains_private_data'] is not False:
  raise ValueError('source privacy/rights status not allowed')
 p=manifest['proof']
 if set(p)!={'labels','operands','total'} or not isinstance(p['labels'],list) or len(p['labels'])!=2:
  raise ValueError('proof fields mismatch')
 if not all(isinstance(v,str) and 1<=len(v)<=10 for v in p['labels']):raise ValueError('labels invalid')
 if not isinstance(p['operands'],list) or len(p['operands'])!=2 or any(type(v)!=int or v<0 or v>9999 for v in p['operands']):
  raise ValueError('invalid operands')
 if type(p['total'])!=int or p['total']!=sum(p['operands']):
  raise ValueError('arithmetic is inconsistent with source data')
 if any(y1>=SAFE_Y or y2>SAFE_Y for x1,y1,x2,y2 in CARDS):raise ValueError('unsafe caption overlap')
 return p

def make_overlay(manifest,show_total,out):
 p=validate(manifest)
 c1,c3,accent=PALETTES[manifest['genre']]
 im=Image.new('RGBA',(1080,1920),(0,0,0,0));d=ImageDraw.Draw(im)
 try:
  reg=ImageFont.truetype(FONT,32);num=ImageFont.truetype(FONT,77);pending=ImageFont.truetype(FONT,37)
 except OSError:
  reg=ImageFont.load_default();num=reg;pending=reg
 labels=[*p['labels'],'合計']; values=[*p['operands'],p['total'] if show_total else '検算中']
 for i,(x1,y1,x2,y2) in enumerate(CARDS):
  color=c3 if i==2 else c1
  d.rounded_rectangle((x1,y1,x2,y2),radius=18,fill=color,outline=accent if i==2 else '#6b9baa',width=3)
  d.text((x1+18,y1+25),labels[i],font=reg,fill='#d5e7ec')
  val=str(values[i]); f=pending if val=='検算中' else num
  bb=d.textbbox((0,0),val,font=f)
  d.text(((x1+x2-(bb[2]-bb[0]))/2,y1+97 if val!='検算中' else y1+112),val,font=f,fill=accent if i==2 else '#ffffff')
 if show_total:
  d.ellipse((975,855,1002,882),fill=accent)
  d.line((981,867,987,873,995,861),fill='#062b30',width=3,joint='curve')
 im.save(out)
 return out

def render(source,out,expected_sha,manifest,start=DEFAULT_START,reveal=DEFAULT_REVEAL,end=DEFAULT_END):
 validate(manifest)
 if sha(source)!=expected_sha:raise ValueError('input SHA256 mismatch')
 meta=probe(source)
 v=next((x for x in meta['streams'] if x['codec_type']=='video'),None)
 a=next((x for x in meta['streams'] if x['codec_type']=='audio'),None)
 if not v or not a or (v['codec_name'],v['width'],v['height'],v['r_frame_rate'])!=('h264',1080,1920,'30/1'):
  raise ValueError('expected 1080x1920 H264 30fps plus audio')
 if (a['codec_name'],a['sample_rate'])!=('aac','48000'):raise ValueError('expected AAC 48kHz')
 duration=float(meta['format']['duration'])
 if not(0<=start<reveal<end<=duration):raise ValueError('invalid scene timing')
 if end>17.35 or start<14.25:raise ValueError('scene-specific overlay must stay in scene06')
 out=Path(out);out.parent.mkdir(parents=True,exist_ok=True)
 with tempfile.TemporaryDirectory() as td:
  first=make_overlay(manifest,False,Path(td)/'proof_pending.png')
  final=make_overlay(manifest,True,Path(td)/'proof_final.png')
  fc=(f"[0:v][1:v]overlay=0:0:enable='gte(t,{start})*lt(t,{reveal})':eof_action=pass[tmp];"
      f"[tmp][2:v]overlay=0:0:enable='gte(t,{reveal})*lt(t,{end})':eof_action=pass[v]")
  call(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(source),'-loop','1','-i',str(first),'-loop','1','-i',str(final),
        '-filter_complex',fc,'-map','[v]','-map','0:a:0','-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p','-c:a','copy',
        '-frames:v',str(int(v.get('nb_frames','691'))),'-movflags','+faststart',str(out)])
 q=probe(out);vo=next(s for s in q['streams'] if s['codec_type']=='video')
 return {'input_sha256':expected_sha,'output_sha256':sha(out),'duration':float(q['format']['duration']),
         'frames':int(vo.get('nb_frames',0)),'audio_adts_sha256_source':audio_sha(source),
         'audio_adts_sha256_output':audio_sha(out),'audio_bitstream_identical':audio_sha(source)==audio_sha(out),
         'changed_scene_seconds':[start,end],'total_reveal_seconds':reveal,'verified_arithmetic':f"{manifest['proof']['operands'][0]}+{manifest['proof']['operands'][1]}={manifest['proof']['total']}",
         'source_rights':'UNVERIFIED','japanese_speech_semantics':'NOT_VERIFIED','phone_playback':'NOT_VERIFIED',
         'release':'HUMAN_REVIEW / PUBLICATION_NOT_APPROVED'}

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--source',required=True);ap.add_argument('--source-sha',required=True)
 ap.add_argument('--out',required=True);ap.add_argument('--manifest',required=True);ap.add_argument('--report')
 args=ap.parse_args();m=json.loads(Path(args.manifest).read_text(encoding='utf-8'))
 q=render(args.source,args.out,args.source_sha,m)
 if args.report:Path(args.report).write_text(json.dumps(q,ensure_ascii=False,indent=2),encoding='utf-8')
 print(json.dumps(q,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
