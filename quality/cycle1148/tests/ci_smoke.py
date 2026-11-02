"""Synthetic-only full-duration video test, no private assets."""
import hashlib,json,subprocess,tempfile
from pathlib import Path
from cta_cards import render,POLICY
with tempfile.TemporaryDirectory() as d:
 d=Path(d);src=d/'src.mp4';out=d/'out.mp4';man=d/'manifest.json'
 subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y',
 '-f','lavfi','-i','color=c=#123047:s=1080x1920:r=30:d=23.1',
 '-f','lavfi','-i','sine=frequency=340:sample_rate=48000:duration=23.1',
 '-c:v','libx264','-preset','ultrafast','-crf','33','-pix_fmt','yuv420p',
 '-c:a','aac','-ar','48000','-shortest',str(src)],check=True)
 man.write_text(json.dumps({'policy':POLICY,'genre':'ai',
 'source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),
 'asset_approval':'review_only_original_graphics','steps':[20.55,20.95,21.55,23.07]}))
 report=render(src,out,man,d)
 subprocess.run(['ffmpeg','-v','error','-xerror','-i',str(out),'-f','null','-'],check=True)
 assert report['frames']==693
 print('Synthetic 23.1s A/V smoke PASS',report['frames'])
