import unittest
from review_gate import ReviewEvidence, may_publish, publication_issues

class ReviewGateTests(unittest.TestCase):
    def test_missing_audio_blocks(self):
        e = ReviewEvidence(True, False, True, True, True, True, True)
        self.assertFalse(may_publish(e))
        self.assertIn("japanese_voice_verified", publication_issues(e))
    def test_missing_rights_blocks(self):
        self.assertFalse(may_publish(ReviewEvidence(True, True, True, True, False, True, True)))
    def test_all_evidence_allows_manual_review(self):
        self.assertTrue(may_publish(ReviewEvidence(True, True, True, True, True, True, True)))

if __name__ == "__main__":
    unittest.main()
