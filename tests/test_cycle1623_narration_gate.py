import unittest
from quality.cycle1623_narration_gate import NarrationEvidence, publication_eligible

class NarrationGateTests(unittest.TestCase):
    def test_tonal_audio_does_not_pass(self):
        self.assertFalse(publication_eligible(NarrationEvidence(True, False, False, True, True)))

    def test_no_approval_fails(self):
        self.assertFalse(publication_eligible(NarrationEvidence(True, True, True, True, False)))

    def test_all_evidence_required(self):
        self.assertTrue(publication_eligible(NarrationEvidence(True, True, True, True, True)))

if __name__ == "__main__":
    unittest.main()
