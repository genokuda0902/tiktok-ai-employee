"""Synthetic, no private media. Does not certify real Japanese speech/captions."""
import hashlib,json,subprocess,tempfile
from pathlib import Path
from scene_parallax import POLICY,sha256,render
with tempfile.TemporaryDirectory() as d:
 p=Path(d);source=p/'source.mp4';out=p/'out.mp4'
 subprocess.run(['ffmpeg','-v','error','-y','-f','lavfi','-i','testsrc2=size=1080x1920:rate=30:duration=2',
 '-f','lavfi','-i','sine=frequency=440:sample_rate=48000:duration=2',
 '-c:v','libx264','-preset','ultrafast','-threads','2','-pix_fmt','yuv420p','-c:a','aac','-shortest',str(source)],check=True)
 manifest=p/'manifest.json';manifest.write_text(json.dumps({'policy':POLICY,'asset_approval':'review_only_no_publication','manual_post_only':True,'source_sha256':sha256(source),'genre':'ai','layout_id':'eight_scene_v1'}))
 report=render(source,out,manifest,p/'report.json',smoke=True)
 assert report['frames']==60 and report['changed_frames']>20
 subprocess.run(['ffmpeg','-v','error','-xerror','-i',str(out),'-f','null','-'],check=True)
 print('SYNTHETIC_SMOKE_PASS',report['frames'],report['changed_frames'])
