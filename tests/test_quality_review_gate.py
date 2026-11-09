import unittest
from unittest.mock import patch
from pathlib import Path
import tempfile
from src.quality_review_gate import inspect

class ReviewGateTests(unittest.TestCase):
    def test_missing_file(self):
        self.assertEqual(inspect("/missing/clip.mp4")["issues"], ["missing_file"])

    @patch("src.quality_review_gate.subprocess.run")
    @patch("src.quality_review_gate.subprocess.check_output")
    def test_silent_1080p_fails_closed(self, probe, decode):
        probe.return_value = b'{"streams":[{"codec_type":"video","width":1080,"height":1920}],"format":{"duration":"20"}}'
        decode.return_value.returncode = 0
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "test.mp4"; p.write_bytes(b"fixture")
            result = inspect(p)
        self.assertFalse(result["ok"])
        self.assertIn("missing_narration_audio", result["issues"])

if __name__ == "__main__":
    unittest.main()
