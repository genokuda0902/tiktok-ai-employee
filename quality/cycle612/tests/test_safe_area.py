"""Cycle612 smoke tests. Run: python -m unittest discover -s quality/cycle612/tests"""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from safe_area import SafeArea, TEN_GENRES, PUBLICATION_STATUS, QUALITY_STATUS

class TestCycle612(unittest.TestCase):
    def test_safe_area(self):
        area = SafeArea()
        self.assertTrue(area.valid())
        self.assertLessEqual(area.x + area.width, 850)
        self.assertLess(area.y + area.height, 1320)

    def test_ten_genres(self):
        self.assertEqual(len(TEN_GENRES), 10)
        self.assertTrue(all(v.startswith("#") and len(v) == 7 for v in TEN_GENRES.values()))

    def test_human_approval_required(self):
        self.assertEqual(PUBLICATION_STATUS, "NOT_APPROVED")
        self.assertEqual(QUALITY_STATUS, "HUMAN_REVIEW")

if __name__ == "__main__":
    unittest.main()
