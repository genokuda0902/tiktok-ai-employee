"""Synthetic-only smoke test: no private media in GitHub."""
from pathlib import Path
import json
import subprocess
import sys
import tempfile
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'code'))
from mobile_safe_footer import render

def run(*args):
    return subprocess.run(args,check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True).stdout

with tempfile.TemporaryDirectory() as d:
    src,dst=Path(d)/'synthetic.mp4',Path(d)/'rendered.mp4'
    run('ffmpeg','-hide_banner','-loglevel','error','-y',
        '-f','lavfi','-i','testsrc2=size=1080x1920:rate=30:duration=2',
        '-f','lavfi','-i','sine=frequency=440:sample_rate=48000:duration=2',
        '-c:v','libx264','-preset','ultrafast','-crf','28','-pix_fmt','yuv420p',
        '-c:a','aac','-b:a','96k','-shortest',str(src))
    render(src,dst)
    meta=json.loads(run('ffprobe','-v','error','-select_streams','v:0',
                        '-show_entries','stream=width,height,nb_frames',
                        '-of','json',str(dst)))['streams'][0]
    assert (meta['width'],meta['height'])==(1080,1920),meta
    assert int(meta['nb_frames'])==60,meta
    run('ffmpeg','-v','error','-xerror','-i',str(dst),'-f','null','-')
    print('Synthetic 60-frame 1080x1920 H264/AAC full decode PASS')
