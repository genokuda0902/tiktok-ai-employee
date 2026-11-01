import sys
from pathlib import Path
import unittest
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from soft_scene_cut import GENRES,DEFAULT_CUTS,ease,blend,validate

class SoftCutTests(unittest.TestCase):
    def test_ten_genres(self):self.assertEqual(len(GENRES),10)
    def test_seven_cuts(self):self.assertEqual(len(DEFAULT_CUTS),7)
    def test_valid_config(self):validate(DEFAULT_CUTS,675)
    def test_invalid_config(self):
        with self.assertRaises(ValueError):validate([20,22],675)
    def test_ease(self):
        self.assertEqual(ease(0),0);self.assertEqual(ease(1),1)
        self.assertEqual([ease(i/20) for i in range(21)],sorted(ease(i/20) for i in range(21)))
    def test_caption_exact(self):
        a=np.zeros((20,10,3),np.uint8);b=np.full_like(a,200)
        for phase in range(6):
            out=blend(a,b,phase,6,12)
            self.assertTrue(np.array_equal(out[12:],b[12:]))
    def test_smooth_first_frame(self):
        a=np.zeros((20,10,3),np.uint8);b=np.full_like(a,200)
        self.assertLess(blend(a,b,0,6,12)[:12].mean(),40)
    def test_last_frame_equals_new(self):
        a=np.zeros((20,10,3),np.uint8);b=np.full_like(a,200)
        self.assertTrue(np.array_equal(blend(a,b,5,6,12),b))
if __name__=='__main__':unittest.main()
