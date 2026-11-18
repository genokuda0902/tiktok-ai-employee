import unittest
from audio_tail_fade import fade_tail
class FadeTests(unittest.TestCase):
    def test_reject_zero(self):
        with self.assertRaises(ValueError): fade_tail("x","y",0)
    def test_reject_three_seconds(self):
        with self.assertRaises(ValueError): fade_tail("x","y",3)
if __name__=="__main__": unittest.main()
