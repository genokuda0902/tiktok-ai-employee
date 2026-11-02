import importlib.util
import json
import subprocess
import tempfile
import unittest
from pathlib import Path

spec=importlib.util.spec_from_file_location('dissolve',Path(__file__).with_name('scene_wipe.py'))
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

class SceneWipeTests(unittest.TestCase):
    def setUp(self):
        self.spec={'frames':180,'duration':6,'width':1080,'height':1920}
        self.man={'policy':m.POLICY,'asset_approval':'private_review_only','source_sha256':'sha','genre':'ai',
                  'roi':{'x':60,'y':190,'width':960,'height':900},'cut_frames':[45,90], 'transition_frames':8}
    def test_all_ten_genres(self):
        for g in m.GENRES:
            self.man['genre']=g
            self.assertEqual(m.validate(self.man,'sha',self.spec)[0],[45,90])
    def test_reject_wrong_sha(self):
        with self.assertRaises(ValueError):m.validate(self.man,'other',self.spec)
    def test_reject_missing_approval(self):
        self.man['asset_approval']='public'
        with self.assertRaises(ValueError):m.validate(self.man,'sha',self.spec)
    def test_reject_subtitle_roi(self):
        self.man['roi']['y']=600
        with self.assertRaises(ValueError):m.validate(self.man,'sha',self.spec)
    def test_reject_unsorted_cuts(self):
        self.man['cut_frames']=[90,45]
        with self.assertRaises(ValueError):m.validate(self.man,'sha',self.spec)
    def test_reject_too_short_dissolve(self):
        self.man['transition_frames']=1
        with self.assertRaises(ValueError):m.validate(self.man,'sha',self.spec)
    def test_reject_missing_fields(self):
        del self.man['genre']
        with self.assertRaises(ValueError):m.validate(self.man,'sha',self.spec)
    def test_wipe_mask_moves_and_is_crisp(self):
        a=m.wipe_alpha(100,0.25,feather=8)
        b=m.wipe_alpha(100,0.75,feather=8)
        self.assertEqual(a[0],0)
        self.assertEqual(a[-1],255)
        self.assertEqual(b[0],0)
        self.assertEqual(b[-1],255)
        self.assertLess(sum(b),sum(a))
        self.assertLess(sum(0<v<255 for v in a),12)
    def test_synthetic_render(self):
        with tempfile.TemporaryDirectory() as t:
            src=Path(t)/'source.mp4';dst=Path(t)/'output.mp4';report=Path(t)/'qa.json'
            # Synthetic 4-second two-scene video; NO private assets in CI.
            v1=Path(t)/'a.mp4';v2=Path(t)/'b.mp4'
            for p,color in [(v1,'0x112233'),(v2,'0x446688')]:
                subprocess.run(['ffmpeg','-v','error','-y','-f','lavfi','-i',f'color=c={color}:s=1080x1920:r=30:d=2',
                    '-f','lavfi','-i','sine=frequency=440:sample_rate=48000:duration=2',
                    '-c:v','libx264','-preset','ultrafast','-crf','30','-pix_fmt','yuv420p',
                    '-c:a','aac','-ar','48000','-ac','2','-metadata:s:a:0','language=jpn','-shortest',str(p)],check=True)
            lst=Path(t)/'list.txt';lst.write_text(f"file '{v1}'\nfile '{v2}'\n")
            subprocess.run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i',str(lst),'-c','copy',str(src)],check=True)
            self.man['source_sha256']=m.sha256(src)
            self.man['cut_frames']=[60]
            self.assertEqual(m.probe(src)['frames'],120)
            q=m.render(src,dst,self.man,report)
            self.assertEqual(q['frames'],120)
            self.assertGreater(q['cut_content_mae'][0],8)
            self.assertTrue(json.loads(report.read_text())['review_only'])
            self.assertEqual(m.probe(dst)['frames'],120)

if __name__=='__main__':unittest.main()
