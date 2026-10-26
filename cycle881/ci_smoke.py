"""Synthetic-only CI; no private Japanese media uploaded or read."""
from dataclasses import replace
import subprocess,tempfile
from pathlib import Path
import imageio_ffmpeg
from proof_audit_scene import DEFAULT,GENRES,validate_proof,progress,review_caption_alignment,CAPTIONS
for genre in GENRES:assert validate_proof(replace(DEFAULT,genre=genre))==(46,29)
assert progress(85)==2
assert not review_caption_alignment(CAPTIONS)['semantic_match_verified']
exe=imageio_ffmpeg.get_ffmpeg_exe()
with tempfile.TemporaryDirectory() as td:
    p=Path(td)/'smoke.mp4'
    subprocess.run([exe,'-v','error','-y','-f','lavfi','-i','color=c=navy:s=360x640:r=30:d=1',
       '-f','lavfi','-i','sine=frequency=440:sample_rate=48000:duration=1',
       '-c:v','libx264','-pix_fmt','yuv420p','-c:a','aac','-shortest',str(p)],
       check=True,timeout=90)
    subprocess.run([exe,'-v','error','-i',str(p),'-f','null','-'],check=True,timeout=90)
print('PASS: synthetic A/V, 10 genres, unverified caption approval gate')
