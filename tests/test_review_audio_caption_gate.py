import unittest
from src.review_audio_caption_gate import Caption, validate_review

class GateTests(unittest.TestCase):
    def test_unverified_fails_closed(self):
        result = validate_review(20, [Caption(1, 3, "確認")])
        self.assertFalse(result["approved"])
        self.assertIn("japanese_speech_not_verified", result["issues"])

    def test_overlapping_captions_fail(self):
        result = validate_review(20, [Caption(1, 4, "前"), Caption(3, 5, "後")], audio_verified=True, japanese_speech_verified=True, rights_approved=True)
        self.assertIn("invalid_caption_timing", result["issues"])

    def test_verified_passes(self):
        result = validate_review(20, [Caption(1, 3, "確認")], audio_verified=True, japanese_speech_verified=True, rights_approved=True)
        self.assertTrue(result["approved"])

if __name__ == "__main__": unittest.main()
