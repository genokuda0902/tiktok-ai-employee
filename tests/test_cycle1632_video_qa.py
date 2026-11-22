import unittest
from unittest.mock import patch
from pathlib import Path
import json
from tools.cycle1632_video_qa import inspect

class QATest(unittest.TestCase):
    @patch("tools.cycle1632_video_qa.subprocess.run")
    @patch("tools.cycle1632_video_qa.subprocess.check_output")
    def test_silent_video_not_approved(self, output, run):
        output.return_value=json.dumps({"streams":[{"codec_type":"video","width":1080,"height":1920,"r_frame_rate":"24/1"}],"format":{"duration":"12"}}).encode()
        r=inspect(Path("mock.mp4"))
        self.assertTrue(r["technical_video_pass"])
        self.assertFalse(r["audio_stream_present"])
        self.assertFalse(r["publication_approved"])
    @patch("tools.cycle1632_video_qa.subprocess.run")
    @patch("tools.cycle1632_video_qa.subprocess.check_output")
    def test_audio_track_not_speech_proof(self, output, run):
        output.return_value=json.dumps({"streams":[{"codec_type":"video","width":1080,"height":1920},{"codec_type":"audio"}],"format":{"duration":"12"}}).encode()
        r=inspect(Path("mock.mp4"))
        self.assertTrue(r["audio_stream_present"])
        self.assertFalse(r["japanese_narration_verified"])
        self.assertFalse(r["speech_caption_sync_verified"])
    @patch("tools.cycle1632_video_qa.subprocess.check_output")
    def test_missing_video_rejected(self, output):
        output.return_value=json.dumps({"streams":[],"format":{"duration":"12"}}).encode()
        with self.assertRaises(ValueError): inspect(Path("mock.mp4"))
if __name__=="__main__": unittest.main()
