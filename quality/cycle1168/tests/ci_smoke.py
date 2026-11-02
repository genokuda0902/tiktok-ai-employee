"""Synthetic-only A/V CI, never includes private production media."""
import hashlib,json,subprocess,tempfile
from pathlib import Path
from prompt_reading_focus import POLICY,DEFAULT_STEPS,render
with tempfile.TemporaryDirectory() as tmp:
 d=Path(tmp);source=d/'synthetic.mp4';out=d/'result.mp4';manifest=d/'manifest.json';report=d/'report.json'
 subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','lavfi','-i','color=c=0x09182e:s=1080x1920:r=30:d=11',
                 '-f','lavfi','-i','sine=frequency=440:sample_rate=48000:duration=11',
                 '-c:v','libx264','-preset','ultrafast','-pix_fmt','yuv420p','-c:a','aac','-ar','48000','-shortest',str(source)],check=True)
 m={'policy':POLICY,'asset_approval':'review_only_no_publication','manual_post_only':True,'genre':'ai',
    'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'steps':DEFAULT_STEPS}
 manifest.write_text(json.dumps(m),encoding='utf-8')
 r=render(source,out,manifest,report)
 assert r['technical_pass'] and r['aac_adts_bit_identical'] and r['after']['frames']==330
 print('Synthetic-only 11-second full decode + audio preservation PASS')
