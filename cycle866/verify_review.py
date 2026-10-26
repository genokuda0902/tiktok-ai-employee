"""cycle866 private local QA: stream identity, full decode, region safety.
No claim of semantic speech/caption alignment or publication rights.
"""
from __future__ import annotations
import argparse,json,subprocess,tempfile
from pathlib import Path
import cv2
import numpy as np
from clean_story_panel import sha256,media_info,START,COUNT,FRAMES

def get_frame(cap,idx):
    cap.set(cv2.CAP_PROP_POS_FRAMES,idx)
    ok,frame=cap.read()
    if not ok: raise RuntimeError(f'cannot read frame {idx}')
    return frame

def verify(src,out):
    src,out=Path(src),Path(out)
    media_info(src);media_info(out)
    for p in (src,out):
        subprocess.run(['ffmpeg','-hide_banner','-v','error','-xerror','-i',str(p),'-f','null','-'],check=True,timeout=150)
    with tempfile.TemporaryDirectory() as d:
        hashes=[]
        for j,p in enumerate((src,out)):
            a=Path(d)/f'{j}.aac'
            subprocess.run(['ffmpeg','-v','error','-i',str(p),'-map','0:a:0',
                            '-c:a','copy','-f','adts',str(a)],check=True,timeout=50)
            hashes.append(sha256(a))
    if hashes[0]!=hashes[1]: raise RuntimeError('Japanese audio AAC changed')
    a,b=cv2.VideoCapture(str(src)),cv2.VideoCapture(str(out))
    samples=[]
    try:
        for i in (40,169,172,190,216,248,250,340,680):
            old,new=get_frame(a,i),get_frame(b,i)
            delta=np.abs(old.astype(np.float32)-new.astype(np.float32))
            samples.append({'frame':i,'scene_delta':round(float(delta[330:1450].mean()),3),
                            'caption_delta':round(float(delta[1490:1840].mean()),3)})
    finally: a.release();b.release()
    scene=[x for x in samples if START<=x['frame']<START+COUNT]
    if any(x['scene_delta']<=15 for x in scene):raise RuntimeError('scene was not materially changed')
    if any(x['caption_delta']>=2.0 for x in samples):raise RuntimeError('caption region damaged')
    if any(x['scene_delta']>=3 for x in samples if x['frame']<START or x['frame']>=START+COUNT):
        raise RuntimeError('outside target scene changed too much')
    return {'source_sha256':sha256(src),'output_sha256':sha256(out),
            'video_codec':'h264','audio_codec':'aac','width':1080,'height':1920,
            'fps':30,'frame_count':FRAMES,'duration_seconds':round(FRAMES/30,3),
            'audio_adts_sha256':hashes[0],'audio_bit_identical':True,
            'full_video_audio_decode':True,'caption_safe_region_preserved':True,
            'sampled_frame_differences':samples,
            'speech_language_content_independently_verified':False,
            'speech_caption_semantics_verified':False,'phone_playback_verified':False,
            'asset_rights_approved':False,'employee_approved':False,
            'publication_approved':False}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('source');p.add_argument('output');p.add_argument('report');a=p.parse_args()
    report=verify(a.source,a.output)
    Path(a.report).write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(report,ensure_ascii=False,indent=2))