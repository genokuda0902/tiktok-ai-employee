"""No private source media: synthetic-only A/V render for GitHub Actions."""
import json
import subprocess
import tempfile
from pathlib import Path
from cinematic_glow import POLICY,render,sha256

with tempfile.TemporaryDirectory() as td:
    d=Path(td);src=d/'source.mp4';out=d/'output.mp4';manifest=d/'manifest.json';report=d/'qa.json'
    subprocess.run(['ffmpeg','-v','error','-y','-f','lavfi','-i','color=c=#152c44:s=1080x1920:r=30:d=2',
                    '-f','lavfi','-i','sine=frequency=440:sample_rate=48000:duration=2',
                    '-c:v','libx264','-threads','2','-preset','ultrafast','-pix_fmt','yuv420p',
                    '-c:a','aac','-ar','48000','-shortest',str(src)],check=True)
    manifest.write_text(json.dumps({'policy':POLICY,'asset_approval':'review_only_no_publication',
            'manual_post_only':True,'genre':'ai','source_sha256':sha256(src),
            'window':[.3,1.5],'chapter_edges':[0,1,2]}))
    try: q=render(src,out,manifest,report)
    except Exception:
        print(report.read_text() if report.exists() else "NO REPORT")
        raise
    assert q['technical_pass'] and q['after']['frames']==60 and q['audio_adts_bit_identical']
    print('SYNTHETIC AV + CHAPTER AUDIO QA PASS')
