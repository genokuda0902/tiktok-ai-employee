import unittest
from quality.cycle1620_gate import publication_ready
class TestGate(unittest.TestCase):
    def test_silent_rejected(self):
        self.assertFalse(publication_ready(dict(video_decode="PASS",width=720,height=1280,audio_present=False)))
    def test_missing_rights_rejected(self):
        self.assertFalse(publication_ready(dict(video_decode="PASS",width=720,height=1280,audio_present=True,speech_synced_captions=True)))
    def test_complete_approved(self):
        self.assertTrue(publication_ready(dict(video_decode="PASS",width=720,height=1280,audio_present=True,speech_synced_captions=True,asset_rights_approved=True,privacy_approved=True,employee_approved=True)))
if __name__=="__main__":unittest.main()
