import unittest
import numpy as np
from render import GENRE_THEMES,DEFAULT_SCENE_FRAMES,transition_weight,matte_transition
class TransitionTests(unittest.TestCase):
    def test_ten_genres(self):self.assertEqual(len(GENRE_THEMES),10)
    def test_seven_cuts(self):self.assertEqual(len(DEFAULT_SCENE_FRAMES)-1,7)
    def test_429_frames(self):self.assertEqual(sum(DEFAULT_SCENE_FRAMES),429)
    def test_weight_symmetry(self):
        self.assertAlmostEqual(transition_weight(54,57),transition_weight(59,57))
    def test_cut_is_masked(self):
        self.assertGreater(transition_weight(56,57),.95)
        self.assertGreater(transition_weight(57,57),.95)
    def test_zero_weight_is_identity(self):
        a=np.full((192,108,3),150,np.uint8)
        self.assertTrue(np.array_equal(a,matte_transition(a,0)))
    def test_text_regions_untouched(self):
        a=np.full((192,108,3),150,np.uint8)
        b=matte_transition(a,1)
        self.assertTrue(np.array_equal(a[:55],b[:55]))
        self.assertTrue(np.array_equal(a[120:],b[120:]))
    def test_card_edge_untouched(self):
        a=np.full((192,108,3),150,np.uint8)
        b=matte_transition(a,1)
        self.assertTrue(np.array_equal(a[:,9],b[:,9]))
        self.assertFalse(np.array_equal(a[70:110,30:80],b[70:110,30:80]))
if __name__=="__main__":unittest.main()
