"""Review-only formula/cell focus in an existing fictional Calc screen recording.

10-genre palette, SHA-pinned local source, fail-closed private-data/release gate.
This is a reimplementation; it does not recover v33 or certify Japanese ASR.
"""
import argparse
import hashlib
import json
import subprocess
import tempfile
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

FPS=30
START=195                 # 6.500s; inside chapter 03 (Calc recording)
COUNT=54                  # end at 8.300s, before chapter 04 at ~8.8s
SAFE_BOTTOM=825           # no overlays in chapter/status/caption area
PALETTES={
 'ai_work':'#35E4DB','money':'#F1C267','career':'#75BAF7',
 'business':'#6ED9AE','health':'#FFA09B','study':'#B7A5F8',
 'lifestyle':'#F5ADD4','technology':'#66D7FC','travel':'#FFCF8D',
 'mindset':'#A6E7BE'}
FORMULA_RECT=(350,343,820,403)
TOTAL_RECT=(230,699,580,773)
FONT='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'


def sha(path):
 h=hashlib.sha256()
 with open(path,'rb') as f:
  for b in iter(lambda:f.read(1<<20),b''): h.update(b)
 return h.hexdigest()


def run(args):
 p=subprocess.run(args,capture_output=True,text=True)
 if p.returncode: raise RuntimeError(f'{args[0]} failed: {p.stderr[-1500:]}')
 return p.stdout


def validate(manifest):
 keys={'genre','synthetic_scenario','review_only','rights_status','contains_private_data'}
 if set(manifest)!=keys: raise ValueError('manifest schema mismatch')
 if manifest['genre'] not in PALETTES: raise ValueError('unsupported genre')
 if manifest['synthetic_scenario'] is not True or manifest['review_only'] is not True:
  raise ValueError('review gate failed')
 if manifest['rights_status']!='unverified' or manifest['contains_private_data'] is not False:
  raise ValueError('privacy/rights gate failed')
 if START+COUNT>264: raise ValueError('chapter boundary overlap')
 for x0,y0,x1,y1 in (FORMULA_RECT,TOTAL_RECT):
  if not (60<=x0<x1<=900 and 240<=y0<y1<SAFE_BOTTOM):
   raise ValueError('unsafe focus geometry')
 return True


def ease(x):
 x=max(0,min(1,x));return x*x*(3-2*x)


def overlay(frame,genre):
 if not 0<=frame<COUNT: raise ValueError('frame outside range')
 if genre not in PALETTES: raise ValueError('unsupported genre')
 rgb=tuple(bytes.fromhex(PALETTES[genre][1:]))
 stage=0 if frame<27 else 1
 j=frame%27
 opacity=round(220*min(ease(j/6),ease((26-j)/6)))
 rect=FORMULA_RECT if stage==0 else TOTAL_RECT
 label='数式を確認  =SUM(C2:C4)' if stage==0 else '合計欄を確認  46 / 29'
 im=Image.new('RGBA',(1080,SAFE_BOTTOM),(0,0,0,0))
 d=ImageDraw.Draw(im)
 x0,y0,x1,y1=rect
 # Halo, followed by precise thin focus frame. No synthetic spreadsheet values.
 for delta,alpha,width in [(8,opacity//5,9),(3,opacity//3,5),(0,opacity,4)]:
  d.rounded_rectangle((x0-delta,y0-delta,x1+delta,y1+delta),radius=12,
                      outline=rgb+(alpha,),width=width)
 # Floating caption sits below the recorded sheet, away from source cells.
 box=(160,222,920,286)
 d.rounded_rectangle(box,radius=15,fill=(2,25,42,round(opacity*.75)),outline=rgb+(opacity,),width=3)
 font=ImageFont.truetype(FONT,31)
 d.text((181,231),label,font=font,fill=(255,255,255,opacity))
 return im


def probe(path):
 return json.loads(run(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(path)]))


def adts_sha(path):
 with tempfile.TemporaryDirectory() as t:
  p=Path(t)/'a.aac'
  run(['ffmpeg','-v','error','-y','-i',str(path),'-map','0:a:0','-c:a','copy','-f','adts',str(p)])
  return sha(p)


def render(source,out,source_sha,manifest):
 validate(manifest)
 if sha(source)!=source_sha: raise ValueError('source SHA mismatch')
 p=probe(source)
 v=next((x for x in p['streams'] if x['codec_type']=='video'),None)
 a=next((x for x in p['streams'] if x['codec_type']=='audio'),None)
 if not v or not a: raise ValueError('both video and audio required')
 if (v['codec_name'],v['width'],v['height'],v['r_frame_rate'])!=('h264',1080,1920,'30/1'):
  raise ValueError('source must be H264 1080x1920 30fps')
 if a['codec_name']!='aac' or a['sample_rate']!='48000':
  raise ValueError('source must be AAC 48kHz')
 n=int(v.get('nb_frames') or round(float(p['format']['duration'])*FPS))
 if n<START+COUNT: raise ValueError('source too short')
 out=Path(out);out.parent.mkdir(parents=True,exist_ok=True)
 with tempfile.TemporaryDirectory() as t:
  for i in range(COUNT): overlay(i,manifest['genre']).save(Path(t)/f'focus_{i:03}.png')
  run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(source),
       '-itsoffset',str(START/FPS),'-framerate','30','-start_number','0',
       '-i',str(Path(t)/'focus_%03d.png'),
       '-filter_complex','[0:v][1:v]overlay=0:0:eof_action=pass:shortest=0:format=auto[v]',
       '-map','[v]','-map','0:a:0','-c:v','libx264','-preset','veryfast',
       '-crf','18','-pix_fmt','yuv420p','-c:a','copy','-frames:v',str(n),
       '-movflags','+faststart',str(out)])
 return {'source_sha256':source_sha,'output_sha256':sha(out),
         'audio_bitstream_identical':adts_sha(source)==adts_sha(out),
         'frame_window':[START,START+COUNT-1],
         'release':'HUMAN_REVIEW / PUBLICATION_NOT_APPROVED',
         'japanese_asr':'NOT_VERIFIED','real_phone_playback':'NOT_VERIFIED'}


def main():
 p=argparse.ArgumentParser()
 p.add_argument('--source',required=True);p.add_argument('--source-sha',required=True)
 p.add_argument('--out',required=True);p.add_argument('--manifest',required=True);p.add_argument('--report')
 a=p.parse_args()
 m=json.loads(Path(a.manifest).read_text(encoding='utf-8'))
 result=render(a.source,a.out,a.source_sha,m)
 if a.report: Path(a.report).write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
 print(json.dumps(result,ensure_ascii=False,indent=2))

if __name__=='__main__': main()
