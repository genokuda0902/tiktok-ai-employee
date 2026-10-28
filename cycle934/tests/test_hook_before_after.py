import importlib.util,unittest
from pathlib import Path
from PIL import Image
p=Path(__file__).resolve().parents[1]/'src'/'hook_before_after.py'
spec=importlib.util.spec_from_file_location('hook',p)
hook=importlib.util.module_from_spec(spec);spec.loader.exec_module(hook)

class HookTests(unittest.TestCase):
 def test_genres(self):self.assertEqual(len(hook.GENRES),10)
 def test_all_genre_contracts(self):
  for genre in hook.GENRES:hook.ensure_contract(genre)
 def test_bad_genre_rejected(self):
  with self.assertRaises(ValueError):hook.ensure_contract('unknown')
 def test_phases(self):
  self.assertEqual([hook.phase(i) for i in [0,23,24,52,53,86]],[0,0,1,1,2,2])
 def test_frame_bounds(self):
  for i in [-1,87]:
   with self.assertRaises(ValueError):hook.phase(i)
 def test_frame_geometry(self):self.assertEqual(hook.draw_hook(0).size,(1080,1450))
 def test_bottom_band_transparent(self):
  for frame in [0,35,86]:
   im=hook.draw_hook(frame)
   self.assertEqual(im.getpixel((500,0))[3],0)
 def test_stage_diff(self):
  a=hook.draw_hook(0).convert('RGB');b=hook.draw_hook(86).convert('RGB')
  self.assertNotEqual(a.tobytes(),b.tobytes())
 def test_all_genre_render(self):
  for g in hook.GENRES: self.assertEqual(hook.draw_hook(53,g).size,(1080,1450))
 def test_policy(self):self.assertIn('PUBLICATION_NOT_APPROVED',hook.POLICY)
 def test_ease_bounds(self):self.assertEqual((hook.ease(-1),hook.ease(2)),(0,1))
 def test_reveal_is_monotonic(self):
  self.assertLess(hook.ease(.2),hook.ease(.5));self.assertLess(hook.ease(.5),hook.ease(.8))

if __name__=='__main__':unittest.main()
