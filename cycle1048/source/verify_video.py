#!/usr/bin/env python3
"""Compare all frames with FFmpeg-decoded source; do not infer semantic quality."""
import argparse,json,subprocess,hashlib
import cv2,numpy as np
from pathlib import Path

def probe(path):
    return json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',path]))

def verify(old,new):
    a,b=cv2.VideoCapture(str(old)),cv2.VideoCapture(str(new))
    n=0; protected=[]; changed=[];outside=[]
    while True:
        ok1,f=a.read();ok2,g=b.read()
        if ok1!=ok2: raise ValueError('unequal video frame counts')
        if not ok1: break
        f=cv2.resize(f,(270,480),interpolation=cv2.INTER_AREA)
        g=cv2.resize(g,(270,480),interpolation=cv2.INTER_AREA)
        d=cv2.absdiff(f,g)
        protected.append(float(d[365:460].mean()))
        if 609<=n<673: changed.append(float(d[0:365].mean()))
        else: outside.append(float(d[0:365].mean()))
        n+=1
    a.release();b.release()
    p=probe(new)
    v=next(x for x in p['streams'] if x['codec_type']=='video')
    aud=next(x for x in p['streams'] if x['codec_type']=='audio')
    assert n==691 and v['width']==1080 and v['height']==1920 and v['r_frame_rate']=='30/1'
    assert v['codec_name']=='h264' and aud['codec_name']=='aac' and int(aud['sample_rate'])==48000
    assert max(protected)<2 and max(outside)<2 and np.mean(changed)>4
    return {'frames':n,'duration_s':float(p['format']['duration']),
            'video':v['codec_name'],'resolution':'1080x1920','fps':'30/1',
            'audio':aud['codec_name'],'audio_hz':int(aud['sample_rate']),
            'protected_subtitle_roi_max_mae_255':round(max(protected),4),
            'unchanged_upper_roi_max_mae_255':round(max(outside),4),
            'changed_upper_roi_mean_mae_255':round(float(np.mean(changed)),4),
            'changed_frames':len(changed),'full_video_decode':'PASS'}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('old');p.add_argument('new');p.add_argument('report');x=p.parse_args()
    r=verify(x.old,x.new)
    Path(x.report).write_text(json.dumps(r,ensure_ascii=False,indent=2))
    print(json.dumps(r,ensure_ascii=False))
