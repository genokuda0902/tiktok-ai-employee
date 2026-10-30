import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'source'))
from kinetic_hook import GENRE_HOOKS,render_plate,fit_text,opacity,validate_source

class KineticHookTest(unittest.TestCase):
 def test_genres(self):self.assertEqual(len(GENRE_HOOKS),10)
 def test_hook_nonblank(self):
  for lines in GENRE_HOOKS.values():
   self.assertEqual(len(lines),2)
   self.assertTrue(all(x.strip() for x in lines))
 def test_plate_dimensions(self):self.assertEqual(render_plate(5,'ai_work').size,(1080,1250))
 def test_plate_rgba(self):self.assertEqual(render_plate(5,'ai_work').mode,'RGBA')
 def test_plate_has_transparent_fade(self):
  self.assertLess(render_plate(35,'ai_work').getpixel((400,400))[3],render_plate(5,'ai_work').getpixel((400,400))[3])
 def test_opacity_monotonic(self):
  vals=[opacity(i) for i in range(36)]
  self.assertTrue(all(x>=y for x,y in zip(vals,vals[1:])))
 def test_opacity_last(self):self.assertEqual(opacity(35),0)
 def test_opacity_invalid(self):
  for i in (-1,36,1.5):
   with self.assertRaises(ValueError):opacity(i)
 def test_unknown_genre(self):
  with self.assertRaises(ValueError):render_plate(2,'unsafe')
 def test_text_fits(self):
  for lines in GENRE_HOOKS.values():
   for text in lines:self.assertIsNotNone(fit_text(text))
 def test_audio_source_gate(self):
  with self.assertRaises(ValueError):validate_source('/nonexistent','0'*64,'ai_work',False)
 def test_genre_rights_gate(self):
  with self.assertRaises(ValueError):validate_source('/nonexistent','0'*64,'beauty',True)
 def test_no_assets_embedded(self):
  import inspect,kinetic_hook
  self.assertNotIn('IMG_5805',inspect.getsource(kinetic_hook))
if __name__=='__main__':unittest.main()
