#!/usr/bin/env python3
"""Review-only, genre-neutral ordered focus for existing prompt comparison.

No private media is uploaded or published. A source hash and approval-policy gate
are required. The effect does not synthesize speech or verify Japanese semantics.
"""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess

POLICY = 'HUMAN_REVIEW/PUBLICATION_NOT_APPROVED'
PALETTES = {
 'ai':'30D5CE','business':'E5B769','money':'54C78C','learning':'AC9AFF',
 'health':'72D6C3','food':'F3B679','travel':'79C8ED','beauty':'E4A8D4',
 'career':'F4C277','life':'8FD3A9'
}
# Coordinates are specifically reviewed for the AI-work master; other genres
# need their own approved ROI/timing manifest. No automatic assumption of fit.
DEFAULT_STEPS = [
 {'name':'purpose','start':9.10,'end':9.56,'rect':[477,504,377,118]},
 {'name':'condition','start':9.56,'end':10.04,'rect':[477,627,377,118]},
 {'name':'format','start':10.04,'end':10.52,'rect':[477,747,377,119]},
]
CAPTION_TOP=1280

def run(cmd):
 return subprocess.run(cmd,check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)

def sha256(path):
 h=hashlib.sha256()
 with open(path,'rb') as f:
  for chunk in iter(lambda:f.read(1024*1024),b''): h.update(chunk)
 return h.hexdigest()

def metadata(path):
 j=json.loads(run(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(path)]).stdout)
 v=next(s for s in j['streams'] if s['codec_type']=='video')
 a=next(s for s in j['streams'] if s['codec_type']=='audio')
 return {'width':v['width'],'height':v['height'],'fps':v['avg_frame_rate'],'frames':int(v.get('nb_frames') or 0),
         'duration':float(j['format']['duration']),'video_codec':v['codec_name'],
         'audio_codec':a['codec_name'],'audio_rate':int(a['sample_rate']),'bytes':Path(path).stat().st_size}

def audio_hash(path):
 return hashlib.sha256(run(['ffmpeg','-v','error','-i',str(path),'-map','0:a:0','-c:a','copy','-f','adts','pipe:1']).stdout).hexdigest()

def validate(manifest,source):
 if manifest.get('policy')!=POLICY or manifest.get('asset_approval')!='review_only_no_publication' or manifest.get('manual_post_only') is not True:
  raise ValueError('Publication policy must fail closed')
 if manifest.get('genre') not in PALETTES or manifest.get('source_sha256')!=sha256(source):
  raise ValueError('Genre or source digest invalid')
 m=metadata(source)
 if (m['width'],m['height'],m['fps'],m['video_codec'],m['audio_codec'],m['audio_rate'])!=(1080,1920,'30/1','h264','aac',48000):
  raise ValueError('Unsupported media dimensions/codecs')
 steps=manifest.get('steps')
 if not isinstance(steps,list) or len(steps)!=3: raise ValueError('Exactly three reading steps required')
 previous=0
 for s in steps:
  if s.get('name') not in ('purpose','condition','format'): raise ValueError('Unknown step')
  a,b=s.get('start'),s.get('end'); rect=s.get('rect')
  if not all(isinstance(x,(int,float)) for x in (a,b)) or a<previous or b<=a or b>m['duration']-.15:
   raise ValueError('Invalid or overlapping times')
  if not isinstance(rect,list) or len(rect)!=4 or not all(isinstance(x,int) for x in rect): raise ValueError('Invalid rectangle')
  x,y,w,h=rect
  if x<32 or y<200 or w<60 or h<40 or x+w>1048 or y+h>=CAPTION_TOP-40:
   raise ValueError('Rectangle could touch unsafe areas')
  previous=b
 if [s['name'] for s in steps]!=['purpose','condition','format']:raise ValueError('Reading order invalid')
 return m

def filter_graph(manifest):
 accent=PALETTES[manifest['genre']]
 out=[]
 for i,s in enumerate(manifest['steps']):
  x,y,w,h=s['rect']
  # Outside stroke only, preserving text within each highlighted row.
  # Slightly different luminance for sequential rhythm; no unsupported claim.
  color=('0x'+accent+'@0.90') if i!=1 else '0xF3BD83@0.90'
  out.append(f"drawbox=x={x}:y={y}:w={w}:h={h}:color={color}:t=5:enable='between(t,{s['start']},{s['end']})'")
 return ','.join(out)

def render(source,output,manifest_path,report):
 source,output,manifest_path,report=map(Path,(source,output,manifest_path,report))
 if source.resolve()==output.resolve():raise ValueError('Do not overwrite source')
 manifest=json.loads(manifest_path.read_text(encoding='utf-8'))
 before=validate(manifest,source)
 output.parent.mkdir(parents=True,exist_ok=True)
 args=['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(source),'-vf',filter_graph(manifest),
       '-map','0:v:0','-map','0:a:0','-c:v','libx264','-preset','veryfast','-crf','20','-threads','4',
       '-pix_fmt','yuv420p','-c:a','copy','-movflags','+faststart','-t',str(before['duration']),str(output)]
 run(args)
 run(['ffmpeg','-v','error','-xerror','-i',str(output),'-f','null','-'])
 after=metadata(output)
 same_audio=audio_hash(source)==audio_hash(output)
 passed=(same_audio and before['frames']==after['frames'] and abs(before['duration']-after['duration'])<.04)
 result={'policy':POLICY,'source_sha256':sha256(source),'output_sha256':sha256(output),
         'genre':manifest['genre'],'steps':manifest['steps'],'before':before,'after':after,
         'full_av_decode':True,'aac_adts_bit_identical':same_audio,'technical_pass':passed,
         'japanese_asr_verified':False,'caption_semantics_verified':False,
         'rights_approved':False,'employee_approved':False,'publication_approved':False}
 report.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
 if not passed:
  output.unlink(missing_ok=True)
  raise RuntimeError('Output failed A/V QA; removed')
 return result

if __name__=='__main__':
 p=argparse.ArgumentParser()
 for n in ('source','output','manifest','report'):p.add_argument('--'+n,required=True)
 a=p.parse_args()
 print(json.dumps(render(a.source,a.output,a.manifest,a.report),ensure_ascii=False,indent=2))
