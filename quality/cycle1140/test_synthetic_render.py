"""CI uses synthetic private-review-labelled A/V, never user media."""
import importlib.util
import json
import subprocess
import sys
import tempfile
from pathlib import Path
spec=importlib.util.spec_from_file_location('subject_push',Path(__file__).with_name('subject_push.py'))
m=importlib.util.module_from_spec(spec);sys.modules[spec.name]=m;spec.loader.exec_module(m)
with tempfile.TemporaryDirectory() as td:
    td=Path(td);src=td/'s.mp4';dst=td/'d.mp4'
    subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','lavfi','-i','color=c=navy:s=1080x1920:r=30:d=2.5',
        '-f','lavfi','-i','sine=frequency=440:sample_rate=48000:duration=2.5','-c:v','libx264','-preset','ultrafast',
        '-pix_fmt','yuv420p','-c:a','aac','-metadata:s:a:0','language=jpn','-shortest',str(src)],check=True)
    manifest={'policy':m.POLICY,'asset_approval':'private_review_only','source_sha256':m.digest(src),'genre':'ai',
        'roi':{'x':110,'y':475,'width':670,'height':500},'start_frame':3,'motion_frames':56,'max_zoom':1.08,'feather_px':32,'title_guard_px':90}
    result=m.render(src,dst,manifest,td/'qa.json')
    assert result['frames']==75 and dst.stat().st_size>1000,result
    print(json.dumps(result,ensure_ascii=False))
