import unittest
from dataclasses import replace
from PIL import Image
from cta_loop import DEFAULT,GENRES,validate,frame,smooth
class TestCycle564(unittest.TestCase):
 def test_ten_genres(self):
  for genre in GENRES:self.assertTrue(validate(replace(DEFAULT,genre=genre)))
 def test_reject_unapproved_rights(self):
  with self.assertRaises(ValueError):validate(replace(DEFAULT,rights='unknown'))
 def test_reject_publication_approval(self):
  with self.assertRaises(ValueError):validate(replace(DEFAULT,review_only=False))
 def test_reject_long_caption(self):
  with self.assertRaises(ValueError):validate(replace(DEFAULT,cta='あ'*19))
 def test_reject_multiline(self):
  with self.assertRaises(ValueError):validate(replace(DEFAULT,cta='テスト\n改行'))
 def test_safe_image_dimensions(self):
  for t in [0,.5,1.2,1.8,1.99]:self.assertEqual(frame(DEFAULT,t).size,(720,1280))
 def test_time_bounds(self):
  for t in [-.1,2.1]:
   with self.assertRaises(ValueError):frame(DEFAULT,t)
 def test_motion_changes(self):self.assertNotEqual(frame(DEFAULT,.2).tobytes(),frame(DEFAULT,1.1).tobytes())
 def test_loop_exact_end(self):
  first=Image.new('RGB',(720,1280),(91,23,45))
  self.assertEqual(frame(DEFAULT,1.96,first).tobytes(),first.tobytes())
 def test_no_early_loop(self):
  first=Image.new('RGB',(720,1280),(91,23,45))
  self.assertNotEqual(frame(DEFAULT,1.7,first).tobytes(),first.tobytes())
 def test_smooth(self):self.assertEqual(smooth(-1),0);self.assertEqual(smooth(2),1)
if __name__=='__main__':unittest.main()
