import unittest
from render import SCENES, scene_at

class TestSceneTiming(unittest.TestCase):
    def test_count(self):
        self.assertEqual(len(SCENES), 5)
    def test_boundaries(self):
        self.assertEqual([scene_at(x) for x in (0, 2.99, 3, 6, 12, 14.99)], [0,0,1,2,4,4])
    def test_captions(self):
        self.assertTrue(all(title and caption for title, caption, _ in SCENES))
if __name__ == "__main__":
    unittest.main()
