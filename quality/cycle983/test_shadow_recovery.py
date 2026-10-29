import sys,unittest
from pathlib import Path
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parent))
from shadow_recovery import GENRES,validate_geometry,shadow_lut,enhance_frame

class ShadowTests(unittest.TestCase):
    def setUp(self): self.lut=shadow_lut()
    def test_ten_genres(self): self.assertEqual(len(GENRES),10)
    def test_fail_closed_unreviewed(self):
        for g in GENRES[1:]:
            with self.assertRaises(ValueError):validate_geometry(1080,1920,30,100,150,1180,g)
    def test_synthetic_other_genre(self):
        validate_geometry(360,640,30,30,40,400,'science',True)
    def test_invalid_geometry(self):
        with self.assertRaises(ValueError):validate_geometry(360,640,30,30,40,630,'ai_work')
    def test_lut_black_white_protected(self):
        self.assertEqual(int(self.lut[0]),0)
        self.assertEqual(int(self.lut[7]),7)
        self.assertEqual(int(self.lut[160]),160)
        self.assertEqual(int(self.lut[255]),255)
    def test_lut_midtones_lifted(self):
        self.assertGreater(int(self.lut[70]),70)
        self.assertGreater(int(self.lut[110]),110)
    def test_lut_monotonic(self):
        self.assertTrue(np.all(np.diff(self.lut.astype(np.int16))>=0))
    def test_protected_caption_exact(self):
        a=np.full((240,128,3),[15,25,45],dtype=np.uint8)
        b=enhance_frame(a,20,150,self.lut,10)
        self.assertTrue(np.array_equal(a[150:],b[150:]))
        self.assertTrue(np.array_equal(a[:20],b[:20]))
    def test_highlights_unchanged(self):
        a=np.full((240,128,3),230,dtype=np.uint8)
        b=enhance_frame(a,20,150,self.lut,10)
        self.assertTrue(np.array_equal(a,b))
    def test_dark_color_lift(self):
        a=np.full((240,128,3),[15,35,50],dtype=np.uint8)
        b=enhance_frame(a,20,150,self.lut,0)
        self.assertGreater(float(b[40:130].mean()),float(a[40:130].mean()))
    def test_invalid_strength(self):
        with self.assertRaises(ValueError):shadow_lut(35)
    def test_no_caption_bleed(self):
        a=np.random.default_rng(4).integers(0,256,(240,128,3),dtype=np.uint8)
        b=enhance_frame(a,20,150,self.lut,10)
        self.assertTrue(np.array_equal(a[150:],b[150:]))

if __name__=='__main__':unittest.main()
