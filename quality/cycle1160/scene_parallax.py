#!/usr/bin/env python3
"""Review-only, subtle content-panel parallax for illustrative scenes.

Not a v33 renderer, 3D generation, source-rights approval, or audio/subtitle ASR.
Source video and rights stay private. No external assets or paid API.
"""
import argparse
import hashlib
import json
import math
import subprocess
from pathlib import Path

import cv2
import numpy as np

POLICY = 'HUMAN_REVIEW/PUBLICATION_NOT_APPROVED'
GENRES = ('ai','business','money','learning','health','food','travel','beauty','career','life')
FPS = 30
# The source's central illustration region only. Chapter strip y>=1000,
# captions y>=1280, and the audio meter are intentionally excluded.
ROIS = {
    'robot_open': (96, 466, 744, 490),
    'problem': (120, 480, 340, 320),
    'closing': (92, 495, 720, 320),
    'synthetic_smoke': (54, 132, 840, 836),
}
SCENES = (
    ('robot_open', 0.36, 2.52, 0.029, 5),
    ('problem', 3.18, 5.34, 0.034, -5),
)


def sha256(path):
    h = hashlib.sha256()
    with open(path,'rb') as f:
        for block in iter(lambda: f.read(1024*1024), b''):
            h.update(block)
    return h.hexdigest()


def probe(path):
    p = json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(path)]))
    v = next(s for s in p['streams'] if s['codec_type']=='video')
    a = next(s for s in p['streams'] if s['codec_type']=='audio')
    if (v['codec_name'],int(v['width']),int(v['height']),v['avg_frame_rate']) != ('h264',1080,1920,'30/1'):
        raise ValueError('Expected H264 1080x1920 30fps')
    if (a['codec_name'],int(a['sample_rate'])) != ('aac',48000):
        raise ValueError('Expected AAC 48kHz')
    return float(p['format']['duration']),int(v.get('nb_frames') or round(float(p['format']['duration'])*FPS))


def validate(manifest,source,duration,smoke=False):
    if manifest.get('policy') != POLICY or manifest.get('asset_approval') != 'review_only_no_publication' or manifest.get('manual_post_only') is not True:
        raise ValueError('Fail closed: publication policy')
    if manifest.get('source_sha256') != sha256(source):
        raise ValueError('Source SHA mismatch')
    if manifest.get('genre') not in GENRES or manifest.get('layout_id') != 'eight_scene_v1':
        raise ValueError('Unsupported genre or layout')
    if not smoke and abs(duration - 23.033333) > 0.07:
        raise ValueError('Expected 8-scene review timeline')
    for x,y,w,h in ROIS.values():
        if x<48 or x+w>940 or y<100 or y+h>990:
            raise ValueError('Unsafe ROI: may overlap protected captions')
    return (('synthetic_smoke',0.1,1.7,0.025,3),) if smoke else SCENES


def feather_mask(w,h,border=38):
    xx = np.minimum(np.arange(w),np.arange(w)[::-1])
    yy = np.minimum(np.arange(h),np.arange(h)[::-1])
    ax = np.clip(xx/border,0,1)
    ay = np.clip(yy/border,0,1)
    # Smoothstep avoids a visible rectangular join to the untouched frame.
    ax = ax*ax*(3-2*ax)
    ay = ay*ay*(3-2*ay)
    return (ay[:,None]*ax[None,:]).astype(np.float32)[:,:,None]


def active_scene(t,scenes):
    for name,start,end,zoom,shift in scenes:
        if start <= t < end:
            return name,(t-start)/(end-start),zoom,shift
    return None


