import unittest
from src.review_focus_card import focus_filter

class FocusCardTests(unittest.TestCase):
    def test_valid_timing(self):
        self.assertIn("between(t,12,16)", focus_filter())
    def test_rejects_zero_duration(self):
        with self.assertRaises(ValueError):
            focus_filter(5,5)
    def test_rejects_negative_start(self):
        with self.assertRaises(ValueError):
            focus_filter(-1,2)

if __name__ == "__main__":
    unittest.main()
