import unittest
from render import caption_at,CAPTIONS
class TestCaptions(unittest.TestCase):
    def test_boundaries(self):
        self.assertEqual([caption_at(t) for t in (0,3,6,9)],CAPTIONS)
    def test_last_frame(self):
        self.assertEqual(caption_at(11.99),CAPTIONS[-1])
    def test_negative(self):
        self.assertEqual(caption_at(-1),CAPTIONS[0])
if __name__=="__main__": unittest.main()
