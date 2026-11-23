import unittest
from quality.cycle1656_audio_gate import publication_allowed
class Tests(unittest.TestCase):
    def setUp(self):
        self.q=dict(width=1080,height=1920,audio_streams=1,japanese_speech_verified=True,caption_speech_sync_verified=True,asset_rights_approved=True,employee_approved=True)
    def test_valid(self): self.assertTrue(publication_allowed(self.q))
    def test_silent(self): self.q["audio_streams"]=0; self.assertFalse(publication_allowed(self.q))
    def test_unverified_language(self): self.q["japanese_speech_verified"]=False; self.assertFalse(publication_allowed(self.q))
    def test_unapproved(self): self.q["employee_approved"]=False; self.assertFalse(publication_allowed(self.q))
if __name__=="__main__": unittest.main()
