"""Frame-complete A/V integrity check, not a Japanese ASR or licensing review."""
from __future__ import annotations
import json,subprocess,tempfile,hashlib
from pathlib import Path
import numpy as np,cv2
from cinematic_closer import sha,media_info,FRAMES,START,COUNT

def stream_sha(p,tmp,label):
 dst=Path(tmp)/(label+'.aac')
 subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-i',str(p),'-map','0:a:0','-c:a','copy','-f','adts',str(dst)],check=True,timeout=30)
 return sha(dst)

def verify(src,out):
 src,out=Path(src),Path(out)
 for p in (src,out):
  media_info(p)
  subprocess.run(['ffmpeg','-hide_banner','-v','error','-xerror','-i',str(p),'-f','null','-'],check=True,timeout=160)
 with tempfile.TemporaryDirectory() as td:
  a,b=stream_sha(src,td,'before'),stream_sha(out,td,'after')
 if a!=b:raise ValueError('inherited AAC stream changed')
 c0=cv2.VideoCapture(str(src));c1=cv2.VideoCapture(str(out))
 caption=[];target=[];outside=[];samples=[]
 try:
  for i in range(FRAMES):
   ok0,f0=c0.read();ok1,f1=c1.read()
   if not (ok0 and ok1):raise ValueError('frame missing '+str(i))
   d=np.abs(f0[1490:1840].astype(np.int16)-f1[1490:1840].astype(np.int16)).mean()
   caption.append(float(d))
   if START<=i<START+COUNT:
    if (i-START)%12==0:
     diff=float(np.abs(f0[132:1490].astype(np.int16)-f1[132:1490].astype(np.int16)).mean())
     target.append(diff);samples.append({'frame':i,'scene_delta':round(diff,3),'subtitle_delta':round(float(d),3)})
   elif i in (0,125,250,400,587):
    outside.append(float(np.abs(f0[132:1490].astype(np.int16)-f1[132:1490].astype(np.int16)).mean()))
 finally:c0.release();c1.release()
 if max(caption)>=2:raise ValueError('subtitle strip changed')
 if min(target)<=10:raise ValueError('new visual not materially different')
 if max(outside)>=3:raise ValueError('unexpected outside-scene edit')
 return {'source_sha256':sha(src),'output_sha256':sha(out),'frame_count':FRAMES,
 'resolution':'1080x1920','video':'H.264 30fps','audio':'AAC 48kHz',
 'duration_seconds':round(FRAMES/30,3),'full_av_decode':True,
 'audio_elementary_sha256':a,'audio_bit_identical':True,
 'subtitle_protected_frames':len(caption),'subtitle_region_max_mean_delta':round(max(caption),3),
 'subtitle_region_p95_mean_delta':round(float(np.percentile(caption,95)),3),
 'outside_scene_sample_max_delta':round(max(outside),3),'scene_samples':samples,
 'independent_japanese_speech_recognition':False,'speech_caption_semantics_verified':False,
 'phone_playback_verified':False,'source_rights_approved':False,'employee_approved':False,
 'publication_approved':False}

if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser();p.add_argument('source');p.add_argument('output');p.add_argument('report');args=p.parse_args()
 r=verify(args.source,args.output)
 Path(args.report).write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf-8')
 print(json.dumps(r,ensure_ascii=False,indent=2))
