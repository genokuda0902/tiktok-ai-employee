"""Only generated synthetic media, never private reference/audio."""
import json,subprocess,tempfile
from pathlib import Path
from before_after_motion import POLICY,digest,render

def run(x):subprocess.run(x,check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
with tempfile.TemporaryDirectory() as d:
    d=Path(d);src=d/'s.mp4';out=d/'o.mp4';m=d/'manifest.json';report=d/'qa.json'
    run(['ffmpeg','-y','-f','lavfi','-i','color=c=0x071021:s=1080x1920:r=30:d=23.033333',
         '-f','lavfi','-i','sine=frequency=440:sample_rate=48000:duration=23.033333',
         '-c:v','libx264','-preset','ultrafast','-threads','2','-pix_fmt','yuv420p',
         '-c:a','aac','-b:a','96k','-shortest',str(src)])
    m.write_text(json.dumps({'policy':POLICY,'asset_approval':'review_only_no_publication',
                'manual_post_only':True,'genre':'ai','source_sha256':digest(src),'window':[20.5,22.99]}))
    r=render(src,out,m,report)
    assert r['technical_pass'] and r['aac_adts_bit_identical'] and out.exists()
    print('Synthetic-only full 23s A/V smoke PASS')