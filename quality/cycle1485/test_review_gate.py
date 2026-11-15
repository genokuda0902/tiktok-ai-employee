import unittest
from unittest.mock import patch
import tempfile
from pathlib import Path
import json
from quality.cycle1485.review_gate import inspect

class ReviewGateTests(unittest.TestCase):
    def test_missing_video_rejected(self):
        with self.assertRaises(FileNotFoundError):
            inspect("/nonexistent/video.mp4", "/nonexistent/sub.srt")
    def test_audio_track_does_not_prove_narration(self):
        with tempfile.TemporaryDirectory() as d:
            v, s = Path(d)/"a.mp4", Path(d)/"a.srt"
            v.write_bytes(b"fake")
            s.write_text("1\n00:00:00,000 --> 00:00:01,000\nテスト\n", encoding="utf-8")
            fake = {"streams": [{"codec_type":"video","width":540,"height":960},{"codec_type":"audio"}]}
            with patch("quality.cycle1485.review_gate.subprocess.run") as run:
                run.return_value.stdout = json.dumps(fake)
                result = inspect(str(v), str(s), approved=True)
            self.assertTrue(result["audio_stream_present"])
            self.assertFalse(result["japanese_narration_verified"])
            self.assertFalse(result["caption_audio_sync_verified"])
            self.assertFalse(result["posting_allowed"])
