import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'source'))
from mascot_intro import GENRES,PALETTES,SAFE_Y,INTRO_FRAMES,alpha_at,intro_frame,validate
class MascotTests(unittest.TestCase):
 def test_ten_genre_palettes(self):self.assertEqual(set(GENRES),set(PALETTES))
 def test_intro_frames(self):self.assertEqual(INTRO_FRAMES,45)
 def test_direct_cut_no_ghost(self):
  self.assertEqual(alpha_at(0),1)
  self.assertEqual(alpha_at(44),1)
  with self.assertRaises(ValueError):alpha_at(45)
 def test_safe_canvas(self):self.assertEqual(intro_frame(0).size,(1080,SAFE_Y))
 def test_original_art_nonempty(self):
  im=intro_frame(5)
  self.assertNotEqual(im.getpixel((540,700)),im.getpixel((10,10)))
 def test_genre_color_variants(self):
  for genre in GENRES:
   with self.subTest(genre=genre):self.assertEqual(intro_frame(2,genre).size,(1080,SAFE_Y))
 def test_no_transparency_over_ui(self):self.assertEqual(intro_frame(44).getchannel('A').getextrema(),(255,255))
 def test_invalid_frame(self):
  with self.assertRaises(ValueError):intro_frame(45)
 def test_unknown_genre(self):
  with self.assertRaises(ValueError):intro_frame(0,'unlisted')
 def test_fail_closed_other_genre(self):
  with self.assertRaises(ValueError):validate('missing.mp4','bad','beauty',True)
 def test_human_review_required(self):
  with self.assertRaises(ValueError):validate('missing.mp4','bad','ai_work',False)
if __name__=='__main__':unittest.main()
