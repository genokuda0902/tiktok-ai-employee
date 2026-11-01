import importlib.util, json, unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from PIL import Image
P=Path(__file__).parent
spec=importlib.util.spec_from_file_location('verifycut',P/'row_verification_cut.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
BASE=json.loads((P/'manifest.json').read_text(encoding='utf8'))
class VerifyCutTests(unittest.TestCase):
 def test_all_ten_genres(self):
  for genre in m.GENRES:self.assertEqual(m.validate(dict(BASE,genre=genre))['genre'],genre)
 def test_bad_math(self):
  with self.assertRaisesRegex(ValueError,'false arithmetic'):m.validate(dict(BASE,expected_total=21))
 def test_private(self):
  with self.assertRaises(ValueError):m.validate(dict(BASE,contains_private_data=True))
 def test_rights(self):
  with self.assertRaises(ValueError):m.validate(dict(BASE,rights_status='approved'))
 def test_publication(self):
  with self.assertRaises(ValueError):m.validate(dict(BASE,review_only=False))
 def test_not_synthetic(self):
  with self.assertRaises(ValueError):m.validate(dict(BASE,synthetic_scenario=False))
 def test_unknown_genre(self):
  with self.assertRaises(ValueError):m.validate(dict(BASE,genre='fake'))
 def test_extra_key(self):
  with self.assertRaises(ValueError):m.validate(dict(BASE,unused=1))
 def test_invalid_bool_number(self):
  with self.assertRaises(ValueError):m.validate(dict(BASE,input_a=True))
 def test_negative_number(self):
  with self.assertRaises(ValueError):m.validate(dict(BASE,input_a=-1))
 def test_label_newline(self):
  with self.assertRaises(ValueError):m.validate(dict(BASE,label='4月\n'))
 def test_bad_stage(self):
  with TemporaryDirectory() as td:
   with self.assertRaises(ValueError):m.image_for(BASE,3,Path(td)/'bad.png')
 def test_images_caption_safe_for_all_genres(self):
  with TemporaryDirectory() as td:
   for genre in m.GENRES:
    for stage in (1,2):
     path=Path(td)/f'{genre}-{stage}.png'
     m.image_for(dict(BASE,genre=genre),stage,path)
     im=Image.open(path)
     self.assertEqual(im.size,(1080,1920))
     self.assertEqual(im.getpixel((540,1300))[3],0)
     self.assertGreaterEqual(im.getpixel((540,900))[3],250)
 def test_sha_rejected(self):
  with TemporaryDirectory() as td:
   path=Path(td)/'dummy';path.write_bytes(b'x')
   with self.assertRaisesRegex(ValueError,'SHA'):m.render(path,Path(td)/'out','invalid',BASE)
 def test_timeline_is_caption_safe(self):self.assertLess(1025,m.SAFE_BOTTOM)
if __name__=='__main__':unittest.main()
