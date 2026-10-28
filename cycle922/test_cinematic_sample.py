import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from cinematic_sample import *
class RenderTests(unittest.TestCase):
 def test_genres(self):self.assertTrue(validate_genres())
 def test_dimensions(self):self.assertEqual(draw_frame(0).size,(540,565))
 def test_beat_changes(self):
  a=draw_frame(4);b=draw_frame(42);c=draw_frame(75)
  self.assertNotEqual(a.tobytes(),b.tobytes())
  self.assertNotEqual(b.tobytes(),c.tobytes())
 def test_bad_genre(self):
  with self.assertRaises(ValueError):draw_frame(0,'invalid')
 def test_bad_frame(self):
  with self.assertRaises(ValueError):draw_frame(87)
 def test_10_genres_render(self):
  for genre in GENRES:self.assertEqual(draw_frame(15,genre).size,(540,565))
 def test_text_bounds(self):
  for title,labels,_ in GENRES.values():
   self.assertLess(text_width(title,38,True),330)
   self.assertTrue(all(text_width(x,25,True)<220 for x in labels))
 def test_no_personal_data(self):
  import inspect
  s=inspect.getsource(draw_frame)+inspect.getsource(sheet)
  for bad in ('@gmail.com','@yahoo.co.jp','https://docs.google.com','auto_post','publish_video'):
   self.assertNotIn(bad,s)
if __name__=='__main__':unittest.main()
