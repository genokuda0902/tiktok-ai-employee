"""Review-only 10-genre prompt Before/After cue, not original v33.

Edits only an approved local review source. It does not publish, download assets,
change audio, or claim that a before/after result was measured.
"""
from __future__ import annotations
import argparse, hashlib, json, subprocess, tempfile
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

GENRES=('ai_work','money','career','business','health','study','lifestyle','technology','travel','mindset')
ACCENTS=dict(zip(GENRES,('#43ded0','#6bd6ad','#82cfff','#54d7c7','#89d8b5','#7bd8ef','#75d6cc','#69d5ff','#87dcc9','#a0caff')))
FONT='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
BOX=(62,1045,1018,1210)
CAPTION_START_Y=1280
DEFAULT_TIMES=(8.85,9.80,10.95)

def sha(path):
 h=hashlib.sha256()
 with open(path,'rb') as f:
  for c in iter(lambda:f.read(1048576),b''):h.update(c)
 return h.hexdigest()

def run(args):
 p=subprocess.run(args,capture_output=True,text=True)
 if p.returncode:raise RuntimeError(p.stderr[-1800:])
 return p.stdout

def probe(path):
 return json.loads(run(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(path)]))

def audio_hash(path):
 with tempfile.TemporaryDirectory() as td:
  p=Path(td)/'audio.aac'
  run(['ffmpeg','-v','error','-y','-i',str(path),'-map','0:a:0','-c:a','copy','-f','adts',str(p)])
  return sha(p)

def validate(m):
 if set(m)!={'genre','review_only','rights_status','contains_private_data','synthetic_scenario','before','after'}:
  raise ValueError('manifest keys not exact')
 if m['genre'] not in GENRES:raise ValueError('genre')
 if m['review_only'] is not True or m['rights_status']!='unverified' or m['contains_private_data'] is not False or m['synthetic_scenario'] is not True:
  raise ValueError('fail-closed review/privacy/rights gate')
 for k in ('before','after'):
  if not isinstance(m[k],str) or not 1<=len(m[k])<=20 or any(x in m[k] for x in ('\n','\r','\x00')):
   raise ValueError('unsafe '+k)
 if BOX[3]>=CAPTION_START_Y:raise ValueError('caption collision')
 return m

def overlay_image(m,after,path):
 validate(m)
 im=Image.new('RGBA',(1080,1920),(0,0,0,0));d=ImageDraw.Draw(im)
 accent=ACCENTS[m['genre']]
 d.rounded_rectangle(BOX,radius=25,fill=(4,21,37,248),outline=accent if after else '#a3b1c0',width=5)
 d.rounded_rectangle((84,1067,270,1124),radius=13,fill=accent if after else '#687688')
 tag='AFTER' if after else 'BEFORE'
 ftag=ImageFont.truetype(FONT,32)
 d.text((114,1072),tag,font=ftag,fill='#001a22' if after else 'white')
 f=ImageFont.truetype(FONT,49)
 message=m['after'] if after else m['before']
 bb=d.textbbox((0,0),message,font=f)
 if bb[2]-bb[0]>680:raise ValueError('text does not fit safe box')
 d.text((292,1070),message,font=f,fill='white',stroke_width=1,stroke_fill='#03101e')
 d.text((90,1145),'架空の例・結果を保証しません',font=ImageFont.truetype(FONT,27),fill='#b8cbd5')
 im.save(path)
 return path

def render(source,out,source_sha,m,times=DEFAULT_TIMES):
 validate(m)
 if sha(source)!=source_sha:raise ValueError('source SHA mismatch')
 p=probe(source);v=next((x for x in p['streams'] if x['codec_type']=='video'),None);a=next((x for x in p['streams'] if x['codec_type']=='audio'),None)
 if not v or (v['codec_name'],v['width'],v['height'],v['r_frame_rate'])!=('h264',1080,1920,'30/1'):raise ValueError('video requirements')
 if not a or (a['codec_name'],a['sample_rate'])!=('aac','48000'):raise ValueError('audio requirements')
 start,mid,end=times
 if not (0<=start<mid<end<=float(p['format']['duration']) and .35<=mid-start<=3 and .35<=end-mid<=3):raise ValueError('time bounds')
 out=Path(out);out.parent.mkdir(parents=True,exist_ok=True)
 with tempfile.TemporaryDirectory() as td:
  before=overlay_image(m,False,Path(td)/'before.png');after=overlay_image(m,True,Path(td)/'after.png')
  fc=(f"[0:v][1:v]overlay=0:0:enable='gte(t,{start})*lt(t,{mid})':eof_action=pass[x];"
      f"[x][2:v]overlay=0:0:enable='gte(t,{mid})*lt(t,{end})':eof_action=pass[v]")
  run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(source),'-loop','1','-i',str(before),'-loop','1','-i',str(after),'-filter_complex',fc,'-map','[v]','-map','0:a:0','-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p','-c:a','copy','-frames:v',str(int(v.get('nb_frames','691'))),'-movflags','+faststart',str(out)])
 q=probe(out);v2=next(x for x in q['streams'] if x['codec_type']=='video')
 return {'source_sha256':source_sha,'output_sha256':sha(out),'changed_seconds':list(times),'duration':float(q['format']['duration']),'frames':int(v2['nb_frames']),'size':[v2['width'],v2['height']],'audio_bitstream_identical':audio_hash(source)==audio_hash(out),'review_only':True,'publication':'NOT_APPROVED','speech_caption_semantics':'UNVERIFIED'}

def main():
 p=argparse.ArgumentParser()
 for k in ('source','source-sha','manifest','out','report'):p.add_argument('--'+k,required=True)
 a=p.parse_args();m=json.loads(Path(a.manifest).read_text(encoding='utf8'))
 result=render(a.source,a.out,a.source_sha,m)
 Path(a.report).write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf8')
 print(json.dumps(result,ensure_ascii=False))
if __name__=='__main__':main()
