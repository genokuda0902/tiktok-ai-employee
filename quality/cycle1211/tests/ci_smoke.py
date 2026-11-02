"""Self-contained 2-second synthetic media smoke: no copyrighted or user assets."""
import sys,subprocess,tempfile
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'code'))
from scene_focus import render,check_probe
with tempfile.TemporaryDirectory() as td:
 src=Path(td)/'synthetic.mp4';dst=Path(td)/'focus.mp4'
 subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','lavfi','-i',
  'color=c=#12313a:s=1080x1920:r=30:d=2','-f','lavfi','-i',
  'sine=frequency=440:sample_rate=48000:duration=2',
  '-c:v','libx264','-preset','ultrafast','-pix_fmt','yuv420p',
  '-c:a','aac','-ar','48000','-t','2',str(src)],check=True)
 result=render(src,dst,'ai',[{'start':0,'end':60,'rect':[100,400,800,1000]}])
 assert result['frames']==60
 assert next(s for s in check_probe(dst)['streams'] if s['codec_type']=='video')['nb_frames']=='60'
 for kind in ['v:0','a:0']:
  subprocess.run(['ffmpeg','-v','error','-i',str(dst),'-map',f'0:{kind}','-f','null','-'],check=True)
 print('Synthetic 60-frame 1080x1920 H264/AAC PASS')
