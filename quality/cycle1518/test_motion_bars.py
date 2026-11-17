import unittest
from motion_bars import progress_at, bar_width

class TestMotionBars(unittest.TestCase):
    def test_before_start(self):
        self.assertEqual(progress_at(0, 0), 0)
    def test_after_end(self):
        self.assertEqual(progress_at(9, 4), 1)
    def test_stagger(self):
        self.assertGreater(progress_at(1.2, 0), progress_at(1.2, 1))
    def test_width(self):
        self.assertEqual(bar_width(50, 1), 235)
    def test_invalid(self):
        with self.assertRaises(ValueError): bar_width(101, 1)

if __name__ == "__main__": unittest.main()
