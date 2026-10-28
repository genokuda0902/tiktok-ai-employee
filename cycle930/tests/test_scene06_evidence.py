import importlib.util, unittest
from pathlib import Path
spec=importlib.util.spec_from_file_location('cycle930',Path(__file__).resolve().parents[1]/'src'/'scene06_evidence.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class EvidenceTests(unittest.TestCase):
 def test_policy(self):self.assertTrue(m.validate());self.assertIn('PUBLICATION_NOT_APPROVED',m.POLICY)
 def test_ten_genres(self):self.assertEqual(len(m.GENRES),10)
 def test_exact_scene(self):self.assertEqual(m.END-m.START,87)
 def test_caption_safe(self):self.assertLess(m.CAPTION_SAFE_Y,m.HEIGHT)
 def test_first_stage(self):self.assertEqual(m.stage(435),0)
 def test_middle_stage(self):self.assertEqual(m.stage(464),1)
 def test_final_stage(self):self.assertEqual(m.stage(521),2)
 def test_bounds_low(self):
  with self.assertRaises(ValueError):m.stage(434)
 def test_bounds_high(self):
  with self.assertRaises(ValueError):m.stage(522)
 def test_render_all_genres(self):
  for genre in m.GENRES:self.assertEqual(m.render(480,genre).size,(1080,1460))
 def test_unknown_genre(self):
  with self.assertRaises(ValueError):m.render(480,'unknown')
 def test_not_publishing(self):self.assertNotIn('post_to_tiktok',Path(m.__file__).read_text())
if __name__=='__main__':unittest.main()
