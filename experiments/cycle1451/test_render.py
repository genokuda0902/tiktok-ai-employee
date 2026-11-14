import unittest
from render import CAPTIONS,make_srt
class TestCaptions(unittest.TestCase):
    def test_count(self): self.assertEqual(len(CAPTIONS),4)
    def test_japanese(self): self.assertIn("合計",make_srt())
    def test_no_overlap(self):
        for a,b in zip(CAPTIONS,CAPTIONS[1:]): self.assertEqual(a[1],b[0])
if __name__=="__main__": unittest.main()
