import unittest
from unittest.mock import patch
from quality_gate import inspect_video

class QualityGateTests(unittest.TestCase):
    @patch("quality_gate.subprocess.check_output")
    def test_silent_rejected(self, probe):
        probe.return_value = '{"streams":[{"codec_type":"video","width":1080,"height":1920}],"format":{"duration":"12"}}'
        result = inspect_video("demo.mp4", {})
        self.assertFalse(result["publication_allowed"])
        self.assertIn("audio stream missing", result["issues"])

    @patch("quality_gate.subprocess.check_output")
    def test_audio_not_enough(self, probe):
        probe.return_value = '{"streams":[{"codec_type":"video","width":1080,"height":1920},{"codec_type":"audio"}],"format":{"duration":"12"}}'
        result = inspect_video("demo.mp4", {})
        self.assertFalse(result["publication_allowed"])
        self.assertIn("japanese_narration_verified not verified", result["issues"])

    @patch("quality_gate.subprocess.check_output")
    def test_explicit_approvals(self, probe):
        probe.return_value = '{"streams":[{"codec_type":"video","width":1080,"height":1920},{"codec_type":"audio"}],"format":{"duration":"12"}}'
        m = {k: True for k in ("japanese_narration_verified","speech_synced_captions_verified","assets_approved","human_approved")}
        self.assertTrue(inspect_video("demo.mp4", m)["publication_allowed"])

if __name__ == "__main__":
    unittest.main()
