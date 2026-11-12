import unittest
from unittest.mock import patch
from quality.cycle1404_qa import inspect

class GateTest(unittest.TestCase):
    @patch("quality.cycle1404_qa.subprocess.check_output")
    def test_silent_video_rejected(self, probe):
        probe.return_value = '{"streams":[{"codec_type":"video","width":1080,"height":1920}]}'
        self.assertFalse(inspect("dummy.mp4")["posting_allowed"])
    @patch("quality.cycle1404_qa.subprocess.check_output")
    def test_audio_alone_is_not_speech(self, probe):
        probe.return_value = '{"streams":[{"codec_type":"video","width":1080,"height":1920},{"codec_type":"audio","codec_name":"aac"}]}'
        self.assertFalse(inspect("dummy.mp4")["posting_allowed"])
