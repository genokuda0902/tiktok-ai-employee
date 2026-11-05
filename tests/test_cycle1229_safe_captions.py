import unittest
from src.cycle1229_safe_captions import CAPTIONS, filtergraph

class TestSafeCaptions(unittest.TestCase):
    def test_three_cues(self): self.assertEqual(len(CAPTIONS), 3)
    def test_nonoverlap(self): self.assertTrue(all(a[1] < b[0] for a, b in zip(CAPTIONS, CAPTIONS[1:])))
    def test_safe_vertical_zone(self): self.assertIn("y=1450", filtergraph())
    def test_time_windows(self): self.assertEqual(filtergraph().count("drawtext="), 3)

if __name__ == "__main__": unittest.main()
