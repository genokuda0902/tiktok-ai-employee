import unittest
from pathlib import Path
from src.cycle1275_review_render import SCENES, W, H, FPS, SECONDS

class ReviewContract(unittest.TestCase):
    def test_vertical_hd(self):
        self.assertEqual((W, H, FPS), (1080, 1920, 30))
    def test_four_scenes(self):
        self.assertEqual(len(SCENES), 4)
        self.assertEqual(len(SCENES) * SECONDS, 12)
    def test_fail_closed(self):
        self.assertFalse(Path("output/cycle1275/APPROVED_FOR_POSTING").exists())

if __name__ == "__main__":
    unittest.main()
