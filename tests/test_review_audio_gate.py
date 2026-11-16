import unittest
from unittest.mock import patch, MagicMock
from tools.review_audio_gate import inspect

class GateTests(unittest.TestCase):
    @patch("tools.review_audio_gate.subprocess.run")
    @patch("tools.review_audio_gate.Path.is_file", return_value=True)
    def test_silent_video_fails_closed(self, exists, run):
        run.side_effect = [MagicMock(stdout='{"streams":[{"codec_type":"video","width":720,"height":1280}]}'), MagicMock(returncode=0)]
        result=inspect("review.mp4")
        self.assertTrue(result["decoded"])
        self.assertFalse(result["audio"])
        self.assertFalse(result["publication_approved"])

    @patch("tools.review_audio_gate.subprocess.run")
    @patch("tools.review_audio_gate.Path.is_file", return_value=True)
    def test_audio_presence_not_narration_proof(self, exists, run):
        run.side_effect = [MagicMock(stdout='{"streams":[{"codec_type":"video"},{"codec_type":"audio"}]}'), MagicMock(returncode=0)]
        result=inspect("review.mp4")
        self.assertTrue(result["audio"])
        self.assertFalse(result["japanese_narration_verified"])
        self.assertFalse(result["publication_approved"])

if __name__ == "__main__":
    unittest.main()
