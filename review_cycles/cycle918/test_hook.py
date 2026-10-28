"""Review-only CI: verifies source renderer and safety; NOT private finished MP4."""
import importlib.util
import pathlib
import unittest
from PIL import Image
SRC=pathlib.Path(__file__).with_name('task_focus_hook.py')
spec=importlib.util.spec_from_file_location('task_focus_hook',SRC)
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
class HookTest(unittest.TestCase):
 def test_ten_genres(self):self.assertEqual(len(m.GENRES),10)
 def test_validate(self):self.assertTrue(m.validate())
 def test_size(self):self.assertEqual((m.W,m.H,m.N,m.FPS,m.TOP),(1080,1160,87,30,300))
 def test_caption_safe(self):self.assertEqual(m.TOP+m.H,1460)
 def test_no_external_media(self):
  src=SRC.read_text()
  for x in ('requests.','http://','https://','upload_file(', 'publish_video('):self.assertNotIn(x,src)
 def test_unique_tasks(self):
  for k,(_,tasks,_,_) in m.GENRES.items():self.assertEqual(len(set(tasks)),3,k)
 def test_titles_fit(self):
  for k,(t,tasks,a,c) in m.GENRES.items():
   self.assertLess(m.textwidth(t,49,True),970,k)
   self.assertLess(m.textwidth(a,77,True),800,k)
 def test_invalid_frame(self):
  with self.assertRaises(ValueError):m.render(87)
 def test_invalid_genre(self):
  with self.assertRaises(ValueError):m.render(0,'unknown')
 def test_three_distinct_beats(self):
  a,b,c=(m.render(i).resize((108,116)) for i in (5,43,80))
  self.assertNotEqual(a.tobytes(),b.tobytes())
  self.assertNotEqual(b.tobytes(),c.tobytes())
 def test_all_genres_render(self):
  for k in m.GENRES:
   x=m.render(0,k)
   self.assertIsInstance(x,Image.Image)
   self.assertEqual(x.size,(1080,1160))
if __name__=='__main__':unittest.main()
