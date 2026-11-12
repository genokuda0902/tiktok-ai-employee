import unittest
from quality.cycle1408_evidence_gate import evaluate

class EvidenceGateTest(unittest.TestCase):
    def test_silent_aac_does_not_pass(self):
        result=evaluate(dict(width=1080,height=1920,full_decode_pass=True,audio_codec="aac",asset_rights_approved=True,employee_approved=True))
        self.assertFalse(result["publication_approved"])
        self.assertIn("japanese_speech_unverified",result["reasons"])
    def test_fully_verified_passes(self):
        self.assertTrue(evaluate(dict(width=1080,height=1920,full_decode_pass=True,japanese_speech_verified=True,speech_caption_sync_verified=True,asset_rights_approved=True,employee_approved=True))["publication_approved"])
    def test_employee_approval_required(self):
        self.assertIn("employee_unapproved",evaluate({})["reasons"])
if __name__=="__main__": unittest.main()
