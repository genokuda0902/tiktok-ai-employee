import importlib.util
from pathlib import Path
import unittest
p=Path(__file__).parent/'focus824.py'
s=importlib.util.spec_from_file_location('focus824',p)
m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
class TestFocus824(unittest.TestCase):
 def test_ten_genres(self):
  self.assertEqual(len(m.PALETTES),10)
  for genre in m.PALETTES:
   self.assertEqual(m.focus_filter(genre,16,3).count('drawbox='),4)
 def test_reject_unknown_genre(self):
  with self.assertRaises(ValueError):m.focus_filter('unknown',16,3)
 def test_reject_bad_time(self):
  for t,d in ((-1,3),(16,1)):
   with self.assertRaises(ValueError):m.focus_filter('ai_work',t,d)
 def test_caption_safe(self):
  for x,y,w,h in (m.FOCUS_A,m.FOCUS_B):
   self.assertGreaterEqual(x,0)
   self.assertLessEqual(x+w,1080)
   self.assertLessEqual(y+h,m.SAFE_CAPTION_TOP)
 def test_two_stages(self):
  s=m.focus_filter('ai_work',16,3.3)
  self.assertIn('between(t,16.140,17.650)',s)
  self.assertIn('between(t,17.650,19.180)',s)
 def test_no_publication(self):
  text=p.read_text()
  self.assertNotIn('requests.post(',text)
  self.assertIn("'auto_post':False",text)
if __name__=='__main__':unittest.main()
