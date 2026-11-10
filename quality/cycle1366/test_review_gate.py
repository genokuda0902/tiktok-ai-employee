import unittest
from review_gate import publication_allowed
class ReviewGateTests(unittest.TestCase):
    def test_audio_track_is_not_japanese_narration(self):
        e=dict(width=1080,height=1920,full_decode_ok=True,audio_codec="aac",
               japanese_narration_verified=False,speech_caption_sync_verified=False,asset_rights_verified=True)
        self.assertFalse(publication_allowed(e,True))
    def test_human_approval_required(self):
        e=dict(width=1080,height=1920,full_decode_ok=True,audio_codec="aac",
               japanese_narration_verified=True,speech_caption_sync_verified=True,asset_rights_verified=True)
        self.assertFalse(publication_allowed(e,False))
        self.assertTrue(publication_allowed(e,True))
if __name__=="__main__":unittest.main()
