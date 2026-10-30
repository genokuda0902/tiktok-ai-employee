"""Offline 1080x1920 H.264 render. SHA-pinned source, no upload/post.

Requires Pillow, numpy, opencv-python-headless and local ffmpeg/ffprobe.
Output is HUMAN_REVIEW only. Input MP4 and output MP4 must stay private.
"""
import argparse, hashlib, json, subprocess
from pathlib import Path
import numpy as np
import cv2
from caption_accessibility import render_plate

def sha(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
    return h.hexdigest()

def chapters(path):
    raw=subprocess.check_output(['ffprobe','-v','error','-show_chapters','-of','json',str(path)])
    items=json.loads(raw)['chapters']
    if len(items)!=8:raise ValueError('expected eight chapters')
    times=[(float(c['start_time']),float(c['end_time'])) for c in items]
    if abs(times[0][0])>.001 or abs(times[-1][1]-22.5)>.05:raise ValueError('timing')
    if any(abs(times[i][1]-times[i+1][0])>.001 for i in range(7)):raise ValueError('gap')
    return times

def render(source,dest,expected_sha,genre='ai_work'):
    source=Path(source);dest=Path(dest)
    if sha(source)!=expected_sha:raise ValueError('source SHA manifest mismatch')
    times=chapters(source);cap=cv2.VideoCapture(str(source))
    if not cap.isOpened():raise RuntimeError('source decode failed')
    if (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))!=(1080,1920):raise ValueError('resolution')
    if abs(cap.get(cv2.CAP_PROP_FPS)-30)>.01:raise ValueError('fps')
    y0,y1=1370,1616;plates=[]
    for i in range(8):
        rgba=np.array(render_plate(i,genre).crop((0,y0,1080,y1)),dtype=np.uint8)
        bgr=cv2.cvtColor(rgba[:,:,:3],cv2.COLOR_RGB2BGR)
        alpha=rgba[:,:,3:4].astype(np.float32)/255
        plates.append((bgr,alpha))
    cmd=['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pixel_format','bgr24',
         '-video_size','1080x1920','-framerate','30','-i','pipe:0','-i',str(source),
         '-map','0:v:0','-map','1:a:0','-map_metadata','1','-map_chapters','1',
         '-c:v','libx264','-preset','veryfast','-crf','21','-pix_fmt','yuv420p',
         '-frames:v','675','-c:a','copy','-metadata:s:a:0','language=jpn',
         '-movflags','+faststart',str(dest)]
    proc=subprocess.Popen(cmd,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
    n=0;scene=0
    try:
        while n<675:
            ok,frame=cap.read()
            if not ok:raise RuntimeError(f'decode ended at frame {n}')
            t=n/30
            while scene<7 and t>=times[scene][1]:scene+=1
            bgr,alpha=plates[scene]
            roi=frame[y0:y1]
            frame[y0:y1]=(roi.astype(np.float32)*(1-alpha)+bgr.astype(np.float32)*alpha).astype(np.uint8)
            proc.stdin.write(frame.tobytes());n+=1
    except Exception:
        proc.kill();raise
    finally:cap.release()
    proc.stdin.close();err=proc.stderr.read().decode(errors='replace');rc=proc.wait()
    if rc:raise RuntimeError(f'ffmpeg exit {rc}: {err[-1000:]}')
    return {'frames':n,'source_sha256':sha(source),'output_sha256':sha(dest)}

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--source',required=True);p.add_argument('--dest',required=True)
    p.add_argument('--expected-sha',required=True);p.add_argument('--genre',default='ai_work')
    a=p.parse_args();print(json.dumps(render(a.source,a.dest,a.expected_sha,a.genre),indent=2))
