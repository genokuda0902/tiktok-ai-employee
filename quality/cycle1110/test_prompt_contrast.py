import importlib.util,json,unittest
from pathlib import Path
from tempfile import TemporaryDirectory
P=Path(__file__).parent
spec=importlib.util.spec_from_file_location('contrast',P/'prompt_contrast.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
BASE=json.loads((P/'manifest.json').read_text())
class ContrastTests(unittest.TestCase):
 def test_genres(self):
  for genre in m.GENRES:
   d=dict(BASE,genre=genre);self.assertEqual(m.validate(d),d)
 def test_private_data_rejected(self):
  with self.assertRaises(ValueError):m.validate(dict(BASE,contains_private_data=True))
 def test_rights_gate(self):
  with self.assertRaises(ValueError):m.validate(dict(BASE,rights_status='approved'))
 def test_publication_gate(self):
  with self.assertRaises(ValueError):m.validate(dict(BASE,review_only=False))
 def test_unknown_genre(self):
  with self.assertRaises(ValueError):m.validate(dict(BASE,genre='unknown'))
 def test_extra_field(self):
  with self.assertRaises(ValueError):m.validate(dict(BASE,extra='x'))
 def test_long_text(self):
  with self.assertRaises(ValueError):m.validate(dict(BASE,after='あ'*21))
 def test_newline(self):
  with self.assertRaises(ValueError):m.validate(dict(BASE,after='あ\nい'))
 def test_caption_safe(self):self.assertLess(m.BOX[3],m.CAPTION_START_Y)
 def test_overlay_for_ten_genres(self):
  with TemporaryDirectory() as td:
   for genre in m.GENRES:
    d=dict(BASE,genre=genre)
    for flag in (False,True):
     p=Path(td)/f'{genre}-{flag}.png';m.overlay_image(d,flag,p)
     from PIL import Image
     im=Image.open(p);self.assertEqual(im.size,(1080,1920));self.assertEqual(im.getpixel((100,1400))[3],0)
 def test_sha_reject(self):
  with TemporaryDirectory() as td:
   f=Path(td)/'src';f.write_text('dummy')
   with self.assertRaises(ValueError):m.render(f,Path(td)/'out','bad',BASE)
if __name__=='__main__':unittest.main()
