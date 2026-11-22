import unittest
from unittest.mock import patch
from types import SimpleNamespace
from quality.cycle1630.quality_gate import inspect

class GateTests(unittest.TestCase):
    @patch("quality.cycle1630.quality_gate.Path.is_file", return_value=False)
    def test_missing_file_fails_closed(self, _):
        self.assertFalse(inspect("missing.mp4")["posting_allowed"])

    @patch("quality.cycle1630.quality_gate.subprocess.run")
    @patch("quality.cycle1630.quality_gate.Path.is_file", return_value=True)
    def test_audio_stream_does_not_prove_japanese_speech(self, _, run):
        run.return_value = SimpleNamespace(returncode=0, stdout='{"streams":[{"codec_type":"video","width":1080,"height":1920},{"codec_type":"audio"}]}')
        result = inspect("sample.mp4", captions_synced=True, assets_approved=True, employee_approved=True)
        self.assertIn("japanese_narration_unverified", result["reasons"])
        self.assertFalse(result["posting_allowed"])

if __name__ == "__main__":
    unittest.main()
