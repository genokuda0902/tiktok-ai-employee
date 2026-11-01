import copy, tempfile, unittest
from pathlib import Path
from PIL import Image
from hook_clarity import GENRES, ACCENTS, SAFE, CAPTION_START_Y, make_overlay, validate
M={'genre':'ai_work','review_only':True,'rights_status':'unverified','contains_private_data':False,
   'synthetic_scenario':True,'headline':['その集計、','まだ手作業？'],'next_step':'最初は、作業を3つ書き出そう'}
class HookTest(unittest.TestCase):
 def test_genre_config(self):
  self.assertEqual(set(GENRES),set(ACCENTS))
  for genre in GENRES:
   m=copy.deepcopy(M);m['genre']=genre;validate(m)
 def test_private_data_gate(self):
  m=copy.deepcopy(M);m['contains_private_data']=True
  with self.assertRaises(ValueError):validate(m)
 def test_release_gate(self):
  m=copy.deepcopy(M);m['review_only']=False
  with self.assertRaises(ValueError):validate(m)
 def test_rights_gate(self):
  m=copy.deepcopy(M);m['rights_status']='approved'
  with self.assertRaises(ValueError):validate(m)
 def test_unknown_keys_gate(self):
  m=copy.deepcopy(M);m['external_asset']='url'
  with self.assertRaises(ValueError):validate(m)
 def test_no_caption_collision(self):self.assertLess(SAFE[3],CAPTION_START_Y)
 def test_overlay_alpha_and_stages(self):
  with tempfile.TemporaryDirectory() as td:
   a=Path(td)/'a.png';b=Path(td)/'b.png'
   make_overlay(M,False,a);make_overlay(M,True,b)
   im=Image.open(b).convert('RGBA')
   self.assertEqual(im.size,(1080,1920))
   self.assertEqual(im.getpixel((400,1450))[3],0)
   self.assertGreater(im.getpixel((200,200))[3],0)
   self.assertNotEqual(a.read_bytes(),b.read_bytes())
 def test_all_ten_genres_render(self):
  with tempfile.TemporaryDirectory() as td:
   for genre in GENRES:
    m=copy.deepcopy(M);m['genre']=genre
    make_overlay(m,True,Path(td)/(genre+'.png'))
    self.assertTrue((Path(td)/(genre+'.png')).exists())
if __name__=='__main__':unittest.main()
