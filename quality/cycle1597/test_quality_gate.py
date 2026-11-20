import unittest
from unittest.mock import patch
from quality_gate import inspect

class GateTests(unittest.TestCase):
    @patch("subprocess.check_output")
    def test_silent_video_rejected(self, probe):
        probe.return_value = '{"streams":[{"codec_type":"video","width":720,"height":1280}],"format":{"duration":"15.0"}}'
        result = inspect("review.mp4")
        self.assertFalse(result["publishable"])
        self.assertIn("missing_japanese_narration", result["reasons"])

    @patch("subprocess.check_output")
    def test_audio_does_not_imply_approval(self, probe):
        probe.return_value = '{"streams":[{"codec_type":"video","width":720,"height":1280},{"codec_type":"audio"}],"format":{"duration":"15.0"}}'
        result = inspect("review.mp4")
        self.assertFalse(result["publishable"])
        self.assertIn("speech_language_unverified", result["reasons"])

if __name__ == "__main__":
    unittest.main()
