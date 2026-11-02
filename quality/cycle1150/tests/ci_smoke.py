import json,subprocess,tempfile
from pathlib import Path
from proof_first_hook import POLICY,render,sha256
with tempfile.TemporaryDirectory() as t:
    d=Path(t);src=d/'synthetic.mp4';out=d/'review.mp4';man=d/'manifest.json'
    subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y',
       '-f','lavfi','-i','color=c=0x091c2d:s=1080x1920:r=30:d=2.0',
       '-f','lavfi','-i','sine=frequency=440:sample_rate=48000:duration=2.0',
       '-c:v','libx264','-threads','2','-preset','ultrafast','-pix_fmt','yuv420p',
       '-c:a','aac','-ar','48000','-shortest',str(src)],check=True)
    man.write_text(json.dumps({'policy':POLICY,'genre':'ai','source_sha256':sha256(src),
       'asset_approval':'review_only_no_publication','manual_post_only':True,
       'proof_text':'46 ＋ 29 ＝ 75','proof_numbers':[46,29,75],
       'window':[0.12,1.5]}),encoding='utf-8')
    r=render(src,out,man,d)
    subprocess.run(['ffmpeg','-v','error','-i',str(out),'-f','null','-'],check=True)
    assert r['frames']==60,r
    print('SYNTHETIC_2S_AV_PASS',r['frames'])
