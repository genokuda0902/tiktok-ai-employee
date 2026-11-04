import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from tools.cycle1204_delivery_gate import inspect


class DeliveryGateTests(unittest.TestCase):
    def test_missing_mp4_fails_closed(self):
        with tempfile.TemporaryDirectory() as d:
            result = inspect(Path(d)/"missing.mp4", Path(d)/"captions.json")
            self.assertFalse(result["approved"])
            self.assertIn("missing_or_empty_mp4", result["errors"])

    @patch("tools.cycle1204_delivery_gate.subprocess.run")
    def test_silent_video_rejected(self, run):
        with tempfile.TemporaryDirectory() as d:
            video = Path(d)/"a.mp4"
            video.write_bytes(b"fake")
            captions = Path(d)/"c.json"
            captions.write_text(json.dumps([{"start": 0, "end": 1, "text": "こんにちは"}]))
            run.return_value.stdout = json.dumps({"streams": [
                {"codec_type": "video", "width": 1080, "height": 1920}],
                "format": {"duration": "23"}})
            result = inspect(video, captions)
            self.assertIn("missing_audio", result["errors"])
            self.assertFalse(result["posting_allowed"])

    @patch("tools.cycle1204_delivery_gate.subprocess.run")
    def test_technical_pass_never_authorizes_post(self, run):
        with tempfile.TemporaryDirectory() as d:
            video = Path(d)/"a.mp4"
            video.write_bytes(b"fake")
            captions = Path(d)/"c.json"
            captions.write_text(json.dumps([{"start": 0, "end": 1, "text": "こんにちは"}]))
            run.return_value.stdout = json.dumps({"streams": [
                {"codec_type": "video", "width": 1080, "height": 1920},
                {"codec_type": "audio"}], "format": {"duration": "23"}})
            result = inspect(video, captions)
            self.assertTrue(result["technical_gate_pass"])
            self.assertFalse(result["approved"])
            self.assertFalse(result["posting_allowed"])
            self.assertFalse(result["semantic_sync_verified"])


if __name__ == "__main__":
    unittest.main()
