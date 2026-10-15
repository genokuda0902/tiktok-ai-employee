"""Numeric and animation regression checks."""
import unittest
from proof_model import Proof,SAMPLE,GENRES
from frame_design import frame,ease
class TestProof(unittest.TestCase):
    def test_sum(self): self.assertEqual(SAMPLE.total,720)
    def test_peak(self): self.assertEqual(SAMPLE.peak,'4月')
    def test_genres(self): self.assertEqual(len(GENRES),10)
    def test_bad_dimensions(self):
        with self.assertRaises(ValueError): Proof(('a',),(1,2)).validate()
    def test_negative(self):
        with self.assertRaises(ValueError): Proof(('a','b'),(1,-2)).validate()
    def test_zero(self):
        with self.assertRaises(ValueError): Proof(('a','b'),(0,0)).validate()
    def test_ease(self):
        self.assertEqual(ease(-1),0)
        self.assertEqual(ease(2),1)
    def test_frame_size(self): self.assertEqual(frame(0).size,(1080,1920))
    def test_motion(self):
        a=frame(0).resize((108,192)).tobytes()
        b=frame(71).resize((108,192)).tobytes()
        self.assertNotEqual(a,b)
if __name__=='__main__': unittest.main()
