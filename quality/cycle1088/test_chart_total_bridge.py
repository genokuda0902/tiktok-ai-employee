import unittest
from PIL import ImageChops
from . import chart_total_bridge as m

class ChartBridgeTest(unittest.TestCase):
 def test_values(self):self.assertEqual(m.totals(m.DEMO),[46,29,75])
 def test_ten_genres(self):self.assertEqual(len(m.PALETTES),10)
 def test_all_genres_draw(self):
  for genre in m.PALETTES:
   with self.subTest(genre=genre):self.assertIsNotNone(m.frame(42,m.DEMO,genre).getbbox())
 def test_transparent_caption_area(self):
  for i in (0,8,20,36,48):
   a=m.frame(i,m.DEMO).getchannel('A')
   self.assertIsNone(a.crop((0,1175,1080,m.SAFE_Y)).getbbox())
 def test_no_unapproved_data(self):
  x={**m.DEMO,'note':'customer export'}
  with self.assertRaises(ValueError):m.totals(x)
 def test_bad_negative(self):
  x={'categories':['4月'],'series':[{'name':'A','values':[-1]},{'name':'B','values':[3]}],'note':'架空データ'}
  with self.assertRaises(ValueError):m.totals(x)
 def test_bad_bool(self):
  x={'categories':['4月'],'series':[{'name':'A','values':[True]},{'name':'B','values':[3]}],'note':'架空データ'}
  with self.assertRaises(ValueError):m.totals(x)
 def test_mismatch_hash(self):
  with self.assertRaises(ValueError):m.check_source(__file__,'0'*64)
 def test_invalid_frame(self):
  with self.assertRaises(ValueError):m.frame(49,m.DEMO)
 def test_invalid_genre(self):
  with self.assertRaises(ValueError):m.frame(2,m.DEMO,'unknown')
 def test_early_late_differ(self):
  a=m.frame(1,m.DEMO).convert('RGB');b=m.frame(45,m.DEMO).convert('RGB')
  self.assertIsNotNone(ImageChops.difference(a,b).getbbox())
 def test_visible_final(self):
  a=m.frame(45,m.DEMO)
  self.assertEqual(a.getchannel('A').getbbox()[0],89)

if __name__=='__main__':unittest.main()
