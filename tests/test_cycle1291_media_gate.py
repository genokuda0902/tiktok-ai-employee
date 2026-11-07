import unittest
from unittest.mock import patch
from types import SimpleNamespace
from quality.cycle1291_media_gate import inspect

class MediaGateTest(unittest.TestCase):
    @patch("quality.cycle1291_media_gate.subprocess.run")
    def test_silent_video_rejected(self, run):
        run.return_value = SimpleNamespace(stdout='{"streams":[{"codec_type":"video","width":1080,"height":1920}],"format":{"duration":"12"}}')
        self.assertIn("narration_missing", inspect("demo.mp4")["reasons"])

    @patch("quality.cycle1291_media_gate.subprocess.run")
    def test_low_resolution_rejected(self, run):
        run.return_value = SimpleNamespace(stdout='{"streams":[{"codec_type":"video","width":720,"height":1280},{"codec_type":"audio"}],"format":{"duration":"12"}}')
        self.assertFalse(inspect("demo.mp4")["approved"])

if __name__ == "__main__":
    unittest.main()
