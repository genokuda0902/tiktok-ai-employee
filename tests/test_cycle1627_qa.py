import unittest
from unittest.mock import patch
from pathlib import Path
import tempfile
import json
from quality.cycle1627_qa import inspect

class TestReviewGate(unittest.TestCase):
    def test_missing_file_fails(self):
        with self.assertRaises(FileNotFoundError):
            inspect("/nonexistent/video.mp4")

    def test_silent_demo_fails_closed(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/"a.mp4";p.write_bytes(b"x")
            payload={"streams":[{"codec_type":"video","codec_name":"h264","width":720,"height":1280}],"format":{"duration":"12"}}
            with patch("subprocess.run") as run:
                run.return_value.stdout=json.dumps(payload)
                self.assertFalse(inspect(p)["posting_allowed"])

    def test_audio_track_alone_not_speech(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/"a.mp4";p.write_bytes(b"x")
            payload={"streams":[{"codec_type":"video","width":720,"height":1280},{"codec_type":"audio"}],"format":{"duration":"12"}}
            with patch("subprocess.run") as run:
                run.return_value.stdout=json.dumps(payload)
                result=inspect(p,assets_approved=True,employee_approved=True)
                self.assertFalse(result["posting_allowed"])
                self.assertFalse(result["checks"]["japanese_speech_verified"])

if __name__=="__main__": unittest.main()
