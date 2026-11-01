import sys, unittest, tempfile
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from action_ladder import GENRE_PALETTE,validate_overlay,make_step_card
from PIL import Image

class BadgeTests(unittest.TestCase):
 def test_ten_genres(self): self.assertEqual(len(GENRE_PALETTE),10)
 def test_safe(self): self.assertTrue(validate_overlay(760,155,290,72,1080,1920,1350))
 def test_caption_collision(self):
  with self.assertRaises(ValueError): validate_overlay(760,1310,290,72,1080,1920,1350)
 def test_outside(self):
  with self.assertRaises(ValueError): validate_overlay(1000,1000,290,72,1080,1920,1350)
 def test_invalid_genre(self):
  with self.assertRaises(ValueError): make_step_card('/tmp/no.png',genre='unknown')
 def test_all_genre_pngs(self):
  with tempfile.TemporaryDirectory() as d:
   for genre in GENRE_PALETTE:
    path=Path(d)/(genre+'.png')
    make_step_card(path,genre)
    with Image.open(path) as im:
     self.assertEqual(im.size,(290,72))
     self.assertEqual(im.mode,'RGBA')
     self.assertEqual(im.getpixel((0,0))[3],0)
     self.assertGreater(im.getpixel((30,30))[3],0)

if __name__=='__main__': unittest.main()
