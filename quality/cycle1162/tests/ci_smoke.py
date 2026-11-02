"""Synthetic-only CI smoke: no user media in GitHub."""
import hashlib
import json
import subprocess
import tempfile
from pathlib import Path
from efficient_encode import POLICY, render, sha256

with tempfile.TemporaryDirectory() as d:
    d = Path(d)
    source = d/'synthetic.mp4'; output = d/'compressed.mp4'
    subprocess.run(['ffmpeg','-v','error','-y','-f','lavfi','-i',
                    'testsrc2=size=1080x1920:rate=30:duration=2',
                    '-f','lavfi','-i','sine=frequency=440:sample_rate=48000:duration=2',
                    '-c:v','libx264','-preset','ultrafast','-crf','12', '-threads','2',
                    '-c:a','aac','-b:a','128k','-pix_fmt','yuv420p',str(source)],check=True)
    manifest = d/'manifest.json'
    manifest.write_text(json.dumps({'policy':POLICY,'asset_approval':'review_only_no_publication',
        'manual_post_only':True,'genre':'ai','layout_id':'eight_scene_v1',
        'source_sha256':sha256(source)}))
    result = render(source, output, manifest, d/'qa.json', smoke=True)
    assert result['quality_gates_pass'] and output.stat().st_size > 1000
    print('Synthetic full A/V and quality gates PASS',result['full_ssim'],result['caption_ssim'])
