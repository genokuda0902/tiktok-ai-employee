import unittest
from render import CAPTIONS,caption_filter
class CaptionTests(unittest.TestCase):
 def test_no_gaps(self):
  self.assertEqual(CAPTIONS[0][0],0)
  self.assertEqual(CAPTIONS[-1][1],15)
  for a,b in zip(CAPTIONS,CAPTIONS[1:]):self.assertEqual(a[1],b[0])
 def test_safe_zone(self):
  f=caption_filter();self.assertIn("y=1450",f);self.assertIn("y=1512",f)
 def test_no_private_text(self):
  self.assertTrue(all("氏名" not in text and "電話番号" not in text for _,_,text in CAPTIONS))
if __name__=="__main__":unittest.main()
