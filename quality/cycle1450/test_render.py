import unittest
from quality.cycle1450.render import publication_approved
class QualityGateTest(unittest.TestCase):
    def test_empty_fails(self): self.assertFalse(publication_approved({}))
    def test_audio_missing_fails(self):
        self.assertFalse(publication_approved(dict(rights_approved=True,privacy_approved=True,speech_caption_sync_verified=True,employee_approved=True)))
    def test_explicit_approvals_pass_gate(self):
        self.assertTrue(publication_approved(dict.fromkeys(("rights_approved","privacy_approved","japanese_voice_verified","speech_caption_sync_verified","employee_approved"),True)))
if __name__=="__main__":unittest.main()
