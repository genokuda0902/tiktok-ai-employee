#!/usr/bin/env python3
"""Review-only first-three-seconds kinetic action cue for ten genres.

Only changes the upper/middle visual ROI. Never changes source audio or subtitles.
Does not establish speech meaning, rights, human approval or v33 equivalence.
"""
import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path

POLICY='HUMAN_REVIEW/PUBLICATION_NOT_APPROVED'
GENRES={
 'ai':'32D8D0','business':'F0BE70','money':'70D89C',
 'learning':'B3A2FF','health':'83DAC9','food':'FFC48D',
 'travel':'86CEFF','beauty':'F2A7D7','career':'F2D181','life':'A2D7AE'
}
FONT='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
CAPTION_TOP=1280
# Per-video reviewed rectangles: x,y,w,h. They avoid headline, chapter HUD, captions.
CARDS=((65,540,225,105),(775,640,240,105),(65,810,225,105))
STARTS=(0.18,0.58,0.98)
END=1.43

def run(args):
 p=subprocess.run(args,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
 if p.returncode: raise RuntimeError('Command failed: '+str(args[:5])+'\n'+p.stderr.decode(errors='replace')[-1500:])
 return p.stdout

def sha(path):
 h=hashlib.sha256()
 with open(path,'rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
 return h.hexdigest()

def probe(path):
 j=json.loads(run(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(path)]))
 v=next(x for x in j['streams'] if x['codec_type']=='video')
 a=next(x for x in j['streams'] if x['codec_type']=='audio')
 return {'width':v['width'],'height':v['height'],'fps':v['avg_frame_rate'],
  'frames':int(v.get('nb_frames',0)),'duration':float(j['format']['duration']),
  'video_codec':v['codec_name'],'audio_codec':a['codec_name'],
  'sample_rate':int(a['sample_rate']),'audio_language':a.get('tags',{}).get('language','und'),
  'bytes':Path(path).stat().st_size}

def aac_sha(path):
 return hashlib.sha256(run(['ffmpeg','-v','error','-i',str(path),'-map','0:a:0','-c:a','copy','-f','adts','pipe:1'])).hexdigest()

def validate(m,source):
 if m.get('policy')!=POLICY or m.get('asset_approval')!='review_only_no_publication' or m.get('manual_post_only') is not True:
  raise ValueError('Fail closed: review-only and manual-post policy')
 if m.get('source_sha256')!=sha(source) or m.get('roi_reviewed') is not True:
  raise ValueError('Fail closed: source hash and reviewed ROI required')
 if m.get('genre') not in GENRES: raise ValueError('Unrecognized genre')
 labels=m.get('hook_labels')
 if not isinstance(labels,list) or len(labels)!=3: raise ValueError('Exactly three hook labels')
 if any(not isinstance(x,str) or not 1<=len(x)<=6 or not re.fullmatch(r'[\u3040-\u30ff\u3400-\u9fff\w・]+',x) for x in labels):
  raise ValueError('Hook labels must be short plain text')
 if m.get('caption_top')!=CAPTION_TOP or m.get('hook_window')!=[0.0,1.45]:
  raise ValueError('Explicit subtitle safe-area and scene review required')
 if any(y+h>=CAPTION_TOP-100 for x,y,w,h in CARDS): raise ValueError('Cards intersect protected caption area')
 p=probe(source)
 if (p['width'],p['height'],p['fps'],p['video_codec'],p['audio_codec'],p['sample_rate'])!=(1080,1920,'30/1','h264','aac',48000):
  raise ValueError('Unsupported media')
 if p['duration']<3.5: raise ValueError('Source too short for hook window')
 return p

def filtergraph(m):
 accent=GENRES[m['genre']]
 f=[]
 # Keep all changes within reviewed intro scene; cards enter in a deliberate 3-beat rhythm.
 for i,((x,y,w,h),start,label) in enumerate(zip(CARDS,STARTS,m['hook_labels'])):
  en=f"enable='between(t,{start:.2f},{END:.2f})'"
  f.append(f'drawbox=x={x}:y={y}:w={w}:h={h}:color=0x031827@0.90:t=fill:{en}')
  f.append(f'drawbox=x={x}:y={y}:w={w}:h={h}:color=0x{accent}@0.93:t=3:{en}')
  f.append(f'drawbox=x={x+10}:y={y+14}:w=44:h=8:color=0x{accent}@1:t=fill:{en}')
  f.append(f"drawtext=fontfile={FONT}:text='{i+1:02d}':fontsize=27:fontcolor=0x{accent}:x={x+15}:y={y+34}:{en}")
  f.append(f"drawtext=fontfile={FONT}:text='{label}':fontsize=44:fontcolor=white:x={x+72}:y={y+24}:{en}")
 # A compact three-step timeline in the safe central area.
 for i in range(3):
  f.append(f"drawbox=x={360+i*120}:y=938:w=113:h=7:color=0x{accent}@0.98:t=fill:enable='between(t,{STARTS[i]:.2f},{END:.2f})'")
 return ','.join(f)

def render(source,output,manifest,report):
 source,output,manifest,report=map(Path,(source,output,manifest,report))
 if source.resolve()==output.resolve(): raise ValueError('Never overwrite source')
 m=json.loads(manifest.read_text(encoding='utf-8'))
 before=validate(m,source)
 output.parent.mkdir(parents=True,exist_ok=True)
 run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(source),'-vf',filtergraph(m),
      '-map','0:v:0','-map','0:a:0','-c:v','libx264','-preset','veryfast','-crf','20',
      '-threads','4','-pix_fmt','yuv420p','-c:a','copy','-movflags','+faststart',
      '-t',str(before['duration']),str(output)])
 run(['ffmpeg','-v','error','-xerror','-i',str(output),'-f','null','-'])
 after=probe(output)
 audio_ok=aac_sha(source)==aac_sha(output)
 ok=audio_ok and before['frames']==after['frames'] and abs(before['duration']-after['duration'])<0.04
 result={'policy':POLICY,'source_sha256':sha(source),'output_sha256':sha(output),
   'genre':m['genre'],'labels':m['hook_labels'],'starts':STARTS,'end':END,
   'before':before,'after':after,'full_av_decode':True,'aac_bit_identical':audio_ok,
   'technical_pass':ok,'independent_japanese_asr':False,
   'speech_caption_semantics_or_timing_verified':False,'smartphone_verified':False,
   'rights_approved':False,'employee_approved':False,'publication_approved':False}
 report.parent.mkdir(parents=True,exist_ok=True)
 report.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
 if not ok:
  output.unlink(missing_ok=True)
  raise RuntimeError('A/V QA failed; deleted output')
 return result

if __name__=='__main__':
 p=argparse.ArgumentParser()
 for n in ('source','output','manifest','report'):p.add_argument('--'+n,required=True)
 a=p.parse_args()
 print(json.dumps(render(a.source,a.output,a.manifest,a.report),ensure_ascii=False,indent=2))
