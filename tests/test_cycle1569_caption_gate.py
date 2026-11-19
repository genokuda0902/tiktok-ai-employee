import unittest
from quality.cycle1569_caption_gate import RenderEvidence, publication_ready

class CaptionGateTests(unittest.TestCase):
    def test_silent_review_rejected(self):
        self.assertFalse(publication_ready(RenderEvidence(True,False,False,True,False)))
    def test_approved_evidence_passes(self):
        self.assertTrue(publication_ready(RenderEvidence(True,True,True,True,True)))

if __name__ == '__main__': unittest.main()
