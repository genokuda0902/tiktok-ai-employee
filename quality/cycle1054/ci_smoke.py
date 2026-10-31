"""Synthetic A/V smoke only. Does NOT validate private 23s Japanese MP4."""
from pathlib import Path
import subprocess,tempfile
from prompt_story import render_frame

def run(cmd):subprocess.run(cmd,check=True,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
with tempfile.TemporaryDirectory() as t:
    p=Path(t);render_frame(30).convert('RGB').save(p/'frame.png');out=p/'synthetic.mp4'
    run(['ffmpeg','-y','-loop','1','-framerate','30','-t','1.5','-i',str(p/'frame.png'),'-f','lavfi','-i','sine=frequency=600:sample_rate=48000:duration=1.5','-shortest','-c:v','libx264','-preset','ultrafast','-pix_fmt','yuv420p','-c:a','aac',str(out)])
    run(['ffmpeg','-v','error','-i',str(out),'-f','null','-'])
    assert out.stat().st_size>1000
print('synthetic 1.5s H264/AAC full decode PASS')
