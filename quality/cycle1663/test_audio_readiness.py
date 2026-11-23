import unittest
from unittest.mock import patch
from audio_readiness import inspect
FULL=dict(narration_language="ja",narration_source_verified=True,caption_timing_verified=True,asset_rights_approved=True,employee_approved=True)
class Tests(unittest.TestCase):
    @patch("audio_readiness.subprocess.check_output",return_value='{"streams":[{"codec_type":"video","width":1080,"height":1920}]}')
    def test_silent(self,_): self.assertIn("audio_stream_missing",inspect("x.mp4",FULL)["reasons"])
    @patch("audio_readiness.subprocess.check_output",return_value='{"streams":[{"codec_type":"video","width":1080,"height":1920},{"codec_type":"audio"}]}')
    def test_effects_not_speech(self,_): self.assertIn("japanese_narration_unverified",inspect("x.mp4",{})["reasons"])
    @patch("audio_readiness.subprocess.check_output",return_value='{"streams":[{"codec_type":"video","width":1080,"height":1920},{"codec_type":"audio"}]}')
    def test_approval(self,_): self.assertFalse(inspect("x.mp4",dict(FULL,employee_approved=False))["approved"])
if __name__=="__main__": unittest.main()
