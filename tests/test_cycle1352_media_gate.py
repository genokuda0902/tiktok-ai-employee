import unittest
from unittest.mock import patch
from tools.cycle1352_media_gate import review

class GateTests(unittest.TestCase):
    @patch("tools.cycle1352_media_gate.probe")
    def test_no_audio_is_rejected(self,p):
        p.return_value={"streams":[{"codec_type":"video","width":1080,"height":1920}]}
        self.assertIn("audio_missing",review("test.mp4")["issues"])
    @patch("tools.cycle1352_media_gate.probe")
    def test_audio_stream_does_not_prove_japanese(self,p):
        p.return_value={"streams":[{"codec_type":"video","width":1080,"height":1920},{"codec_type":"audio"}]}
        self.assertIn("japanese_narration_unverified",review("test.mp4")["issues"])
        self.assertFalse(review("test.mp4")["posting_allowed"])
    @patch("tools.cycle1352_media_gate.probe")
    def test_resolution_rejected(self,p):
        p.return_value={"streams":[{"codec_type":"video","width":720,"height":1280}]}
        self.assertIn("resolution",review("test.mp4")["issues"])
if __name__=="__main__": unittest.main()
