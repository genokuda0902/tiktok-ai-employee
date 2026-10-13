import copy,unittest
from contrast_scene import GENRES,scene,validate,ease,W,H
CFG={'genre':GENRES[0],'rights':'SYNTHETIC_OR_OWNER_APPROVED','contains_private_data':False,'review_status':'HUMAN_REVIEW','publication':'NOT_APPROVED','claims_real_results':False,'before':'手作業で集計','after':'AIで補助','action':'入力して検算'}
class TestContrast(unittest.TestCase):
 def test_all_ten_genres(self):
  for g in GENRES:
   c=copy.deepcopy(CFG);c['genre']=g;self.assertTrue(validate(c))
 def test_dimensions(self):self.assertEqual(scene(.5,CFG).size,(W,H))
 def test_visual_progress(self):self.assertNotEqual(scene(.0,CFG).tobytes(),scene(1.8,CFG).tobytes())
 def test_no_private(self):
  c=copy.deepcopy(CFG);c['contains_private_data']=True
  with self.assertRaises(ValueError):validate(c)
 def test_no_unauthorized_rights(self):
  c=copy.deepcopy(CFG);c['rights']='UNKNOWN'
  with self.assertRaises(ValueError):validate(c)
 def test_no_publication(self):
  c=copy.deepcopy(CFG);c['publication']='APPROVED'
  with self.assertRaises(ValueError):validate(c)
 def test_no_claims(self):
  c=copy.deepcopy(CFG);c['claims_real_results']=True
  with self.assertRaises(ValueError):validate(c)
 def test_reject_long_text(self):
  c=copy.deepcopy(CFG);c['after']='長'*19
  with self.assertRaises(ValueError):validate(c)
 def test_reject_newlines(self):
  c=copy.deepcopy(CFG);c['before']='before\nafter'
  with self.assertRaises(ValueError):validate(c)
 def test_reject_unsupported_genre(self):
  c=copy.deepcopy(CFG);c['genre']='other'
  with self.assertRaises(ValueError):validate(c)
 def test_easing_bounds(self):self.assertEqual(ease(-1),0);self.assertEqual(ease(2),1)
if __name__=='__main__':unittest.main()
