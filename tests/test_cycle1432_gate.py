import unittest
from quality.cycle1432_gate import VideoEvidence, publication_ready

class QualityGateTests(unittest.TestCase):
    def setUp(self):
        self.good = dict(video_codec="h264", width=1080, height=1920,
            duration_seconds=15.0, audio_codec="aac",
            japanese_narration_verified=True, captions_synced=True,
            assets_approved=True, employee_approved=True, decode_passed=True)
    def test_complete_approval(self):
        self.assertTrue(publication_ready(VideoEvidence(**self.good)))
    def test_sound_effect_is_not_narration(self):
        self.assertFalse(publication_ready(VideoEvidence(**{**self.good, "japanese_narration_verified":False})))
    def test_employee_approval_required(self):
        self.assertFalse(publication_ready(VideoEvidence(**{**self.good, "employee_approved":False})))
    def test_caption_sync_required(self):
        self.assertFalse(publication_ready(VideoEvidence(**{**self.good, "captions_synced":False})))

if __name__ == "__main__":
    unittest.main()
