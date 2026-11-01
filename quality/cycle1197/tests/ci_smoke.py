"""Synthetic 2s H264/AAC video; no private media."""
import subprocess,sys,tempfile
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'code'))
from audio_meter import main
with tempfile.TemporaryDirectory() as tmp:
 d=Path(tmp); source=d/'in.mp4'; out=d/'out.mp4'
 subprocess.run(['ffmpeg','-y','-v','error','-f','lavfi','-i',
  'color=c=black:s=1080x1920:r=30:d=2','-f','lavfi','-i',
  'sine=frequency=400:sample_rate=48000:duration=2','-c:v','libx264',
  '-preset','ultrafast','-pix_fmt','yuv420p','-c:a','aac',
  '-shortest',str(source)],check=True)
 sys.argv=['audio_meter.py',str(source),str(out),'--overlay-dir',str(d/'frames')]
 main()
 subprocess.run(['ffmpeg','-v','error','-xerror','-i',str(out),'-f','null','-'],check=True)
 assert out.exists() and out.stat().st_size>1000
 print('SYNTHETIC_SMOKE_PASS')
