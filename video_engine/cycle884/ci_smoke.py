"""Synthetic-only CI smoke: never reads/uploads private review footage."""
import subprocess
import tempfile
from pathlib import Path
from row_focus import create_overlays,frame_overlay

def run(args):subprocess.run(args,check=True,timeout=100,stdout=subprocess.DEVNULL)
with tempfile.TemporaryDirectory() as d:
    d=Path(d);frames=d/'overlay';create_overlays(frames,count=45)
    source=d/'source.mp4';output=d/'result.mp4'
    run(['ffmpeg','-v','error','-y','-f','lavfi','-i','color=c=0x132039:s=1080x1920:r=30:d=1.5',
         '-f','lavfi','-i','sine=frequency=440:sample_rate=48000:duration=1.5',
         '-shortest','-c:v','libx264','-preset','ultrafast','-pix_fmt','yuv420p',
         '-c:a','aac',str(source)])
    run(['ffmpeg','-v','error','-y','-i',str(source),'-framerate','30','-i',str(frames/'%03d.png'),
         '-filter_complex','[0:v][1:v]overlay=0:0:shortest=1:format=auto[v]',
         '-map','[v]','-map','0:a:0','-c:v','libx264','-preset','ultrafast',
         '-pix_fmt','yuv420p','-c:a','copy',str(output)])
    run(['ffmpeg','-v','error','-xerror','-i',str(output),'-f','null','-'])
    assert output.stat().st_size>1000
print('SYNTHETIC 45-frame H264/AAC smoke PASS')
