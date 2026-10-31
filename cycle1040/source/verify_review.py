#!/usr/bin/env python3
"""Offline review metrics; amplitude-only, not Japanese ASR."""
import argparse,hashlib,json,re,subprocess,cv2,numpy as np
from pathlib import Path

def get_frames(p):
 cap=cv2.VideoCapture(str(p))
 while True:
  ok,frame=cap.read()
  if not ok:break
  yield cv2.resize(frame,(270,480),interpolation=cv2.INTER_AREA)
 cap.release()

def parse_srt(p):
 s=Path(p).read_text(encoding='utf-8-sig').strip().split('\n\n');c=[]
 for block in s:
  lines=block.strip().splitlines();times=lines[1].split(' --> ')
  def seconds(v):
   h,m,rest=v.split(':');return int(h)*3600+int(m)*60+float(rest.replace(',','.'))
  c.append((seconds(times[0]),seconds(times[1]),' '.join(lines[2:])))
 if not c or any(e<=b or not t.strip() for b,e,t in c):raise ValueError('bad SRT')
 if any(c[i][1]>c[i+1][0]+.001 for i in range(len(c)-1)):raise ValueError('overlapping cues')
 return c

def verify(src,dst,srt):
 caps=parse_srt(srt)
 roi=[];upper=[];post=[];frames=0
 for i,(a,b) in enumerate(zip(get_frames(src),get_frames(dst))):
  diff=np.abs(a.astype(np.int16)-b.astype(np.int16))
  roi.append(float(diff[320:460].mean()))
  if i<45:upper.append(float(diff[:320].mean()))
  else:post.append(float(diff[:320].mean()))
  frames+=1
 if frames!=691:raise ValueError('frame count mismatch')
 if len(caps)!=8 or abs(caps[-1][1]-23.033)>.03:raise ValueError('SRT count/end mismatch')
 if max(roi)>3:raise ValueError('caption ROI modified unexpectedly')
 if np.mean(upper)<10:raise ValueError('intro lacks meaningful change')
 if max(post)>3:raise ValueError('post-intro changed unexpectedly')
 return {'frames':frames,'srt_cues':len(caps),'srt_end':caps[-1][1],
         'subtitle_roi_max_mean_abs_delta_255':round(max(roi),4),
         'intro_upper_mean_abs_delta_255':round(float(np.mean(upper)),4),
         'post_intro_upper_max_mean_abs_delta_255':round(max(post),4),
         'subtitle_content_audio_semantic_match':'NOT_VERIFIED',
         'spoken_japanese_independent_asr':'NOT_VERIFIED'}
if __name__=='__main__':
 p=argparse.ArgumentParser()
 for x in ('source','dest','srt','report'):p.add_argument('--'+x,required=True)
 a=p.parse_args();r=verify(a.source,a.dest,a.srt)
 Path(a.report).write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf-8')
 print(json.dumps(r,ensure_ascii=False))
