import unittest
from speech_evidence import publication_ready, review_evidence

class GateTest(unittest.TestCase):
    def test_tone_is_not_narration(self):
        result = review_evidence(video_codec="h264", width=1080, height=1920, audio_codec="aac")
        self.assertTrue(result["audio_stream_present"])
        self.assertFalse(result["japanese_narration_verified"])
        self.assertFalse(result["publication_approved"])
    def test_approval_fails_closed(self):
        self.assertFalse(publication_ready(has_audio_stream=True, verified_japanese_speech=False, captions_speech_aligned=False, rights_approved=True, employee_approved=False))
    def test_only_all_evidence_passes(self):
        self.assertTrue(publication_ready(has_audio_stream=True, verified_japanese_speech=True, captions_speech_aligned=True, rights_approved=True, employee_approved=True))

if __name__ == "__main__":
    unittest.main()
