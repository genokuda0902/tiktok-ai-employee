import unittest
from tools.cycle1206_step_overlay import build_filter

class OverlayTests(unittest.TestCase):
    def test_window(self):
        self.assertIn(r"between(t\,15\,20)", build_filter())
    def test_invalid(self):
        with self.assertRaises(ValueError):
            build_filter(20, 15)
    def test_steps(self):
        self.assertEqual(build_filter().count("drawtext="), 4)

if __name__ == "__main__":
    unittest.main()
