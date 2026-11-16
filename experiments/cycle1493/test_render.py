import unittest
from render import SCENES
class TestReview(unittest.TestCase):
    def test_four_scenes(self): self.assertEqual(len(SCENES),4)
    def test_japanese_text(self): self.assertTrue(all(any(ord(c)>127 for c in a+b) for a,b in SCENES))
    def test_nonempty(self): self.assertTrue(all(a and b for a,b in SCENES))
if __name__=="__main__": unittest.main()
