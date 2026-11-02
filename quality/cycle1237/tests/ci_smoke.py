"""Offline 36-frame video smoke test. Uses only generated synthetic footage/audio."""
import importlib.util
import subprocess
import tempfile
from pathlib import Path
root=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('mod',root/'clean_comparison.py')
mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
with tempfile.TemporaryDirectory() as td:
 d=Path(td);meta=d/'chapters.txt'
 meta.write_text(';FFMETADATA1\n[CHAPTER]\nTIMEBASE=1/1000\nSTART=0\nEND=1200\ntitle=synthetic\n')
 src=d/'src.mp4';dst=d/'dst.mp4'
 cmd=['ffmpeg','-v','error','-y','-f','lavfi','-i','color=c=#08101e:s=1080x1920:r=30:d=1.2',
  '-f','lavfi','-i','sine=frequency=220:sample_rate=48000:duration=1.2',
  '-f','ffmetadata','-i',str(meta),'-map','0:v','-map','1:a','-map_chapters','2',
  '-c:v','libx264','-preset','ultrafast','-pix_fmt','yuv420p','-c:a','aac','-shortest',str(src)]
 subprocess.run(cmd,check=True)
 qa=mod.render(src,dst,start=0,end=1.2)
 assert qa['frames']==36 and qa['chapters']==1 and qa['audio_bitstream_identical']
 print('Synthetic 36-frame A/V smoke: PASS')
