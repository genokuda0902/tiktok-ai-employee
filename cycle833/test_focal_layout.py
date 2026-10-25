"""No-network tests for cycle833 reusable visual layout core."""
import unittest
from focal_layout import (
    GENRES, FRAMES, FOCUS_Y, PHOTO_RECT, CAPTION_RECT,
    focal_crop, progress_segments, validate_layout
)

class Cycle833LayoutTests(unittest.TestCase):
    def test_ten_genres_have_eight_unique_headlines(self):
        self.assertEqual(len(GENRES), 10)
        for palette, scenes in GENRES.values():
            self.assertEqual(len(scenes), 8)
            self.assertEqual(len(set(scenes)), 8)
            self.assertTrue(palette.startswith("#"))

    def test_timeline(self):
        self.assertEqual(sum(FRAMES), 775)
        self.assertAlmostEqual(sum(FRAMES)/30, 25.833333, places=5)

    def test_focal_crop_subject_changes(self):
        a=focal_crop(240,405,956,1000,.10)
        b=focal_crop(240,405,956,1000,.90)
        self.assertEqual((a.width,a.height), (956,1000))
        self.assertLess(a.top,b.top)

    def test_crop_bounds(self):
        for focus in FOCUS_Y:
            c=focal_crop(240,405,956,1000,focus)
            self.assertGreaterEqual(c.left,0)
            self.assertGreaterEqual(c.top,0)
            self.assertLessEqual(c.left+c.width,c.resized_width)
            self.assertLessEqual(c.top+c.height,c.resized_height)

    def test_progress(self):
        self.assertEqual(sum(progress_segments(0)),1)
        self.assertEqual(sum(progress_segments(7)),8)

    def test_safe_zone(self):
        self.assertLess(PHOTO_RECT[3],CAPTION_RECT[1])
        self.assertLessEqual(CAPTION_RECT[3],1800)
        validate_layout()

    def test_invalid(self):
        with self.assertRaises(ValueError): focal_crop(0,405,956,1000,.5)
        with self.assertRaises(ValueError): focal_crop(240,405,956,1000,2)
        with self.assertRaises(ValueError): progress_segments(8)

if __name__=="__main__":
    unittest.main()
