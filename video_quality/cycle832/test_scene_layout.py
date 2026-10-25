"""Cycle832 portable geometry tests. Run: python -m unittest discover -s video_quality/cycle832 -p 'test_*.py'"""
import unittest
from scene_layout import (
    WIDTH, HEIGHT, GENRE_ACCENTS, FRAME_COUNTS, PHOTO_BOX,
    SUBTITLE_BOX, source_crop, validate_layout,
)

class SceneLayoutTests(unittest.TestCase):
    def test_ten_genres(self):
        self.assertEqual(len(GENRE_ACCENTS), 10)
        self.assertTrue(all(v.startswith("#") and len(v) == 7 for v in GENRE_ACCENTS.values()))

    def test_vertical_format(self):
        self.assertEqual((WIDTH, HEIGHT), (1080, 1920))
        self.assertEqual(sum(FRAME_COUNTS), 775)

    def test_all_crops_inside_source(self):
        self.assertTrue(validate_layout())
        self.assertEqual(len({source_crop(i) for i in range(8)}), 8)

    def test_subtitle_region(self):
        self.assertGreater(SUBTITLE_BOX[1], PHOTO_BOX[1])
        self.assertLessEqual(SUBTITLE_BOX[3], HEIGHT)

    def test_invalid_scene(self):
        with self.assertRaises(ValueError):
            source_crop(8)

if __name__ == "__main__":
    unittest.main()
