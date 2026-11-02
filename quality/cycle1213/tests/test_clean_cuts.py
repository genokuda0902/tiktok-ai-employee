import sys,unittest
from pathlib import Path
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'code'))
from clean_cuts import validate,replacement_map,apply_clean_cut,GENRES,DEFAULT_BOUNDARIES

class CleanCutTests(unittest.TestCase):
    def test_ten_genres(self):
        self.assertEqual(len(GENRES),10)
        for g in GENRES:self.assertTrue(validate([20,40],60,3,5,g))
    def test_invalid_genre(self):
        with self.assertRaises(ValueError):validate([20],60,3,5,'unknown')
    def test_unsorted(self):
        with self.assertRaises(ValueError):validate([40,20],60,3,5)
    def test_duplicate(self):
        with self.assertRaises(ValueError):validate([20,20],60,3,5)
    def test_outside(self):
        with self.assertRaises(ValueError):validate([4],60,3,5)
    def test_too_close(self):
        with self.assertRaises(ValueError):validate([20,28],60,3,5)
    def test_invalid_radius(self):
        with self.assertRaises(ValueError):validate([20],60,5,5)
    def test_replacement_count(self):
        self.assertEqual(len(replacement_map(DEFAULT_BOUNDARIES,675)),88)
    def test_no_blended_titles(self):
        m=replacement_map([20],60,3,5)
        self.assertEqual([m[i] for i in range(17,20)],[15]*3)
        self.assertEqual([m[i] for i in range(20,24)],[25]*4)
    def test_untouched_frames(self):
        m=replacement_map([20],60,3,5)
        self.assertNotIn(16,m);self.assertNotIn(24,m)
    def test_subtitle_preservation(self):
        a=np.full((12,5,3),12,dtype=np.uint8)
        b=np.full((12,5,3),240,dtype=np.uint8)
        o=apply_clean_cut(a,b,7)
        self.assertTrue(np.all(o[:7]==240))
        self.assertTrue(np.all(o[7:]==12))
    def test_reference(self):
        m=replacement_map([20,40],60,3,5)
        self.assertEqual(m[19],15);self.assertEqual(m[40],45)

if __name__=='__main__':unittest.main()
