import unittest
from visual_spec_core import WIDTH,HEIGHT,FPS,PALETTES,SCENES,CAPTION_BAND,VISUAL_BAND,inside,validate
class TestVisualSpecCore(unittest.TestCase):
 def test_format(self):self.assertEqual((WIDTH,HEIGHT,FPS),(1080,1920,30))
 def test_genres(self):self.assertEqual(len(PALETTES),10)
 def test_scenes(self):self.assertEqual(len(SCENES),8)
 def test_unique_pictograms(self):self.assertEqual(len({s.pictogram for s in SCENES}),8)
 def test_every_genre_valid(self):
  for g in PALETTES:self.assertTrue(validate(g))
 def test_invalid_genre(self):
  with self.assertRaises(ValueError):validate('invalid')
 def test_caption_safe(self):self.assertLess(VISUAL_BAND[3],CAPTION_BAND[1])
 def test_caption_inside(self):self.assertTrue(inside(CAPTION_BAND))
 def test_visual_inside(self):self.assertTrue(inside(VISUAL_BAND))
 def test_reject_negative(self):self.assertFalse(inside((-1,1,2,3)))
 def test_reject_inverted(self):self.assertFalse(inside((10,10,5,20)))
 def test_no_fake_savings_claim(self):self.assertNotIn('75%',str(SCENES))
 def test_no_user_data(self):self.assertNotIn('genokuda',str(SCENES).lower())
if __name__=='__main__':unittest.main()
