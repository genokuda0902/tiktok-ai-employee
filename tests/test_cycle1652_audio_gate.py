import unittest
from quality.cycle1652_audio_gate import can_post

class TestGate(unittest.TestCase):
    def test_no_audio_rejected(self):
        self.assertFalse(can_post({"video_present":True,"audio_present":False,"japanese_speech_verified":False,"caption_sync_verified":False,"quality_approved":False,"posting_allowed":False}))
    def test_audio_only_is_not_speech_proof(self):
        self.assertFalse(can_post({"video_present":True,"audio_present":True,"japanese_speech_verified":False,"caption_sync_verified":True,"quality_approved":True,"posting_allowed":True}))
    def test_all_verified_required(self):
        self.assertTrue(can_post(dict.fromkeys(("video_present","audio_present","japanese_speech_verified","caption_sync_verified","quality_approved","posting_allowed"),True)))
if __name__=="__main__": unittest.main()
