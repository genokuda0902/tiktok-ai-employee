import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import pair_trace as p
class PairTraceTests(unittest.TestCase):
 def test_ten_genres(self):
  self.assertEqual(len(p.GENRE_ACCENTS),10)
  for g in p.GENRE_ACCENTS:
   self.assertEqual(p.filter_graph(g,8.233,11.0).count('drawbox='),6)
 def test_safe_layout(self):
  self.assertTrue(p.validate_layout(p.DEFAULT_PAIRS))
  with self.assertRaises(ValueError):
   p.validate_layout([[(80,1150,200,80),(500,600,200,80)]]*3)
 def test_no_frame_edge(self):
  with self.assertRaises(ValueError):
   p.validate_layout([[(1000,600,200,80),(500,600,200,80)]]*3)
 def test_bad_genre(self):
  with self.assertRaises(ValueError):p.filter_graph('unknown',8.2,11.0)
 def test_short_scene(self):
  with self.assertRaises(ValueError):p.filter_graph('ai',8.2,10.0)
 def test_timing(self):
  f=p.filter_graph('ai',8.233,11.0)
  for a,b in [(8.433,9.123),(9.243,9.933),(10.053,10.743)]:
   self.assertIn(f'{a:.3f}',f);self.assertIn(f'{b:.3f}',f)
 def test_chapter(self):
  m={'chapters':[{'start_time':'8.233','end_time':'11.000','tags':{'title':'04/08'}}]}
  self.assertEqual(p.chapter_window(m),(8.233,11.0))
 def test_missing_chapter(self):
  with self.assertRaises(ValueError):p.chapter_window({'chapters':[]})
 def test_no_overwrite(self):
  with self.assertRaises(ValueError):p.render('/tmp/no-file','/tmp/no-file')
if __name__=='__main__':unittest.main()
