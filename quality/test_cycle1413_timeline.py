import unittest
from cycle1413_timeline import scene_at, step_label

class TimelineTest(unittest.TestCase):
    def test_boundaries(self):
        self.assertEqual([scene_at(t,[3]*5) for t in [0,3,6,9,12,15]], [0,1,2,3,4,4])
    def test_indicator(self):
        self.assertEqual(step_label(9,[3]*5),"STEP 04 / 05")
    def test_invalid(self):
        for durations in [[],[3,0],[-1,3]]:
            with self.assertRaises(ValueError): scene_at(0,durations)
if __name__ == "__main__": unittest.main()
