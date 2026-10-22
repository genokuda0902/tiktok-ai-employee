import unittest
from proof_contract import GENRES,VALUES,verify
class ProofContractTests(unittest.TestCase):
    def test_ten_genres(self):
        self.assertEqual(len(GENRES),10)
        for genre in GENRES:
            self.assertTrue(verify(genre,VALUES,"HUMAN_REVIEW",False,"employee_manual_after_approval","synthetic_arithmetic_only"))
    def test_fail_closed(self):
        good=(GENRES[0],VALUES,"HUMAN_REVIEW",False,"employee_manual_after_approval","synthetic_arithmetic_only")
        for i,bad in enumerate(("other",[1,2,3,4],"APPROVED",True,"auto","AI_saved_10min")):
            args=list(good);args[i]=bad
            with self.assertRaises(ValueError):verify(*args)
if __name__=="__main__":unittest.main()
