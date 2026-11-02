"""Synthetic-only CI: no real user MP4, no external assets, no publishing."""
import importlib.util
import json
import subprocess
import tempfile
from pathlib import Path
P=Path(__file__).resolve().parents[1]/'code'/'chapter_tail_pacing.py'
spec=importlib.util.spec_from_file_location('chapter_tail_pacing',P)
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
def run(a):subprocess.run(a,check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
def main():
 with tempfile.TemporaryDirectory() as d:
  src,dst=Path(d)/'source.mp4',Path(d)/'out.mp4'
  run(['ffmpeg','-y','-loglevel','error','-f','lavfi','-i','color=c=#101e32:s=1080x1920:r=30:d=3',
       '-f','lavfi','-i','sine=frequency=440:sample_rate=48000:duration=2.3',
       '-filter_complex','[1:a]apad=pad_dur=0.7[a]','-map','0:v','-map','[a]',
       '-c:v','libx264','-preset','ultrafast','-pix_fmt','yuv420p','-c:a','aac','-t','3',str(src)])
  result=m.optimize(src,dst,genre='travel')
  assert 0.25<=result['saved_seconds']<=0.55,result
  assert result['output_frames']<result['source_frames'],result
  run(['ffmpeg','-v','error','-xerror','-i',str(dst),'-f','null','-'])
  streams=m.probe(dst)['streams']
  v=next(s for s in streams if s['codec_type']=='video')
  a=next(s for s in streams if s['codec_type']=='audio')
  assert (v['width'],v['height'],v['codec_name'])==(1080,1920,'h264')
  assert (a['codec_name'],a['sample_rate'])==('aac','48000')
  print('PASS synthetic 1080x1920 A/V, tail detection, shortened MP4, full decode',json.dumps(result))
if __name__=='__main__':main()
