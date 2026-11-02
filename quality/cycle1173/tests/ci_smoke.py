"""Synthetic A/V only: no private user footage or audio is uploaded to GitHub."""
import json
import subprocess
import sys
import tempfile
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import clean_audio_rail as q

with tempfile.TemporaryDirectory() as d:
    d=Path(d)
    src=d/'source.mp4'; out=d/'out.mp4'; man=d/'manifest.json'; rep=d/'report.json'
    subprocess.run(['ffmpeg','-v','error','-y','-f','lavfi','-i','color=c=0x0b1730:s=1080x1920:r=30:d=2.0',
        '-f','lavfi','-i','sine=frequency=440:sample_rate=48000:duration=2.0',
        '-c:v','libx264','-preset','ultrafast','-pix_fmt','yuv420p','-c:a','aac','-ar','48000','-shortest',str(src)],check=True)
    man.write_text(json.dumps({'policy':q.POLICY,'asset_approval':'review_only_no_publication',
       'manual_post_only':True,'roi_reviewed':True,'source_sha256':q.digest(src),
       'genre':'ai','caption_safe_bottom':q.CAPTION_SAFE_BOTTOM}))
    result=q.render(src,out,man,rep)
    assert result['technical_pass'] and result['audio_bit_identical']
    print('Synthetic 60-frame A/V smoke PASS')
