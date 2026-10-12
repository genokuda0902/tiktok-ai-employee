import json, unittest
from pathlib import Path
from proof_close import GENRES, validate, ease, scene
CFG=json.loads((Path(__file__).parent/'config.json').read_text(encoding='utf-8'))
class ProofCloseTest(unittest.TestCase):
 def test_ten_genres(self):
  self.assertEqual(len(GENRES),10)
  for g in GENRES:validate(dict(CFG,genre=g))
 def test_validation(self):validate(CFG)
 def test_privacy_fail_closed(self):
  with self.assertRaises(ValueError):validate(dict(CFG,contains_private_data=True))
 def test_rights_fail_closed(self):
  with self.assertRaises(ValueError):validate(dict(CFG,rights='UNKNOWN'))
 def test_publish_fail_closed(self):
  with self.assertRaises(ValueError):validate(dict(CFG,publication='APPROVED'))
 def test_real_claim_fail_closed(self):
  with self.assertRaises(ValueError):validate(dict(CFG,claims_real_results=True))
 def test_values_validation(self):
  for vals in ([1,2,3],[-1,2,3,4],[True,2,3,4],[1,2,3,10000]):
   with self.assertRaises(ValueError):validate(dict(CFG,values=vals))
 def test_labels_validation(self):
  with self.assertRaises(ValueError):validate(dict(CFG,labels=['1月','2月','3月']))
 def test_title_validation(self):
  with self.assertRaises(ValueError):validate(dict(CFG,verification_title='x'*20))
 def test_easing(self):
  self.assertEqual(ease(-1),0);self.assertEqual(ease(2),1);self.assertLess(ease(.3),ease(.8))
 def test_visual_frames(self):
  a=scene(.3,CFG);b=scene(1.4,CFG)
  self.assertEqual(a.size,(1080,1920));self.assertNotEqual(a.tobytes(),b.tobytes())
 def test_total_is_720(self):self.assertEqual(sum(CFG['values']),720)
if __name__=='__main__':unittest.main()
