import unittest
from unittest.mock import patch
from pathlib import Path
import tempfile
import json
from quality.cycle1331_media_gate import inspect

class GateTest(unittest.TestCase):
    def test_missing_file_rejected(self):
        self.assertEqual(inspect("/no/such/file.mp4")["issues"], ["missing_file"])

    @patch("quality.cycle1331_media_gate.subprocess.run")
    def test_silent_low_resolution_rejected(self, run):
        run.side_effect = [type("R", (), {"returncode":0, "stdout":json.dumps({
            "streams":[{"codec_type":"video","width":720,"height":1280}],
            "format":{"duration":"14.4"}})})(),
            type("R", (), {"returncode":0})()]
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/"test.mp4"; p.write_bytes(b"x")
            result=inspect(p)
        self.assertFalse(result["approved"])
        self.assertIn("missing_audio",result["issues"])
        self.assertIn("low_resolution",result["issues"])

if __name__ == "__main__": unittest.main()
