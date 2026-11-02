"""Offline synthetic 1080x1920 30fps H264/AAC smoke, no user media."""
import subprocess, sys, tempfile
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from quality_rate_control import encode

def run(args):
    p=subprocess.run(args,capture_output=True,text=True)
    if p.returncode: raise RuntimeError(p.stderr[-1200:])

with tempfile.TemporaryDirectory() as td:
    src=Path(td)/'synthetic.mp4'; dst=Path(td)/'output.mp4'
    run(['ffmpeg','-v','error','-y','-f','lavfi','-i','testsrc2=size=1080x1920:rate=30:duration=1.1',
         '-f','lavfi','-i','sine=frequency=500:sample_rate=48000:duration=1.1',
         '-c:v','libx264','-preset','ultrafast','-crf','27','-pix_fmt','yuv420p',
         '-c:a','aac','-b:a','96k','-metadata:s:a:0','language=jpn',
         '-shortest',str(src)])
    r=encode(src,dst,verify_quality=False)
    assert r['frames']==33 and r['resolution']==[1080,1920]
    assert r['aac_bitstream_identical'] and r['full_av_decode']=='PASS'
    print('CI_SMOKE_PASS',r['frames'],r['output_bytes'])
