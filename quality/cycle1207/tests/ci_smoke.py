"""Synthetic 30-frame H264/AAC render, never private video."""
import importlib.util,json,subprocess,tempfile
from pathlib import Path
spec=importlib.util.spec_from_file_location('mid',Path(__file__).resolve().parents[1]/'midtone_lift.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
def run(cmd):subprocess.run(cmd,check=True,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
with tempfile.TemporaryDirectory() as td:
 src=Path(td)/'synthetic.mp4';dst=Path(td)/'out.mp4'
 run(['ffmpeg','-y','-f','lavfi','-i','color=c=0x10253a:s=1080x1920:r=30:d=1','-f','lavfi','-i','sine=frequency=300:sample_rate=48000:duration=1','-c:v','libx264','-preset','ultrafast','-pix_fmt','yuv420p','-c:a','aac','-shortest',str(src)])
 m.render(src,dst,frames=30)
 assert m.validate_source(m.probe(dst))==30
 run(['ffmpeg','-v','error','-i',str(dst),'-map','0:v:0','-f','null','-'])
 run(['ffmpeg','-v','error','-i',str(dst),'-map','0:a:0','-f','null','-'])
 print(json.dumps({'frames':30,'resolution':'1080x1920','decode':'PASS'}))
