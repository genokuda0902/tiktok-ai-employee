#!/usr/bin/env python3
"""All-frame decoded RGB ROI comparison for the 18-frame upper-only loop bridge."""
import argparse,json,subprocess
from pathlib import Path
import numpy as np

def stream(path):
    return subprocess.Popen(['ffmpeg','-v','error','-i',str(path),'-vf','scale=270:480:flags=bilinear',
        '-pix_fmt','rgb24','-f','rawvideo','-'],stdout=subprocess.PIPE,stderr=subprocess.PIPE)

def verify(a,b,report):
    pa,pb=stream(a),stream(b); size=270*480*3
    capmax=0.; upper_unedited_max=0.; edited_sum=0.; edited_count=0
    for i in range(691):
        x=pa.stdout.read(size);y=pb.stdout.read(size)
        if len(x)!=size or len(y)!=size:raise RuntimeError('short decode at frame '+str(i))
        aa=np.frombuffer(x,np.uint8).reshape((480,270,3)).astype(np.int16)
        bb=np.frombuffer(y,np.uint8).reshape((480,270,3)).astype(np.int16)
        capmax=max(capmax,float(np.abs(aa[320:]-bb[320:]).mean()))
        if i<673:upper_unedited_max=max(upper_unedited_max,float(np.abs(aa[:320]-bb[:320]).mean()))
        else:edited_sum+=float(np.abs(aa[:320]-bb[:320]).mean());edited_count+=1
    if pa.stdout.read(1) or pb.stdout.read(1):raise RuntimeError('extra frames')
    for p in (pa,pb):
        if p.wait()!=0:raise RuntimeError(p.stderr.read().decode(errors='replace')[-1000:])
    result={'all_frames_compared':691,'protected_caption_roi_max_mae_255':round(capmax,4),
            'upper_outside_transition_max_mae_255':round(upper_unedited_max,4),
            'upper_transition_mean_mae_255':round(edited_sum/edited_count,4),
            'protected_caption_visual_meaning':'NOT_INDEPENDENTLY_VERIFIED'}
    if capmax>2.5:raise RuntimeError('caption region changed too much')
    Path(report).write_text(json.dumps(result,indent=2))
    return result
if __name__=='__main__':
    p=argparse.ArgumentParser()
    for n in ('source','dest','report'):p.add_argument('--'+n,required=True)
    a=p.parse_args();print(json.dumps(verify(a.source,a.dest,a.report)))
