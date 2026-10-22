import copy,sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from chart_contract import GENRES,MONTHS,validate,phase,START,END
BASE={"supported_genres":list(GENRES),"genre":"AI・仕事効率化","monthly_sales":MONTHS,"total_yen":650000,"new_assets":"original_vector_only","source_rights":"unverified_review_only","audio_rights":"unverified_review_only","review_status":"HUMAN_REVIEW","quality_approved":False,"publication_approved":False,"publish_mode":"employee_manual_after_approval","performance_claim":None}
class ContractTest(unittest.TestCase):
 def test_ten_genres(self):
  self.assertEqual(len(GENRES),10)
  for g in GENRES:
   m=dict(BASE,genre=g);self.assertTrue(validate(m))
 def test_numbers(self):self.assertEqual(sum(MONTHS.values()),650000)
 def test_invalid_number(self):
  with self.assertRaises(ValueError):validate(dict(BASE,total_yen=650001))
 def test_rights(self):
  with self.assertRaises(ValueError):validate(dict(BASE,audio_rights="approved"))
 def test_publication(self):
  with self.assertRaises(ValueError):validate(dict(BASE,publication_approved=True))
 def test_assets(self):
  with self.assertRaises(ValueError):validate(dict(BASE,new_assets="external"))
 def test_claim(self):
  with self.assertRaises(ValueError):validate(dict(BASE,performance_claim="10分→1分"))
 def test_phase(self):
  self.assertEqual(phase(START),"paste");self.assertEqual(phase(START+20),"chart");self.assertEqual(phase(END-1),"verify")
 def test_boundary(self):
  with self.assertRaises(ValueError):phase(END)
if __name__=="__main__":unittest.main()
