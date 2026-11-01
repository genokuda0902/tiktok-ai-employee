#!/usr/bin/env python3
"""CI synthetic-only render/decode and exact H.264 preservation test."""
import json
import subprocess
import sys
import tempfile
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from voice_presence import render,probe

def run(args, capture=False):
    r=subprocess.run(args,check=True,capture_output=True,text=True)
    return r.stdout if capture else None

def stream_hash(path):
    return run(['ffmpeg','-v','error','-i',str(path),'-map','0:v:0',
                '-c','copy','-f','streamhash','-hash','SHA256','-'],True).strip()

with tempfile.TemporaryDirectory() as d:
    src=Path(d)/'synthetic_source.mp4'
    out=Path(d)/'synthetic_voice_eq.mp4'
    run(['ffmpeg','-nostdin','-hide_banner','-loglevel','error',
         '-f','lavfi','-i','color=c=0x123448:s=1080x1920:r=30:d=2.2',
         '-f','lavfi','-i','sine=frequency=440:sample_rate=48000:duration=2.2',
         '-map','0:v','-map','1:a','-shortest',
         '-c:v','libx264','-preset','ultrafast','-crf','28','-pix_fmt','yuv420p',
         '-c:a','aac','-b:a','128k','-metadata:s:a:0','language=jpn',str(src)])
    result=render(src,out,'ai')
    data=probe(out)
    v=next(s for s in data['streams'] if s['codec_type']=='video')
    a=next(s for s in data['streams'] if s['codec_type']=='audio')
    assert (int(v['width']),int(v['height']))==(1080,1920)
    assert a['codec_name']=='aac' and int(a['sample_rate'])==48000
    assert stream_hash(src)==stream_hash(out),'video bitstream changed'
    run(['ffmpeg','-v','error','-xerror','-i',str(out),'-f','null','-'])
    print(json.dumps({'ci_synthetic':'PASS','frames':result['frames'],
                      'video_bitstream':'identical','full_decode':'PASS'}))
