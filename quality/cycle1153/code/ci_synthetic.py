"""CI uses only generated video and synthetic tones, never private media."""
from __future__ import annotations
import json
import subprocess
import tempfile
from pathlib import Path
from diagram_microcontrast import render,probe

def run(cmd): subprocess.run(cmd,check=True,capture_output=True)
with tempfile.TemporaryDirectory() as td:
    src=Path(td)/'synthetic.mp4';out=Path(td)/'enhanced.mp4'
    run(['ffmpeg','-hide_banner','-loglevel','error','-y',
         '-f','lavfi','-i','testsrc2=size=360x640:rate=30:duration=2',
         '-f','lavfi','-i','sine=frequency=440:sample_rate=48000:duration=2',
         '-c:v','libx264','-preset','ultrafast','-pix_fmt','yuv420p',
         '-c:a','aac','-shortest',str(src)])
    render(src,out,roi=(20,130,320,300),caption_top=450,preset='ultrafast')
    run(['ffmpeg','-hide_banner','-loglevel','error','-xerror','-i',str(out),'-f','null','-'])
    streams=probe(out)['streams'];v=next(x for x in streams if x['codec_type']=='video')
    a=next(x for x in streams if x['codec_type']=='audio')
    assert (v['width'],v['height'])==(360,640)
    assert v['codec_name']=='h264' and a['codec_name']=='aac'
    print(json.dumps({'synthetic_frames':60,'codec':v['codec_name'],'audio':a['codec_name'],'decode':'PASS'}))
