import unittest
from quality.cycle1587_evidence import Evidence, publication_approved

class EvidenceTest(unittest.TestCase):
    def test_review_only_is_rejected(self):
        self.assertFalse(publication_approved(Evidence(True,False,False,True,False)))
    def test_audio_alone_is_insufficient(self):
        self.assertFalse(publication_approved(Evidence(True,True,False,True,True)))
    def test_all_proofs_required(self):
        self.assertTrue(publication_approved(Evidence(True,True,True,True,True)))
if __name__ == "__main__":
    unittest.main()
