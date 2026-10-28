"""cycle941: feather-masked Ken Burns micro-motion for 9:16 review slides.
No paid service, upload, auto-post, or merge. Source audio bitstream copied.
"""
from __future__ import annotations
import argparse, json, math, subprocess
from pathlib import Path

SCENE_EDGES = (0.,2.9,5.8,8.7,11.6,14.5,17.4,20.3,23.04)
MOTION_SCENES = (0,2,6,7)
ROI = (90,350,900,840)
PROFILES = {
 'ai_productivity':.022, 'business':.019, 'finance':.014,
 'education':.019, 'health':.013, 'beauty':.021,
 'food':.020, 'travel':.024, 'lifestyle':.020, 'technology':.022,
}
MAX_PAN_PX = 7.
FEATHER = 50

def eased_pulse(progress):
    if not 0 <= progress <= 1: raise ValueError('progress outside [0,1]')
    return math.sin(math.pi*progress)**2

def scene_at(t):
    if t < 0: raise ValueError('negative time')
    for i,end in enumerate(SCENE_EDGES[1:]):
        if t < end: return i
    return len(SCENE_EDGES)-2

def motion_params(t,genre):
    if genre not in PROFILES: raise ValueError('unknown genre')
    i=scene_at(t)
    if i not in MOTION_SCENES: return 1.,0.,0.
    u=min(1.,max(0.,(t-SCENE_EDGES[i])/(SCENE_EDGES[i+1]-SCENE_EDGES[i])))
    p=eased_pulse(u)
    return 1.+PROFILES[genre]*p, MAX_PAN_PX*p, -MAX_PAN_PX*.45*p

def make_mask(w,h,feather=FEATHER):
    import numpy as np
    if w<=2*feather or h<=2*feather: raise ValueError('ROI too small')
    xx=np.minimum(np.arange(w),np.arange(w)[::-1])
    yy=np.minimum(np.arange(h),np.arange(h)[::-1])
    u=np.clip(np.minimum(yy[:,None],xx[None,:])/feather,0.,1.)
    return (u*u*(3-2*u)).astype('float32')[:,:,None]

def process_frame(frame,t,genre,mask=None):
    import cv2,numpy as np
    if frame.shape[:2]!=(1920,1080): raise ValueError('expected 1080x1920')
    scale,dx,dy=motion_params(t,genre)
    if scale==1.: return frame
    x,y,w,h=ROI
    if mask is None: mask=make_mask(w,h)
    src=frame[y:y+h,x:x+w]
    mat=np.array([[scale,0,(1-scale)*(w-1)/2+dx],
                  [0,scale,(1-scale)*(h-1)/2+dy]],dtype='float32')
    moved=cv2.warpAffine(src,mat,(w,h),flags=cv2.INTER_LINEAR,
                         borderMode=cv2.BORDER_REFLECT_101)
    frame[y:y+h,x:x+w]=np.clip(src*(1-mask)+moved*mask,0,255).astype('uint8')
    return frame

def run(source,output,genre,report):
    import cv2
    source,output,report=Path(source),Path(output),Path(report)
    if genre not in PROFILES: raise ValueError('unknown genre')
    if not source.is_file(): raise FileNotFoundError(source)
    capture=cv2.VideoCapture(str(source))
    fps=capture.get(cv2.CAP_PROP_FPS)
    total=int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
    if abs(fps-30)>.01 or total!=691: raise ValueError('unexpected source fps/frames')
    output.parent.mkdir(parents=True,exist_ok=True)
    video_only=output.with_suffix('.video.mp4')
    command=['ffmpeg','-hide_banner','-loglevel','error','-y',
             '-f','rawvideo','-pixel_format','bgr24',
             '-video_size','1080x1920','-framerate','30','-i','pipe:0',
             '-an','-c:v','libx264','-preset','veryfast','-crf','18',
             '-pix_fmt','yuv420p','-movflags','+faststart',str(video_only)]
    encoder=subprocess.Popen(command,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
    mask=make_mask(ROI[2],ROI[3]);n=0;changed=0
    try:
        while True:
            ok,frame=capture.read()
            if not ok: break
            if motion_params(n/fps,genre)[0]>1.000001:
                changed+=1
                process_frame(frame,n/fps,genre,mask)
            encoder.stdin.write(frame.tobytes());n+=1
        encoder.stdin.close()
        error=encoder.stderr.read().decode('utf8','replace')
        if encoder.wait(): raise RuntimeError('ffmpeg encode '+error[-1000:])
    finally:
        capture.release()
        if encoder.poll() is None: encoder.kill()
    if n!=691: raise RuntimeError('incorrect frame count')
    subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y',
                    '-i',str(video_only),'-i',str(source),
                    '-map','0:v:0','-map','1:a:0','-c:v','copy',
                    '-c:a','copy','-movflags','+faststart',str(output)],
                   check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    video_only.unlink(missing_ok=True)
    result={'genre':genre,'motion_scenes_1_based':[i+1 for i in MOTION_SCENES],
            'roi_xywh':ROI,'max_scale':1+PROFILES[genre],
            'max_pan_px':MAX_PAN_PX,'feather_px':FEATHER,
            'frames':n,'frames_with_motion':changed,
            'audio':'AAC stream copied; no independent ASR',
            'subtitles':'burned captions outside ROI',
            'publication':'HUMAN_REVIEW / PUBLICATION_NOT_APPROVED'}
    report.parent.mkdir(parents=True,exist_ok=True)
    report.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf8')
    return result

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--source',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True)
    p.add_argument('--report',type=Path,required=True)
    p.add_argument('--genre',choices=sorted(PROFILES),default='ai_productivity')
    a=p.parse_args()
    print(json.dumps(run(a.source,a.output,a.genre,a.report),ensure_ascii=False,indent=2))
if __name__=='__main__': main()
