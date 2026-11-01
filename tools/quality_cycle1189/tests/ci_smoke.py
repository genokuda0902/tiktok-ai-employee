#!/usr/bin/env python3
"""GitHub Actions: synthetic-only 1080x1920 narration video + cursor overlay QA."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'code'))
from ui_save_motion import Plan,render,probe

def cmd(args,output=False):
 p=subprocess.run(args,check=True,capture_output=True,text=True)
 return p.stdout.strip() if output else None

def audio_hash(path):
 return cmd(['ffmpeg','-v','error','-i',str(path),'-map','0:a:0','-c','copy',
             '-f','streamhash','-hash','SHA256','-'],True)

with tempfile.TemporaryDirectory() as d:
 src=Path(d)/'synthetic_source.mp4';out=Path(d)/'synthetic_review.mp4'
 cmd(['ffmpeg','-nostdin','-hide_banner','-loglevel','error',
      '-f','lavfi','-i','color=c=0x0a2838:s=1080x1920:r=30:d=2.2',
      '-f','lavfi','-i','sine=frequency=440:sample_rate=48000:duration=2.2',
      '-map','0:v','-map','1:a','-shortest','-c:v','libx264',
      '-preset','ultrafast','-crf','28','-pix_fmt','yuv420p',
      '-c:a','aac','-b:a','128k','-metadata:s:a:0','language=jpn',str(src)])
 result=render(src,out,'ai',Plan(start=.1,duration=1.8),preset='ultrafast',crf=25)
 data=probe(out)
 v=next(x for x in data['streams'] if x['codec_type']=='video')
 a=next(x for x in data['streams'] if x['codec_type']=='audio')
 assert (int(v['width']),int(v['height']),int(v['nb_frames']))==(1080,1920,66)
 assert (a['codec_name'],int(a['sample_rate']))==('aac',48000)
 assert audio_hash(src)==audio_hash(out),'narration stream changed'
 cmd(['ffmpeg','-v','error','-xerror','-i',str(out),'-f','null','-'])
 print(json.dumps({'ci_synthetic':'PASS','frames':result['frames'],
                   'audio_bitstream':'identical','full_decode':'PASS',
                   'no_private_assets':True}))
