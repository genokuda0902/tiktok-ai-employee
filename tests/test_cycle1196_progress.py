import unittest
from tools.cycle1196_progress import progress_filter

class ProgressTests(unittest.TestCase):
    def test_filter_uses_time(self):
        self.assertIn("t/23.033000", progress_filter(23.033))
    def test_invalid_duration(self):
        with self.assertRaises(ValueError): progress_filter(0)
    def test_invalid_dimensions(self):
        with self.assertRaises(ValueError): progress_filter(10, width=100)
    def test_vertical_safe_area(self):
        self.assertIn("y=1830", progress_filter(23.033))

if __name__ == "__main__": unittest.main()
