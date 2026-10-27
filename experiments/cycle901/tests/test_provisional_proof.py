import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from provisional_proof import GENRES,STATUS,POLICY,START,END,sum_evidence,validate_proof,validate_layout
class TestProvisionalProof(unittest.TestCase):
 def test_genres(self):self.assertEqual(len(GENRES),10);self.assertEqual(len(set(GENRES)),10)
 def test_layout(self):self.assertTrue(validate_layout());self.assertGreater(END,START)
 def test_before(self):self.assertEqual(sum_evidence([(12,8),(16,9),(17,11)]),(45,28))
 def test_after(self):self.assertEqual(sum_evidence([(12,8),(16,9),(18,12)]),(46,29))
 def test_empty(self):
  with self.assertRaises(ValueError):sum_evidence([])
 def test_negative(self):
  with self.assertRaises(ValueError):sum_evidence([(1,-1)])
 def test_float(self):
  with self.assertRaises(ValueError):sum_evidence([(1.0,1)])
 def test_ten_genres_fail_closed(self):
  for g in GENRES:self.assertFalse(validate_proof(genre=g,state='provisional',displayed=(45,28),source=(46,29))['publication_approved'])
 def test_unverified_claim(self):
  with self.assertRaises(ValueError):validate_proof(genre='ai_work',state='verified',displayed=(45,28),source=(46,29))
 def test_matching_verified_requires_review(self):self.assertTrue(validate_proof(genre='ai_work',state='verified',displayed=(46,29),source=(46,29))['human_review_required'])
 def test_private(self):
  with self.assertRaises(ValueError):validate_proof(genre='ai_work',state='provisional',displayed=(45,28),contains_private_data=True)
 def test_approved(self):
  with self.assertRaises(ValueError):validate_proof(genre='ai_work',state='provisional',displayed=(45,28),approved=True)
 def test_unknown(self):
  with self.assertRaises(ValueError):validate_proof(genre='unknown',state='provisional',displayed=(45,28))
 def test_policy(self):self.assertIn('NOT_APPROVED',POLICY);self.assertIn('provisional',STATUS)
if __name__=='__main__':unittest.main()
