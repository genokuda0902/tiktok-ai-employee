import unittest
from unittest.mock import patch
from types import SimpleNamespace
from quality.cycle1252.video_gate import inspect

class VideoGateTest(unittest.TestCase):
    @patch("quality.cycle1252.video_gate.subprocess.run")
    def test_silent_video_cannot_pass_speech_gate(self,run):
        run.side_effect=[
            SimpleNamespace(stdout='{"streams":[{"codec_type":"video","codec_name":"h264","width":1080,"height":1920}],"format":{"duration":"12"}}',returncode=0),
            SimpleNamespace(stderr="",returncode=0)]
        result=inspect("synthetic.mp4")
        self.assertTrue(result["video_ok"])
        self.assertFalse(result["audio_present"])
        self.assertFalse(result["japanese_narration_verified"])
        self.assertFalse(result["publish_approved"])
if __name__=="__main__": unittest.main()
