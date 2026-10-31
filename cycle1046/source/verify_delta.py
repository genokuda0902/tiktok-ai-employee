"""Visual QA comparing source and review-only MP4 without uploading media."""
import cv2, numpy as np, json, argparse
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--before',required=True);p.add_argument('--after',required=True);p.add_argument('--out',required=True);a=p.parse_args()
b=cv2.VideoCapture(a.before);c=cv2.VideoCapture(a.after)
protected=[]; changed=[]; unchanged=[]; n=0
while True:
    ok,x=b.read(); ok2,y=c.read()
    if not ok and not ok2:break
    if not(ok and ok2):raise RuntimeError('different frame counts')
    x=cv2.resize(x,(270,480));y=cv2.resize(y,(270,480))
    delta=np.abs(x.astype(np.float32)-y.astype(np.float32))
    protected.append(float(delta[365:,:,:].mean()))
    (changed if 87<=n<174 else unchanged).append(float(delta[:365,:,:].mean()))
    n+=1
b.release();c.release()
if n!=691:raise RuntimeError('unexpected frame count')
if max(protected)>2:raise RuntimeError('subtitle protected ROI drift too high')
if max(unchanged)>2:raise RuntimeError('unmodified scenes drift too high')
if np.mean(changed)<12:raise RuntimeError('scene change not meaningful')
report={'frames':n,'protected_caption_roi_y':'1460..1919','protected_roi_max_mae_255':max(protected),'unmodified_upper_roi_max_mae_255':max(unchanged),'changed_upper_roi_mean_mae_255':float(np.mean(changed)),'visual_qa':'PASS','speech_semantics':'NOT_VERIFIED','smartphone_playback':'NOT_VERIFIED'}
Path(a.out).write_text(json.dumps(report,indent=2,ensure_ascii=False))
print(json.dumps(report,ensure_ascii=False))
