import sys, unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
import scene02_workflow_clarity as m
class TestCycle926(unittest.TestCase):
 def test_genres(self):self.assertEqual(len(m.GENRES),10)
 def test_geometry(self):self.assertTrue(m.validate())
 def test_scene_start(self):self.assertEqual(m.stage_for_frame(87),0)
 def test_scene_stage2(self):self.assertEqual(m.stage_for_frame(116),1)
 def test_scene_stage3(self):self.assertEqual(m.stage_for_frame(145),2)
 def test_last(self):self.assertEqual(m.stage_for_frame(173),2)
 def test_invalid_before(self):
  with self.assertRaises(ValueError):m.stage_for_frame(86)
 def test_invalid_after(self):
  with self.assertRaises(ValueError):m.stage_for_frame(174)
 def test_review_only(self):self.assertIn('PUBLICATION_NOT_APPROVED',m.POLICY)
 def test_all_3steps(self):self.assertTrue(all(len(x[1])==3 for x in m.GENRES.values()))
 def test_caption_band(self):self.assertEqual(m.CAPTION_SAFE_Y,1460)
 def test_render_dimensions(self):
  from PIL import Image
  self.assertEqual(m.render_stage(0).size,(1080,1460))
 def test_render_10_genres(self):
  for name in m.GENRES:
   self.assertEqual(m.render_stage(1,name).size,(1080,1460))
 def test_invalid_genre(self):
  with self.assertRaises(ValueError):m.render_stage(0,'unknown')
 def test_invalid_stage(self):
  with self.assertRaises(ValueError):m.render_stage(4)
if __name__=='__main__':unittest.main()
