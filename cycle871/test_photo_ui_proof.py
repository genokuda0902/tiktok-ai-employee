import unittest
from PIL import Image
from photo_ui_proof import GENRES,POLICY,draw_frame,check_inputs,fit_text,START,COUNT,TOP,BOTTOM

class ReviewOnlyUITests(unittest.TestCase):
 def setUp(self):
  self.photo=Image.new('RGB',(941,1672),'#153a52')
  self.ui=[Image.new('RGB',(900,560),'#f0f6fa') for _ in range(26)]
 def test_genres(self): self.assertEqual(len(GENRES),10)
 def test_all_genres(self):
  for g in GENRES: self.assertEqual(draw_frame(self.photo,self.ui,0,g).size,(1080,BOTTOM-TOP))
 def test_last_frame(self): self.assertEqual(draw_frame(self.photo,self.ui,77).mode,'RGB')
 def test_review_gate(self):
  self.assertFalse(POLICY['publication_approved']);self.assertFalse(POLICY['automatic_posting']);self.assertFalse(POLICY['external_upload'])
 def test_bad_genre(self):
  with self.assertRaises(ValueError): check_inputs('not_a_genre',self.photo,self.ui)
 def test_missing_ui(self):
  with self.assertRaises(ValueError): check_inputs('ai_work',self.photo,self.ui[:25])
 def test_small_photo(self):
  with self.assertRaises(ValueError): check_inputs('ai_work',Image.new('RGB',(800,1600)),self.ui)
 def test_bad_frame(self):
  with self.assertRaises(ValueError): draw_frame(self.photo,self.ui,COUNT)
 def test_copy_clipping(self):
  with self.assertRaises(ValueError): fit_text('長い'*100,100,53)
 def test_region(self): self.assertEqual((START,COUNT,TOP,BOTTOM),(510,78,132,1490))

if __name__=='__main__': unittest.main()
