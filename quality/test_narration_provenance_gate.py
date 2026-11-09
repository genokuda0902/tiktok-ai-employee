import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from narration_provenance_gate import check

class TestNarrationGate(unittest.TestCase):
    def test_missing(self):
        self.assertEqual(check("/missing.mp4", "/missing.json")["reason"], "missing_file")

    def test_silent(self):
        with tempfile.TemporaryDirectory() as d:
            v = Path(d)/"v.mp4"; v.touch()
            m = Path(d)/"m.json"; m.write_text("{}")
            with patch("narration_provenance_gate.subprocess.check_output", return_value=json.dumps({"streams":[{"codec_type":"video"}]})):
                self.assertEqual(check(v,m)["reason"], "missing_audio")

    def test_audio_without_provenance(self):
        with tempfile.TemporaryDirectory() as d:
            v = Path(d)/"v.mp4"; v.touch()
            m = Path(d)/"m.json"; m.write_text("{}")
            with patch("narration_provenance_gate.subprocess.check_output", return_value=json.dumps({"streams":[{"codec_type":"video"},{"codec_type":"audio"}]})):
                self.assertEqual(check(v,m)["reason"], "missing_narration_provenance")

    def test_unapproved(self):
        with tempfile.TemporaryDirectory() as d:
            v = Path(d)/"v.mp4"; v.touch()
            m = Path(d)/"m.json"; m.write_text(json.dumps({"narration_language":"ja","narration_source":"local","narration_text":"テスト","voice_rights_reviewed":True,"captions_sync_reviewed":True,"human_approved":False}))
            with patch("narration_provenance_gate.subprocess.check_output", return_value=json.dumps({"streams":[{"codec_type":"video"},{"codec_type":"audio"}]})):
                self.assertEqual(check(v,m)["reason"], "review_not_complete")
if __name__ == "__main__": unittest.main()
