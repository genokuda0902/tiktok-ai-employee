import unittest
from tools.cycle1193_transition import fade_filter, render

class TestTransition(unittest.TestCase):
    def test_three_cuts(self):
        self.assertEqual(fade_filter().count("fade=t=out"), 3)
    def test_bad_order(self):
        with self.assertRaises(ValueError):
            fade_filter((6, 3))
    def test_bad_duration(self):
        with self.assertRaises(ValueError):
            fade_filter((0.1,), 0.12)
    def test_review_gate(self):
        with self.assertRaises(ValueError):
            render("in.mp4", "out.mp4")

if __name__ == "__main__":
    unittest.main()
