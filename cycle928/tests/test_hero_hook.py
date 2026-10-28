import sys, unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
import hero_hook as m
class TestHero(unittest.TestCase):
 def test_genres(self):self.assertEqual(len(m.GENRES),10)
 def test_validate(self):self.assertTrue(m.validate())
 def test_stage_edges(self):self.assertEqual([m.stage(x) for x in (0,28,29,57,58,86)],[0,0,1,1,2,2])
 def test_stage_out_of_range(self):
  for x in (-1,87):
   with self.assertRaises(ValueError):m.stage(x)
 def test_safe_area(self):self.assertEqual(m.CAPTION_SAFE_Y,1460)
 def test_policy(self):self.assertIn('PUBLICATION_NOT_APPROVED',m.POLICY)
 def test_render_all_genres(self):
  for name in m.GENRES:self.assertEqual(m.render_frame(40,name).size,(1080,1460))
 def test_invalid_genre(self):
  with self.assertRaises(ValueError):m.render_frame(0,'bad')
 def test_different_beats(self):self.assertNotEqual(m.render_frame(0).tobytes(),m.render_frame(70).tobytes())
 def test_no_true_data(self):self.assertIn('DEMO / 架空の表',m.render_frame.__code__.co_consts)
if __name__=='__main__':unittest.main()
