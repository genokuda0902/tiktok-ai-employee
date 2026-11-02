#!/usr/bin/env python3
"""CI: generate 30 frames of synthetic, rights-free H264/AAC and full decode."""
import importlib.util
import pathlib
import subprocess
import tempfile
ROOT=pathlib.Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('content_detail',ROOT/'code'/'content_detail.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

def run(cmd):
    p=subprocess.run(cmd,capture_output=True,text=True)
    if p.returncode: raise RuntimeError(p.stderr[-2000:])

with tempfile.TemporaryDirectory() as td:
    src=pathlib.Path(td)/'synthetic.mp4';out=pathlib.Path(td)/'out.mp4'
    run(['ffmpeg','-hide_banner','-loglevel','error','-y',
         '-f','lavfi','-i','color=c=0x09232d:s=1080x1920:r=30:d=1',
         '-f','lavfi','-i','sine=frequency=430:sample_rate=48000:duration=1',
         '-c:v','libx264','-preset','ultrafast','-crf','28','-pix_fmt','yuv420p',
         '-c:a','aac','-shortest',str(src)])
    m.render(src,out,genre='learning',frames=30,crf=22)
    info=m.probe(out)
    assert m.validate_source(info)==30
    run(['ffmpeg','-hide_banner','-loglevel','error','-xerror','-i',str(out),
         '-map','0:v:0','-f','null','-', '-map','0:a:0','-f','null','-'])
    print('CI synthetic: PASS (30 frames, H264/AAC, full decode, learning profile)')
