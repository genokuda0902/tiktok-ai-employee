import unittest
from pathlib import Path
import tempfile
from cinematic_glow import POLICY,GENRES,create_glow,validate_manifest

class GlowTest(unittest.TestCase):
    def test_ten_genres(self):
        self.assertEqual(len(GENRES),10)
        self.assertEqual(len(set(GENRES)),10)
    def test_fail_closed_policy(self):
        with self.assertRaises(ValueError):validate_manifest({'policy':'PUBLIC'},'/tmp/not-real.mp4')
    def test_asset_alpha(self):
        from PIL import Image
        with tempfile.TemporaryDirectory() as t:
            p=Path(t)/'g.png';create_glow(p,40,60)
            im=Image.open(p)
            self.assertEqual(im.mode,'RGBA')
            self.assertGreater(im.getpixel((20,30))[3],im.getpixel((0,0))[3])
            self.assertLessEqual(im.getpixel((20,30))[3],58)
    def test_policy_review_only(self):
        self.assertIn('NOT_APPROVED',POLICY)

if __name__=='__main__':unittest.main()
