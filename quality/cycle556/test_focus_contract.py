import unittest
from focus_contract import GENRES,STAGES,validate,stage_at,readiness
class TestFocusContract(unittest.TestCase):
    def test_ten_genres(self):
        for genre in GENRES: self.assertTrue(validate(genre=genre))
    def test_wrong_total(self):
        with self.assertRaises(ValueError): validate(total=721)
    def test_wrong_formula(self):
        with self.assertRaises(ValueError): validate(formula="=SUM(C2:C5)")
    def test_negative(self):
        with self.assertRaises(ValueError): validate(values=(120,-1,200,250),total=569)
    def test_stages(self): self.assertEqual([stage_at(x) for x in (0,.94,.95,2.04,2.05,2.99)],[0,0,1,1,2,2])
    def test_no_gaps(self):
        for a,b in zip(STAGES,STAGES[1:]): self.assertEqual(a[1],b[0])
    def test_voice_gate(self): self.assertEqual(readiness()["publication"],"NOT_APPROVED")
if __name__=="__main__": unittest.main()
