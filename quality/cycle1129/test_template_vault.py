import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from template_vault import GENRE_DATA,render_art,W,H,ease

class TemplateVaultTests(unittest.TestCase):
 def test_ten_genres(self):self.assertEqual(len(GENRE_DATA),10)
 def test_image_dimensions(self):self.assertEqual(render_art(0).size,(951,803))
 def test_rgb(self):self.assertEqual(render_art(.7).mode,'RGB')
 def test_invalid_genre(self):
  with self.assertRaises(ValueError):render_art(0,'unapproved')
 def test_motion(self):self.assertNotEqual(render_art(.2).tobytes(),render_art(1.2).tobytes())
 def test_save_confirmation(self):
  a,b=render_art(1.2),render_art(1.9)
  self.assertNotEqual(a.crop((567,485,884,563)).tobytes(),b.crop((567,485,884,563)).tobytes())
 def test_genre_specific(self):self.assertNotEqual(render_art(1.9,'ai_work').tobytes(),render_art(1.9,'travel').tobytes())
 def test_all_genres_render(self):
  for genre in GENRE_DATA:self.assertEqual(render_art(1.9,genre).size,(W,H))
 def test_easing(self):
  self.assertEqual(ease(-2),0)
  self.assertEqual(ease(5),1)

if __name__=='__main__':unittest.main()
