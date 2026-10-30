"""14-beat proof-focus montage for narrated 8-chapter vertical videos.

No external assets, fabricated claims, or posting. AAC is stream-copied;
existing Japanese subtitles and the header are protected.
"""
from __future__ import annotations
import argparse
import json
import subprocess
import cv2
import numpy as np

GENRE_IDS = ('ai_work','finance','health','education','travel',
             'cooking','beauty','gadgets','business','lifestyle')
FOCUS = {2:(.50,.48),3:(.50,.52),4:(.50,.47),
         5:(.50,.50),6:(.50,.53),7:(.50,.50)}
CONTENT=(0,155,1080,1435)
CHAPTERS=(0.,2.633,5.800,8.600,11.333,14.100,16.767,19.767,22.500)
FPS=30

def chapter_at(t):
    return next((i+1 for i in range(8) if CHAPTERS[i]<=t<CHAPTERS[i+1]),8)

def detail_active(t,chapter):
    if chapter not in FOCUS: return False
    start,end=CHAPTERS[chapter-1:chapter+1]
    return start+(end-start)*.45<=t<end

def focus_content(frame,chapter,zoom=1.20):
    """Bounded detail panel; preserve header and baked subtitle pixels."""
    x0,y0,x1,y1=CONTENT
    src=frame[y0:y1,x0:x1]
    h,w=src.shape[:2]
    crop_w=round(w/zoom); crop_h=round(h/zoom)
    fx,fy=FOCUS[chapter]
    left=int(np.clip(round(fx*w-crop_w/2),0,w-crop_w))
    top=0  # keep heading visible; bottom details remain in dimmed context
    px,py,pw,ph=54,250,972,1080
    detail=cv2.resize(src[top:top+crop_h,left:left+crop_w],(pw,ph),
                      interpolation=cv2.INTER_CUBIC)
    out=frame.copy()
    out[y0:y1,x0:x1]=(out[y0:y1,x0:x1].astype(np.float32)*.43).astype(np.uint8)
    cv2.rectangle(out,(px-10,py-10),(px+pw+10,py+ph+10),(2,8,19),-1)
    out[py:py+ph,px:px+pw]=detail
    cv2.rectangle(out,(px-2,py-2),(px+pw+1,py+ph+1),(175,197,43),3)
    return out

def probe(path):
    return json.loads(subprocess.check_output(
        ['ffprobe','-v','error','-show_streams','-show_chapters','-of','json',path],text=True))

def render(source,output,genre='ai_work',smoke=False):
    if genre not in GENRE_IDS: raise ValueError('unknown genre')
    info=probe(source)
    video=next(s for s in info['streams'] if s['codec_type']=='video')
    audio=next(s for s in info['streams'] if s['codec_type']=='audio')
    if (video['width'],video['height'])!=(1080,1920) or video['avg_frame_rate']!='30/1':
        raise ValueError('requires 1080x1920 30fps source')
    if audio['codec_name']!='aac': raise ValueError('requires AAC source')
    cap=cv2.VideoCapture(source)
    if not cap.isOpened(): raise RuntimeError('cannot open source')
    cmd=['ffmpeg','-hide_banner','-loglevel','error','-y',
         '-f','rawvideo','-pix_fmt','bgr24','-s','1080x1920','-r','30','-i','pipe:0',
         '-i',source,'-map','0:v:0','-map','1:a:0','-map_metadata','1',
         '-map_chapters','1','-c:v','libx264','-preset','veryfast','-crf','18',
         '-pix_fmt','yuv420p','-r','30','-c:a','copy','-movflags','+faststart',output]
    proc=subprocess.Popen(cmd,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
    frames=0;detail_frames=0;chapters=set();starts=[];last=False
    try:
        while True:
            ok,frame=cap.read()
            if not ok: break
            t=frames/FPS
            chapter=chapter_at(t)
            active=detail_active(t,chapter)
            if active: frame=focus_content(frame,chapter);detail_frames+=1
            if active and not last: starts.append(round(t,3))
            last=active
            chapters.add(chapter)
            proc.stdin.write(frame.tobytes())
            frames+=1
    finally:
        cap.release()
        if proc.stdin: proc.stdin.close()
    error=proc.stderr.read().decode('utf-8','replace')
    if proc.wait()!=0: raise RuntimeError('ffmpeg failed: '+error[-2000:])
    if not smoke and frames!=675: raise RuntimeError(f'unexpected frame count: {frames}')
    return {'genre':genre,'frames':frames,'chapters':sorted(chapters),
            'detail_frames':detail_frames,'focus_start_seconds':starts,
            'visual_beats':8+len(FOCUS),
            'note':'Original AAC copied; baked Japanese subtitles below y=1435 untouched'}

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('source');parser.add_argument('output')
    parser.add_argument('--genre',default='ai_work')
    parser.add_argument('--smoke',action='store_true',help='allow short synthetic CI video')
    args=parser.parse_args()
    print(json.dumps(render(args.source,args.output,args.genre,args.smoke),
                     ensure_ascii=False,indent=2))
