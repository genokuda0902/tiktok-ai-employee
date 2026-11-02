"""Synthetic 1080x1920 3-second MP4 render, keyframe and full decode smoke."""
import sys
import tempfile
import subprocess
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'code'))
from scene_keyframe_packager import render,keyframes

with tempfile.TemporaryDirectory() as tmp:
    src,dst=Path(tmp)/'input.mp4',Path(tmp)/'output.mp4'
    subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y',
                    '-f','lavfi','-i','color=c=0x061625:s=1080x1920:r=30:d=3',
                    '-f','lavfi','-i','sine=frequency=250:sample_rate=48000:duration=3',
                    '-c:v','libx264','-preset','ultrafast','-pix_fmt','yuv420p',
                    '-c:a','aac','-shortest',str(src)],check=True)
    result=render(src,dst,(30,60),crf=19,preset='medium')
    assert result['frames']==90,result
    assert result['faststart']
    assert len(keyframes(dst))>=3
    subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-xerror',
                    '-i',str(dst),'-map','0:v:0','-map','0:a:0','-f','null','-'],check=True)
    print('SYNTHETIC 1080x1920 90f PASS',result)
