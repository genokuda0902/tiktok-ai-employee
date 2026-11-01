"""CI-only 2s synthetic 1080x1920 video, no private assets or paid APIs."""
import sys,subprocess,tempfile
from pathlib import Path
from dataclasses import replace
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'code'))
from calculation_trace import DEMO,render
with tempfile.TemporaryDirectory() as td:
    src=Path(td)/'synthetic.mp4';dst=Path(td)/'rendered.mp4'
    subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','lavfi','-i',
                    'color=c=0x0b2536:s=1080x1920:r=30:d=2','-f','lavfi','-i',
                    'sine=frequency=440:sample_rate=48000:duration=2','-c:v','libx264',
                    '-preset','ultrafast','-pix_fmt','yuv420p','-c:a','aac',str(src)],check=True)
    result=render(str(src),str(dst),replace(DEMO,first_frame=10,last_frame=46),genre='travel')
    assert result['frames']==60
    subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-i',str(dst),'-f','null','-'],check=True)
    print('Synthetic render and full decode PASS:',result)
