import unittest
from cycle662_evidence_gate import first_stable_evidence, claim_visible, release_allowed

class GateTests(unittest.TestCase):
    def test_claim_waits_for_proof(self):
        onset=first_stable_evidence([False,False,True,True,True])
        self.assertEqual(onset,2)
        self.assertFalse(claim_visible(1,onset,True))
        self.assertTrue(claim_visible(2,onset,True))
    def test_missing_proof_is_rejected(self):
        with self.assertRaises(ValueError):
            first_stable_evidence([False,True,False])
    def test_not_approved(self):
        self.assertFalse(release_allowed(narration_verified=False,
            rights_approved=False,human_approved=False,subtitle_sync_verified=False))

if __name__=="__main__": unittest.main()
