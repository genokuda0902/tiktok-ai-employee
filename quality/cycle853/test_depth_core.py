import unittest
from depth_core import GENRE_ACCENTS, MAX_SCALE, fit_scale, scene_frames, scene_filter, check_segments

class CoreTest(unittest.TestCase):
    def test_genres(self): self.assertEqual(len(GENRE_ACCENTS), 10)
    def test_scale_limit(self): self.assertEqual(fit_scale(200, 200), MAX_SCALE)
    def test_scale_no_crop(self): self.assertAlmostEqual(fit_scale(1200, 600), 2/3)
    def test_invalid_dimension(self):
        with self.assertRaises(ValueError): fit_scale(0, 100)
    def test_frames(self):
        self.assertEqual(sum(scene_frames(i) for i in range(8)) - 7*9, 691)
    def test_parallax_rates_differ(self):
        f = scene_filter(0)
        self.assertIn('16*sin(n/17', f)
        self.assertIn('23*sin(n/19', f)
        self.assertIn('overlay=0:0', f)
    def test_truncated_segment_rejected(self):
        with self.assertRaises(ValueError): check_segments([94]*8)
    def test_segments_valid(self):
        self.assertTrue(check_segments([94]*7 + [96]))

if __name__ == '__main__': unittest.main()
