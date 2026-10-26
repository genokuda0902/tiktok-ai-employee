"""Offline media verification; no claim of Japanese ASR or publication approval."""
import argparse, hashlib, json, subprocess
from pathlib import Path
import cv2
import numpy as np

def audio_hash(path):
    p=subprocess.run(['ffmpeg','-v','error','-i',str(path),'-map','0:a:0',
                      '-c:a','copy','-f','adts','-'],capture_output=True,check=True)
    return hashlib.sha256(p.stdout).hexdigest()

def verify(before,after):
    subprocess.run(['ffmpeg','-v','error','-xerror','-i',str(after),'-f','null','-'],
                   check=True,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE,timeout=120)
    old=cv2.VideoCapture(str(before));new=cv2.VideoCapture(str(after))
    if not old.isOpened() or not new.isOpened():raise RuntimeError('unable to open MP4')
    protected=[];outside=[];inside=[];changed=0;total=0
    while True:
        ok1,a=old.read();ok2,b=new.read()
        if ok1!=ok2:raise ValueError('frame count mismatch')
        if not ok1:break
        if a.shape!=(1920,1080,3) or b.shape!=a.shape:raise ValueError('frame shape mismatch')
        # sample 1/4 resolution to avoid excessive memory; check all frames.
        cap=np.abs(a[1490:1920:4,::4].astype('int16')-b[1490:1920:4,::4].astype('int16'))
        protected.append(float(cap.mean()))
        mid=np.abs(a[132:1490:4,::4].astype('int16')-b[132:1490:4,::4].astype('int16'))
        d=float(mid.mean())
        if 510<=total<=587:
            inside.append(d)
            if d>5:changed+=1
        else:outside.append(d)
        total+=1
    old.release();new.release()
    before_a,after_a=audio_hash(before),audio_hash(after)
    checks={
      'frames_691':total==691,
      'audio_stream_identical':before_a==after_a,
      'all_caption_strips_preserved':max(protected)<1.0,
      'outside_scene_unchanged':max(outside)<1.0,
      'new_scene_has_visible_change':changed>=70,
      'full_audio_video_decode':True,
    }
    return {'checks':checks,'all_pass':all(checks.values()),'frames':total,
            'modified_scene_frames_above_delta5':changed,
            'inside_scene_mean_delta':float(np.mean(inside)),
            'caption_region_max_mean_delta':max(protected),
            'outside_scene_max_mean_delta':max(outside),
            'source_audio_adts_sha256':before_a,'output_audio_adts_sha256':after_a,
            'limitations':['no independent Japanese ASR / speech-caption semantic timing',
                           'no real smartphone playback','no inherited source rights clearance',
                           'no v33 source MP4 comparison','no employee approval']}
if __name__=='__main__':
 p=argparse.ArgumentParser()
 for name in ('before','after','report'):p.add_argument('--'+name,required=True)
 a=p.parse_args();result=verify(Path(a.before),Path(a.after))
 Path(a.report).write_text(json.dumps(result,ensure_ascii=False,indent=2))
 print(json.dumps(result,ensure_ascii=False))
 if not result['all_pass']:raise SystemExit(1)