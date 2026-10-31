import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import numpy as np
from scene_safe_dip import CAPTIONS,PALETTES,DIP_FACTORS,caption_plate,dip_roi

class TestSceneSafeDip(unittest.TestCase):
    def test_eight_scenes(self):self.assertEqual(len(CAPTIONS),8)
    def test_ten_genres(self):self.assertEqual(len(PALETTES),10)
    def test_all_caption_plates(self):
        for genre in PALETTES:
            for i in range(8):
                with self.subTest(genre=genre,i=i):
                    p=caption_plate(i,genre)
                    self.assertEqual(p.size,(1080,246))
    def test_no_debug_english(self):
        import inspect,scene_safe_dip
        self.assertNotIn('JAPANESE CAPTION',inspect.getsource(scene_safe_dip.caption_plate))
    def test_dip_symmetric(self):
        x=np.full((2,2,3),200,dtype=np.uint8)
        self.assertEqual([int(dip_roi(x,i)[0,0,0]) for i in [-2,-1,0,1]],[144,60,60,144])
    def test_no_crossfade_ghost(self):
        self.assertEqual(int(dip_roi(np.zeros((2,2,3),dtype=np.uint8),0).sum()),0)
    def test_dip_invalid(self):
        with self.assertRaises(ValueError):dip_roi(np.zeros((2,2,3),dtype=np.uint8),2)
    def test_caption_invalid(self):
        with self.assertRaises(ValueError):caption_plate(8)
    def test_genre_invalid(self):
        with self.assertRaises(ValueError):caption_plate(0,'not-a-genre')

if __name__=='__main__':unittest.main()
