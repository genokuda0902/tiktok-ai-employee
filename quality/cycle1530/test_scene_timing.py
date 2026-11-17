import unittest
from scene_timing import scene_index, publication_allowed

class SceneTimingTests(unittest.TestCase):
    def test_hook_ends_at_1_5_seconds(self):
        self.assertEqual([scene_index(t) for t in (0, 1.49, 1.5, 4.99, 5, 8.5, 11.99)], [0,0,1,1,2,3,3])
    def test_invalid_time(self):
        for t in (-1,12):
            with self.assertRaises(ValueError): scene_index(t)
    def test_publication_fails_closed(self):
        self.assertFalse(publication_allowed())
        self.assertFalse(publication_allowed(True,True,True,False))
        self.assertTrue(publication_allowed(True,True,True,True))

if __name__ == "__main__": unittest.main()