def transform_frame(frame,t,scenes,masks=None):
    info = active_scene(t,scenes)
    if info is None:
        return frame,False
    name,phase,zoom,shift=info
    envelope=math.sin(math.pi*phase)**2
    if envelope<1e-5:
        return frame,False
    x,y,w,h=ROIS[name]
    region=frame[y:y+h,x:x+w]
    scale=1.0+zoom*envelope
    # Small opposite horizontal drift on successive illustrative scenes.
    dx=shift*envelope
    m=cv2.getRotationMatrix2D((w/2,h/2),0,scale)
    m[0,2]+=dx
    altered=cv2.warpAffine(region,m,(w,h),flags=cv2.INTER_CUBIC,borderMode=cv2.BORDER_REFLECT_101)
    mask=masks[name] if masks is not None else feather_mask(w,h)
    alpha=mask*min(1.0,envelope*3)
    mixed=np.clip(region.astype(np.float32)*(1-alpha)+altered.astype(np.float32)*alpha,0,255).astype(np.uint8)
    out=frame.copy();out[y:y+h,x:x+w]=mixed
    return out,True


def render(source,output,manifest,report_path,smoke=False):
    source,output,manifest,report_path=map(Path,(source,output,manifest,report_path))
    if source.resolve()==output.resolve():raise ValueError('Never overwrite source')
    m=json.loads(manifest.read_text(encoding='utf-8'))
    duration,expected_frames=probe(source)
    scenes=validate(m,source,duration,smoke)
    output.parent.mkdir(parents=True,exist_ok=True)
    cap=cv2.VideoCapture(str(source));masks={s[0]:feather_mask(ROIS[s[0]][2],ROIS[s[0]][3]) for s in scenes}
    cmd=['ffmpeg','-hide_banner','-loglevel','error','-y',
         '-f','rawvideo','-pix_fmt','bgr24','-s','1080x1920','-r','30','-i','pipe:0',
         '-i',str(source),'-map','0:v:0','-map','1:a:0',
         '-c:v','libx264','-preset','superfast','-crf','19','-pix_fmt','yuv420p','-threads','4',
         '-c:a','copy','-movflags','+faststart','-t',f'{duration:.6f}',str(output)]
    proc=subprocess.Popen(cmd,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
    n=0;changed=0;by_scene={s[0]:0 for s in scenes}
    try:
        while True:
            ok,frame=cap.read()
            if not ok:break
            transformed,flag=transform_frame(frame,n/FPS,scenes,masks)
            proc.stdin.write(transformed.tobytes())
            if flag:
                changed+=1
                by_scene[active_scene(n/FPS,scenes)[0]]+=1
            n+=1
        proc.stdin.close();err=proc.stderr.read().decode(errors='replace');rc=proc.wait()
        if rc:raise RuntimeError('ffmpeg encode failed: '+err[-2000:])
    except Exception:
        try:proc.kill()
        except Exception:pass
        raise
    finally:cap.release()
    out_duration,out_frames=probe(output)
    if n!=expected_frames or out_frames!=expected_frames or abs(out_duration-duration)>0.07:
        raise RuntimeError(f'Frame/duration mismatch source {expected_frames}, decoded {n}, output {out_frames}')
    report={'policy':POLICY,'source_sha256':sha256(source),'output_sha256':sha256(output),
            'genre':m['genre'],'layout_id':m['layout_id'],'duration':out_duration,
            'frames':out_frames,'changed_frames':changed,'changed_by_scene':by_scene,
            'rois':ROIS,'scene_windows':scenes,'japanese_asr_verified':False,
            'subtitle_semantic_timing_verified':False,'source_rights_approved':False,
            'publication_approved':False,'note':'Illustrative panel push-in; NOT 3D or real camera motion'}
    report_path.parent.mkdir(parents=True,exist_ok=True)
    report_path.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    return report

if __name__=='__main__':
    p=argparse.ArgumentParser()
    for arg in ('source','output','manifest','report'):p.add_argument('--'+arg,required=True)
    p.add_argument('--smoke',action='store_true')
    a=p.parse_args()
    print(json.dumps(render(a.source,a.output,a.manifest,a.report,a.smoke),ensure_ascii=False,indent=2))
