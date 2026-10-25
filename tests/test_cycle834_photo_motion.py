import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from cycle834_photo_motion import GENRE_MOTION, PHOTO_RECT, VIDEO_SIZE, motion_filter

class TestCycle834(unittest.TestCase):
    def test_ten_genres(self):
        self.assertEqual(len(GENRE_MOTION), 10)
    def test_all_motion_is_subtle(self):
        for zoom, travel in GENRE_MOTION.values():
            self.assertGreater(zoom, 0)
            self.assertLess(zoom, 0.06)
            self.assertGreater(travel, 0)
            self.assertLess(travel, 0.8)
    def test_geometry(self):
        self.assertEqual(VIDEO_SIZE, (1080, 1920))
        self.assertEqual(PHOTO_RECT, (62, 390, 1018, 1390))
    def test_photo_only_overlay(self):
        f = motion_filter("ai_work")
        self.assertIn("crop=956:1000:62:390", f)
        self.assertIn("alphamerge", f)
        self.assertIn("overlay=62:390", f)
    def test_presets_differ(self):
        self.assertNotEqual(motion_filter("ai_work"), motion_filter("wellness"))
    def test_invalid_genre(self):
        with self.assertRaises(ValueError):
            motion_filter("unknown")
    def test_no_upload_or_publish(self):
        import inspect
        import cycle834_photo_motion as m
        source = inspect.getsource(m.render)
        self.assertNotIn("requests.post", source)
        self.assertNotIn("tiktok.upload", source)

if __name__ == "__main__":
    unittest.main()
