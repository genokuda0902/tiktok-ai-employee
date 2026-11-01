"""Offline synthetic CI: exact frame count, full decode and untouched AAC."""
from pathlib import Path
import subprocess, tempfile, json, importlib.util, hashlib
spec=importlib.util.spec_from_file_location('content_parallax',str(Path(__file__).resolve().parents[1]/'code/content_parallax.py'))
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

def cmd(args):
 return subprocess.run(args,check=True,capture_output=True,text=True).stdout

def audio_sha(path):
 with tempfile.NamedTemporaryFile(suffix='.aac') as f:
  cmd(['ffmpeg','-v','error','-y','-i',str(path),'-map','0:a:0','-c:a','copy','-f','adts',f.name])
  return hashlib.sha256(Path(f.name).read_bytes()).hexdigest()

with tempfile.TemporaryDirectory() as td:
 td=Path(td);src=td/'s.mp4';dst=td/'d.mp4'
 cmd(['ffmpeg','-v','error','-y','-f','lavfi','-i','testsrc2=size=1080x1920:rate=30:duration=2',
      '-f','lavfi','-i','sine=frequency=440:sample_rate=48000:duration=2',
      '-c:v','libx264','-preset','ultrafast','-crf','28','-c:a','aac','-shortest',str(src)])
 info=m.render(src,dst)
 assert info['frames_expected']==60,info
 assert m.check_video(m.probe(dst))==60
 cmd(['ffmpeg','-v','error','-i',str(dst),'-map','0:v:0','-f','null','-','-map','0:a:0','-f','null','-'])
 assert audio_sha(src)==audio_sha(dst),'Audio AAC bitstream changed'
 print(json.dumps({'synthetic_frames':60,'full_decode':'PASS','aac_copy':'PASS'}))
