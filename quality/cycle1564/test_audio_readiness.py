import unittest
from audio_readiness import Evidence, review

class AudioReadinessTest(unittest.TestCase):
    def test_silent_aac_is_rejected(self):
        result=review(Evidence(True,False,False,False,True,False))
        self.assertFalse(result["publication_approved"])
        self.assertIn("japanese_speech",result["missing"])
    def test_effects_only_rejected(self):
        self.assertFalse(review(Evidence(True,False,False,False,True,True))["publication_approved"])
    def test_unapproved_rights_rejected(self):
        self.assertFalse(review(Evidence(True,True,True,True,False,True))["publication_approved"])
    def test_verified_evidence_passes_logic_only(self):
        self.assertTrue(review(Evidence(True,True,True,True,True,True))["publication_approved"])
if __name__=="__main__": unittest.main()
