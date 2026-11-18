import unittest
from src.review_media_gate import publication_allowed

class TestGate(unittest.TestCase):
    def test_audio_track_not_speech(self):
        self.assertFalse(publication_allowed({"video_ok": True, "audio_stream_present": True}))
    def test_missing_approval_blocks(self):
        r = dict.fromkeys(("video_ok", "audio_stream_present", "japanese_narration_verified", "caption_sync_verified", "asset_rights_approved", "employee_approved"), True)
        r["employee_approved"] = False
        self.assertFalse(publication_allowed(r))
    def test_all_verified(self):
        r = dict.fromkeys(("video_ok", "audio_stream_present", "japanese_narration_verified", "caption_sync_verified", "asset_rights_approved", "employee_approved"), True)
        self.assertTrue(publication_allowed(r))

if __name__ == "__main__": unittest.main()
