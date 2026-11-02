import hashlib,json,subprocess,tempfile
from pathlib import Path
from problem_visual import POLICY,render,sha256,probe
with tempfile.TemporaryDirectory() as t:
 d=Path(t);src=d/'synthetic.mp4';out=d/'out.mp4';m=d/'manifest.json'
 subprocess.run(['ffmpeg','-v','error','-y','-f','lavfi','-i','color=c=navy:s=1080x1920:r=30:d=4','-f','lavfi','-i','sine=frequency=430:sample_rate=48000:duration=4','-c:v','libx264','-preset','ultrafast','-pix_fmt','yuv420p','-c:a','aac','-shortest',str(src)],check=True)
 m.write_text(json.dumps({'policy':POLICY,'asset_approval':'review_only_no_publication','manual_post_only':True,'source_sha256':sha256(src),'genre':'ai','window':[1,3.1]}))
 r=render(src,out,m,d/'work');subprocess.run(['ffmpeg','-v','error','-xerror','-i',str(out),'-f','null','-'],check=True)
 assert probe(out)[1]==120
 print('SYNTHETIC_CI_PASS',r['output_sha256'])
