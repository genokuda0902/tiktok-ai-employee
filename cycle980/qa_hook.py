#!/usr/bin/env python3
"""Objective A/V QA; does not assert Japanese semantic correctness."""
import argparse,hashlib,json,subprocess
from pathlib import Path
import cv2,numpy as np
from hook_before_after import probe,sha,HOOK_FRAMES,SAFE_Y

def audio_sha(path):
 p=subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-i',str(path),'-map','0:a:0','-c:a','copy','-f','adts','pipe:1'],check=True,stdout=subprocess.PIPE)
 return hashlib.sha256(p.stdout).hexdigest()

def verify(src,dst):
 n,meta=probe(src);m,ometa=probe(dst)
 assert n==m,'Frame count changed'
 assert audio_sha(src)==audio_sha(dst),'AAC elementary audio changed'
 a=cv2.VideoCapture(str(src));b=cv2.VideoCapture(str(dst))
 capmax=0;outside_max=0;changed=[];frame=0
 while True:
  ok1,x=a.read();ok2,y=b.read()
  if not ok1 and not ok2:break
  assert ok1 and ok2,'Decode length mismatch'
  # 1/4-size ROI proxy, not a pixel-perfect caption guarantee.
  qx=x[SAFE_Y::4,::4];qy=y[SAFE_Y::4,::4]
  capmax=max(capmax,float(np.abs(qx.astype('int16')-qy.astype('int16')).mean()))
  if frame<HOOK_FRAMES:
   changed.append(float(np.abs(x[:SAFE_Y:4,::4].astype('int16')-y[:SAFE_Y:4,::4].astype('int16')).mean()))
  else:
   outside_max=max(outside_max,float(np.abs(x[::8,::8].astype('int16')-y[::8,::8].astype('int16')).mean()))
  frame+=1
 a.release();b.release()
 assert frame==n
 assert capmax<3.0,capmax
 assert outside_max<3.0,outside_max
 assert min(changed)>5.0,min(changed)
 subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-xerror','-i',str(dst),'-f','null','-'],check=True)
 return {'source_sha256':sha(src),'output_sha256':sha(dst),'frames':frame,'resolution':'1080x1920','fps':30,'duration_sec':float(ometa['format']['duration']),'video_codec':ometa['streams'][0]['codec_name'],'audio_codec':ometa['streams'][1]['codec_name'],'audio_sample_rate':ometa['streams'][1]['sample_rate'],'aac_adts_sha256':audio_sha(dst),'aac_unchanged':True,'caption_roi_max_mean_delta_1_4':round(capmax,4),'outside_hook_max_mean_delta_1_8':round(outside_max,4),'hook_mean_delta_1_4':round(sum(changed)/len(changed),4),'hook_min_delta_1_4':round(min(changed),4),'full_av_decode':'PASS','independent_japanese_asr':'NOT_VERIFIED','caption_semantics_timing':'NOT_VERIFIED','publication_approved':False}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--source',required=True);p.add_argument('--output',required=True);p.add_argument('--report',required=True);a=p.parse_args()
 r=verify(Path(a.source),Path(a.output));Path(a.report).write_text(json.dumps(r,ensure_ascii=False,indent=2));print(json.dumps(r,ensure_ascii=False,indent=2))