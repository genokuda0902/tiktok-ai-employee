import unittest
from src.quality_story_timeline import Scene, validate_timeline, scene_index_at

class TestStoryTimeline(unittest.TestCase):
    def setUp(self):
        self.scenes = [Scene(0,4,"BEFORE"), Scene(4,8,"ACTION"), Scene(8,12,"AFTER")]
    def test_complete(self):
        self.assertTrue(validate_timeline(self.scenes,12))
    def test_boundaries(self):
        self.assertEqual([scene_index_at(t,self.scenes) for t in (0,3.99,4,7.99,8,11.99)],[0,0,1,1,2,2])
    def test_gap_rejected(self):
        with self.assertRaises(ValueError):
            validate_timeline([Scene(0,4,"A"),Scene(5,12,"B")],12)
    def test_overlap_rejected(self):
        with self.assertRaises(ValueError):
            validate_timeline([Scene(0,5,"A"),Scene(4,12,"B")],12)

if __name__ == "__main__":
    unittest.main()
