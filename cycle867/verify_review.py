"""Private QA for cycle867. Pixel tests do not establish spoken-language semantics."""
from __future__ import annotations
import argparse, json, subprocess, tempfile
from pathlib import Path
import cv2
import numpy as np
from audit_focus import media_info,sha256,START,COUNT,FRAMES

def audio_hash(path,folder,label):
    p=Path(folder)/f'{label}.aac'
    subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-i',str(path),
        '-map','0:a:0','-c:a','copy','-f','adts',str(p)],check=True,timeout=50)
    return sha256(p)

def verify(source,output):
    source,output=Path(source),Path(output)
    media_info(source);media_info(output)
    for p in (source,output):
        subprocess.run(['ffmpeg','-hide_banner','-v','error','-xerror','-i',str(p),
                        '-f','null','-'],check=True,timeout=160)
    with tempfile.TemporaryDirectory() as folder:
        a,b=audio_hash(source,folder,'old'),audio_hash(output,folder,'new')
    if a!=b:raise RuntimeError('AAC payload changed')
    cap0=cv2.VideoCapture(str(source));cap1=cv2.VideoCapture(str(output))
    samples=[];caption=[];changed=[];outside=[]
    try:
        for i in range(FRAMES):
            ok0,f0=cap0.read();ok1,f1=cap1.read()
            if not(ok0 and ok1):raise RuntimeError(f'frame {i} unreadable')
            # Check every frame's burned subtitle area, not just 9 sample frames.
            d=np.abs(f0[1490:1840].astype(np.int16)-f1[1490:1840].astype(np.int16))
            caption.append(float(d.mean()))
            if START<=i<START+COUNT:
                # Sample 1/10 changed frames; all frames checked for subtitle integrity.
                if (i-START)%10==0:
                    scene=float(np.abs(f0[132:1490].astype(np.int16)-f1[132:1490].astype(np.int16)).mean())
                    changed.append(scene);samples.append({'frame':i,'scene_delta':round(scene,3),'caption_delta':round(caption[-1],3)})
            elif i in (0,100,335,422,600,690):
                outside.append(float(np.abs(f0[132:1490].astype(np.int16)-f1[132:1490].astype(np.int16)).mean()))
    finally:
        cap0.release();cap1.release()
    if not changed or min(changed)<10:raise RuntimeError('target visual not materially changed')
    if max(caption)>=2.0:raise RuntimeError('burned subtitle region altered')
    if outside and max(outside)>=3.0:raise RuntimeError('unintended out-of-range change')
    return {'source_sha256':sha256(source),'output_sha256':sha256(output),
        'resolution':'1080x1920','video':'H.264 30fps 691 frames',
        'audio':'AAC 48000Hz','duration_seconds':round(FRAMES/30,3),
        'full_video_audio_decode':True,'audio_adts_sha256':a,
        'audio_bit_identical':True,'caption_region_checked_frames':len(caption),
        'caption_region_max_mean_delta':round(max(caption),3),
        'caption_region_p95_mean_delta':round(float(np.percentile(caption,95)),3),
        'caption_region_preserved':True,'target_scene_sample_deltas':samples,
        'outside_scene_sample_max_delta':round(max(outside),3),
        'speech_language_content_independently_verified':False,
        'speech_caption_semantics_verified':False,'phone_playback_verified':False,
        'source_rights_approved':False,'employee_approved':False,
        'publication_approved':False}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('source');p.add_argument('output');p.add_argument('report');a=p.parse_args()
    result=verify(a.source,a.output)
    Path(a.report).write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(result,ensure_ascii=False,indent=2))