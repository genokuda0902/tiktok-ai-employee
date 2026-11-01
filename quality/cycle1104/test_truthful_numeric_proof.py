import copy
import tempfile
import unittest
from pathlib import Path
from PIL import Image
from truthful_numeric_proof import GENRES,PALETTES,SAFE_Y,CARDS,make_overlay,validate

M={'genre':'ai_work','synthetic_scenario':True,'review_only':True,'rights_status':'unverified',
   'contains_private_data':False,'proof':{'labels':['営業A','営業B'],'operands':[46,29],'total':75}}
class NumericProofTest(unittest.TestCase):
 def test_all_genres_are_supported(self):
  self.assertEqual(set(GENRES),set(PALETTES))
  for genre in GENRES:
   m=copy.deepcopy(M);m['genre']=genre;self.assertEqual(validate(m)['total'],75)
 def test_wrong_sum_rejected(self):
  m=copy.deepcopy(M);m['proof']['total']=76
  with self.assertRaisesRegex(ValueError,'inconsistent'):validate(m)
 def test_negative_operand_rejected(self):
  m=copy.deepcopy(M);m['proof']['operands'][0]=-1
  with self.assertRaises(ValueError):validate(m)
 def test_bool_operand_rejected(self):
  m=copy.deepcopy(M);m['proof']['operands'][0]=True
  with self.assertRaises(ValueError):validate(m)
 def test_private_data_rejected(self):
  m=copy.deepcopy(M);m['contains_private_data']=True
  with self.assertRaises(ValueError):validate(m)
 def test_publication_rejected(self):
  m=copy.deepcopy(M);m['review_only']=False
  with self.assertRaises(ValueError):validate(m)
 def test_unknown_fields_rejected(self):
  m=copy.deepcopy(M);m['personal_name']='test'
  with self.assertRaises(ValueError):validate(m)
 def test_missing_rights_field_rejected(self):
  m=copy.deepcopy(M);del m['rights_status']
  with self.assertRaises(ValueError):validate(m)
 def test_caption_safe(self):
  self.assertTrue(all(y2<SAFE_Y for x1,y1,x2,y2 in CARDS))
 def test_overlay_alpha_is_confined_to_cards(self):
  with tempfile.TemporaryDirectory() as td:
   p=Path(td)/'a.png';make_overlay(M,True,p)
   im=Image.open(p).convert('RGBA');self.assertEqual(im.size,(1080,1920))
   self.assertEqual(im.getpixel((500,1500))[3],0)
   self.assertGreater(im.getpixel((450,900))[3],0)
 def test_pending_and_final_differ(self):
  with tempfile.TemporaryDirectory() as td:
   p1=Path(td)/'a.png';p2=Path(td)/'b.png';make_overlay(M,False,p1);make_overlay(M,True,p2)
   self.assertNotEqual(p1.read_bytes(),p2.read_bytes())
 def test_all_genres_render_without_confidential_assets(self):
  with tempfile.TemporaryDirectory() as td:
   for g in GENRES:
    m=copy.deepcopy(M);m['genre']=g
    make_overlay(m,True,Path(td)/(g+'.png'))
    self.assertTrue((Path(td)/(g+'.png')).is_file())
if __name__=='__main__':unittest.main()
