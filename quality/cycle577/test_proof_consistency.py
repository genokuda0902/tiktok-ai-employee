import unittest, tempfile
from pathlib import Path
from PIL import Image
from proof_consistency import DATA, GENRES, validate_proof, make_overlay

class ProofConsistencyTests(unittest.TestCase):
    def test_all_ten_genres_use_one_contract(self):
        for genre in GENRES:
            self.assertTrue(validate_proof(DATA,'B2:B5',720,genre))
    def test_wrong_range_rejected(self):
        with self.assertRaises(ValueError):validate_proof(DATA,'A1:A4',720,'ai_productivity')
    def test_wrong_sum_rejected(self):
        with self.assertRaises(ValueError):validate_proof(DATA,'B2:B5',700,'ai_productivity')
    def test_wrong_count_rejected(self):
        with self.assertRaises(ValueError):validate_proof((120,150,200),'B2:B5',470,'ai_productivity')
    def test_unrecognized_genre_rejected(self):
        with self.assertRaises(ValueError):validate_proof(DATA,'B2:B5',720,'other')
    def test_overlay_transparency_and_dimensions(self):
        with tempfile.TemporaryDirectory() as t:
            p=Path(t)/'o.png';make_overlay(p)
            im=Image.open(p)
            self.assertEqual(im.size,(1080,1920))
            self.assertEqual(im.getpixel((20,20))[3],0)
            self.assertEqual(im.getpixel((700,1300))[3],255)
if __name__=='__main__':unittest.main()
