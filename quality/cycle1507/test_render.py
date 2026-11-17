import unittest
from render import SCENES,W,H
class TestRender(unittest.TestCase):
 def test_resolution(self):self.assertEqual((W,H),(1080,1920))
 def test_scenes(self):self.assertEqual(len(SCENES),4)
 def test_caption_lengths(self):
  for title,sub in SCENES:
   self.assertLessEqual(len(title),20)
   self.assertLessEqual(len(sub),25)
if __name__=='__main__':unittest.main()
