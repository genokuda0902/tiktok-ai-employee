import unittest
from cycle776_contract import GENRES,MONTHS,validate,phase
class TestCycle776(unittest.TestCase):
 def test_ten_genres(self): self.assertEqual(len(GENRES),10)
 def test_sales(self): self.assertEqual(sum(MONTHS.values()),650000)
 def test_phases(self):
  self.assertEqual(phase(195),'attach')
  self.assertEqual(phase(230),'type')
  self.assertEqual(phase(272),'send')
  self.assertEqual(phase(298),'processing')
 def test_out_of_range(self):
  with self.assertRaises(ValueError):phase(300)
 def test_reject_auto_publish(self):
  m=dict(supported_genres=list(GENRES),genre=GENRES[0],monthly_sales=MONTHS,total_yen=650000,new_assets='original_vector_only',source_rights='unverified_review_only',audio_rights='unverified_review_only',quality_approved=False,publication_approved=False,review_status='HUMAN_REVIEW',publish_mode='employee_manual_after_approval',performance_claim=None)
  self.assertTrue(validate(m))
  m['publish_mode']='auto_post'
  with self.assertRaises(ValueError):validate(m)
if __name__=='__main__':unittest.main()
