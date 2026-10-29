"""Local-only completed-video checks; no private media uploaded to CI."""
import argparse,hashlib,json,subprocess
import cv2,numpy as np
from pathlib import Path

def sh(path):
 h=hashlib.sha256()
 with open(path,'rb') as f:
  for b in iter(lambda:f.read(1<<20),b''):h.update(b)
 return h.hexdigest()

def call(cmd):
 p=subprocess.run(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=180)
 if p.returncode:raise RuntimeError(p.stderr.decode()[-1200:])
 return p.stdout

def probe(path):return json.loads(call(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(path)]))
def audio_hash(path):return hashlib.sha256(call(['ffmpeg','-v','error','-i',str(path),'-map','0:a:0','-c','copy','-f','adts','-'])).hexdigest()

def check(src,dst):
 s=probe(src);o=probe(dst)
 v=next(x for x in o['streams'] if x['codec_type']=='video')
 a=next(x for x in o['streams'] if x['codec_type']=='audio')
 assert v['codec_name']=='h264' and (v['width'],v['height'])==(1080,1920)
 assert v['avg_frame_rate']=='30/1' and int(v['nb_frames'])==691
 assert a['codec_name']=='aac' and int(a['sample_rate'])==48000 and a['channels']==2
 assert abs(float(o['format']['duration'])-691/30)<.02
 for selector in ('0:v:0','0:a:0'):
  call(['ffmpeg','-v','error','-xerror','-i',str(dst),'-map',selector,'-f','null','-'])
 assert audio_hash(src)==audio_hash(dst),'Japanese AAC stream changed'
 x=cv2.VideoCapture(str(src));y=cv2.VideoCapture(str(dst))
 n=0;max_protected=0.;changed=[];outside=[]
 while True:
  aok,aa=x.read();bok,bb=y.read()
  if not aok and not bok:break
  assert aok and bok,'frame count mismatch'
  protected_a=cv2.resize(aa[1490:1850],(270,90));protected_b=cv2.resize(bb[1490:1850],(270,90))
  delta=float(np.abs(protected_a.astype(np.int16)-protected_b.astype(np.int16)).mean())
  max_protected=max(max_protected,delta)
  roi_a=cv2.resize(aa[150:1350],(135,150));roi_b=cv2.resize(bb[150:1350],(135,150))
  diff=float(np.abs(roi_a.astype(np.int16)-roi_b.astype(np.int16)).mean())
  (changed if 348<=n<435 else outside).append(diff)
  n+=1
 x.release();y.release()
 assert n==691
 assert max_protected<3.0, max_protected
 assert np.mean(changed)>20, np.mean(changed)
 assert max(outside)<4, max(outside)
 return {'source_sha256':sh(src),'output_sha256':sh(dst),'duration_seconds':float(o['format']['duration']),
         'resolution':'1080x1920','video':'H.264 30fps 691 frames full decode PASS',
         'audio':'AAC 48kHz stereo full decode PASS','audio_adts_sha256':audio_hash(dst),
         'audio_bitstream_identical':True,'protected_caption_roi_max_mean_pixel_delta':round(max_protected,4),
         'changed_scene_mean_pixel_delta':round(float(np.mean(changed)),4),
         'outside_scene_max_mean_pixel_delta':round(float(max(outside)),4),
         'japanese_speech_content_independent_asr':'NOT TESTED',
         'smartphone_playback':'NOT TESTED','publication':'NOT APPROVED'}

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('source');p.add_argument('output');p.add_argument('report');a=p.parse_args()
 result=check(a.source,a.output)
 Path(a.report).write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
 print(json.dumps(result,ensure_ascii=False))
