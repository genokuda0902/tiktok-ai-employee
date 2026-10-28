import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from save_flow import PRESETS,validate_presets,draw
class TestSaveFlow(unittest.TestCase):
 def test_genre_count(self):self.assertEqual(len(PRESETS),10)
 def test_presets_fit(self):self.assertTrue(validate_presets())
 def test_frame_size(self):self.assertEqual(draw(0).size,(1080,1160))
 def test_distinct_beats(self):
  a=draw(10).resize((108,116));b=draw(42).resize((108,116));c=draw(76).resize((108,116))
  self.assertNotEqual(a.tobytes(),b.tobytes());self.assertNotEqual(b.tobytes(),c.tobytes())
 def test_all_genres(self):
  for g in PRESETS:self.assertEqual(draw(65,g).size,(1080,1160))
 def test_no_performance_claims(self):
  for vals in PRESETS.values():self.assertFalse(any(w in ''.join(vals) for w in ['絶対','保証','100%','売上倍増']))
 def test_invalid_frame(self):
  with self.assertRaises(ValueError):draw(87)
 def test_invalid_genre(self):
  with self.assertRaises(ValueError):draw(0,'missing')
if __name__=='__main__':unittest.main()
