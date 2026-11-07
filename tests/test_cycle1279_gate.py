import unittest
from unittest.mock import patch
import json
from quality.cycle1279_gate import inspect

class GateTest(unittest.TestCase):
    @patch("quality.cycle1279_gate.subprocess.run")
    def test_silent_video_fails_closed(self, run):
        run.return_value.stdout = json.dumps({"streams":[{"codec_type":"video","width":1080,"height":1920}]})
        result = inspect("demo.mp4")
        self.assertFalse(result["posting_allowed"])
        self.assertIn("missing_narration_audio", result["issues"])

    @patch("quality.cycle1279_gate.subprocess.run")
    def test_audio_stream_alone_never_approves(self, run):
        run.return_value.stdout = json.dumps({"streams":[{"codec_type":"video","width":1080,"height":1920},{"codec_type":"audio"}]})
        result = inspect("demo.mp4")
        self.assertFalse(result["posting_allowed"])
        self.assertIn("japanese_narration_not_human_verified", result["issues"])

if __name__ == "__main__": unittest.main()
