"""Cycle903: two-line Japanese caption focus + audio pause candidate audit.

Review-only reimplementation. Requires local, non-public source MP4. No ASR:
RMS pause candidates are NOT word alignment or speech transcription.
"""
from __future__ import annotations
import argparse
import array
import hashlib
import json
import math
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import wave

GENRES = ('ai_work','business','education','finance','health','lifestyle',
          'technology','travel','food','entertainment')
SCENES = ((0,88),(89,169),(170,250),(251,335),(336,421),(422,506),(507,587),(588,690))
FPS = 30
TOTAL_FRAMES = 691
W, H = 1080, 226
PANEL_Y = 1490
FONT = '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
POLICY = {
 'human_review_required': True,
 'employee_approval_required': True,
 'publication_approved': False,
 'automatic_posting': False,
 'public_media_upload': False,
 'paid_service': False,
 'merge_without_approval': False,
 'semantic_audio_caption_verified': False,
 'status': 'HUMAN_REVIEW / PUBLICATION_NOT_APPROVED',
}


def sha256(path):
 h=hashlib.sha256()
 with open(path,'rb') as f:
  for chunk in iter(lambda:f.read(1024*1024),b''):
   h.update(chunk)
 return h.hexdigest()


def validate_manifest(data):
 if not isinstance(data,dict) or data.get('genre') not in GENRES:
  raise ValueError('unsupported genre')
 if data.get('publication_approved') is not False or data.get('employee_approval') is not False:
  raise ValueError('review-only source: approval must remain false')
 if data.get('contains_private_data') is not False:
  raise ValueError('private-data review must be explicitly false')
 if not isinstance(data.get('source_sha256'),str) or len(data['source_sha256'])!=64 or any(c not in '0123456789abcdef' for c in data['source_sha256']):
  raise ValueError('exact source SHA256 required')
 captions=data.get('captions')
 if not isinstance(captions,list) or len(captions)!=8:
  raise ValueError('exactly eight scene captions required')
 for c in captions:
  if not isinstance(c,list) or len(c)!=2 or not all(isinstance(x,str) and 1<=len(x)<=36 and '\n' not in x for x in c):
   raise ValueError('two short Japanese caption lines per scene required')
 return captions


def choose_switch_frame(levels, start, end, fps=FPS):
 """Choose low-energy *candidate* around scene midpoint; not semantic alignment."""
 length=end-start+1
 lo=start+int(length*.38); hi=start+int(length*.64)
 if not levels:
  return (lo+hi)//2
 def local_energy(frame):
  center=int(frame/fps*50)
  sl=levels[max(0,center-6):min(len(levels),center+7)]
  return sum(sl)/max(1,len(sl))
 return min(range(lo,hi+1),key=lambda f:(local_energy(f),abs(f-(start+end)/2)))


def read_rms(wav_path):
 """20ms RMS at 16kHz, mono PCM16. BGM can make pauses ambiguous."""
 out=[]
 with wave.open(str(wav_path),'rb') as w:
  if (w.getnchannels(),w.getsampwidth(),w.getframerate()) != (1,2,16000):
   raise ValueError('audio must be mono 16k PCM16')
  while True:
   b=w.readframes(320)
   if not b:break
   x=array.array('h');x.frombytes(b)
   if not x:break
   out.append(math.sqrt(sum(float(v)*v for v in x)/len(x))/32768.0)
 return out


def render_panel(line1,line2,focus,blend=0.0,font_path=FONT):
 from PIL import Image,ImageDraw,ImageFont
 if not Path(font_path).exists():raise FileNotFoundError('Noto CJK font required')
 im=Image.new('RGB',(W,H),(5,14,32));d=ImageDraw.Draw(im)
 # two-stage focus: bright active line, dimmed but still legible other line
 d.rectangle((48,8,1032,216),fill=(7,19,39),outline=(34,89,116),width=2)
 font=ImageFont.truetype(font_path,64)
 alpha=max(0.0,min(1.0,blend))
 active=(246,250,255);muted=(166,186,207)
 c1=tuple(round(active[i]*(1-alpha)+muted[i]*alpha) for i in range(3)) if focus==0 else muted
 c2=tuple(round(muted[i]*(1-alpha)+active[i]*alpha) for i in range(3)) if focus==0 else active
 # focus=0: first line bright, focus=1: second line bright
 if focus==0:
  c1=tuple(round(active[i]*(1-alpha)+muted[i]*alpha) for i in range(3))
  c2=tuple(round(muted[i]*(1-alpha)+active[i]*alpha) for i in range(3))
 else:
  c1=muted;c2=active
 for txt in (line1,line2):
  bb=d.textbbox((0,0),txt,font=font)
  if bb[2]-bb[0]>890:raise ValueError('caption exceeds safe width')
 d.rounded_rectangle((67,42,75,109),radius=4,fill=(65,212,229) if focus==0 else (39,89,115))
 d.rounded_rectangle((67,125,75,192),radius=4,fill=(65,212,229) if focus==1 else (39,89,115))
 d.text((93,36),line1,font=font,fill=c1,stroke_width=0)
 d.text((93,119),line2,font=font,fill=c2,stroke_width=0)
 return im


