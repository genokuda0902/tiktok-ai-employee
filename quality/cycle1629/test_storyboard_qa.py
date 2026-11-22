import unittest
from quality.cycle1629.storyboard_qa import ReviewEvidence, assess

class StoryboardQATest(unittest.TestCase):
    def sample(self, **kwargs):
        fields = dict(width=1080, height=1920, duration_seconds=12,
                      scene_count=4, audio_stream_present=True,
                      japanese_speech_verified=True,
                      captions_synced_verified=True, assets_approved=True,
                      employee_approved=True)
        fields.update(kwargs)
        return ReviewEvidence(**fields)

    def test_tone_is_not_speech(self):
        result = assess(self.sample(japanese_speech_verified=False))
        self.assertFalse(result["publication_approved"])

    def test_no_audio_is_rejected(self):
        self.assertIn("audio_missing", assess(self.sample(audio_stream_present=False))["failures"])

    def test_review_only_720p_is_rejected(self):
        self.assertIn("target_resolution_not_met", assess(self.sample(width=720, height=1280))["failures"])

    def test_approval_is_required(self):
        self.assertFalse(assess(self.sample(employee_approved=False))["publication_approved"])

if __name__ == "__main__":
    unittest.main()
