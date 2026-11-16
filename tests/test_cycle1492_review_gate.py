import unittest
from unittest.mock import patch
from quality.cycle1492_review_gate import inspect

class TestReviewGate(unittest.TestCase):
    @patch("quality.cycle1492_review_gate.Path.is_file", return_value=True)
    @patch("quality.cycle1492_review_gate.subprocess.check_output")
    def test_silent_video_blocked(self, probe, exists):
        probe.return_value = b'{"streams":[{"codec_type":"video","width":720,"height":1280}],"format":{"duration":"12.08"}}'
        result = inspect("review.mp4")
        self.assertFalse(result["audio_present"])
        self.assertFalse(result["posting_allowed"])
        self.assertFalse(result["japanese_narration_verified"])
        self.assertEqual(result["quality_status"], "PUBLICATION_NOT_APPROVED")

    @patch("quality.cycle1492_review_gate.Path.is_file", return_value=True)
    @patch("quality.cycle1492_review_gate.subprocess.check_output")
    def test_audio_track_does_not_prove_japanese(self, probe, exists):
        probe.return_value = b'{"streams":[{"codec_type":"video","width":720,"height":1280},{"codec_type":"audio"}],"format":{"duration":"12"}}'
        result = inspect("review.mp4")
        self.assertTrue(result["audio_present"])
        self.assertFalse(result["japanese_narration_verified"])
        self.assertFalse(result["posting_allowed"])
