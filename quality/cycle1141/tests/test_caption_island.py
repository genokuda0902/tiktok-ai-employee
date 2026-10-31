import sys
import tempfile
import unittest
from pathlib import Path
from PIL import Image
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'code'))
from caption_island import (GENRES,alpha_at,make_mask,CROP_TOP,
                            LOCK_TOP,WIDTH,HEIGHT)

class CaptionIslandTests(unittest.TestCase):
    def test_ten_genres(self):
        self.assertEqual(len(GENRES),10)
        self.assertEqual(len(set(GENRES)),10)
    def test_alpha_start(self):
        self.assertEqual(alpha_at(CROP_TOP),0)
    def test_alpha_end(self):
        self.assertEqual(alpha_at(LOCK_TOP),255)
    def test_alpha_monotonic(self):
        values=[alpha_at(y) for y in range(CROP_TOP,LOCK_TOP+1)]
        self.assertEqual(values,sorted(values))
    def test_mask_size(self):
        with tempfile.TemporaryDirectory() as tmp:
            im=Image.open(make_mask(Path(tmp)/'mask.png'))
            self.assertEqual(im.size,(WIDTH,HEIGHT-CROP_TOP))
            self.assertEqual(im.mode,'L')
    def test_mask_horizontal_consistency(self):
        with tempfile.TemporaryDirectory() as tmp:
            im=Image.open(make_mask(Path(tmp)/'mask.png'))
            for y in (0,40,80,129,130,200,699):
                self.assertEqual(im.getpixel((0,y)),im.getpixel((WIDTH-1,y)))
    def test_invalid_mask(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(ValueError):
                make_mask(Path(tmp)/'bad.png',1500,1400)
    def test_safe_band(self):
        self.assertTrue(1320<=LOCK_TOP<=1400)
        self.assertGreaterEqual(HEIGHT-LOCK_TOP,500)

if __name__=='__main__':
    unittest.main()
