import unittest
from unittest.mock import patch
import json
import tempfile
from pathlib import Path
from quality.cycle1347_gate import inspect_mp4

class GateTests(unittest.TestCase):
    def probe(self,streams,**flags):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/"test.mp4";p.write_bytes(b"fake")
            with patch("subprocess.check_output",return_value=json.dumps({"streams":streams}).encode()):
                return inspect_mp4(p,**flags)
    def test_beep_is_not_narration(self):
        r=self.probe([{"codec_type":"video","width":1080,"height":1920},{"codec_type":"audio"}])
        self.assertIn("japanese_narration_unverified",r["issues"])
        self.assertFalse(r["passed"])
    def test_low_resolution_rejected(self):
        r=self.probe([{"codec_type":"video","width":540,"height":960},{"codec_type":"audio"}],narration_verified=True,captions_verified=True,rights_approved=True,human_approved=True)
        self.assertIn("wrong_resolution",r["issues"])
    def test_approved_metadata_passes_technical_gate(self):
        r=self.probe([{"codec_type":"video","width":1080,"height":1920},{"codec_type":"audio"}],narration_verified=True,captions_verified=True,rights_approved=True,human_approved=True)
        self.assertTrue(r["passed"])

if __name__=="__main__":unittest.main()
