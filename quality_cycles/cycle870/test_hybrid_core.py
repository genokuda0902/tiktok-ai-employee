import unittest
from hybrid_core import *

class HybridCoreTest(unittest.TestCase):
    def test_ten_genres(self):
        self.assertEqual(len(GENRES),10)
        for g in GENRES:self.assertTrue(validate(genre=g))
    def test_native_vertical(self):self.assertEqual((W,H,FPS),(1080,1920,30))
    def test_overlay_is_caption_safe(self):self.assertLess(Placement().y+Placement().h,CAPTION_Y0)
    def test_crop_within_video(self):self.assertTrue(validate())
    def test_reject_crop_overflow(self):
        with self.assertRaises(ValueError):validate(crop=Crop(x=800))
    def test_reject_caption_overlap(self):
        with self.assertRaises(ValueError):validate(place=Placement(y=600))
    def test_reject_distorted_aspect(self):
        with self.assertRaises(ValueError):validate(place=Placement(w=650))
    def test_reject_segment_overrun(self):
        with self.assertRaises(ValueError):validate(segment=Segment(8,24))
    def test_reject_unknown_genre(self):
        with self.assertRaises(ValueError):validate(genre='unknown')
    def test_filter_contains_overlay_and_crop(self):
        f=overlay_filter()
        self.assertIn('crop=800:760:80:320',f)
        self.assertIn('crop=800:760:80:540',f)
        self.assertIn('overlay=90:510',f)
    def test_previous_change_not_repeated(self):
        self.assertIn('split=3',overlay_filter())
        self.assertAlmostEqual(Segment().end-Segment().start,8.8)

if __name__=='__main__':unittest.main()
