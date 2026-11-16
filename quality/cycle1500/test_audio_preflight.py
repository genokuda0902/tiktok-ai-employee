import unittest
from unittest.mock import patch
from types import SimpleNamespace
import json
from audio_preflight import inspect

class GateTests(unittest.TestCase):
    @patch("audio_preflight.subprocess.run")
    def test_silent_video_rejected(self, run):
        run.return_value=SimpleNamespace(returncode=0,stdout=json.dumps({"streams":[{"codec_type":"video","width":720,"height":1280}]}),stderr="")
        self.assertEqual(inspect("silent.mp4")["reason"],"missing_audio")
    @patch("audio_preflight.subprocess.run")
    def test_audio_not_automatically_approved(self, run):
        run.return_value=SimpleNamespace(returncode=0,stdout=json.dumps({"streams":[{"codec_type":"video"},{"codec_type":"audio","codec_name":"aac"}]}),stderr="")
        self.assertFalse(inspect("with_audio.mp4")["approved"])
    @patch("audio_preflight.subprocess.run")
    def test_probe_failure_rejected(self, run):
        run.return_value=SimpleNamespace(returncode=1,stdout="",stderr="invalid")
        self.assertEqual(inspect("bad.mp4")["reason"],"ffprobe_failed")
if __name__=="__main__": unittest.main()
