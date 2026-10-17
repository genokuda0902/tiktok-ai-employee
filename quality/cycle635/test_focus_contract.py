import json
import pathlib
import unittest

regions = json.loads(pathlib.Path(__file__).with_name("focus_regions.json").read_text())

class FocusTest(unittest.TestCase):
    def test_safe_zone(self):
        for kind in ("select", "formula", "proof"):
            x1, y1, x2, y2 = regions[kind]
            self.assertTrue(30 <= x1 < x2 <= 510)
            self.assertTrue(205 <= y1 < y2 < regions["safe_bottom_y"])
    def test_caption_safe(self):
        self.assertLess(regions["safe_caption_y"][1], 205)
    def test_not_approved(self):
        self.assertEqual(regions["publication"], "NOT_APPROVED")

if __name__ == "__main__":
    unittest.main()
