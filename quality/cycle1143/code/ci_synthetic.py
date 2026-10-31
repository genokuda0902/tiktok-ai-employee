"""Zero-cost synthetic-only CI smoke test. No user/private assets."""
from __future__ import annotations
import hashlib
import json
import subprocess
import tempfile
from pathlib import Path
from illustration_lift import render, probe

def run(cmd):
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL)

def audio_hash(path):
    data=subprocess.check_output(['ffmpeg','-v','error','-i',str(path),
        '-map','0:a:0','-c:a','copy','-f','adts','-'])
    return hashlib.sha256(data).hexdigest()

def main():
    with tempfile.TemporaryDirectory(prefix='cycle1143_ci_') as d:
        src, dst=Path(d)/'src.mp4',Path(d)/'dst.mp4'
        run(['ffmpeg','-v','error','-y','-f','lavfi',
             '-i','testsrc2=size=1080x1920:rate=30:duration=1.5',
             '-f','lavfi','-i','sine=frequency=440:sample_rate=48000:duration=1.5',
             '-shortest','-c:v','libx264','-preset','ultrafast','-crf','27',
             '-pix_fmt','yuv420p','-c:a','aac','-b:a','96k','-metadata:s:a:0','language=jpn',
             str(src)])
        render(src,dst,'travel')
        out=probe(dst)
        assert out['width']==1080 and out['height']==1920 and out['fps']=='30/1',out
        assert out['frames']==45 and out['audio_codec']=='aac',out
        assert audio_hash(src)==audio_hash(dst),'audio changed'
        run(['ffmpeg','-v','error','-i',str(dst),'-f','null','-'])
        print(json.dumps({'status':'PASS','genre':'travel','frames':45,
            'audio_identical':True,'full_decode':'PASS','private_media':'NONE'},indent=2))

if __name__=='__main__': main()
