import unittest
from quality.cycle482.scene_timing import validate_timeline

class SceneTimingTests(unittest.TestCase):
    def test_valid(self):
        self.assertTrue(validate_timeline([(0, 1.5), (1.5, 3)], 3))
    def test_missing_start(self):
        with self.assertRaises(ValueError):
            validate_timeline([(0.5, 3)], 3)
    def test_gap(self):
        with self.assertRaises(ValueError):
            validate_timeline([(0, 1), (1.5, 3)], 3)
    def test_missing_end(self):
        with self.assertRaises(ValueError):
            validate_timeline([(0, 1)], 3)
    def test_reverse(self):
        with self.assertRaises(ValueError):
            validate_timeline([(0, 0)], 0)

if __name__ == '__main__':
    unittest.main()
