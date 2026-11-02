"""Synthetic 2-second 1080x1920 Japanese-tagged AAC H264 render/decode; no private media."""
import json, subprocess, tempfile
from pathlib import Path
from readable_takeaway import sha256, render, probe, POLICY
with tempfile.TemporaryDirectory() as td:
    p=Path(td); source=p/'source.mp4'; out=p/'out.mp4'; manifest=p/'manifest.json'
    subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','lavfi','-i',
                    'color=c=0x071323:s=1080x1920:r=30:d=2','-f','lavfi','-i',
                    'sine=frequency=220:sample_rate=48000:duration=2','-c:v','libx264',
                    '-preset','ultrafast','-threads','2','-pix_fmt','yuv420p','-c:a','aac',
                    '-metadata:s:a:0','language=jpn','-shortest',str(source)],check=True)
    manifest.write_text(json.dumps({'policy':POLICY,'genre':'ai','source_sha256':sha256(source),
                                   'takeaway':'3つの作業を選ぶ','start':0.4,'end':1.5}),encoding='utf-8')
    info=render(source,out,manifest)
    assert info['frames']==60,info
    subprocess.run(['ffmpeg','-v','error','-xerror','-i',str(out),'-f','null','-'],check=True)
    print('Synthetic 2s A/V decode PASS:',info['frames'],'frames')
