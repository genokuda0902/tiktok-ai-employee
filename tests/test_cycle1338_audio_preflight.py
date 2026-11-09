import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from tools.cycle1338_audio_preflight import check

class PreflightTests(unittest.TestCase):
    def test_missing(self):
        self.assertEqual(check("/missing/media.mp4")["errors"], ["missing_media"])

    def test_silent(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "test.mp4"
            p.write_bytes(b"x")
            with patch("tools.cycle1338_audio_preflight.subprocess.run") as run:
                run.return_value.stdout = '{"streams":[{"codec_type":"video","width":1080,"height":1920}]}'
                self.assertIn("missing_audio", check(p)["errors"])

    def test_low_resolution(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "test.mp4"
            p.write_bytes(b"x")
            with patch("tools.cycle1338_audio_preflight.subprocess.run") as run:
                run.return_value.stdout = '{"streams":[{"codec_type":"video","width":720,"height":1280},{"codec_type":"audio"}]}'
                self.assertIn("low_resolution", check(p)["errors"])

if __name__ == "__main__":
    unittest.main()
