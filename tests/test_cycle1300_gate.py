import unittest
from unittest.mock import patch
import json
import tempfile
from pathlib import Path
from quality.cycle1300_gate import inspect

class GateTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.path = Path(self.tmp.name) / "demo.mp4"
        self.path.write_bytes(b"placeholder")
    def tearDown(self):
        self.tmp.cleanup()
    def probe(self, audio=True):
        streams = [{"codec_type": "video", "width": 1080, "height": 1920}]
        if audio: streams.append({"codec_type": "audio"})
        return {"streams": streams, "format": {"duration": "18.0"}}
    def test_no_audio_blocks(self):
        with patch("subprocess.run") as run:
            run.return_value.stdout = json.dumps(self.probe(False))
            self.assertFalse(inspect(self.path)["publication_allowed"])
    def test_audio_does_not_prove_japanese_narration(self):
        with patch("subprocess.run") as run:
            run.return_value.stdout = json.dumps(self.probe(True))
            result = inspect(self.path, True, True, True)
            self.assertFalse(result["publication_allowed"])
            self.assertFalse(result["checks"]["japanese_voice_reviewed"])
    def test_missing_file(self):
        with self.assertRaises(FileNotFoundError):
            inspect(self.path.with_name("missing.mp4"))

if __name__ == "__main__":
    unittest.main()
