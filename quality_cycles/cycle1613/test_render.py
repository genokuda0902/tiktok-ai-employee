import unittest
from render import validate
class CaptionTests(unittest.TestCase):
 def test_valid(self):validate([("字幕",0,3),("次",3,5)],5)
 def test_overlap_rejected(self):
  with self.assertRaises(AssertionError):validate([("字幕",0,4),("次",3,5)],5)
 def test_overlong_rejected(self):
  with self.assertRaises(AssertionError):validate([("あ"*19,0,3)],5)
if __name__=="__main__":unittest.main()
