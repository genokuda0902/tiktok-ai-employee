import unittest
from unittest.mock import patch
from quality.cycle1604_preflight import inspect

class PreflightTests(unittest.TestCase):
    def test_silent_15fps_rejected(self):
        data={"streams":[{"codec_type":"video","width":720,"height":1280,"avg_frame_rate":"15/1"}],"format":{"duration":"15"}}
        with patch("quality.cycle1604_preflight.probe", return_value=data):
            report=inspect("synthetic.mp4")
        self.assertIn("low_frame_rate",report["reasons"])
        self.assertIn("missing_audio",report["reasons"])
        self.assertFalse(report["publication_approved"])
    def test_24fps_with_audio_still_unapproved(self):
        data={"streams":[{"codec_type":"video","width":720,"height":1280,"avg_frame_rate":"24/1"},{"codec_type":"audio"}],"format":{"duration":"15"}}
        with patch("quality.cycle1604_preflight.probe", return_value=data):
            report=inspect("synthetic.mp4")
        self.assertNotIn("low_frame_rate",report["reasons"])
        self.assertIn("japanese_speech_unverified",report["reasons"])
        self.assertFalse(report["publication_approved"])
if __name__=="__main__": unittest.main()
