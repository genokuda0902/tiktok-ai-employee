import unittest
import numpy as np
from ghost_free_guard import GENRES,apply_single_source,matte_for,make_shifts

class TestGuard(unittest.TestCase):
    def test_ten_genres(self):self.assertEqual(len(GENRES),10)
    def test_single_source_no_ghost(self):
        a=np.full((100,100,3),80,np.uint8)
        roi=(10,10,80,80)
        out=apply_single_source(a,30,roi,matte_for(roi,8))
        self.assertEqual(int(out[50,50,0]),110)
        self.assertEqual(int(out[0,0,0]),80)
        self.assertEqual(int(out[10,10,0]),80)
        self.assertEqual(int(out[50,50,0]),int(out[50,50,2]))
    def test_source_unmodified(self):
        a=np.full((100,100,3),80,np.uint8);b=a.copy()
        apply_single_source(a,-20,(10,10,80,80),matte_for((10,10,80,80),8))
        self.assertTrue(np.array_equal(a,b))
    def test_reject_large_shift(self):
        with self.assertRaises(ValueError):apply_single_source(np.zeros((100,100,3),np.uint8),91,(10,10,80,80))
    def test_reject_invalid_feather(self):
        with self.assertRaises(ValueError):matte_for((10,10,80,80),41)
    def test_reject_duplicate_cuts(self):
        with self.assertRaises(ValueError):make_shifts('none.mp4',[20,20])
    def test_reject_unsupported_genre(self):self.assertNotIn('unapproved',GENRES)

if __name__=='__main__':unittest.main()
