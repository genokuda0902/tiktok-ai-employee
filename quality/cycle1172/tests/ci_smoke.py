"""Synthetic-only CI. Never uploads original/derived private MP4."""
import importlib.util
import json
import subprocess
import tempfile
from pathlib import Path
P=Path(__file__).resolve().parents[1]/'kinetic_hook.py'
s=importlib.util.spec_from_file_location('kinetic_hook',P)
k=importlib.util.module_from_spec(s);s.loader.exec_module(k)
with tempfile.TemporaryDirectory() as td:
 td=Path(td);src=td/'source.mp4';out=td/'out.mp4';m=td/'manifest.json';q=td/'qa.json'
 subprocess.run(['ffmpeg','-y','-loglevel','error','-f','lavfi','-i','color=c=0x07182b:s=1080x1920:r=30:d=4',
  '-f','lavfi','-i','sine=frequency=440:sample_rate=48000:duration=4','-c:v','libx264',
  '-preset','ultrafast','-threads','2','-pix_fmt','yuv420p','-c:a','aac','-t','4',str(src)],check=True)
 m.write_text(json.dumps({'policy':k.POLICY,'asset_approval':'review_only_no_publication',
  'manual_post_only':True,'source_sha256':k.sha(src),'roi_reviewed':True,
  'genre':'ai','hook_labels':['集計','確認','報告'],'caption_top':1280,'hook_window':[0.0,1.45]}),encoding='utf-8')
 result=k.render(src,out,m,q)
 assert result['technical_pass'] and result['aac_bit_identical'] and out.stat().st_size>0
 print('synthetic smoke PASS',out.stat().st_size)
