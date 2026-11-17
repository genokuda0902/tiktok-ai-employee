import unittest
from unittest.mock import patch
import json
import tempfile
from pathlib import Path
from quality_cycle1508 import inspect

class GateTests(unittest.TestCase):
    def test_silent_or_unverified_never_passes(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "manifest.json"
            path.write_text(json.dumps({"posting_allowed": True}), encoding="utf-8")
            sample = {"streams":[{"codec_type":"video","codec_name":"h264","width":720,"height":1280},
                                  {"codec_type":"audio","codec_name":"aac"}],
                      "format":{"duration":"8.0"}}
            with patch("subprocess.check_output", return_value=json.dumps(sample)):
                result = inspect("fake.mp4", path)
            self.assertFalse(result["posting_allowed"])
            self.assertIn("JAPANESE_NARRATION_UNVERIFIED", result["problems"])
            self.assertIn("HUMAN_APPROVAL_MISSING", result["problems"])

if __name__ == "__main__": unittest.main()
