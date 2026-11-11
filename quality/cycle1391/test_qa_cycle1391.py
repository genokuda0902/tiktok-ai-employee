import unittest
from unittest.mock import patch
from qa_cycle1391 import evaluate

class QualityGateTests(unittest.TestCase):
    @patch("qa_cycle1391.probe")
    def test_silent_video_fails(self, mock_probe):
        mock_probe.return_value = {"streams":[{"codec_type":"video","width":1080,"height":1920}]}
        self.assertEqual(evaluate("dummy.mp4")["issues"], ["missing_narration"])
    @patch("qa_cycle1391.probe")
    def test_low_resolution_fails(self, mock_probe):
        mock_probe.return_value = {"streams":[{"codec_type":"video","width":720,"height":1280},{"codec_type":"audio"}]}
        self.assertEqual(evaluate("dummy.mp4")["issues"], ["not_1080x1920"])

if __name__ == "__main__":
    unittest.main()
