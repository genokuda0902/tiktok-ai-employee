import unittest
from quality_contract import sumif_proof
ROWS=[{'id':'R1','team':'A','value':12},{'id':'R3','team':'A','value':9},{'id':'R5','team':'A','value':14}]
class TestProof(unittest.TestCase):
    def test_total(self): self.assertTrue(sumif_proof(ROWS))
    def test_wrong_total(self):
        with self.assertRaises(ValueError): sumif_proof(ROWS,displayed=34)
    def test_wrong_ids(self):
        with self.assertRaises(ValueError): sumif_proof(ROWS,evidence_ids=('R1','R2','R5'))
