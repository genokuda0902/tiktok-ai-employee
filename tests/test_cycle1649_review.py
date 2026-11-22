import unittest
from tools.cycle1649_review import CUES
class CaptionTest(unittest.TestCase):
    def test_coverage(self):
        self.assertEqual(CUES[0][0],0)
        self.assertEqual(CUES[-1][1],12)
        self.assertTrue(all(a<b and (i==0 or a==CUES[i-1][1]) for i,(a,b,_) in enumerate(CUES)))
    def test_no_empty_captions(self):
        self.assertTrue(all(text.strip() for _,_,text in CUES))
if __name__=="__main__": unittest.main()
