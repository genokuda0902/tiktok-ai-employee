import unittest
from quality.cycle649.qa import validate_scenes, validate_numeric_proof, can_publish

SCENES=[
(0,1.5,"AIの合計、合ってる？","hook"),
(1.5,4,"元データは4か月","table"),
(4,7,"本物のCalcで確認","table"),
(7,10,"数式はここ","formula"),
(10,13,"合計は650","result"),
(13,16.5,"グラフも検算","chart"),
(16.5,20,"AIの数字は必ず確認","cta"),
]
class TestCycle649(unittest.TestCase):
 def test_timing(self): self.assertTrue(validate_scenes(SCENES))
 def test_numeric_proof(self): self.assertTrue(validate_numeric_proof([120,150,200,180],650,"=SUM(B2:B5)"))
 def test_numeric_mismatch_fails(self):
  with self.assertRaises(AssertionError): validate_numeric_proof([120,150,200,181],650)
 def test_hook_too_long_fails(self):
  with self.assertRaises(AssertionError): validate_scenes([(0,2,"hook","h"),(2,20,"end","e")])
 def test_unapproved_voice_blocks(self):
  self.assertFalse(can_publish({"publication":"APPROVED","employee_approved":True,"asset_rights":"APPROVED","narration":{"status":"MISSING"},"caption_sync":"VERIFIED","privacy_review":"PASSED","auto_post":False}))
 def test_no_auto_post(self):
  self.assertFalse(can_publish({"publication":"APPROVED","employee_approved":True,"asset_rights":"APPROVED","narration":{"status":"APPROVED"},"caption_sync":"VERIFIED","privacy_review":"PASSED","auto_post":True}))
 def test_all_gates(self):
  self.assertTrue(can_publish({"publication":"APPROVED","employee_approved":True,"asset_rights":"APPROVED","narration":{"status":"APPROVED"},"caption_sync":"VERIFIED","privacy_review":"PASSED","auto_post":False}))
if __name__=="__main__": unittest.main()
