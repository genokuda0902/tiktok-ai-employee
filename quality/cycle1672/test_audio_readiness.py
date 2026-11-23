import unittest
from quality.cycle1672.audio_readiness import publication_allowed

class AudioReadinessTest(unittest.TestCase):
    def test_silent_video_blocked(self):
        self.assertFalse(publication_allowed({"video_present": True, "audio_present": False}))
    def test_audio_only_is_not_japanese_speech(self):
        self.assertFalse(publication_allowed({"video_present": True, "audio_present": True}))
    def test_explicit_complete_evidence(self):
        self.assertTrue(publication_allowed(dict.fromkeys(("video_present", "audio_present", "japanese_speech_verified", "speech_synced_captions_verified", "asset_rights_approved", "employee_approved"), True)))

if __name__ == "__main__":
    unittest.main()
