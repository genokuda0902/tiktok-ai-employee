import unittest
from proof_contract import GENRES,validate,ease,heights
C={"genre":"AI・仕事効率化","rights":"SYNTHETIC_OR_OWNER_APPROVED","contains_private_data":False,"review_status":"HUMAN_REVIEW","publication":"NOT_APPROVED","claims_real_results":False,"hook":"Excel集計、まだ手入力？","labels":["1月","2月","3月","4月"],"values":[120,150,200,250]}
class QualityTests(unittest.TestCase):
 def test_ten_genres(self):
  self.assertEqual(len(GENRES),10)
  for genre in GENRES:validate(dict(C,genre=genre))
 def test_review_gate(self):
  for field,value in [("rights","UNKNOWN"),("contains_private_data",True),("publication","APPROVED"),("claims_real_results",True)]:
   with self.subTest(field=field),self.assertRaises(ValueError):validate(dict(C,**{field:value}))
 def test_bad_values(self):
  for vals in [[1,-2,3,4],[1,2,3],[1,2,3,"4"]]:
   with self.assertRaises(ValueError):validate(dict(C,values=vals))
 def test_motion(self):
  self.assertEqual(ease(0),0)
  self.assertEqual(ease(1),1)
  self.assertNotEqual(heights(C,.2),heights(C,1.3))
 def test_hook_length(self):
  with self.assertRaises(ValueError):validate(dict(C,hook="x"*17))
if __name__=="__main__":unittest.main()
