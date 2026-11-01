#!/usr/bin/env python3
"""CI uses a synthetic clip only; private real footage is never uploaded."""
import json,subprocess,tempfile
from pathlib import Path
from comparison_focus import run
with tempfile.TemporaryDirectory() as tmp:
 tmp=Path(tmp);src=tmp/'synthetic.mp4';dst=tmp/'focus.mp4'
 subprocess.run(['ffmpeg','-nostdin','-hide_banner','-loglevel','error','-y',
   '-f','lavfi','-i','color=c=0x071323:s=1080x1920:r=30:d=4',
   '-f','lavfi','-i','sine=frequency=440:sample_rate=48000:duration=4',
   '-vf','drawbox=x=91:y=550:w=747:h=172:color=0x4e1838:t=fill,drawbox=x=91:y=794:w=747:h=211:color=0x063d47:t=fill',
   '-c:v','libx264','-preset','ultrafast','-crf','28','-c:a','aac','-b:a','96k','-shortest',str(src)],check=True)
 run(src,dst,before_start=.5,before_end=1.7,after_start=1.9,after_end=3.5)
 p=subprocess.run(['ffprobe','-v','error','-show_entries','stream=codec_name,width,height,nb_frames,sample_rate','-of','json',str(dst)],capture_output=True,text=True,check=True)
 streams=json.loads(p.stdout)['streams'];vs=next(x for x in streams if x['codec_name']=='h264')
 assert vs['width']==1080 and vs['height']==1920 and int(vs['nb_frames'])==120
 assert any(x['codec_name']=='aac' for x in streams)
 subprocess.run(['ffmpeg','-v','error','-xerror','-i',str(dst),'-f','null','-'],check=True)
 print('SYNTHETIC_CI_PASS: 1080x1920 120 frames H264 AAC full decode')
