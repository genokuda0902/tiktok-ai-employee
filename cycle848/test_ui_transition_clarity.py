import unittest
import numpy as np
from ui_transition_clarity import GENRES,POLICY,BOUNDARIES,repair_region

class TransitionTests(unittest.TestCase):
    def setUp(self):
        self.b=tuple(BOUNDARIES)
        self.a=np.zeros((1920,1080,3),dtype=np.uint8)
        self.a[:1540]=40
        self.a[1540:]=170
        self.clean={b-12:np.full_like(self.a,100) for b in self.b}
        self.clean.update({b+12:np.full_like(self.a,200) for b in self.b})
    def test_ten_genres(self):self.assertEqual(len(GENRES),10)
    def test_seven_boundaries(self):self.assertEqual(len(self.b),7)
    def test_left_clean_frame(self):
        o,b=repair_region(self.a,83,self.b,self.clean,10)
        self.assertEqual(b,89);self.assertEqual(int(o[500,500,0]),100)
    def test_right_clean_frame(self):
        o,b=repair_region(self.a,94,self.b,self.clean,10)
        self.assertEqual(b,89);self.assertEqual(int(o[500,500,0]),200)
    def test_caption_unchanged(self):
        o,_=repair_region(self.a,89,self.b,self.clean,10)
        self.assertTrue(np.array_equal(o[1540:],self.a[1540:]))
    def test_outside_window_unchanged(self):
        o,b=repair_region(self.a,75,self.b,self.clean,10)
        self.assertIsNone(b);self.assertTrue(np.array_equal(o,self.a))
    def test_boundary_frame_is_right(self):
        o,_=repair_region(self.a,89,self.b,self.clean,10)
        self.assertEqual(int(o[500,500,0]),200)
    def test_safety_flags(self):
        self.assertIs(POLICY['publication_approved'],False)
        self.assertIs(POLICY['automatic_posting'],False)
    def test_audio_stream_copy_contract(self):
        import inspect
        from ui_transition_clarity import render
        self.assertIn("'-c:a','copy'",inspect.getsource(render))
    def test_nonmutating_input(self):
        original=self.a.copy();repair_region(self.a,90,self.b,self.clean,10)
        self.assertTrue(np.array_equal(original,self.a))

if __name__=='__main__':unittest.main()
