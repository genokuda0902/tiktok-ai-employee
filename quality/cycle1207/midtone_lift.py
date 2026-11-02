#!/usr/bin/env python3
"""Offline central-panel midtone lift; no text replacement, paid API, or posting."""
from __future__ import annotations
import argparse
import json
import subprocess
from pathlib import Path
FPS=30
ROI=(64,500,952,816)
GENRE_PROFILES={
 'ai':12,'business':11,'money':10,'learning':12,'health':10,
 'food':9,'travel':10,'beauty':9,'career':11,'life':10,
}
def run(cmd):
 p=subprocess.run(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
 if p.returncode:raise RuntimeError('Command failed: '+p.stderr[-1800:])
 return p.stdout
def probe(path):
 return json.loads(run(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(path)]))
def validate_source(info):
 v=next((s for s in info['streams'] if s.get('codec_type')=='video'),None)
 a=next((s for s in info['streams'] if s.get('codec_type')=='audio'),None)
 if not v or not a:raise ValueError('Audio and video required')
 if (v.get('codec_name'),int(v['width']),int(v['height']),v['r_frame_rate'])!=('h264',1080,1920,'30/1'):
  raise ValueError('Expected H264 1080x1920 30fps')
 if a.get('codec_name')!='aac' or int(a['sample_rate'])!=48000:
  raise ValueError('Expected AAC 48kHz')
 return int(v.get('nb_frames') or round(float(info['format']['duration'])*FPS))
def validate_roi(roi):
 if len(roi)!=4 or any(not isinstance(z,int) for z in roi):raise ValueError('Invalid ROI')
 x,y,w,h=roi
 if x<48 or x+w>1032 or y<470 or y+h>1340 or w<600 or h<600 or any(z%2 for z in roi):
  raise ValueError('ROI overlaps protected captions, footer, or edge controls')
 return roi
def build_filter(roi=ROI,lift=12):
 x,y,w,h=validate_roi(roi)
 if not 7<=lift<=14:raise ValueError('Unsafe lift value')
 expr=(f'if(between(val,24,185),'
       f'min(235,val+{lift}*min(1,max(0,(val-24)/35))*'
       f'min(1,max(0,(185-val)/40))),val)')
 return (f'[0:v]split=2[base][mid];'
         f'[mid]crop={w}:{h}:{x}:{y},lutyuv=y=\\'{expr}\\'[adjusted];'
         f'[base][adjusted]overlay={x}:{y}:shortest=1:format=auto[outv]')
def render(src,dst,genre='ai',frames=None,crf=16):
 if genre not in GENRE_PROFILES:raise ValueError('Unknown genre')
 n=validate_source(probe(src))
 if frames is not None:
  if not 1<=frames<=n:raise ValueError('Invalid frame count')
  n=frames
 if not 14<=crf<=22:raise ValueError('CRF outside approved range')
 dst=Path(dst);dst.parent.mkdir(parents=True,exist_ok=True)
 cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(src),
      '-filter_complex',build_filter(lift=GENRE_PROFILES[genre]),
      '-map','[outv]','-map','0:a:0','-c:v','libx264','-preset','veryfast',
      '-crf',str(crf),'-pix_fmt','yuv420p','-r','30','-fps_mode','cfr',
      '-c:a','copy','-frames:v',str(n),'-movflags','+faststart',
      '-metadata:s:a:0','language=jpn',str(dst)]
 run(cmd)
 if validate_source(probe(dst))!=n:raise RuntimeError('Frame count mismatch')
 return {'genre':genre,'roi':ROI,'lift':GENRE_PROFILES[genre],'frames':n,'output':str(dst)}
def main():
 p=argparse.ArgumentParser();p.add_argument('source');p.add_argument('output')
 p.add_argument('--genre',choices=sorted(GENRE_PROFILES),default='ai')
 p.add_argument('--frames',type=int);p.add_argument('--crf',type=int,default=16)
 a=p.parse_args()
 print(json.dumps(render(a.source,a.output,a.genre,a.frames,a.crf),ensure_ascii=False))
if __name__=='__main__':main()
