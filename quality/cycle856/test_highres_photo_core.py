import unittest
from highres_photo_core import *

class QualityGate(unittest.TestCase):
    def test_ten_genres(self): self.assertTrue(validate_genres())
    def test_safe_geometry(self): self.assertTrue(check_geometry())
    def test_native_1024x1536(self):
        r=cover_geometry((1024,1536));self.assertLessEqual(r['scale'],1);self.assertEqual(r['crop_px'],(630,630))
    def test_native_941x1672(self): self.assertLessEqual(cover_geometry((941,1672))['scale'],1)
    def test_native_822x859(self): self.assertLessEqual(cover_geometry((822,859))['scale'],1)
    def test_native_680x650(self): self.assertLessEqual(cover_geometry((680,650))['scale'],1)
    def test_reject_low_resolution(self):
        with self.assertRaises(ValueError): cover_geometry((500,500))
    def test_reject_empty(self):
        with self.assertRaises(ValueError): cover_geometry((0,1500))
    def test_portrait_crop(self):
        r=cover_geometry((1024,1536));self.assertGreater(r['display_px'][1],630)
    def test_unique_genres(self): self.assertEqual(len(GENRES),len(set(GENRES)))

if __name__=='__main__': unittest.main()
