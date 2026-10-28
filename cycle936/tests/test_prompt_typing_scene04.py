import sys, unittest
from pathlib import Path
from PIL import ImageChops
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from prompt_typing_scene04 import (GENRES, POLICY, SAFE_Y, SCENE_START, SCENE_END, WIDTH,
    draw_prompt, phase, validate)

class PromptSceneTests(unittest.TestCase):
 def test_ten_genres(self): self.assertEqual(len(GENRES),10)
 def test_every_genre_renders(self):
  for g in GENRES:
   with self.subTest(genre=g): self.assertEqual(draw_prompt(40,g).size,(WIDTH,SAFE_Y))
 def test_timing_phases(self): self.assertEqual([phase(f) for f in (0,28,29,57,58,86)],[0,0,1,1,2,2])
 def test_outside_frame_rejected(self):
  for f in (-1,87):
   with self.assertRaises(ValueError):phase(f)
 def test_unknown_genre_rejected(self):
  with self.assertRaises(ValueError):validate('unsupported')
 def test_progress_changes_pixels(self):
  a=draw_prompt(4);b=draw_prompt(38);c=draw_prompt(77)
  self.assertIsNotNone(ImageChops.difference(a.convert("RGB"),b.convert("RGB")).getbbox())
  self.assertIsNotNone(ImageChops.difference(b.convert("RGB"),c.convert("RGB")).getbbox())
 def test_safe_caption_geometry(self):self.assertLess(SAFE_Y,1490)
 def test_exact_scene_length(self):self.assertEqual(SCENE_END-SCENE_START,87)
 def test_publication_denied(self):self.assertIn('PUBLICATION_NOT_APPROVED',POLICY)
 def test_no_unapproved_assets(self):
  from prompt_typing_scene04 import render
  import inspect
  src=inspect.getsource(render)
  self.assertNotIn('requests.',src);self.assertNotIn('upload',src.lower().replace('public_media_upload',''))
 def test_no_false_productivity_claims(self):
  for triple in GENRES.values():self.assertTrue(all('倍' not in s and '%' not in s for s in triple))
 def test_visual_bounds(self):
  im=draw_prompt(86);self.assertEqual(im.getbbox()[3],1431)

if __name__=='__main__':unittest.main()
