import unittest
from unittest.mock import patch
import json
from audio_preflight import inspect_media

class AudioPreflightTests(unittest.TestCase):
    def test_silent_video_blocked(self):
        with patch("subprocess.check_output",return_value=json.dumps({"streams":[{"codec_type":"video","codec_name":"h264"}]})):
            r=inspect_media("sample.mp4")
        self.assertFalse(r["publishable"])
        self.assertIn("missing_audio_stream",r["reasons"])

    def test_audio_not_speech_proof(self):
        with patch("subprocess.check_output",return_value=json.dumps({"streams":[{"codec_type":"video"},{"codec_type":"audio","codec_name":"aac"}]})):
            r=inspect_media("sample.mp4")
        self.assertTrue(r["technical_audio_present"])
        self.assertFalse(r["publishable"])
        self.assertIn("japanese_narration_unverified",r["reasons"])

    def test_manual_approval_required(self):
        with patch("subprocess.check_output",return_value=json.dumps({"streams":[{"codec_type":"video"},{"codec_type":"audio"}]})):
            r=inspect_media("sample.mp4",True,True)
        self.assertFalse(r["publishable"])
        self.assertTrue(r["manual_approval_required"])

if __name__=="__main__": unittest.main()
