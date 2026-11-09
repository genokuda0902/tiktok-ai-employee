import unittest
from tools.review_motion import filtergraph

class MotionTest(unittest.TestCase):
    def test_vertical(self):
        self.assertIn("s=1080x1920:fps=30", filtergraph())
    def test_bounded_zoom(self):
        self.assertIn("1.045", filtergraph())
    def test_invalid(self):
        for v in (0.9, 1.2):
            with self.assertRaises(ValueError):
                filtergraph(max_zoom=v)

if __name__ == "__main__":
    unittest.main()
