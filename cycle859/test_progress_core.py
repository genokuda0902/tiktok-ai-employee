import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent))
from progress_core import *

class TestProgress(unittest.TestCase):
    def test_ten_genres(self):self.assertEqual(len(PALETTES),10)
    def test_start_empty(self):self.assertEqual(progress_pixels(0),0)
    def test_last_full(self):self.assertEqual(progress_pixels(690),960)
    def test_midpoint(self):self.assertEqual(progress_pixels(345),480)
    def test_monotonic(self):
        v=[progress_pixels(i) for i in range(691)]
        self.assertTrue(all(a<=b for a,b in zip(v,v[1:])))
    def test_no_overflow(self):self.assertTrue(all(0<=progress_pixels(i)<=960 for i in range(691)))
    def test_safe_region(self):self.assertTrue(validate_placement())
    def test_invalid_frame(self):
        with self.assertRaises(ValueError):progress_pixels(691)
    def test_negative_frame(self):
        with self.assertRaises(ValueError):progress_pixels(-1)
    def test_invalid_geometry(self):
        with self.assertRaises(ValueError):progress_pixels(0,1)
    def test_invalid_genre(self):
        with self.assertRaises(ValueError):color_for_genre('unknown')
    def test_genre_colors_unique(self):self.assertEqual(len(set(PALETTES.values())),10)
if __name__=='__main__':unittest.main()
