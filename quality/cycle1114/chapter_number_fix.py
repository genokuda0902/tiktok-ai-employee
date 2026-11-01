#!/usr/bin/env python3
"""Correct mismatched scene02 header 01/08 -> 02/08 (review only).

Only the two-character header number is replaced. No audio, subtitles, body,
confidential data, or posting rights are modified. Generic ten-genre palette.
"""
from __future__ import annotations
import argparse,hashlib,json,subprocess,tempfile
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont

PALETTES={
 'ai':('#0c3341','#68ded4'), 'business':('#0c3341','#74d6f5'),
 'money':('#0c3341','#f5d88c'), 'learning':('#0c3341','#8ed8ff'),
 'health':('#0c3341','#7de8c5'), 'food':('#0c3341','#ffc18d'),
 'travel':('#0c3341','#8fe4ef'), 'beauty':('#0c3341','#ffb9d9'),
 'career':('#0c3341','#9dcaff'), 'life':('#0c3341','#c2e5a6')}
FONT='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
DEFAULT_TIMES=(2.9,5.8)
# x182..230, y99..139, within the top header only. Subtitles begin y1280.
PATCH=(182,99,230,139)

def sha(p):
 h=hashlib.sha256()
 with open(p,'rb') as f:
  for part in iter(lambda:f.read(1048576),b''):h.update(part)
 return h.hexdigest()

def run(cmd):return subprocess.run(cmd,check=True,capture_output=True,text=True).stdout

def probe(path):return json.loads(run(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(path)]))

def validate(source,output,expected_sha,genre,scene_index,total,times):
 if genre not in PALETTES:raise ValueError('unknown genre')
 if scene_index!=2 or total!=8:raise ValueError('only observed scene 02/08 correction allowed')
 if Path(source).resolve()==Path(output).resolve():raise ValueError('source overwrite forbidden')
 if sha(source)!=expected_sha:raise ValueError('source SHA mismatch')
 if len(times)!=2 or not (0<=times[0]<times[1]):raise ValueError('invalid time range')
 p=probe(source);v=next((s for s in p['streams'] if s['codec_type']=='video'),None)
 a=next((s for s in p['streams'] if s['codec_type']=='audio'),None)
 if not v or (v['codec_name'],int(v['width']),int(v['height']),v['r_frame_rate'])!=('h264',1080,1920,'30/1'):raise ValueError('requires 1080x1920 H264 30fps')
 if not a or (a['codec_name'],a['sample_rate'])!=('aac','48000'):raise ValueError('requires AAC 48kHz')
 if times[1]>float(p['format']['duration'])+.03:raise ValueError('invalid time range')
 if PATCH[3]>=180:raise ValueError('protected content region')
 return int(v['nb_frames'])

def make_patch(path,genre,scene_index=2,total=8):
 if genre not in PALETTES or scene_index!=2 or total!=8:raise ValueError('unapproved replacement')
 bg,fg=PALETTES[genre]
 im=Image.new('RGBA',(1080,1920),(0,0,0,0));d=ImageDraw.Draw(im)
 x1,y1,x2,y2=PATCH
 d.rectangle((x1,y1,x2,y2),fill=bg)
 font=ImageFont.truetype(FONT,33)
 d.text((x1+1,y1+1),f'{scene_index:02d}',font=font,fill=fg)
 im.save(path)
 return path

def audio_sha(path):
 p=subprocess.run(['ffmpeg','-v','error','-i',str(path),'-map','0:a:0','-c:a','copy','-f','adts','-'],check=True,capture_output=True)
 return hashlib.sha256(p.stdout).hexdigest()

def render(source,output,expected_sha,genre='ai',scene_index=2,total=8,times=DEFAULT_TIMES):
 n=validate(source,output,expected_sha,genre,scene_index,total,times)
 Path(output).parent.mkdir(parents=True,exist_ok=True)
 with tempfile.TemporaryDirectory() as td:
  png=make_patch(Path(td)/'patch.png',genre,scene_index,total)
  filt=f"[0:v][1:v]overlay=0:0:enable='gte(t,{times[0]})*lt(t,{times[1]})':eof_action=pass,format=yuv420p[v]"
  run(['ffmpeg','-nostdin','-hide_banner','-loglevel','error','-y','-i',str(source),'-loop','1','-i',str(png),
       '-filter_complex',filt,'-map','[v]','-map','0:a:0','-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p','-c:a','copy','-frames:v',str(n),'-movflags','+faststart',str(output)])
 q=probe(output);v=next(s for s in q['streams'] if s['codec_type']=='video')
 if int(v['nb_frames'])!=n:raise RuntimeError('frame count changed')
 return {'source_sha256':expected_sha,'output_sha256':sha(output),'frames':n,'duration':float(q['format']['duration']),
         'change':'scene02 header STEP 01/08 -> STEP 02/08','edited_seconds':list(times),
         'audio_bitstream_identical':audio_sha(source)==audio_sha(output),'japanese_asr':'UNVERIFIED',
         'caption_semantic_match':'UNVERIFIED','rights':'UNVERIFIED','publication':'NOT_APPROVED'}
if __name__=='__main__':
 p=argparse.ArgumentParser()
 for k in ('source','source-sha','out','report'):p.add_argument('--'+k,required=True)
 p.add_argument('--genre',default='ai',choices=PALETTES)
 a=p.parse_args();r=render(a.source,a.out,a.source_sha,a.genre)
 Path(a.report).write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf8');print(json.dumps(r,ensure_ascii=False))
