#!/usr/bin/env python3
"""Small no-network integration smoke; exact frame count and AAC copy."""
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile

spec=importlib.util.spec_from_file_location('chapter_progress',Path(__file__).resolve().parents[1]/'code'/'chapter_progress.py')
mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)

def run(cmd): subprocess.run(cmd,check=True,capture_output=True,text=True)

def audio_sha(path):
    p=subprocess.run(['ffmpeg','-v','error','-i',str(path),'-map','0:a:0','-c','copy','-f','adts','pipe:1'],check=True,capture_output=True)
    return hashlib.sha256(p.stdout).hexdigest()

with tempfile.TemporaryDirectory() as d:
    src=Path(d)/'synthetic.mp4';dst=Path(d)/'output.mp4'
    run(['ffmpeg','-v','error','-y','-f','lavfi','-i','color=c=0x091923:s=1080x1920:r=30:d=1',
         '-f','lavfi','-i','sine=frequency=420:sample_rate=48000:duration=1',
         '-map','0:v:0','-map','1:a:0','-c:v','libx264','-preset','ultrafast','-pix_fmt','yuv420p',
         '-c:a','aac','-b:a','96k','-frames:v','30',str(src)])
    mod.render(src,dst,starts=(0,8,16,24))
    info=mod.probe(dst)
    frames=mod.validate_source(info)
    assert frames==30,(frames,info)
    assert audio_sha(src)==audio_sha(dst),'AAC payload modified'
    run(['ffmpeg','-v','error','-xerror','-i',str(dst),'-map','0:v:0','-f','null','-'])
    run(['ffmpeg','-v','error','-xerror','-i',str(dst),'-map','0:a:0','-f','null','-'])
    print(json.dumps({'smoke':'PASS','frames':frames,'audio_bitstream':'identical','decode':'PASS'}))