def run(cmd,quiet=True):
 p=subprocess.run(cmd,stdout=subprocess.PIPE if quiet else None,stderr=subprocess.PIPE if quiet else None,text=True)
 if p.returncode:
  raise RuntimeError(f'command failed ({p.returncode}): {cmd[:4]}\n{p.stderr[-3000:] if quiet else ""}')
 return p.stdout or ''


def probe(path):
 return json.loads(run(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(path)]))


def validate_media(path):
 p=probe(path)
 v=next((s for s in p['streams'] if s['codec_type']=='video'),None)
 a=next((s for s in p['streams'] if s['codec_type']=='audio'),None)
 if not v or not a or v.get('width')!=1080 or v.get('height')!=1920 or v.get('codec_name')!='h264' or a.get('codec_name')!='aac':
  raise ValueError('expected H264 1080x1920 + AAC source')
 if v.get('r_frame_rate')!='30/1':raise ValueError('expected 30fps')
 if int(v.get('nb_frames') or 0)!=TOTAL_FRAMES:raise ValueError('expected 691 frames')
 return p


def build(source,output,manifest,workdir=None):
 from PIL import Image
 source=Path(source).resolve();output=Path(output).resolve()
 if source==output or output.exists():raise ValueError('never overwrite input or output')
 data=json.loads(Path(manifest).read_text(encoding='utf-8'))
 captions=validate_manifest(data)
 if sha256(source)!=data['source_sha256']:raise ValueError('source hash mismatch')
 validate_media(source)
 with tempfile.TemporaryDirectory(prefix='cycle903_',dir=workdir) as tmp:
  tmp=Path(tmp); wav=tmp/'mono.wav'
  run(['ffmpeg','-v','error','-y','-i',str(source),'-vn','-ac','1','-ar','16000','-c:a','pcm_s16le',str(wav)])
  rms=read_rms(wav)
  switches=[choose_switch_frame(rms,a,b) for a,b in SCENES]
  images=tmp/'panels';images.mkdir()
  for i,((a,b),(line1,line2),mid) in enumerate(zip(SCENES,captions,switches)):
   # Each frame links to a small set of static panels, no private media embedded.
   variants={}
   for state in range(7):
    if state==0: im=render_panel(line1,line2,0,0)
    elif state==6:im=render_panel(line1,line2,1,0)
    else:im=render_panel(line1,line2,0,state/6)
    path=images/f's{i}_{state}.png';im.save(path)
    variants[state]=path
   for frame in range(a,b+1):
    if frame<mid-2:state=0
    elif frame>mid+2:state=6
    else:state=frame-(mid-2)+1
    (images/f'f{frame:04d}.png').symlink_to(variants[state].name)
  overlay=tmp/'caption_overlay.mp4'
  run(['ffmpeg','-v','error','-y','-framerate','30','-start_number','0','-i',str(images/'f%04d.png'),
       '-frames:v',str(TOTAL_FRAMES),'-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p',str(overlay)])
  run(['ffmpeg','-v','error','-y','-i',str(source),'-i',str(overlay),
       '-filter_complex',f'[0:v][1:v]overlay=0:{PANEL_Y}:shortest=1[v]',
       '-map','[v]','-map','0:a:0','-c:v','libx264','-preset','veryfast','-crf','18',
       '-pix_fmt','yuv420p','-c:a','copy','-frames:v',str(TOTAL_FRAMES),'-movflags','+faststart',str(output)])
  report={
   'status':POLICY['status'],'source_sha256':sha256(source),'output_sha256':sha256(output),
   'genre':data['genre'],'caption_focus_switch_frames':switches,
   'rms_pause_candidate_only':True,'independent_asr_performed':False,
   'spoken_japanese_semantics_verified':False,'word_level_alignment_verified':False,
   'employee_approval':False,'public_posting_allowed':False,
  }
  return report


def release_gate(report,independent_asr=None):
 """No publication on this cycle. Missing independent ASR must fail closed."""
 if not independent_asr or not report.get('spoken_japanese_semantics_verified'):
  raise PermissionError('PUBLICATION_NOT_APPROVED: independent Japanese ASR/semantic review missing')
 raise PermissionError('PUBLICATION_NOT_APPROVED: employee and rights review missing')


def main():
 p=argparse.ArgumentParser()
 p.add_argument('--source',required=True);p.add_argument('--output',required=True)
 p.add_argument('--manifest',required=True);p.add_argument('--report',required=True)
 a=p.parse_args();report=build(a.source,a.output,a.manifest)
 Path(a.report).write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
 print(json.dumps(report,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
