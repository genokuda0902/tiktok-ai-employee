import unittest
from scene_ticks import marker_filter
class TestSceneTicks(unittest.TestCase):
    def test_position(self):
        self.assertIn("x=540",marker_filter([5],10))
    def test_outside(self):
        with self.assertRaises(ValueError): marker_filter([11],10)
    def test_duplicates(self):
        with self.assertRaises(ValueError): marker_filter([3,3],10)
if __name__=="__main__": unittest.main()
