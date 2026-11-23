import unittest
from unittest.mock import patch
import json
from quality.audio_failclosed import inspect

class TestAudioGate(unittest.TestCase):
    @patch("subprocess.check_output")
    def test_missing_audio_is_rejected(self, mock):
        mock.return_value=json.dumps({"streams":[{"codec_type":"video","width":1080,"height":1920}]}).encode()
        self.assertIn("missing narration audio stream",inspect("review.mp4"))
    @patch("subprocess.check_output")
    def test_wrong_dimensions_are_rejected(self, mock):
        mock.return_value=json.dumps({"streams":[{"codec_type":"video","width":720,"height":1280},{"codec_type":"audio"}]}).encode()
        self.assertIn("expected 1080x1920 video",inspect("review.mp4"))
