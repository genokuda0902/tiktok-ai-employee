import unittest
from unittest.mock import patch
from types import SimpleNamespace
from pathlib import Path
from tempfile import TemporaryDirectory
from quality.cycle1295_probe import probe

class ProbeTest(unittest.TestCase):
    def test_silent_video_rejected(self):
        with TemporaryDirectory() as d:
            p=Path(d)/"demo.mp4";p.touch()
            fake=SimpleNamespace(stdout='{"streams":[{"codec_type":"video","width":1080,"height":1920}]}')
            with patch("subprocess.run", return_value=fake):
                result=probe(p)
            self.assertIn("missing_audio", result["issues"])
            self.assertFalse(result["posting_allowed"])
    def test_no_file(self):
        with self.assertRaises(FileNotFoundError):
            probe("/nonexistent/review.mp4")
if __name__=="__main__":
    unittest.main()
