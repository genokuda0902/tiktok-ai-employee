import unittest
from progress_rail import progress_filter

class ProgressRailTest(unittest.TestCase):
    def test_filter_uses_elapsed_time(self):
        self.assertIn("iw*t/23.033333", progress_filter(23.033333))
    def test_filter_is_top_only(self):
        self.assertIn("y=0", progress_filter(23.033333))
        self.assertIn("h=12", progress_filter(23.033333))
    def test_rejects_invalid_duration(self):
        with self.assertRaises(ValueError):
            progress_filter(0)

if __name__ == "__main__":
    unittest.main()
