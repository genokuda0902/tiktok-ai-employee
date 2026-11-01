import unittest
import tempfile
from pathlib import Path
from PIL import Image
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from status_strip_cleanup import (check_bounds,make_patch,GENRES,COPY,FIRST,LAST,X,Y,W,H)

class StripCleanupTest(unittest.TestCase):
 def test_bounds(self): self.assertTrue(check_bounds())
 def test_duration(self): self.assertEqual(LAST-FIRST+1,48)
 def test_safe_zone(self): self.assertLess(Y+H,1340)
 def test_no_new_claims(self): self.assertIn('架空の入力例',COPY)
 def test_ten_genres(self): self.assertEqual(len(GENRES),10)
 def test_genre_palette(self):
  for key,val in GENRES.items():
   self.assertTrue(key and val.startswith('#') and len(val)==7)
 def test_patch_dimensions(self):
  with tempfile.TemporaryDirectory() as t:
   f=make_patch(Path(t)/'p.png')
   with Image.open(f) as im:
    self.assertEqual(im.size,(W,H));self.assertEqual(im.mode,'RGBA')
    self.assertEqual(im.getpixel((W//2,H//2))[3],255)
 def test_bad_genre(self):
  with tempfile.TemporaryDirectory() as t:
   with self.assertRaises(ValueError):make_patch(Path(t)/'p.png','invalid')

if __name__=='__main__': unittest.main()
