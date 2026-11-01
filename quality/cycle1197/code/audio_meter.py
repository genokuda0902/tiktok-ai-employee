#!/usr/bin/env python3
"""Free/offline audio-reactive meter. No uploaded user media in CI."""
from __future__ import annotations
import argparse, json, subprocess
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw

FPS=30
SAMPLE_RATE=48000
BAR_COUNT=7
GENRE_COLORS={
 'ai':'#4DE3D2','business':'#8EC5FF','money':'#63E5B8',
 'learning':'#A7C4FF','health':'#74E4C4','food':'#A9E69B',
 'travel':'#78D6F0','beauty':'#D5B6F7','career':'#82C4F8','life':'#98E0C5'}
METER_X,METER_Y,METER_W,METER_H=718,1485,129,41

def run(cmd):
 return subprocess.run(cmd,check=True,capture_output=True,text=True).stdout

def video_frames(path):
 data=json.loads(run(['ffprobe','-v','error','-select_streams','v:0',
   '-show_entries','stream=nb_frames','-of','json',str(path)]))
 return int(data['streams'][0]['nb_frames'])

def audio_samples(path):
 p=subprocess.run(['ffmpeg','-v','error','-i',str(path),'-map','0:a:0',
   '-ac','1','-ar',str(SAMPLE_RATE),'-f','f32le','-'],check=True,capture_output=True)
 return np.frombuffer(p.stdout,dtype='<f4').copy()

def envelope(samples,frames,fps=FPS):
 """Amplitude in [0,1] per frame and bar, gated and smoothed."""
 if fps<=0 or frames<=0: raise ValueError('invalid fps/frames')
 n=SAMPLE_RATE//fps
 if SAMPLE_RATE%fps: raise ValueError('fps must divide sample rate')
 needed=frames*n
 if len(samples)<needed: samples=np.pad(samples,(0,needed-len(samples)))
 a=samples[:needed].reshape(frames,n).astype(np.float64)
 parts=np.array_split(a,BAR_COUNT,axis=1)
 rms=np.stack([np.sqrt(np.mean(p*p,axis=1)) for p in parts],axis=1)
 p90=float(np.percentile(np.sqrt(np.mean(a*a,axis=1)),90))
 scale=max(0.03,p90)
 values=np.clip((rms-0.008)/(scale-0.008),0,1)**0.8
 smooth=np.zeros_like(values)
 for i in range(frames):
  prev=smooth[i-1] if i else np.zeros(BAR_COUNT)
  rate=np.where(values[i]>prev,0.70,0.38)
  smooth[i]=prev+rate*(values[i]-prev)
 return smooth

def make_overlays(levels,directory,color):
 directory.mkdir(parents=True,exist_ok=True)
 for i,vals in enumerate(levels):
  im=Image.new('RGBA',(METER_W,METER_H),(0,0,0,0))
  d=ImageDraw.Draw(im)
  for j,val in enumerate(vals):
   height=int(round(3+30*float(val)))
   x=7+j*17
   y=(METER_H-height)//2
   d.rounded_rectangle((x,y,x+11,y+height),radius=4,fill=color)
  im.save(directory/f'{i:04d}.png',optimize=True)

def render(source,target,overlays,frames):
 # Only the old fictional meter is replaced; subtitles are untouched.
 vf=(f'[0:v]delogo=x={METER_X}:y={METER_Y}:w={METER_W}:h={METER_H}:show=0[clean];'
     f'[clean][1:v]overlay={METER_X}:{METER_Y}:format=auto:shortest=1[v]')
 subprocess.run(['ffmpeg','-y','-hide_banner','-loglevel','error','-i',str(source),
  '-framerate',str(FPS),'-start_number','0','-i',str(overlays/'%04d.png'),
  '-filter_complex',vf,'-map','[v]','-map','0:a:0','-c:v','libx264',
  '-preset','veryfast','-crf','18','-pix_fmt','yuv420p','-c:a','copy',
  '-frames:v',str(frames),'-video_track_timescale','30000',
  '-movflags','+faststart',str(target)],check=True)

def main():
 ap=argparse.ArgumentParser()
 ap.add_argument('source',type=Path)
 ap.add_argument('target',type=Path)
 ap.add_argument('--genre',choices=GENRE_COLORS,default='ai')
 ap.add_argument('--overlay-dir',type=Path,default=Path('/tmp/audio_meter_frames'))
 ap.add_argument('--metadata',type=Path)
 args=ap.parse_args()
 frames=video_frames(args.source)
 levels=envelope(audio_samples(args.source),frames)
 make_overlays(levels,args.overlay_dir,GENRE_COLORS[args.genre])
 render(args.source,args.target,args.overlay_dir,frames)
 result={'frames':frames,'audio_reactive':True,'genre':args.genre,
  'mean_bar_height':float((3+30*levels).mean()),
  'peak_bar_height':float((3+30*levels).max()),
  'quiet_frames':int((levels.mean(axis=1)<0.08).sum()),
  'source':'decoded AAC PCM, 48kHz mono',
  'visual_region':[METER_X,METER_Y,METER_W,METER_H]}
 if args.metadata: args.metadata.write_text(json.dumps(result,indent=2))
 print(json.dumps(result))

if __name__=='__main__': main()
