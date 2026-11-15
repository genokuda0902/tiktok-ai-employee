import unittest
from unittest.mock import patch
from pathlib import Path
from tempfile import TemporaryDirectory
import json
from tools.delivery_qa import inspect

class DeliveryQATests(unittest.TestCase):
    def test_missing_mp4_fails(self):
        self.assertEqual(inspect("/nonexistent.mp4")["errors"], ["mp4_missing"])
    def test_audio_track_is_not_narration(self):
        with TemporaryDirectory() as d:
            p = Path(d)/"x.mp4"; p.write_bytes(b"fake")
            payload = {"streams":[{"codec_type":"video","width":1080,"height":1920},
                                  {"codec_type":"audio"}], "format":{}}
            with patch("tools.delivery_qa.subprocess.run") as run:
                run.return_value.returncode=0
                run.return_value.stdout=json.dumps(payload)
                result=inspect(p)
            self.assertFalse(result["approved"])
            self.assertIn("japanese_narration_unverified", result["errors"])
            self.assertIn("rights_unapproved", result["errors"])
    def test_silent_video_fails(self):
        with TemporaryDirectory() as d:
            p=Path(d)/"x.mp4";p.write_bytes(b"fake")
            with patch("tools.delivery_qa.subprocess.run") as run:
                run.return_value.returncode=0
                run.return_value.stdout=json.dumps({"streams":[{"codec_type":"video","width":720,"height":1280}]})
                self.assertIn("audio_missing", inspect(p)["errors"])
if __name__=="__main__":
    unittest.main()
