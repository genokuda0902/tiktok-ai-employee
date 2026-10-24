import unittest
from root_cause_depth import ACCENTS,STEPS,draw,validate,smooth,START,COUNT,X,Y,CW,CH,W,H
class RootCauseDepthTests(unittest.TestCase):
 def test_genres(self): self.assertEqual(len(ACCENTS),10)
 def test_all_genres_draw(self):
  for g in ACCENTS:
   with self.subTest(g=g): self.assertEqual(draw(89,g).size,(CW,CH))
 def test_requires_explicit_fictional_flag(self):
  with self.assertRaises(ValueError):validate('sales_business',STEPS,False)
 def test_rejects_unknown_genre(self):
  with self.assertRaises(ValueError):validate('fake',STEPS,True)
 def test_rejects_newlines(self):
  with self.assertRaises(ValueError):validate('sales_business',('a\nb','c','d'),True)
 def test_rejects_long_text(self):
  with self.assertRaises(ValueError):validate('sales_business',('abcdefghijkl','c','d'),True)
 def test_requires_three_steps(self):
  with self.assertRaises(ValueError):validate('sales_business',('a','b'),True)
 def test_out_of_bounds(self):
  with self.assertRaises(ValueError):draw(COUNT)
 def test_smooth_bounds(self): self.assertEqual((smooth(-1),smooth(2)),(0,1))
 def test_safe_overlay_region(self): self.assertTrue(X>=100 and X+CW<=W-100 and Y>=620 and Y+CH<=1360)
 def test_frames(self):self.assertEqual((START,START+COUNT-1),(360,449))
 def test_opaque_center(self):self.assertEqual(draw(60).getpixel((400,200))[3],255)
 def test_animation_changes(self):self.assertNotEqual(draw(0).tobytes(),draw(85).tobytes())
if __name__=='__main__':unittest.main()
