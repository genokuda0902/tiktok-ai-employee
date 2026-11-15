import unittest
from render import SCENES,srt
class CaptionTests(unittest.TestCase):
    def test_timing(self):
        self.assertEqual(SCENES[0][0],0)
        self.assertEqual(SCENES[-1][1],15)
        self.assertTrue(all(SCENES[i][1]==SCENES[i+1][0] for i in range(len(SCENES)-1)))
    def test_srt(self): self.assertEqual(srt().count("-->"),5)
if __name__=="__main__": unittest.main()
