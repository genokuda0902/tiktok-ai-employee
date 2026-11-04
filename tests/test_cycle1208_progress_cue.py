import unittest
from tools.cycle1208_progress_cue import progress_filter

class ProgressCueTests(unittest.TestCase):
    def test_positive_duration(self):
        self.assertIn("min(t/23.033", progress_filter(23.033))
    def test_reject_zero(self):
        with self.assertRaises(ValueError):
            progress_filter(0)
    def test_top_edge(self):
        self.assertIn("y=0", progress_filter(10))
if __name__ == "__main__":
    unittest.main()
