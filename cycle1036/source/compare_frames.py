"""Local private before/after video comparison. No media upload."""
import argparse,json,cv2,numpy as np

def audit(before,after):
 a,b=cv2.VideoCapture(before),cv2.VideoCapture(after)
 count=0; cap=[]; rest=[]; hero=[]
 while True:
  ok1,x=a.read();ok2,y=b.read()
  if not ok1 and not ok2:break
  if ok1!=ok2:raise RuntimeError('frame count mismatch')
  x=cv2.resize(x,(270,480),interpolation=cv2.INTER_AREA)
  y=cv2.resize(y,(270,480),interpolation=cv2.INTER_AREA)
  diff=cv2.absdiff(x,y).astype(np.float32)
  cap.append(float(diff[372:460,:,:].mean()))
  if count<36:hero.append(float(diff[:300,:,:].mean()))
  else:rest.append(float(diff.mean()))
  count+=1
 a.release();b.release()
 if count!=691:raise RuntimeError('expected 691 frames')
 return {'frames_compared':count,'caption_roi_y':'1490..1840',
  'caption_roi_max_mae_255':round(max(cap),4),
  'caption_roi_p95_mae_255':round(float(np.percentile(cap,95)),4),
  'opening_content_mae_avg_255':round(float(np.mean(hero)),4),
  'opening_content_mae_min_255':round(min(hero),4),
  'after_hook_whole_frame_mae_max_255':round(max(rest),4),
  'after_hook_whole_frame_mae_avg_255':round(float(np.mean(rest)),4)}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('before');p.add_argument('after');p.add_argument('report');z=p.parse_args()
 r=audit(z.before,z.after)
 with open(z.report,'w') as f:json.dump(r,f,indent=2)
 print(json.dumps(r))
