import unittest
from cycle592_clean_proof import Scene,GENRE_COLORS,validate,draw_frame,W,H,FPS,START,DURATION

class SceneTests(unittest.TestCase):
 def test_ten_genres(self):
  self.assertEqual(len(GENRE_COLORS),10)
  for genre in GENRE_COLORS:self.assertTrue(validate(Scene(genre=genre)))
 def test_correct_sum(self):self.assertTrue(validate(Scene()))
 def test_reject_wrong_sum(self):
  with self.assertRaises(ValueError):validate(Scene(total=721))
 def test_reject_negative_value(self):
  with self.assertRaises(ValueError):validate(Scene(values=(-1,150,200,250),total=599))
 def test_reject_missing_disclosure(self):
  with self.assertRaises(ValueError):validate(Scene(disclosure=''))
 def test_reject_unknown_genre(self):
  with self.assertRaises(ValueError):validate(Scene(genre='unknown'))
 def test_reject_duplicate_labels(self):
  with self.assertRaises(ValueError):validate(Scene(labels=('A','A','B','C')))
 def test_video_dimensions(self):self.assertEqual((W,H,FPS,START,DURATION),(1080,1920,30,4.0,2.0))
 def test_render_early(self):self.assertEqual(draw_frame(0).size,(W,H))
 def test_render_late(self):self.assertEqual(draw_frame(59).size,(W,H))
 def test_invalid_frame(self):
  with self.assertRaises(ValueError):draw_frame(60)

if __name__=='__main__':unittest.main()
