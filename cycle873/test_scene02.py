import unittest
from PIL import Image
from scene02 import GENRES,POLICY,START,COUNT,TOP,BOTTOM,validate,make_frame,text_fits,smooth

class SceneTests(unittest.TestCase):
 def setUp(self):self.photo=Image.new('RGB',(1000,1600),'#123456')
 def test_ten_genres(self):self.assertEqual(len(GENRES),10)
 def test_all_text_fits(self):
  for key in GENRES:validate(key,self.photo)
 def test_bad_genre(self):
  with self.assertRaises(ValueError):validate('bad',self.photo)
 def test_too_small_photo(self):
  with self.assertRaises(ValueError):validate('ai_work',Image.new('RGB',(200,200)))
 def test_policy_fail_closed(self):
  self.assertFalse(POLICY['publication_approved']);self.assertFalse(POLICY['external_upload']);self.assertFalse(POLICY['automatic_posting'])
 def test_frame_bounds(self):
  for n in (-1,COUNT):
   with self.assertRaises(ValueError):make_frame(Image.new('RGB',(1080,BOTTOM-TOP)),n)
 def test_frame_dimensions(self):self.assertEqual(make_frame(Image.new('RGB',(1080,BOTTOM-TOP)),0).size,(1080,BOTTOM-TOP))
 def test_frame_progress(self):
  bg=Image.new('RGB',(1080,BOTTOM-TOP),'#123456')
  self.assertNotEqual(make_frame(bg,0).tobytes(),make_frame(bg,79).tobytes())
 def test_smooth(self):self.assertEqual(smooth(0),0);self.assertEqual(smooth(1),1)
 def test_frame_location(self):self.assertEqual((START,COUNT,TOP,BOTTOM),(90,80,132,1490))
 def test_overflow_detector(self):self.assertFalse(text_fits('あ'*100,50,200))

if __name__=='__main__':unittest.main()
