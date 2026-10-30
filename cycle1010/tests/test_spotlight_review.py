import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path
src=Path(__file__).resolve().parents[1]/'source'/'spotlight_review.py'
spec=importlib.util.spec_from_file_location('spotlight_review',src)
mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)

class SpotlightTests(unittest.TestCase):
    def test_genre_catalog_has_ten(self):self.assertEqual(len(mod.GENRES),10)
    def test_fail_closed_other_genre(self):
        with self.assertRaisesRegex(ValueError,'fail closed'):
            mod.validate_source('/missing','/missing2','business',True,mod.SOURCE_SHA256)
    def test_review_required(self):
        with self.assertRaisesRegex(ValueError,'review-only'):
            mod.validate_source('/missing','/missing2','ai_work',False,mod.SOURCE_SHA256)
    def test_first_frame_is_clean(self):self.assertEqual(mod.phase(0),('none',0.0))
    def test_end_frame_is_clean(self):self.assertEqual(mod.phase(1.5),('none',0.0))
    def test_before_mid(self):self.assertEqual(mod.phase(0.4),('before',1.0))
    def test_after_mid(self):self.assertEqual(mod.phase(1.1),('after',1.0))
    def test_smooth_transition(self):
        for t in [0.15,0.22,0.69,0.81,0.86,1.41]:
            side,x=mod.phase(t);self.assertIn(side,('before','after'));self.assertTrue(0<=x<=1)
    def test_caption_safe(self):self.assertLessEqual(mod.OVERLAY_Y+mod.OVERLAY_HEIGHT,mod.CAPTION_SAFE_Y)
    def test_duration(self):self.assertEqual(mod.END_FRAME,45)
    def test_sha_mismatch_fails(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'dummy.mp4';p.write_bytes(b'not a video')
            with self.assertRaisesRegex(ValueError,'SHA256 mismatch'):
                mod.validate_source(p,Path(d)/'out.mp4','ai_work',True,mod.SOURCE_SHA256)
if __name__=='__main__':unittest.main()
