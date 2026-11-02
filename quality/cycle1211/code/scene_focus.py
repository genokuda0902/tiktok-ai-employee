#!/usr/bin/env python3
"""Zero-cost, review-only scene focus cue for 10-genre vertical slide videos."""
from __future__ import annotations
import argparse, hashlib, json, math, subprocess
from pathlib import Path
import cv2
import numpy as np

WIDTH, HEIGHT, FPS, SAFE_Y = 1080, 1920, 30, 1240
GENRE_COLORS = {
 'ai':'#41dfd3','business':'#4ba8ff','money':'#efc96b',
 'learning':'#8cb8ff','health':'#65d9ae','food':'#f7b36a',
 'travel':'#6ccfe8','beauty':'#f4a4d1','career':'#91c7ff','life':'#c1d982'
}
SCENES = [
 {'start':42,'end':96,'rect':[76,605,924,755]},
 {'start':96,'end':171,'rect':[82,510,548,1010]},
 {'start':171,'end':252,'rect':[70,460,944,1160]},
 {'start':252,'end':333,'rect':[78,485,558,1130]},
 {'start':333,'end':414,'rect':[508,530,952,1110]},
 {'start':414,'end':501,'rect':[74,840,951,1150]},
 {'start':501,'end':579,'rect':[610,760,952,1120]},
 {'start':579,'end':675,'rect':[80,650,945,850]},
]
def validate(scenes, frame_count=675):
 assert 1<=len(scenes)<=16
 for s in scenes:
  assert 0<=s['start']<s['end']<=frame_count
  x1,y1,x2,y2=s['rect']
  assert 30<=x1<x2<=WIDTH-30
  assert 200<=y1<y2<=SAFE_Y
 assert all(a['end']<=b['start'] for a,b in zip(scenes,scenes[1:]))
 return True

def color_bgr(genre):
 if genre not in GENRE_COLORS: raise ValueError('Unknown genre')
 h=GENRE_COLORS[genre].lstrip('#')
 return tuple(int(h[i:i+2],16) for i in (4,2,0))

def envelope(relative_frame,fps=FPS,duration=0.72):
 t=relative_frame/fps
 if t<0 or t>=duration:return 0.
 return math.sin(math.pi*t/duration)**2

def apply_focus(frame,rect,color,strength):
 if strength<=0:return frame
 x1,y1,x2,y2=rect; margin=20
 a,b=max(0,x1-margin),max(0,y1-margin)
 c,d=min(WIDTH,x2+margin),min(SAFE_Y,y2+margin)
 roi=frame[b:d,a:c]; layer=np.zeros_like(roi)
 cv2.rectangle(layer,(x1-a,y1-b),(x2-a,y2-b),color,3,cv2.LINE_AA)
 glow=cv2.GaussianBlur(layer,(0,0),sigmaX=9,sigmaY=9)
 delta=(glow.astype(np.float32)*.7+layer.astype(np.float32)*.5)*strength
 roi[:]=np.clip(roi.astype(np.float32)+delta,0,255).astype(np.uint8)
 return frame

def check_probe(path):
 info=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(path)]))
 v=next(s for s in info['streams'] if s['codec_type']=='video')
 a=next(s for s in info['streams'] if s['codec_type']=='audio')
 assert (v['codec_name'],int(v['width']),int(v['height']),v['r_frame_rate'])==('h264',WIDTH,HEIGHT,'30/1')
 assert a['codec_name']=='aac' and int(a['sample_rate'])==48000
 return info

def render(src,dst,genre='ai',scenes=SCENES):
 src,dst=Path(src),Path(dst);check_probe(src)
 cap=cv2.VideoCapture(str(src))
 if not cap.isOpened():raise RuntimeError('Failed to open input')
 count=int(cap.get(cv2.CAP_PROP_FRAME_COUNT));validate(scenes,count)
 cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-f','rawvideo','-pix_fmt','bgr24',
 '-s',f'{WIDTH}x{HEIGHT}','-r',str(FPS),'-i','pipe:0','-i',str(src),
 '-map','0:v:0','-map','1:a:0','-map_metadata','1','-map_chapters','1',
 '-c:v','libx264','-preset','veryfast','-crf','17','-pix_fmt','yuv420p',
 '-c:a','copy','-movflags','+faststart',str(dst)]
 proc=subprocess.Popen(cmd,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
 n=0;enhanced=0;accent=color_bgr(genre)
 try:
  while True:
   ok,frame=cap.read()
   if not ok:break
   for scene in scenes:
    if scene['start']<=n<scene['end']:
     strength=envelope(n-scene['start'])
     if strength>0:
      apply_focus(frame,scene['rect'],accent,strength);enhanced+=1
     break
   proc.stdin.write(frame.tobytes());n+=1
  proc.stdin.close();err=proc.stderr.read().decode(errors='replace')
  rc=proc.wait()
  if rc:raise RuntimeError(f'ffmpeg error {rc}: {err[-2000:]}')
 finally:
  cap.release()
  if proc.poll() is None:proc.kill()
 if n!=count:raise RuntimeError(f'Frame loss: expected {count}, got {n}')
 info=check_probe(dst);v=next(s for s in info['streams'] if s['codec_type']=='video')
 if int(v.get('nb_frames',0))!=n:raise RuntimeError(f'Encoded frame loss: {v.get("nb_frames")} != {n}')
 return {'frames':n,'enhanced_frames':enhanced,'genre':genre,'source':str(src),'output':str(dst),
 'output_sha256':hashlib.sha256(dst.read_bytes()).hexdigest(),'safe_y':SAFE_Y}

if __name__=='__main__':
 ap=argparse.ArgumentParser()
 ap.add_argument('src');ap.add_argument('dst');ap.add_argument('--genre',default='ai')
 args=ap.parse_args()
 print(json.dumps(render(args.src,args.dst,args.genre),ensure_ascii=False,indent=2))
