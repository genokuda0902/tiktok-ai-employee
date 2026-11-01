import hashlib
import importlib.util
import subprocess
import tempfile
import unittest
from pathlib import Path

spec=importlib.util.spec_from_file_location('caption_accessibility',Path(__file__).with_name('caption_accessibility.py'))
mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)

class CaptionsTest(unittest.TestCase):
    def test_eight_scene_cues(self):
        mod.validate_cues(mod.SCENE_CAPTIONS,23.033333)
        self.assertEqual(len(mod.SCENE_CAPTIONS),8)
    def test_ten_genres_shared(self):
        self.assertEqual(len(mod.GENRES),10)
        for genre in mod.GENRES:
            self.assertTrue(genre)
            mod.validate_cues(mod.SCENE_CAPTIONS,23.033333)
    def test_srt_japanese(self):
        s=mod.make_srt(mod.SCENE_CAPTIONS)
        self.assertIn('00:00:20,300 --> 00:00:23,033',s)
        self.assertIn('小さな時短を、毎日の習慣にしよう。',s)
    def test_fail_closed_timing(self):
        with self.assertRaises(ValueError): mod.validate_cues([(0,1,'OK'),(0.8,2,'overlap')],2)
        with self.assertRaises(ValueError): mod.validate_cues([(0,1,'OK')],3)
    def test_fail_closed_pii(self):
        with self.assertRaises(ValueError): mod.validate_cues([(0,3,'test@example.com')],3)
        with self.assertRaises(ValueError): mod.validate_cues([(0,3,'09012345678')],3)
    def test_synthetic_mux_and_hash_guard(self):
        with tempfile.TemporaryDirectory() as d:
            d=Path(d); src=d/'synthetic.mp4'; out=d/'out.mp4'; srt=d/'scene.srt'; report=d/'report.json'
            subprocess.run(['ffmpeg','-y','-v','error','-f','lavfi','-i','color=c=0x223344:s=320x568:r=15:d=3','-f','lavfi','-i','sine=frequency=440:sample_rate=48000:duration=3','-shortest','-c:v','libx264','-pix_fmt','yuv420p','-c:a','aac',str(src)],check=True)
            with self.assertRaises(ValueError): mod.build(src,out,srt,report,'0'*64,[(0,3,'これは合成動画です。')],(320,568),15)
            self.assertFalse(out.exists())
            r=mod.build(src,out,srt,report,mod.sha256(src),[(0,3,'これは合成動画です。')],(320,568),15)
            self.assertEqual(r['decode'],'PASS')
            self.assertTrue(out.is_file() and srt.is_file())
            with self.assertRaises(FileExistsError): mod.build(src,out,srt,report,mod.sha256(src),[(0,3,'合成動画')],(320,568),15)

if __name__=='__main__':unittest.main()
