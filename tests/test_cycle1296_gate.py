import unittest
from unittest.mock import patch
from quality.cycle1296_gate import assess

class GateTests(unittest.TestCase):
    @patch("quality.cycle1296_gate.probe")
    def test_silent_rejected(self, probe):
        probe.return_value={"streams":[{"codec_type":"video","width":1080,"height":1920}]}
        self.assertFalse(assess("sample.mp4", True, True, True, True)["publication_approved"])
    @patch("quality.cycle1296_gate.probe")
    def test_low_resolution_rejected(self, probe):
        probe.return_value={"streams":[{"codec_type":"video","width":720,"height":1280},{"codec_type":"audio"}]}
        self.assertFalse(assess("sample.mp4", True, True, True, True)["publication_approved"])
    @patch("quality.cycle1296_gate.probe")
    def test_all_gates_required(self, probe):
        probe.return_value={"streams":[{"codec_type":"video","width":1080,"height":1920},{"codec_type":"audio"}]}
        self.assertTrue(assess("sample.mp4", True, True, True, True)["publication_approved"])
        self.assertFalse(assess("sample.mp4", True, False, True, True)["publication_approved"])
