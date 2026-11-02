import json,subprocess,tempfile
from pathlib import Path
from prompt_contrast import POLICY,render,sha256
with tempfile.TemporaryDirectory() as t:
 d=Path(t);src=d/'s.mp4';out=d/'o.mp4';man=d/'m.json'
 subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','lavfi','-i','color=c=0x11253a:s=1080x1920:r=30:d=2',
 '-f','lavfi','-i','sine=frequency=600:sample_rate=48000:duration=2','-c:v','libx264','-threads','2','-preset','ultrafast',
 '-pix_fmt','yuv420p','-c:a','aac','-ar','48000','-shortest',str(src)],check=True)
 man.write_text(json.dumps({'policy':POLICY,'genre':'ai','source_sha256':sha256(src),
 'asset_approval':'review_only_no_publication','manual_post_only':True,'window':[0.3,1.7]}))
 r=render(src,out,man,d)
 subprocess.run(['ffmpeg','-v','error','-i',str(out),'-f','null','-'],check=True)
 assert r['frames']==60,r
 print('SYNTHETIC_2S_60FRAME_AV_PASS')
