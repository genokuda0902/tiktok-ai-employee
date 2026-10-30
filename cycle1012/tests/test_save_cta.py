import importlib.util
import tempfile
import unittest
from pathlib import Path

SRC=Path(__file__).resolve().parents[1]/'source'/'save_cta.py'
spec=importlib.util.spec_from_file_location('save_cta',SRC)
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

class TestSaveCTA(unittest.TestCase):
    def test_ten_genres_have_distinct_copy(self):
        self.assertEqual(len(m.GENRE_CTA),10)
        self.assertGreaterEqual(len(set(m.GENRE_CTA.values())),7)
    def test_fail_closed_unknown(self):
        with self.assertRaisesRegex(ValueError,'unknown'):
            m.validate('/missing','/tmp/out','unknown',True)
    def test_fail_closed_unapproved_genre(self):
        with self.assertRaisesRegex(ValueError,'approval'):
            m.validate('/missing','/tmp/out','health',True)
    def test_fail_closed_public_mode(self):
        with self.assertRaisesRegex(ValueError,'approval'):
            m.validate('/missing','/tmp/out','ai_work',False)
    def test_fail_closed_missing_media(self):
        with self.assertRaisesRegex(ValueError,'source/output'):
            m.validate('/missing','/tmp/out','ai_work',True)
    def test_placement_preserves_review_banner_and_subtitles(self):
        self.assertLess(m.OVERLAY_Y+m.OVERLAY_H,m.REVIEW_BANNER_Y)
        self.assertLess(m.OVERLAY_Y+m.OVERLAY_H,m.CAPTION_SAFE_Y)
    def test_only_final_scene(self):
        self.assertEqual(m.START_FRAME,630)
        self.assertEqual(m.TOTAL_FRAMES,691)
    def test_fade(self):
        self.assertEqual(m.fade(629),0)
        self.assertEqual(m.fade(630),0)
        self.assertGreater(m.fade(637),0)
        self.assertAlmostEqual(m.fade(641),1)
    def test_image_has_no_pixels_outside_cta_region(self):
        from PIL import Image
        font='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
        if not Path(font).is_file():self.skipTest('font missing')
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'cta.png';m.draw(p,650,'ai_work',font)
            im=Image.open(p)
            self.assertEqual(im.size,(1080,100))
            self.assertEqual(im.getpixel((0,0))[3],0)
            self.assertGreater(im.getpixel((75,50))[3],0)
    def test_no_new_publication_approval(self):
        self.assertNotIn('auto_post',m.GENRE_CTA)

if __name__=='__main__':unittest.main()
