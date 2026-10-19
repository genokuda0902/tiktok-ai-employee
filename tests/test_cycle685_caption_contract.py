"""Standard-library CI tests for the cycle685 caption contract."""
import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
FILE = ROOT / "quality" / "cycle685" / "caption_contract.py"
spec = importlib.util.spec_from_file_location("caption_contract", FILE)
contract = importlib.util.module_from_spec(spec)
spec.loader.exec_module(contract)

class TestCaptionContract(unittest.TestCase):
    def test_ten_genres(self):
        self.assertEqual(len(contract.PALETTES), 10)
        for genre in contract.PALETTES:
            self.assertIn("NOT_APPROVED", contract.validate(genre, list(range(1, 9))))
    def test_caption_zone(self):
        self.assertGreaterEqual(contract.CAPTION_TOP, 1300)
        self.assertLessEqual(contract.CAPTION_BOTTOM, 1700)
        self.assertEqual((contract.WIDTH, contract.HEIGHT, contract.FPS), (1080, 1920, 30))
    def test_seven_caption_scenes(self):
        self.assertEqual(sorted(contract.CAPTIONS), list(range(1, 8)))
        for a,b in contract.CAPTIONS.values():
            self.assertTrue(a)
            self.assertLess(len(a+b), 30)
    def test_review_gate(self):
        with self.assertRaises(ValueError):
            contract.validate("science", list(range(1, 9)), approved=True)
        with self.assertRaises(ValueError):
            contract.validate("science", list(range(1, 9)), auto_post=True)
    def test_invalid_genre_and_scene_order(self):
        with self.assertRaises(ValueError):
            contract.validate("invalid", list(range(1, 9)))
        with self.assertRaises(ValueError):
            contract.validate("science", [2, 1, 3, 4, 5, 6, 7, 8])

if __name__ == "__main__":
    unittest.main()
