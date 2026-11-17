import unittest
from scene_plan import SCENES,scene_at,publication_approved
class Tests(unittest.TestCase):
    def test_scene_boundaries(self):
        self.assertEqual([scene_at(t) for t in (0,2.5,5,7.5,9.9)], [0,1,2,3,3])
    def test_invalid_timestamp(self):
        with self.assertRaises(ValueError):scene_at(10)
    def test_fail_closed(self):
        self.assertFalse(publication_approved(True,True,True,False))
        self.assertTrue(publication_approved(True,True,True,True))
if __name__ == "__main__": unittest.main()
