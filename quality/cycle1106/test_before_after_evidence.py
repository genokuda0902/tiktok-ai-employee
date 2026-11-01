import copy
import tempfile
import unittest
from pathlib import Path
from PIL import Image
from before_after_evidence import GENRES, PALETTES, CAPTION_START_Y, RIBBON, make_overlay, validate

M={'genre':'ai_work','synthetic_scenario':True,'review_only':True,'rights_status':'unverified',
   'contains_private_data':False,'proof':{'operands':[46,29],'total':75},
   'labels':{'before':'BEFORE / 検算前','after':'AFTER / 検算後','pending':'合計は要確認',
             'note':'架空データの計算確認のみ・元データの正確性は別確認'}}
class EvidenceTest(unittest.TestCase):
 def test_genres(self):
  self.assertEqual(set(GENRES),set(PALETTES))
  for genre in GENRES:
   m=copy.deepcopy(M);m['genre']=genre
   self.assertEqual(validate(m)['total'],75)
 def test_wrong_total_rejected(self):
  m=copy.deepcopy(M);m['proof']['total']=74
  with self.assertRaisesRegex(ValueError,'arithmetic'):validate(m)
 def test_bool_operand_rejected(self):
  m=copy.deepcopy(M);m['proof']['operands'][0]=True
  with self.assertRaises(ValueError):validate(m)
 def test_negative_operand_rejected(self):
  m=copy.deepcopy(M);m['proof']['operands'][0]=-1
  with self.assertRaises(ValueError):validate(m)
 def test_private_data_rejected(self):
  m=copy.deepcopy(M);m['contains_private_data']=True
  with self.assertRaises(ValueError):validate(m)
 def test_unapproved_release_rejected(self):
  m=copy.deepcopy(M);m['review_only']=False
  with self.assertRaises(ValueError):validate(m)
 def test_unknown_field_rejected(self):
  m=copy.deepcopy(M);m['employee']='X'
  with self.assertRaises(ValueError):validate(m)
 def test_no_caption_overlap(self):
  self.assertLess(RIBBON[3],CAPTION_START_Y)
 def test_render_alpha_and_before_after_difference(self):
  with tempfile.TemporaryDirectory() as td:
   a=Path(td)/'a.png';b=Path(td)/'b.png'
   make_overlay(M,False,a);make_overlay(M,True,b)
   im=Image.open(b).convert('RGBA')
   self.assertEqual(im.size,(1080,1920))
   self.assertEqual(im.getpixel((300,1400))[3],0)
   self.assertGreater(im.getpixel((600,1120))[3],0)
   self.assertNotEqual(a.read_bytes(),b.read_bytes())
 def test_all_genres_render(self):
  with tempfile.TemporaryDirectory() as td:
   for genre in GENRES:
    m=copy.deepcopy(M);m['genre']=genre
    make_overlay(m,True,Path(td)/(genre+'.png'))
    self.assertTrue((Path(td)/(genre+'.png')).exists())
if __name__=='__main__':unittest.main()
