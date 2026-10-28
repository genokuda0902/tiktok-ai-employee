import importlib.util, pathlib, unittest
from PIL import Image
HERE=pathlib.Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('calc_live_insert',HERE.parent/'src'/'calc_live_insert.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class TestCalcLiveInsert(unittest.TestCase):
 def test_ten_genres(self):self.assertEqual(len(m.GENRES),10)
 def test_scene_length(self):self.assertEqual(m.END-m.START,87)
 def test_caption_safe(self):self.assertLess(m.SAFE_Y,1490)
 def test_policy(self):self.assertIn('PUBLICATION_NOT_APPROVED',m.POLICY)
 def test_unknown_genre_rejected(self):
  with self.assertRaises(ValueError):m.ensure_contract('unapproved')
 def test_stage_start(self):self.assertEqual(m.beat(m.START),0)
 def test_stage_middle(self):self.assertEqual(m.beat(m.START+40),1)
 def test_stage_end(self):self.assertEqual(m.beat(m.END-1),2)
 def test_stage_bounds(self):
  with self.assertRaises(ValueError):m.beat(m.END)
 def test_render_shape(self):
  img=m.draw_frame(Image.new('RGB',(1440,900),'white'),m.START,'ai_work')
  self.assertEqual(img.size,(1080,1460))
 def test_all_genres_render(self):
  sample=Image.new('RGB',(1440,900),'white')
  for g in m.GENRES:self.assertEqual(m.draw_frame(sample,m.START,g).size,(1080,1460))
if __name__=='__main__':unittest.main()
