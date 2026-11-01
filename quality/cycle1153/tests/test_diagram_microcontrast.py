import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'code'))
from diagram_microcontrast import GENRE_STRENGTH,validate_roi,filtergraph

class MicrocontrastTest(unittest.TestCase):
    def test_ten_genres(self):
        self.assertEqual(len(GENRE_STRENGTH),10)
        for strength in GENRE_STRENGTH.values():
            self.assertTrue(0.3 <= strength <= 0.6)
    def test_safe_area(self):
        self.assertTrue(validate_roi((64,460,952,840),1080,1920,1350))
    def test_overlap_rejected(self):
        with self.assertRaisesRegex(ValueError,'caption'):
            validate_roi((64,1000,952,400),1080,1920,1350)
    def test_outside_rejected(self):
        with self.assertRaisesRegex(ValueError,'outside'):
            validate_roi((64,460,1050,840),1080,1920,1350)
    def test_negative_rejected(self):
        with self.assertRaises(ValueError):
            validate_roi((-1,10,20,20),1080,1920,1350)
    def test_filter_preserves_unmodified_region(self):
        s=filtergraph((64,460,952,840),.52)
        self.assertIn('split=2[untouched][diagram]',s)
        self.assertIn('crop=952:840:64:460',s)
        self.assertIn('5:5:0[detail]',s)
        self.assertIn('overlay=64:460',s)
    def test_strength_bounds(self):
        with self.assertRaises(ValueError):filtergraph((0,0,20,20),1.5)
    def test_every_genre_filter(self):
        for k,s in GENRE_STRENGTH.items():
            self.assertIn('unsharp=5:5:',filtergraph((0,0,20,20),s),k)

if __name__=='__main__':unittest.main()
