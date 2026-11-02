"""Offline synthetic A/V smoke. No paid APIs or source assets."""
import sys,tempfile,subprocess
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from scene_zoom import render
def cmd(a):
 p=subprocess.run(a,capture_output=True,text=True)
 if p.returncode:raise RuntimeError(p.stderr[-1000:])
with tempfile.TemporaryDirectory() as td:
 src=Path(td)/'source.mp4';out=Path(td)/'result.mp4'
 cmd(['ffmpeg','-v','error','-y','-f','lavfi','-i','testsrc2=size=1080x1920:rate=30:duration=1.1',
      '-f','lavfi','-i','sine=frequency=440:sample_rate=48000:duration=1.1',
      '-c:v','libx264','-preset','ultrafast','-crf','28','-pix_fmt','yuv420p',
      '-c:a','aac','-b:a','96k','-metadata:s:a:0','language=jpn','-shortest',str(src)])
 r=render(src,out,'ai')
 assert r['frames']==33 and r['resolution']==[1080,1920] and r['audio_bitstream_identical']
 print('SMOKE PASS',r['frames'])
