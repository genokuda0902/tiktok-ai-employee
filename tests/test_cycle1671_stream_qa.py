import unittest
from unittest.mock import patch
from quality.cycle1671_stream_qa import inspect

class StreamGateTests(unittest.TestCase):
    @patch("quality.cycle1671_stream_qa.probe")
    def test_silent_video_rejected(self, mock):
        mock.return_value = {"streams":[{"codec_type":"video","width":1080,"height":1920}]}
        self.assertFalse(inspect("demo.mp4", True, True, True, True)["publishable"])

    @patch("quality.cycle1671_stream_qa.probe")
    def test_audio_is_not_speech_evidence(self, mock):
        mock.return_value = {"streams":[{"codec_type":"video","width":1080,"height":1920},{"codec_type":"audio"}]}
        self.assertFalse(inspect("demo.mp4", False, True, True, True)["publishable"])

    @patch("quality.cycle1671_stream_qa.probe")
    def test_all_evidence_required(self, mock):
        mock.return_value = {"streams":[{"codec_type":"video","width":1080,"height":1920},{"codec_type":"audio"}]}
        self.assertTrue(inspect("demo.mp4", True, True, True, True)["publishable"])
        self.assertFalse(inspect("demo.mp4", True, True, True, False)["publishable"])

if __name__ == "__main__":
    unittest.main()
