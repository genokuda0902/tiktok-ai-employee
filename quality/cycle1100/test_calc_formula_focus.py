import unittest
from calc_formula_focus import (PALETTES,START,COUNT,SAFE_BOTTOM,FORMULA_RECT,TOTAL_RECT,
                                validate,overlay,ease)
from PIL import Image

class FocusTests(unittest.TestCase):
 def setUp(self):
  self.m={'genre':'ai_work','synthetic_scenario':True,'review_only':True,
          'rights_status':'unverified','contains_private_data':False}
 def test_all_ten_genres(self):
  self.assertEqual(len(PALETTES),10)
  for g in PALETTES:
   m={**self.m,'genre':g};self.assertTrue(validate(m))
   self.assertEqual(overlay(15,g).size,(1080,SAFE_BOTTOM))
 def test_fail_closed_private_data(self):
  with self.assertRaises(ValueError):validate({**self.m,'contains_private_data':True})
 def test_fail_closed_rights(self):
  with self.assertRaises(ValueError):validate({**self.m,'rights_status':'approved'})
 def test_fail_closed_review(self):
  with self.assertRaises(ValueError):validate({**self.m,'review_only':False})
 def test_fail_closed_scenario(self):
  with self.assertRaises(ValueError):validate({**self.m,'synthetic_scenario':False})
 def test_fail_closed_schema(self):
  with self.assertRaises(ValueError):validate({**self.m,'extra':'bad'})
 def test_reject_unknown_genre(self):
  with self.assertRaises(ValueError):validate({**self.m,'genre':'unknown'})
 def test_chapter_boundaries(self):
  self.assertEqual(START,195);self.assertEqual(COUNT,54)
  self.assertLessEqual(START+COUNT,264)
 def test_protected_subtitles(self):
  for i in [0,6,15,26,27,42,53]:
   im=overlay(i,'ai_work');self.assertEqual(im.height,825)
 def test_two_stages(self):
  self.assertNotEqual(overlay(12,'ai_work').tobytes(),overlay(39,'ai_work').tobytes())
 def test_no_frame_outside(self):
  for i in [-1,54]:
   with self.assertRaises(ValueError):overlay(i,'ai_work')
 def test_focus_rects_inside_picture(self):
  for x0,y0,x1,y1 in (FORMULA_RECT,TOTAL_RECT):
   self.assertTrue(0<x0<x1<1080 and 0<y0<y1<SAFE_BOTTOM)
 def test_ease_limits(self):
  self.assertEqual(ease(-2),0);self.assertEqual(ease(2),1)
 def test_alpha_not_all_transparent(self):
  self.assertGreater(overlay(14,'ai_work').getchannel('A').getextrema()[1],0)
if __name__=='__main__':unittest.main()
