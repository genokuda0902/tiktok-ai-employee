import importlib.util
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

spec=importlib.util.spec_from_file_location('cinematic_hero_light',Path(__file__).with_name('cinematic_hero_light.py'))
m=importlib.util.module_from_spec(spec);sys.modules[spec.name]=m;spec.loader.exec_module(m)

@unittest.skipUnless(shutil.which('ffmpeg') and shutil.which('ffprobe'),'requires free ffmpeg')
class SyntheticVideoTests(unittest.TestCase):
    def test_h264_aac_jpn_render_and_decode(self):
        with tempfile.TemporaryDirectory() as d:
            d=Path(d);src=d/'source.mp4';dst=d/'result.mp4';report=d/'qa.json'
            subprocess.run(['ffmpeg','-v','error','-y','-f','lavfi','-i','color=c=0x123049:s=1080x1920:r=30',
                '-f','lavfi','-i','sine=frequency=440:sample_rate=48000','-t','1.5','-shortest',
                '-c:v','libx264','-threads','2','-pix_fmt','yuv420p','-c:a','aac','-metadata:s:a:0','language=jpn',str(src)],check=True)
            manifest={'policy':m.POLICY,'asset_approval':'private_review_only','source_sha256':m.sha256(src),
                'genre':'ai','roi':{'x':110,'y':475,'width':670,'height':500},
                'start_frame':4,'sweep_frames':29,'color_rgb':[105,220,245],'max_alpha':0.16}
            r=m.render(src,dst,manifest,report)
            self.assertEqual(r['frames'],45)
            self.assertEqual(r['resolution'],[1080,1920])
            self.assertTrue(dst.stat().st_size>10000)
            self.assertTrue(json.loads(report.read_text())['output_sha256'])

if __name__=='__main__':unittest.main()
