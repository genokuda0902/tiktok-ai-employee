import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"tools"/"quality"))
from cycle1015_selective_detail import GENRES,ROI,make_filter

class TestSelectiveDetail(unittest.TestCase):
    def test_ten_genres(self):
        self.assertEqual(len(GENRES),10)
    def test_caption_safe_zone(self):
        self.assertLess(ROI[1]+ROI[3],1400)
    def test_filter(self):
        self.assertIn("unsharp=5:5:0.32",make_filter())
    def test_bad_genre(self):
        with self.assertRaises(ValueError):make_filter("invalid")
    def test_strength_limit(self):
        with self.assertRaises(ValueError):make_filter(strength=1.0)
    def test_audio_not_filtered(self):
        self.assertNotIn("0:a",make_filter())
if __name__=="__main__":
    unittest.main()
