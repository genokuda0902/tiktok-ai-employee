import unittest
from progress import progress_filter

class TestProgress(unittest.TestCase):
    def test_segments(self):
        result = progress_filter(24, 24)
        self.assertEqual(result.count("drawbox="), 24)
        self.assertIn("gte(t,23.0000)", result)

    def test_invalid(self):
        for duration, count in [(0, 24), (24, 0), (24, 101)]:
            with self.assertRaises(ValueError):
                progress_filter(duration, count)

if __name__ == "__main__":
    unittest.main()
