import unittest
import numpy as np
from loop_seam import GENRES, LoopSpec, blend_frame, seam_difference

class TestLoop(unittest.TestCase):
    def test_genres(self):
        for genre in GENRES:
            LoopSpec(genre=genre).validate()
    def test_endpoints(self):
        a=np.zeros((4,4,3),dtype=np.uint8)
        b=np.full((4,4,3),255,dtype=np.uint8)
        self.assertTrue(np.array_equal(blend_frame(a,b,0,27),a))
        self.assertTrue(np.array_equal(blend_frame(a,b,26,27),b))
    def test_seam_metric(self):
        a=np.zeros((4,4,3),dtype=np.uint8)
        self.assertEqual(seam_difference(a,a),0)
    def test_approval_guard(self):
        with self.assertRaises(ValueError):
            LoopSpec(publication_status='APPROVED').validate()

if __name__=='__main__': unittest.main()
