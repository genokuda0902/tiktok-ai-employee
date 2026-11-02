import hashlib,json,subprocess,tempfile
from pathlib import Path
from proof_story import POLICY,sha256,render,probe
with tempfile.TemporaryDirectory() as t:
    d=Path(t);src=d/'synthetic.mp4';out=d/'review.mp4';m=d/'manifest.json'
    subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','lavfi','-i','color=c=#0d263e:s=1080x1920:r=30:d=5','-f','lavfi','-i','sine=frequency=440:sample_rate=48000:duration=5','-c:v','libx264','-threads','2','-preset','ultrafast','-pix_fmt','yuv420p','-c:a','aac','-ar','48000','-shortest',str(src)],check=True)
    m.write_text(json.dumps({'policy':POLICY,'asset_approval':'review_only_no_publication','manual_post_only':True,'source_sha256':sha256(src),'genre':'ai','window':[1,3.8]}))
    result=render(src,out,m,d/'work')
    subprocess.run(['ffmpeg','-v','error','-i',str(out),'-f','null','-'],check=True)
    assert probe(out)[1]==150,result
    print('SYNTHETIC QA PASS',result)
