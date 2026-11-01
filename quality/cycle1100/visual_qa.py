"""Offline source/output frame QA; no OCR or ASR claims."""
import argparse,json,cv2,numpy as np
from pathlib import Path

def compare(source,output):
 a=cv2.VideoCapture(str(source));b=cv2.VideoCapture(str(output))
 if not a.isOpened() or not b.isOpened():raise RuntimeError('cannot open both videos')
 n=0;changes=[];other=[];captions=[];target=[]
 while True:
  ok,x=a.read();ok2,y=b.read()
  if ok!=ok2:raise RuntimeError('frame count mismatch')
  if not ok:break
  x=cv2.resize(x,(270,480),interpolation=cv2.INTER_AREA).astype(np.int16)
  y=cv2.resize(y,(270,480),interpolation=cv2.INTER_AREA).astype(np.int16)
  d=np.abs(x-y)
  captions.append(float(d[373:460].mean()))
  if 195<=n<249:
   changes.append(float(d.mean()));target.append(float(d[50:210].mean()))
  else:other.append(float(d.mean()))
  n+=1
 a.release();b.release()
 return {'frames_compared':n,'target_frames':len(changes),
         'target_picture_mean_delta':round(float(np.mean(target)),4),
         'target_fullframe_mean_delta':round(float(np.mean(changes)),4),
         'outside_target_max_mean_delta':round(float(max(other)),4),
         'caption_region_max_mean_delta':round(float(max(captions)),4),
         'caption_region_mean_delta':round(float(np.mean(captions)),4),
         'sample_scale':'270x480 quarter-resolution',
         'caption_region':'original y=1492..1840 (approx)',
         'japanese_caption_semantics':'NOT_VERIFIED'}

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('source');p.add_argument('output');p.add_argument('--report');a=p.parse_args()
 r=compare(a.source,a.output)
 if a.report:Path(a.report).write_text(json.dumps(r,ensure_ascii=False,indent=2))
 print(json.dumps(r,ensure_ascii=False,indent=2))
