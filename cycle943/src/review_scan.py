"""Cycle943: subtle 3-step review focus for Japanese image-first video.
This only highlights *items to inspect*; it does not mark them verified.
No publishing, payment, or automatic upload.
"""
from __future__ import annotations
import argparse, json, subprocess
from pathlib import Path

SCENE_START, SCENE_END = 11.6, 14.5
ROWS = ((110,698,782,826),(110,865,782,995),(110,1032,782,1162))
# BGR palettes, not a one-style-fits-all template.
PALETTES = {
    'ai_productivity':(207,204,38), 'business':(204,169,52),
    'finance':(101,192,101), 'education':(205,160,75),
    'health':(129,192,87), 'beauty':(180,116,224),
    'food':(75,162,239), 'travel':(231,175,83),
    'lifestyle':(179,155,205), 'technology':(239,197,75),
}

def beat_at(t):
    if not SCENE_START <= t < SCENE_END:
        return None
    beat = min(2,int((t-SCENE_START)*3/(SCENE_END-SCENE_START)))
    start = SCENE_START + beat*(SCENE_END-SCENE_START)/3
    u = (t-start)*3/(SCENE_END-SCENE_START)
    return beat, min(1,max(0,u))

def envelope(u):
    if not 0<=u<=1: raise ValueError('u out of range')
    p=min(1.,u/.16,(1-u)/.16)
    return p*p*(3-2*p)

def rounded_outline(img,p0,p1,color,thickness=5,r=14):
    import cv2
    x0,y0=p0;x1,y1=p1
    cv2.line(img,(x0+r,y0),(x1-r,y0),color,thickness,cv2.LINE_AA)
    cv2.line(img,(x0+r,y1),(x1-r,y1),color,thickness,cv2.LINE_AA)
    cv2.line(img,(x0,y0+r),(x0,y1-r),color,thickness,cv2.LINE_AA)
    cv2.line(img,(x1,y0+r),(x1,y1-r),color,thickness,cv2.LINE_AA)
    for c,a,b in [((x0+r,y0+r),180,270),((x1-r,y0+r),270,360),
                  ((x0+r,y1-r),90,180),((x1-r,y1-r),0,90)]:
        cv2.ellipse(img,c,(r,r),0,a,b,color,thickness,cv2.LINE_AA)

def apply_focus(frame,t,genre='ai_productivity'):
    import cv2
    if genre not in PALETTES: raise ValueError('unknown genre')
    if frame.shape[:2]!=(1920,1080): raise ValueError('requires 1080x1920')
    beat=beat_at(t)
    if beat is None: return frame
    i,u=beat; x0,y0,x1,y1=ROWS[i]
    ax,ay,bx,by=88,y0-13,803,y1+15
    roi=frame[ay:by,ax:bx]
    layer=roi.copy()
    color=PALETTES[genre]
    rounded_outline(layer,(x0-ax,y0-ay),(x1-ax,y1-ay),color,5,15)
    cv2.rectangle(layer,(5,15),(13,min(by-ay-16,86)),color,-1,cv2.LINE_AA)
    width=int((x1-x0-48)*u)
    cv2.line(layer,(x0-ax+24,y1-ay-12),(x0-ax+24+width,y1-ay-12),color,4,cv2.LINE_AA)
    strength=.78*envelope(u)
    if strength>0:
        cv2.addWeighted(layer,strength,roi,1-strength,0,dst=roi)
    return frame

def run(source,output,report,genre='ai_productivity'):
    import cv2
    if genre not in PALETTES: raise ValueError('unknown genre')
    source,output,report=map(Path,(source,output,report))
    if not source.is_file(): raise FileNotFoundError(source)
    capture=cv2.VideoCapture(str(source))
    fps=capture.get(cv2.CAP_PROP_FPS)
    frames=int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
    if abs(fps-30)>.01 or frames!=691: raise ValueError('unexpected input fps or frame count')
    output.parent.mkdir(parents=True,exist_ok=True)
    video_only=output.with_name('cycle943_video_only.mp4')
    encoder=subprocess.Popen(['ffmpeg','-hide_banner','-loglevel','error','-y',
        '-f','rawvideo','-pixel_format','bgr24','-video_size','1080x1920',
        '-framerate','30','-i','pipe:0','-an','-c:v','libx264',
        '-preset','veryfast','-crf','19','-pix_fmt','yuv420p',
        '-movflags','+faststart',str(video_only)],stdin=subprocess.PIPE,stderr=subprocess.PIPE)
    count=0; changed=0; by_beat=[0,0,0]
    try:
        while True:
            ok,frame=capture.read()
            if not ok: break
            beat=beat_at(count/fps)
            if beat is not None:
                apply_focus(frame,count/fps,genre)
                changed+=1;by_beat[beat[0]]+=1
            encoder.stdin.write(frame.tobytes())
            count+=1
        encoder.stdin.close()
        error=encoder.stderr.read().decode('utf8','replace')
        if encoder.wait()!=0: raise RuntimeError(error[-1000:])
    finally:
        capture.release()
        if encoder.poll() is None: encoder.kill()
    if count!=691: raise RuntimeError('frame count mismatch')
    subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y',
        '-i',str(video_only),'-i',str(source),'-map','0:v:0',
        '-map','1:a:0','-c:v','copy','-c:a','copy',
        '-movflags','+faststart',str(output)],check=True)
    video_only.unlink(missing_ok=True)
    result={'cycle':943,'genre':genre,'source':source.name,'output':output.name,
        'change':'Three sequential review-item focus scans; no verification statuses changed',
        'scene_seconds':[SCENE_START,SCENE_END], 'frames':count,
        'scene_frames':changed,'frames_per_beat':by_beat,
        'genre_palettes':len(PALETTES),
        'approval':'HUMAN_REVIEW / PUBLICATION_NOT_APPROVED'}
    report.parent.mkdir(parents=True,exist_ok=True)
    report.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    return result

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--source',required=True)
    p.add_argument('--output',required=True)
    p.add_argument('--report',required=True)
    p.add_argument('--genre',default='ai_productivity',choices=sorted(PALETTES))
    a=p.parse_args()
    print(json.dumps(run(a.source,a.output,a.report,a.genre),ensure_ascii=False,indent=2))
