import unittest
from action_story import GENRE_COLORS,ROWS,FRAME_COUNT,render_frame,validate_plan,WIDTH,HEIGHT
class ActionStoryTests(unittest.TestCase):
 def test_ten_genres(self): self.assertEqual(len(GENRE_COLORS),10)
 def test_all_genres_render(self):
  for name in GENRE_COLORS:
   with self.subTest(name=name):
    self.assertEqual(render_frame(46,name).size,(WIDTH,HEIGHT))
 def test_all_rows_complete(self): self.assertTrue(validate_plan())
 def test_missing_deadline_fails_closed(self):
  with self.assertRaises(ValueError): validate_plan((ROWS[0],ROWS[1],('期限','—')))
 def test_missing_role_fails_closed(self):
  with self.assertRaises(ValueError): validate_plan((('','担当'),ROWS[1],ROWS[2]))
 def test_missing_label_fails_closed(self):
  with self.assertRaises(ValueError): validate_plan((ROWS[0],ROWS[1],('いつか','明日')))
 def test_frame_bounds(self):
  for n in (-1,FRAME_COUNT):
   with self.assertRaises(ValueError): render_frame(n)
 def test_invalid_genre(self):
  with self.assertRaises(ValueError): render_frame(0,'unknown')
 def test_motion_changes_pixels(self):
  self.assertNotEqual(render_frame(0).tobytes(),render_frame(89).tobytes())
 def test_overlay_is_transparent_outside_card(self):
  im=render_frame(30)
  self.assertEqual(im.getpixel((0,0))[3],0)
  self.assertEqual(im.getpixel((350,200))[3],255)
 def test_no_private_identifiers(self):
  s=' '.join(' '.join(x) for x in ROWS)
  for v in ('@','電話番号','住所','個人情報'): self.assertNotIn(v,s)
if __name__=='__main__': unittest.main()
