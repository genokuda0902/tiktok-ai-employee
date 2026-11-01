"""Offline synthetic 2s render/decode. No user footage in CI."""
import sys,subprocess,tempfile
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from soft_scene_cut import render
with tempfile.TemporaryDirectory() as td:
    src=Path(td)/'source.mp4';dst=Path(td)/'result.mp4'
    subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y',
        '-f','lavfi','-i','color=c=0x092034:s=1080x1920:r=30:d=1',
        '-f','lavfi','-i','color=c=0x2f736f:s=1080x1920:r=30:d=1',
        '-f','lavfi','-i','sine=frequency=440:sample_rate=48000:duration=2',
        '-filter_complex','[0:v][1:v]concat=n=2:v=1:a=0[v]',
        '-map','[v]','-map','2:a','-c:v','libx264','-preset','ultrafast',
        '-pix_fmt','yuv420p','-c:a','aac',str(src)],check=True)
    assert render(src,dst,cuts=(30,),genre='travel')==60
    subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-xerror',
        '-i',str(dst),'-f','null','-'],check=True)
    print('synthetic full decode PASS')
